from flask import request
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, HiddenField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired, ValidationError, Optional
# Import equipment and utility data for populating form fields and validation
from ..data.equipment.weapons import WEAPONS
from ..data.equipment.armor import ARMOR
from ..data.equipment.adventuring_gear import (
    ADVENTURING_GEAR, AMMUNITION_OPTIONS, ARCANE_FOCUS_OPTIONS,
    HOLY_SYMBOL_OPTIONS, MUSICAL_INSTRUMENT_OPTIONS, TOOL_OPTIONS
)
from ..data.equipment import has_weapon_proficiency, has_armor_proficiency
from .equipment_categories import SpecialEquipmentForm

# EquipmentForm is a cleaned-up version of the main equipment selection form for D&D characters.
# It provides logic for selecting armor, weapons, gear, and special items, with validation and cost calculation.
class EquipmentForm(FlaskForm):
    class Meta:
        csrf = True  # Enable CSRF protection explicitly
    
    # Hidden field for the user's budget (in gold pieces)
    budget = HiddenField('Budget', validators=[DataRequired()])
    
    # Armor and shield selection fields
    armor = SelectField('Armor', choices=[('', '-- Select Armor --')], validators=[])
    shield = SelectField('Shield', choices=[('', '-- No Shield --')], validators=[])
    
    # Special equipment (tools, instruments, spell foci, etc.)
    special_equipment = FormField(SpecialEquipmentForm)
    
    # Adventuring gear (multiple selection)
    adventuring_gear = SelectMultipleField('Adventuring Gear', choices=[], validators=[])
    
    # Weapon selection fields (multiple selection for each category)
    simple_melee = SelectMultipleField('Simple Melee Weapons', validators=[])
    simple_ranged = SelectMultipleField('Simple Ranged Weapons', validators=[])
    martial_melee = SelectMultipleField('Martial Melee Weapons', validators=[])
    martial_ranged = SelectMultipleField('Martial Ranged Weapons', validators=[])
    
    # Hidden field to trigger equipment validation
    equipment_check = HiddenField('Equipment Check', validators=[])
    
    def __init__(self, *args, **kwargs):
        # Initialize the parent FlaskForm
        super().__init__(*args, **kwargs)
        self.char_class = None  # Will be set by the route
        self.remaining_funds = 0
        self.total_cost = 0
        self.validation_errors = []  # Store custom validation errors
        
        # Ensure all SelectMultipleFields are initialized as empty lists
        if self.adventuring_gear.data is None:
            self.adventuring_gear.data = []
        if self.simple_melee.data is None:
            self.simple_melee.data = []
        if self.simple_ranged.data is None:
            self.simple_ranged.data = []
        if self.martial_melee.data is None:
            self.martial_melee.data = []
        if self.martial_ranged.data is None:
            self.martial_ranged.data = []
            
        # Populate all field choices
        self._setup_choices()
    
    def _setup_choices(self):
        """Setup all the choices for form fields."""
        # Populate armor choices from ARMOR data, skipping shields (handled separately)
        armor_choices = [('', '-- Select Armor --')]
        for category, armor_list in ARMOR.items():
            if category != 'shield':
                for armor_item in armor_list:
                    if not isinstance(armor_item, dict):
                        continue
                    cost_str = f"{armor_item.get('cost', {}).get('gp', 0)} gp"
                    if 'cost' in armor_item and 'sp' in armor_item['cost']:
                        cost_str = f"{armor_item['cost']['sp']} sp"
                    armor_choices.append((
                        f"{category}:{armor_item['name']}", 
                        f"{armor_item['name']} (AC {armor_item['ac']}) - {cost_str}"
                    ))
        self.armor.choices = armor_choices
        
        # Populate shield choices
        shield_choices = [('', '-- No Shield --')]
        if 'shield' in ARMOR:
            for shield_item in ARMOR['shield']:
                cost_str = f"{shield_item.get('cost', {}).get('gp', 0)} gp"
                shield_choices.append((
                    f"shield:{shield_item['name']}", 
                    f"{shield_item['name']} (+{shield_item['ac_bonus']} AC) - {cost_str}"
                ))
        self.shield.choices = shield_choices
        
        # Helper to format weapon choices with price
        def format_weapon_choice(category, weapon):
            cost = weapon.get('cost', {})
            if 'gp' in cost and cost['gp'] > 0:
                cost_str = f"{cost['gp']} gp"
            elif 'sp' in cost and cost['sp'] > 0:
                cost_str = f"{cost['sp']} sp"
            elif 'cp' in cost and cost['cp'] > 0:
                cost_str = f"{cost['cp']} cp"
            else:
                cost_str = "0 gp"
            return (f"{category}:{weapon['name']}", f"{weapon['name']} ({cost_str})")
        
        # Populate weapon choices for each category
        self.simple_melee.choices = [format_weapon_choice('simple_melee', weapon) 
                                   for weapon in WEAPONS['simple_melee']]
        self.simple_ranged.choices = [format_weapon_choice('simple_ranged', weapon)
                                    for weapon in WEAPONS['simple_ranged']]
        self.martial_melee.choices = [format_weapon_choice('martial_melee', weapon)
                                    for weapon in WEAPONS['martial_melee']]
        self.martial_ranged.choices = [format_weapon_choice('martial_ranged', weapon)
                                     for weapon in WEAPONS['martial_ranged']]
        
        # Helper to format cost for gear and special items
        def format_cost(cost_dict):
            if 'gp' in cost_dict and cost_dict['gp'] > 0:
                return f"{cost_dict['gp']} gp"
            elif 'sp' in cost_dict and cost_dict['sp'] > 0:
                return f"{cost_dict['sp']} sp"
            elif 'cp' in cost_dict and cost_dict['cp'] > 0:
                return f"{cost_dict['cp']} cp"
            else:
                return "0 gp"
        
        # Populate adventuring gear choices
        gear_choices = [(key, f"{item['name']} ({format_cost(item.get('cost', {}))})") 
                       for key, item in ADVENTURING_GEAR.items()]
        self.adventuring_gear.choices = gear_choices
        
        # Populate special equipment choices (ammunition, focus, etc.)
        if hasattr(self.special_equipment, 'ammunition_selection'):
            self.special_equipment.ammunition_selection.choices = [
                ('', '-- Select Ammunition --')] + [
                (key, f"{item['name']} ({format_cost(item.get('cost', {}))})") 
                for key, item in AMMUNITION_OPTIONS.items()]
        
        if hasattr(self.special_equipment, 'arcane_focus_selection'):
            self.special_equipment.arcane_focus_selection.choices = [
                ('', '-- Select Arcane Focus --')] + [
                (key, f"{item['name']} ({format_cost(item.get('cost', {}))})") 
                for key, item in ARCANE_FOCUS_OPTIONS.items()]
        
        if hasattr(self.special_equipment, 'holy_symbol_selection'):
            self.special_equipment.holy_symbol_selection.choices = [
                ('', '-- Select Holy Symbol --')] + [
                (key, f"{item['name']} ({format_cost(item.get('cost', {}))})") 
                for key, item in HOLY_SYMBOL_OPTIONS.items()]
        
        if hasattr(self.special_equipment, 'musical_instrument_selection'):
            self.special_equipment.musical_instrument_selection.choices = [
                ('', '-- Select Instrument --')] + [
                (key, f"{item['name']} ({format_cost(item.get('cost', {}))})") 
                for key, item in MUSICAL_INSTRUMENT_OPTIONS.items()]
        
        if hasattr(self.special_equipment, 'tool_selection'):
            self.special_equipment.tool_selection.choices = [
                ('', '-- Select Tool --')] + [
                (key, f"{item['name']} ({format_cost(item.get('cost', {}))})") 
                for key, item in TOOL_OPTIONS.items()]
        
        # Populate spell scroll choices based on selected class and level
        from ..data.spells import (wizard_cantrips, wizard_level1_spells,
                                 cleric_cantrips, level1_cleric_spells)
        
        def get_spell_choices(spell_class, level):
            if spell_class == 'wizard':
                return wizard_cantrips if level == '0' else wizard_level1_spells
            elif spell_class == 'cleric':
                return cleric_cantrips if level == '0' else level1_cleric_spells
            return []
        
        if hasattr(self.special_equipment, 'spell_selection'):
            spell_class = self.special_equipment.spell_scroll_class.data or 'wizard'
            spell_level = self.special_equipment.spell_scroll_level.data or '0'
            spell_list = get_spell_choices(spell_class, spell_level)
            self.special_equipment.spell_selection.choices = [('', '-- Select Spell --')] + [
                (key, name) for key, name in spell_list
            ]

    def calculate_total_cost(self):
        """Calculate the total cost of all selected equipment in gold pieces."""
        total_gp = 0.0
        
        # Add armor cost if selected
        if self.armor.data:
            armor_type, armor_name = self.armor.data.split(':')
            # Find the armor in the correct category
            for armor in ARMOR[armor_type]:
                if armor['name'] == armor_name:
                    total_gp += self._convert_to_gp(armor['cost'])
                    break
        
        # Add shield cost if selected
        if self.shield.data:
            shield_type, shield_name = self.shield.data.split(':')
            for shield in ARMOR[shield_type]:
                if shield['name'] == shield_name:
                    total_gp += self._convert_to_gp(shield['cost'])
                    break
        
        # Add costs for selected weapons
        for weapon_type in [self.simple_melee, self.simple_ranged, 
                          self.martial_melee, self.martial_ranged]:
            for weapon_id in weapon_type.data:
                weapon_category, weapon_name = weapon_id.split(':')
                # Find the weapon in the appropriate category
                for weapon in WEAPONS[weapon_category]:
                    if weapon['name'] == weapon_name:
                        total_gp += self._convert_to_gp(weapon.get('cost', {'gp': 0}))
                        break
        
        # Add costs for special equipment
        if self.special_equipment:
            # Arcane Focus
            if (self.special_equipment.has_arcane_focus.data and 
                self.special_equipment.arcane_focus_selection.data):
                selection = self.special_equipment.arcane_focus_selection.data
                if selection in ARCANE_FOCUS_OPTIONS:
                    total_gp += self._convert_to_gp(ARCANE_FOCUS_OPTIONS[selection]['cost'])
            
            # Holy Symbol
            if (self.special_equipment.has_holy_symbol.data and 
                self.special_equipment.holy_symbol_selection.data):
                selection = self.special_equipment.holy_symbol_selection.data
                if selection in HOLY_SYMBOL_OPTIONS:
                    total_gp += self._convert_to_gp(HOLY_SYMBOL_OPTIONS[selection]['cost'])
            
            # Ammunition
            if (self.special_equipment.has_ammunition.data and 
                self.special_equipment.ammunition_selection.data):
                selection = self.special_equipment.ammunition_selection.data
                if selection in AMMUNITION_OPTIONS:
                    total_gp += self._convert_to_gp(AMMUNITION_OPTIONS[selection]['cost'])
            
            # Musical Instrument
            if (self.special_equipment.has_musical_instrument.data and 
                self.special_equipment.musical_instrument_selection.data):
                selection = self.special_equipment.musical_instrument_selection.data
                if selection in MUSICAL_INSTRUMENT_OPTIONS:
                    total_gp += self._convert_to_gp(MUSICAL_INSTRUMENT_OPTIONS[selection]['cost'])
            
            # Tools
            if (self.special_equipment.has_tools.data and 
                self.special_equipment.tool_selection.data):
                selection = self.special_equipment.tool_selection.data
                if selection in TOOL_OPTIONS:
                    total_gp += self._convert_to_gp(TOOL_OPTIONS[selection]['cost'])
            
            # Spell Scroll
            if self.special_equipment.has_spell_scroll.data:
                level = self.special_equipment.spell_scroll_level.data
                if level == '0':
                    total_gp += 30  # 30gp for cantrip
                elif level == '1':
                    total_gp += 50  # 50gp for 1st level
        
        # Add costs for adventuring gear
        for item_id in self.adventuring_gear.data:
            if item_id in ADVENTURING_GEAR:
                total_gp += self._convert_to_gp(ADVENTURING_GEAR[item_id]['cost'])
        
        return total_gp
    
    def _convert_to_gp(self, cost):
        """Convert a cost dictionary to gold pieces."""
        total = 0.0
        total += cost.get('pp', 0) * 10    # 1 pp = 10 gp
        total += cost.get('gp', 0)         # 1 gp = 1 gp
        total += cost.get('sp', 0) / 10    # 10 sp = 1 gp
        total += cost.get('cp', 0) / 100   # 100 cp = 1 gp
        return total

    def validate(self):
        """Validate the selected equipment against budget and class restrictions."""
        print("DEBUG: Starting custom validate method")
        if not super().validate():
            print("DEBUG: super().validate() failed")
            for field_name, field in self._fields.items():
                if field.errors:
                    print(f"DEBUG: Field {field_name} has errors: {field.errors}")
            self.validation_errors.append('Form validation failed. Please check all required fields.')
            return False

        print("DEBUG: super().validate() passed")
        total_cost = self.calculate_total_cost()
        print(f"DEBUG: Total cost calculated: {total_cost}gp")
        
        try:
            budget = float(self.budget.data)
            print(f"DEBUG: Budget: {budget}gp")
            
            # Calculate remaining funds in gp
            self.remaining_funds = budget - total_cost
            self.total_cost = total_cost
            print(f"DEBUG: Remaining funds: {self.remaining_funds}gp")

            if total_cost > budget:
                print("DEBUG: Cost exceeds budget - adding error")
                self.validation_errors.append(f'Total cost ({total_cost:.2f} gp) exceeds budget ({budget} gp)')
                return False

            # Check armor proficiency
            if self.armor.data:
                print(f"DEBUG: Checking armor proficiency for {self.armor.data}")
                armor_type, armor_name = self.armor.data.split(':')
                if not has_armor_proficiency(self.char_class, armor_type):
                    print(f"DEBUG: No proficiency with {armor_type} armor")
                    self.validation_errors.append(f'{self.char_class}s are not proficient with {armor_type} armor')
                    return False
            
            # Check class-specific equipment restrictions
            if self.char_class == 'Wizard':
                print("DEBUG: Checking Wizard restrictions")
                if (self.special_equipment.has_holy_symbol.data and 
                    self.special_equipment.holy_symbol_selection.data):
                    print("DEBUG: Wizard trying to use holy symbol")
                    self.validation_errors.append('Wizards cannot use Holy Symbols')
                    return False
                
            elif self.char_class == 'Cleric':
                print("DEBUG: Checking Cleric restrictions")
                if (self.special_equipment.has_arcane_focus.data and 
                    self.special_equipment.arcane_focus_selection.data):
                    print("DEBUG: Cleric trying to use arcane focus")
                    self.validation_errors.append('Clerics cannot use Arcane Focus items')
                    return False
            
            # Store calculated values
            self.total_cost = total_cost
            self.remaining_funds = budget - total_cost
            print(f"DEBUG: Remaining funds: {self.remaining_funds}gp")
            
            # For purchase, validate against budget
            action = request.form.get('action', '')
            print(f"DEBUG: Action is: {action}")
            if action == 'purchase' and total_cost > budget:
                print("DEBUG: Cost exceeds budget")
                self.validation_errors.append('Total cost exceeds available funds')
                return False
            
            print("DEBUG: All validation checks passed")
            return True
            
        except (ValueError, TypeError) as e:
            print(f"DEBUG: Budget validation error: {e}")
            self.validation_errors.append('Invalid budget value')
            return False

    @property
    def selected_equipment(self):
        """Return structured dictionary of selected equipment."""
        equipment = {
            'armor': None,
            'shield': None,
            'weapons': [],
            'adventuring_gear': [],
            'special_equipment': {},
            'total_cost_gp': self.calculate_total_cost()
        }

        # Process armor
        if self.armor.data:
            category, name = self.armor.data.split(':')
            armor = next((a for a in ARMOR[category] if a['name'] == name), None)
            if armor:
                equipment['armor'] = {
                    'name': armor['name'],
                    'type': category,
                    'ac': armor['ac'],
                    'add_dex': armor['add_dex'],
                    'max_dex': armor['max_dex'],
                    'cost': armor['cost'],
                    'stealth_disadvantage': armor['stealth_disadvantage']
                }

        # Process shield
        if self.shield.data:
            category, name = self.shield.data.split(':')
            shield = next((s for s in ARMOR[category] if s['name'] == name), None)
            if shield:
                equipment['shield'] = {
                    'name': shield['name'],
                    'ac_bonus': shield['ac_bonus'],
                    'cost': shield['cost']
                }

        # Process weapons
        for category in ['simple_melee', 'simple_ranged', 'martial_melee', 'martial_ranged']:
            field = getattr(self, category)
            for selection in field.data:
                if selection:  # Skip empty selections
                    cat, name = selection.split(':')
                    weapon = next((w for w in WEAPONS[cat] if w['name'] == name), None)
                    if weapon:
                        equipment['weapons'].append({
                            'name': weapon['name'],
                            'category': cat,
                            'damage': weapon['damage'],
                            'damage_type': weapon['damage_type'],
                            'properties': weapon['properties'],
                            'cost': weapon['cost']
                        })

        # Process adventuring gear
        for gear_id in self.adventuring_gear.data:
            if gear_id in ADVENTURING_GEAR:
                gear_item = ADVENTURING_GEAR[gear_id]
                equipment['adventuring_gear'].append({
                    'name': gear_item['name'],
                    'cost': gear_item['cost']
                })

        # Process special equipment
        if self.special_equipment:
            spec_eq = self.special_equipment
            
            # Arcane Focus
            if spec_eq.has_arcane_focus.data and spec_eq.arcane_focus_selection.data:
                selection = spec_eq.arcane_focus_selection.data
                if selection in ARCANE_FOCUS_OPTIONS:
                    equipment['special_equipment']['arcane_focus'] = {
                        'name': ARCANE_FOCUS_OPTIONS[selection]['name'],
                        'cost': ARCANE_FOCUS_OPTIONS[selection]['cost']
                    }
            
            # Holy Symbol
            if spec_eq.has_holy_symbol.data and spec_eq.holy_symbol_selection.data:
                selection = spec_eq.holy_symbol_selection.data
                if selection in HOLY_SYMBOL_OPTIONS:
                    equipment['special_equipment']['holy_symbol'] = {
                        'name': HOLY_SYMBOL_OPTIONS[selection]['name'],
                        'cost': HOLY_SYMBOL_OPTIONS[selection]['cost']
                    }
            
            # Musical Instrument
            if spec_eq.has_musical_instrument.data and spec_eq.musical_instrument_selection.data:
                selection = spec_eq.musical_instrument_selection.data
                if selection in MUSICAL_INSTRUMENT_OPTIONS:
                    equipment['special_equipment']['musical_instrument'] = {
                        'name': MUSICAL_INSTRUMENT_OPTIONS[selection]['name'],
                        'cost': MUSICAL_INSTRUMENT_OPTIONS[selection]['cost']
                    }
            
            # Tools
            if spec_eq.has_tools.data and spec_eq.tool_selection.data:
                selection = spec_eq.tool_selection.data
                if selection in TOOL_OPTIONS:
                    equipment['special_equipment']['tools'] = {
                        'name': TOOL_OPTIONS[selection]['name'],
                        'cost': TOOL_OPTIONS[selection]['cost']
                    }
            
            # Ammunition
            if spec_eq.has_ammunition.data and spec_eq.ammunition_selection.data:
                selection = spec_eq.ammunition_selection.data
                if selection in AMMUNITION_OPTIONS:
                    equipment['special_equipment']['ammunition'] = {
                        'name': AMMUNITION_OPTIONS[selection]['name'],
                        'cost': AMMUNITION_OPTIONS[selection]['cost']
                    }

        return equipment
