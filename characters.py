# dnd_builder/characters.py
# -------------------------
# This module handles all character creation steps and logic for the D&D Character Builder app.
# It includes routes for each step of the character creation process, helper functions, and constants.
#
# Each section, function, and route is now commented in detail for clarity and maintainability.
#
# ——— Imports ———
# Standard library imports
import random  # Used for dice rolls and random choices
from werkzeug.datastructures import MultiDict  # For manipulating form data

# Flask imports
from flask import Blueprint, render_template, request, redirect, url_for, session, flash  # Flask web framework imports

# App-specific imports
from .forms.equipment_form import EquipmentForm  # Form for equipment selection
from .data.equipment.weapons import WEAPONS      # Weapon data
from .data.equipment.armor import ARMOR          # Armor data
from .data.equipment import has_weapon_proficiency, has_armor_proficiency  # Proficiency checkers
from .data.spells import wizard_cantrips, wizard_level1_spells, cleric_cantrips, level1_cleric_spells  # Spell lists
from .forms.skills_form import SkillsForm        # Form for skill selection
from .data.class_skills import CLASS_SKILLS      # Class skill data
from .utils.spell_utils import calc_spell_save_dc, calc_spell_attack_bonus  # Spell stat calculators
from .forms.class_form import ClassForm          # Form for class selection
from .utils.currency_utils import convert_gp_to_coins, format_coin_display  # Currency utilities

# Create a Flask Blueprint for character-related routes
bp = Blueprint("characters", __name__, url_prefix="/characters")

# ————— Constants —————

# Labels for the six D&D ability scores
ABILITY_LABELS = [
    "Strength", "Dexterity", "Constitution",
    "Intelligence", "Wisdom", "Charisma"
]

# Racial bonuses for each playable race
RACIAL_BONUSES = {
    "Elf":      {"dexterity": 2, "charisma": 1},
    "Dwarf":    {"constitution": 2, "strength": 1},
    "Halfling": {"dexterity": 2, "constitution": 1},
    "Human":    {}
}

# Class features for each class
CLASS_FEATURES = {
    "Cleric": ["Spellcasting", "Divine Order"],
    "Fighter": ["Fighting Style", "Second Wind", "Weapon Mastery"],
    "Rogue": ["Expertise", "Sneak Attack", "Thieves' Cant", "Weapon Mastery"],
    "Wizard": ["Spellcasting", "Ritual Adept", "Arcane Recovery"],
}

# Hit die for each class (used to calculate HP at level 1)
CLASS_HIT_DIE = {
    "Cleric": 8,   # 1d8
    "Fighter": 10, # 1d10
    "Rogue": 8,    # 1d8
    "Wizard": 6    # 1d6
}

# List of available fighting styles for Fighters
FIGHTING_STYLES = [
    "Archery",
    "Blind Fighting",
    "Defense",
    "Dueling",
    "Great Weapon Fighting",
    "Interception",
    "Protection",
    "Thrown Weapon Fighting",
    "Two-Weapon Fighting",
    "Unarmed Fighting",
]

# Map each skill to its governing ability
SKILL_ABILITIES = {
    "Athletics":               "strength",
    "Acrobatics":              "dexterity",
    "Sleight of Hand":         "dexterity",
    "Stealth":                 "dexterity",
    "Arcana":                  "intelligence",
    "History":                 "intelligence",
    "Investigation":           "intelligence",
    "Nature":                  "intelligence",
    "Religion":                "intelligence",
    "Animal Handling":         "wisdom",
    "Insight":                 "wisdom",
    "Medicine":                "wisdom",
    "Perception":              "wisdom",
    "Survival":                "wisdom",
    "Deception":               "charisma",
    "Intimidation":            "charisma",
    "Performance":             "charisma",
    "Persuasion":              "charisma",
}

# Coin values for currency conversion
COIN_VALUES = {"pp": 500, "gp": 100, "sp": 10, "cp": 1}
PROFICIENCY_BONUS = 2

# ————— Helpers —————

def roll_stat():
    """Roll 4d6, rerolling all 1s and 2s, then drop the lowest."""
    rolls = []
    for _ in range(4):
        # Keep rolling until we get a 3 or higher
        roll = random.randint(1, 6)
        while roll <= 2:
            roll = random.randint(1, 6)
        rolls.append(roll)
    # Drop the lowest die and sum the remaining three
    rolls = sorted(rolls)
    return sum(rolls[1:])

def coins_to_cp(coins: dict) -> int:
    """Convert a coin-dict to total copper pieces."""
    return sum(COIN_VALUES[d] * count for d, count in coins.items())

def cp_to_coins(cp_total: int) -> dict:
    """Convert a copper total back into a coin-dict."""
    rem = cp_total
    result = {}
    for denom in ("pp", "gp", "sp", "cp"):
        result[denom], rem = divmod(rem, COIN_VALUES[denom])
    return result

# ————— Step 1: Roll Ability Scores —————

@bp.route("/step1", methods=["GET", "POST"])
def step1_abilities():
    """First step: Roll ability scores and initialize session."""
    if request.method == "POST":
        session.clear()
        session["stats"] = {
            lbl.lower(): roll_stat() for lbl in ABILITY_LABELS
        }
        session["coins_left"] = {"gp": 100}
        return redirect(url_for("characters.step1_abilities"))

    return render_template(
        "index.html",
        labels=ABILITY_LABELS,
        stats=session.get("stats", {})
    )

# ————— Step 2: Choose Race —————

@bp.route("/step2_race", methods=["GET", "POST"])
def step2_race():
    """Second step: Choose a race and apply racial bonuses."""
    if request.method == "POST":
        race = request.form["race"]
        session["race"] = race

        base = session["stats"].copy()
        bonuses = RACIAL_BONUSES.get(race, {})
        adjusted_stats = {
            k: base[k] + bonuses.get(k, 0) for k in base
        }
        session["adjusted_stats"] = adjusted_stats
        # Calculate and store Constitution modifier for later HP calculation
        con_mod = (adjusted_stats['constitution'] - 10) // 2
        session["constitution_modifier"] = con_mod
        return redirect(url_for("characters.step2_race_summary"))

    return render_template(
        "race.html",
        races=list(RACIAL_BONUSES.keys())
    )

@bp.route("/step2_race_summary")
def step2_race_summary():
    """Show summary of stats after race selection."""
    return render_template(
        "race_summary.html",
        labels=ABILITY_LABELS,
        base_stats=session.get("stats", {}),
        adjusted_stats=session.get("adjusted_stats", {}),
        race=session.get("race")
    )

# ————— Step 3: Choose Class —————

@bp.route("/step3_class", methods=["GET", "POST"])
def step3_class():
    """Third step: Choose a class and set primary ability, HP, and clear old data."""
    classes = ["Fighter", "Wizard", "Rogue", "Cleric"]
    form = ClassForm(classes)
    if form.validate_on_submit():
        chosen_class = form.class_choice.data
        session["class"] = chosen_class
        # Clear expertise data for non-Rogue classes
        if chosen_class != "Rogue":
            session["expertise"] = []
        # Clear any leftover equipment/form validation data to prevent cross-contamination
        session.pop('equipment', None)
        session.pop('coins_left', None)
        session.pop('skill_proficiencies', None)
        session.pop('fighting_style', None)
        session.pop('cantrips', None)
        session.pop('level1_spells', None)
        # Calculate HP when class is chosen
        hit_die = CLASS_HIT_DIE[chosen_class]
        con_mod = session.get("constitution_modifier", 0)
        max_hp = hit_die + con_mod
        session["max_hp"] = max_hp
        session["current_hp"] = max_hp  # At character creation, current HP equals max HP
        # Handle primary ability selection
        if chosen_class == "Fighter":
            # Fighter gets to choose between Strength and Dexterity
            primary_ability = form.primary_ability.data
            if primary_ability:
                session["primary_ability"] = primary_ability
                return redirect(url_for("characters.fighter_selection"))
            else:
                flash("Fighters must select a primary ability: Strength or Dexterity.")
                return render_template("class.html", form=form)
        else:
            # Set primary abilities for other classes automatically
            primary_abilities = {
                "Wizard": "Intelligence",
                "Cleric": "Wisdom", 
                "Rogue": "Dexterity"
            }
            session["primary_ability"] = primary_abilities.get(chosen_class)
            # Clear fighting style for non-Fighter classes
            session.pop("fighting_style", None)
            return redirect(url_for("characters.step4_skills"))
    return render_template("class.html", form=form)

# ————— Fighter Primary Ability Selection —————

@bp.route("/fighter_selection", methods=["GET", "POST"])
def fighter_selection():
    """Special step for Fighters to select fighting style and skills."""
    if session.get("class") != "Fighter":
        return redirect(url_for("characters.step3_class"))
    # Ensure primary ability was already selected in previous step
    if not session.get("primary_ability"):
        flash("Please select your class and primary ability first.")
        return redirect(url_for("characters.step3_class"))
    if request.method == "POST":
        fighting_style = request.form.get("fighting_style")
        skills = request.form.getlist("skills")
        # Validate skills (Fighters get 2 skills)
        if len(skills) != 2:
            flash("Fighters must select exactly 2 skills.")
            fighting_styles = ["Archery", "Defense", "Dueling", "Great Weapon Fighting", "Protection", "Two-Weapon Fighting"]
            fighter_skills = CLASS_SKILLS.get("Fighter", [])
            return render_template("class_fighter.html", 
                                 fighting_styles=fighting_styles,
                                 skills=fighter_skills,
                                 selected_fighting=fighting_style,
                                 selected_skills=skills,
                                 primary_ability=session.get("primary_ability"))
        if fighting_style:
            session["fighting_style"] = fighting_style
            session["skills"] = skills
            return redirect(url_for("characters.step5_equipment"))
        else:
            flash("Please select a fighting style.")
    fighting_styles = ["Archery", "Defense", "Dueling", "Great Weapon Fighting", "Protection", "Two-Weapon Fighting"]
    fighter_skills = CLASS_SKILLS.get("Fighter", [])
    return render_template("class_fighter.html", 
                         fighting_styles=fighting_styles,
                         skills=fighter_skills,
                         primary_ability=session.get("primary_ability"))

# ————— Step 4: Skills Selection —————

@bp.route("/step4_skills", methods=["GET", "POST"])
def step4_skills():
    """Fourth step: Choose skills and expertise (for Rogues)."""
    char_class = session.get("class")
    if not char_class:
        return redirect(url_for("characters.step3_class"))
    form = SkillsForm(allowed_skills=CLASS_SKILLS.get(char_class, []), char_class=char_class)
    if request.method == "POST":
        # For Rogues, handle the two-step process for expertise
        if char_class == 'Rogue':
            # Check if we have skills selected but validation failed due to expertise
            if form.skills.data and len(form.skills.data) == 4:
                if not form.validate_on_submit():
                    # If only expertise validation failed, update expertise choices
                    if 'expertise' in form.errors and len(form.errors) == 1:
                        form.expertise.choices = [(skill, skill.replace('_', ' ').title()) 
                                                 for skill in form.skills.data]
                        return render_template("step4_skills.html", 
                                             form=form,
                                             char_class=char_class,
                                             chosen_class=char_class,
                                             show_expertise=True)
        if form.validate_on_submit():
            # Normalize skill names to match SKILL_ABILITIES keys (title case, spaces)
            def normalize_skill_name(name):
                for key in SKILL_ABILITIES.keys():
                    if name.replace('_', ' ').strip().lower() == key.lower():
                        return key
                return name  # fallback
            normalized_skills = [normalize_skill_name(s) for s in form.skills.data]
            # Force save normalized skills to session
            session["skill_proficiencies"] = normalized_skills
            # Save expertise for Rogues, or clear for others
            if hasattr(form, 'expertise') and form.expertise.data:
                normalized_expertise = [normalize_skill_name(s) for s in form.expertise.data]
                session["expertise"] = normalized_expertise
            else:
                session["expertise"] = []
            # Route to spell selection for spellcasters, equipment for others
            if char_class in ["Wizard", "Cleric"]:
                return redirect(url_for("characters.spell_selection"))
            return redirect(url_for("characters.step5_equipment"))
        else:
            return render_template("step4_skills.html", 
                                 form=form,
                                 char_class=char_class,
                                 chosen_class=char_class)
    # GET branch
    return render_template("step4_skills.html", 
                         form=form,
                         char_class=char_class,
                         chosen_class=char_class)

# ————— Spell Selection —————

@bp.route("/spell_selection", methods=["GET", "POST"])
def spell_selection():
    """Fifth step: Choose cantrips and level 1 spells (for Wizards and Clerics)."""
    char_class = session.get("class")
    if not char_class or char_class not in ["Wizard", "Cleric"]:
        return redirect(url_for("characters.step3_class"))

    # Calculate spell preparation info for both classes
    # For character creation, both classes get the same amount for maximum potential
    if char_class == "Cleric":
        wisdom_score = session.get("adjusted_stats", {}).get("wisdom", 10)
        wisdom_mod = (wisdom_score - 10) // 2
        spells_preparable = max(1, wisdom_mod + 1)  # For gameplay reference
        creation_spells = 6  # For character creation, select 6 spells like wizards
    elif char_class == "Wizard":
        creation_spells = 6  # Wizards get 6 spells in their spellbook at 1st level
        spells_preparable = 6
    
    if request.method == "POST":
        # Check if this is actually a form submission
        if 'submit' not in request.form and 'choose_spells' not in request.form:
            print("DEBUG: No submit button found in form data!")
        
        cantrips = request.form.getlist("cantrips")
        level1_spells = request.form.getlist("level1_spells")
        
        # Parse the spell data if it's coming as tuple strings
        def parse_spell_data(spell_value):
            """Extract spell ID from various formats"""
            if isinstance(spell_value, str):
                if spell_value.startswith("('") and "'" in spell_value:
                    # Handle tuple string like "('light', 'Light', False)" or "('command', 'Command')"
                    # Remove parentheses and split by comma
                    cleaned = spell_value.strip("()").replace("'", "")
                    parts = [part.strip() for part in cleaned.split(", ")]
                    return parts[0]  # Return the spell ID (first part)
                else:
                    return spell_value  # Already just the spell ID
            else:
                return str(spell_value)
        
        parsed_cantrips = []
        for cantrip in cantrips:
            parsed_cantrips.append(parse_spell_data(cantrip))
        
        parsed_level1_spells = []
        for spell in level1_spells:
            parsed_level1_spells.append(parse_spell_data(spell))
        
        # Validate spell selections based on class mechanics
        # Both classes select 6 spells at creation for maximum potential
        if len(parsed_cantrips) != 3:
            flash("Select exactly 3 cantrips.")
            return redirect(url_for("characters.spell_selection"))
        
        if len(parsed_level1_spells) != creation_spells:
            if char_class == "Wizard":
                flash(f"Select exactly 3 cantrips and {creation_spells} first-level spells for your spellbook.")
            else:  # Cleric
                flash(f"Select exactly 3 cantrips and {creation_spells} first-level spells to prepare.")
            return redirect(url_for("characters.spell_selection"))

        # Store spell selections and class-specific info in session
        session["cantrips"] = parsed_cantrips
        if char_class == "Wizard":
            session["level1_spells"] = parsed_level1_spells  # Spells in spellbook
        else:  # Cleric
            session["level1_spells"] = parsed_level1_spells  # Prepared spells
            session["spells_preparable"] = spells_preparable  # Number of spells they can prepare
        
        return redirect(url_for("characters.step5_equipment"))

    # Get appropriate spell lists and class-specific context
    if char_class == "Wizard":
        from .data.spells import wizard_cantrips, wizard_level1_spells
        context = {
            "cantrips": wizard_cantrips,
            "level1_spells": wizard_level1_spells,
            "spellcasting_note": f"Choose 3 cantrips and {creation_spells} first-level spells for your spellbook. "
                                "You can only prepare a number of these spells each day after a long rest.",
            "spells_preparable": creation_spells
        }
    else:  # Cleric
        context = {
            "cantrips": cleric_cantrips,
            "level1_spells": level1_cleric_spells,
            "spellcasting_note": f"Choose 3 cantrips that you will always know. "
                                f"Choose {creation_spells} first-level spells to prepare at character creation. "
                                f"(During gameplay, you can prepare {spells_preparable} spells daily based on Wisdom.)",
            "spells_preparable": creation_spells
        }

    return render_template("spells.html", 
                         char_class=char_class,
                         show_level1_selection=True,  # Both Wizard and Cleric should show level 1 selection
                         **context)

# ————— Step 5: Equipment Selection —————

@bp.route("/step5_equipment", methods=["GET", "POST"])
def step5_equipment():
    """Fifth step: Select equipment, weapons, and armor."""
    if request.method == "POST":
        print(f"DEBUG: Equipment POST request received")
        print(f"DEBUG: All form keys: {list(request.form.keys())}")
        print(f"DEBUG: Form data: {dict(request.form)}")
    
    # Get character info from session
    char_class = session.get("class")
    if not char_class:
        print("DEBUG: No character class in session, redirecting")
        return redirect(url_for("characters.step3_class"))
    
    print(f"DEBUG: Equipment step - Class is: {char_class}")

    # Clear equipment data if coming from a previous step
    if request.method == "GET" and request.referrer and 'step4_skills' in request.referrer:
        session.pop('coins_left', None)
        session.pop('equipment', None)

    dex_mod = (session.get("adjusted_stats", {}).get("dexterity", 10) - 10) // 2
    
    # Define starting gold by class
    class_starting_gold = {
        "Cleric": 110,
        "Fighter": 155,
        "Rogue": 100,
        "Wizard": 55
    }
    
    starting_gp = class_starting_gold[char_class]  # Use direct lookup since we know char_class is valid
    
    # Always reset coins when starting equipment step
    # Convert starting gold to a complete coin dictionary
    session["coins_left"] = {"pp": 0, "gp": starting_gp, "sp": 0, "cp": 0}
    session["previous_class"] = char_class
    
    coins_left = session.get("coins_left")
    budget_gp = coins_left.get("gp", starting_gp)
    print(f"DEBUG: Starting budget: {budget_gp}gp")

    # Set default values for GET request
    remaining_funds = budget_gp

    # Create form and populate with request data if it's a POST
    # For POST requests, pass the form data to the constructor
    if request.method == 'POST':
        # Create a mutable copy of form data and add budget
        form_data = MultiDict(request.form)
        form_data['budget'] = str(budget_gp)
        form = EquipmentForm(form_data)
    else:
        form = EquipmentForm()
        form.budget.data = str(budget_gp)
    
    # Set form properties
    form.char_class = char_class
    print(f"DEBUG: Set form budget to: {form.budget.data}")
    
    # Set up spell choices for spell scrolls based on class and level
    if request.method == 'POST':
        level = request.form.get('special_equipment-spell_scroll_level', '0')
        spell_class = request.form.get('special_equipment-spell_scroll_class', 'wizard')
    else:
        level = '0'
        spell_class = 'wizard'
    
    # Get appropriate spell list
    from .data.spells import (wizard_cantrips, wizard_level1_spells,
                            cleric_cantrips, level1_cleric_spells)
    
    if spell_class == 'wizard':
        spells = wizard_cantrips if level == '0' else wizard_level1_spells
    else:
        if level == '0':
            # Cleric cantrips have 3 elements, extract first 2
            spells = [(spell[0], spell[1]) for spell in cleric_cantrips]
        else:
            spells = level1_cleric_spells
    
    # Update spell selection choices
    form.special_equipment.spell_selection.choices = [
        (spell_id, spell_name) for spell_id, spell_name in spells
    ]

    # Initialize equipment for both GET and POST
    equipment = {
        'armor': None,
        'shield': None,
        'weapons': [],
        'armor_class': 10 + dex_mod,  # Base AC
        'total_cost_gp': 0
    }
    
    if request.method == 'POST':
        print(f"DEBUG: POST request received")
        print(f"DEBUG: Form data: {request.form}")
        print(f"DEBUG: CSRF token present: {'csrf_token' in request.form}")
        
        # Ensure budget is set before validation
        print(f"DEBUG: Form budget before validation: {form.budget.data}")
        if not form.budget.data:
            form.budget.data = str(budget_gp)
            print(f"DEBUG: Set form budget to: {form.budget.data}")
        
        # Check if this is a special equipment toggle request
        if request.form.get('action') == 'toggle_special':
            print(f"DEBUG: Toggling special equipment visibility")
            
            # Create a new form instance with preserved data to maintain state
            preserved_form = EquipmentForm(formdata=request.form)
            preserved_form.char_class = char_class
            preserved_form.budget.data = str(budget_gp)
            
            # Re-render the form with updated checkbox states
            remaining_coins = convert_gp_to_coins(budget_gp)
            return render_template('step5_equipment.html',
                                form=preserved_form,
                                starting_funds=budget_gp,
                                remaining_coins=remaining_coins,
                                remaining_funds=preserved_form.remaining_funds,
                                equipment=equipment,
                                format_coin_display=format_coin_display)
        
        # Check if this is a spell list update request
        if request.form.get('action') == 'update_spells':
            print(f"DEBUG: Updating spell choices")
            
            # Preserve all current form selections
            form_data = request.form.to_dict(flat=False)
            
            # Create a new form instance with preserved data to maintain state
            preserved_form = EquipmentForm(formdata=request.form)
            preserved_form.char_class = char_class
            preserved_form.budget.data = str(budget_gp)
            
            # Explicitly preserve the spell scroll checkbox state
            if request.form.get('special_equipment-has_spell_scroll'):
                preserved_form.special_equipment.has_spell_scroll.data = True
            
            print(f"DEBUG: Spell scroll checkbox state: {preserved_form.special_equipment.has_spell_scroll.data}")
            
            # Update spell selection choices based on current class and level
            spell_class = preserved_form.special_equipment.spell_scroll_class.data or 'wizard'
            spell_level = preserved_form.special_equipment.spell_scroll_level.data or '0'
            
            from .data.spells import (wizard_cantrips, wizard_level1_spells,
                                     cleric_cantrips, level1_cleric_spells)
            
            def get_spell_choices(spell_class, level):
                if spell_class == 'wizard':
                    return wizard_cantrips if level == '0' else wizard_level1_spells
                elif spell_class == 'cleric':
                    if level == '0':
                        # Cleric cantrips have 3 elements, extract first 2
                        return [(spell[0], spell[1]) for spell in cleric_cantrips]
                    else:
                        return level1_cleric_spells
                return []
            
            spell_list = get_spell_choices(spell_class, spell_level)
            # Add pricing to spell choices
            spell_price = 30 if spell_level == '0' else 50  # 30gp for cantrips, 50gp for 1st level
            preserved_form.special_equipment.spell_selection.choices = [('', '-- Select Spell --')] + [
                (key, f"{name} ({spell_price} gp)") for key, name in spell_list
            ]
            
            print(f"DEBUG: Updated spell choices for {spell_class} level {spell_level}: {len(spell_list)} spells")
            
            # Re-render the form with updated spell choices and preserved state
            remaining_coins = convert_gp_to_coins(budget_gp)
            return render_template('step5_equipment.html',
                                form=preserved_form,
                                starting_funds=budget_gp,
                                remaining_coins=remaining_coins,
                                remaining_funds=preserved_form.remaining_funds,  # Add this for template compatibility
                                equipment=equipment,
                                format_coin_display=format_coin_display)
        
        # Validate form
        form.equipment_check.data = "check"  # Trigger equipment validation
        print(f"DEBUG: About to validate form...")
        
        # Check each field for errors before validation
        for field_name, field in form._fields.items():
            if hasattr(field, 'data'):
                print(f"DEBUG: Field {field_name}: data={field.data}, raw_data={getattr(field, 'raw_data', None)}")
        
        is_valid = form.validate()
        print(f"DEBUG: Form validation result: {is_valid}")
        
        # Check for field errors after validation
        for field_name, field in form._fields.items():
            if field.errors:
                print(f"DEBUG: Field {field_name} has errors: {field.errors}")
        
        print(f"DEBUG: Form validation errors: {getattr(form, 'validation_errors', [])}")
        print(f"DEBUG: Form field errors: {form.errors}")
        
        if is_valid:
            print("DEBUG: Form validated successfully")
            
            # Calculate costs in gold pieces
            total_cost_gp = form.calculate_total_cost()  # in gold pieces
            remaining_gp = budget_gp - total_cost_gp
            
            # Convert costs to coin denominations
            total_coins = convert_gp_to_coins(total_cost_gp)
            remaining_coins = convert_gp_to_coins(remaining_gp)
            
            # Format for display
            total_cost_str = format_coin_display(total_coins)
            remaining_funds_str = format_coin_display(remaining_coins)
            
            print(f"DEBUG: Total cost: {total_cost_str}")
            print(f"DEBUG: Remaining: {remaining_funds_str}")
            
            # Store the remaining funds in the session
            session['coins_left'] = remaining_coins
            
            # Get selected equipment and process proficiencies
            equipment = form.selected_equipment
            equipment['armor_class'] = 10 + dex_mod  # Base AC
            equipment['unusable_items'] = []  # Track items character can't use effectively
            
            # Check armor proficiency
            if equipment['armor']:
                armor = equipment['armor']
                if not has_armor_proficiency(char_class, armor['type']):
                    equipment['unusable_items'].append({
                        'item': armor['name'],
                        'type': 'armor',
                        'reason': f"Not proficient with {armor['type']} armor"
                    })
            
            # Check shield proficiency
            if equipment['shield']:
                if not has_armor_proficiency(char_class, 'shields'):
                    equipment['unusable_items'].append({
                        'item': equipment['shield']['name'],
                        'type': 'shield',
                        'reason': "Not proficient with shields"
                    })
            
            # Check weapon proficiencies
            for weapon in equipment['weapons']:
                weapon_category = weapon.get('category', '')
                if weapon_category.startswith('martial'):
                    # Use the full category name for proficiency check
                    if not has_weapon_proficiency(char_class, weapon_category):
                        equipment['unusable_items'].append({
                            'item': weapon['name'],
                            'type': 'weapon',
                            'reason': f"Not proficient with martial weapons"
                        })
            
            # If this is a preview, render with the preview flag
            if request.form.get('action') == 'preview':
                remaining_coins = convert_gp_to_coins(form.remaining_funds)
                return render_template('step5_equipment.html',
                                    form=form,
                                    starting_funds=budget_gp,
                                    remaining_coins=remaining_coins,
                                    remaining_funds=form.remaining_funds,  # Add this for template compatibility
                                    preview=True,
                                    equipment=equipment,
                                    format_coin_display=format_coin_display)
                                    
            # If this is a purchase and we have enough funds
            elif request.form.get('action') == 'purchase':
                if form.remaining_funds >= 0:
                    # Calculate final costs in gold pieces
                    total_cost = form.calculate_total_cost()
                    remaining_gp = budget_gp - total_cost
                    remaining_coins = convert_gp_to_coins(remaining_gp)
                    
                    # Store equipment and update funds
                    session['equipment'] = equipment
                    session['coins_left'] = remaining_coins
                    print(f"DEBUG: Purchase completed. Starting: {budget_gp}gp, Cost: {total_cost}gp, Remaining: {format_coin_display(remaining_coins)}")
                    
                    # Flash warnings about unusable items
                    if equipment['unusable_items']:
                        warnings = []
                        for item in equipment['unusable_items']:
                            warnings.append(f"{item['item']}: {item['reason']}")
                        flash("Warning: You purchased items you aren't proficient with: " + "; ".join(warnings))
                    
                    return redirect(url_for('characters.character_name'))
                else:
                    flash("You don't have enough funds for this purchase.")
                    # Re-render the form with the error
                    remaining_coins = convert_gp_to_coins(form.remaining_funds)
                    return render_template('step5_equipment.html',
                                        form=form,
                                        starting_funds=budget_gp,
                                        remaining_coins=remaining_coins,
                                        remaining_funds=form.remaining_funds,  # Add this for template compatibility
                                        equipment=equipment,
                                        format_coin_display=format_coin_display)
        else:
            print("DEBUG: Form validation failed")
            print(f"DEBUG: Form validation errors: {getattr(form, 'validation_errors', [])}")
            print(f"DEBUG: Form field errors: {form.errors}")
            # Re-render the form with errors
            for error in getattr(form, 'validation_errors', []):
                flash(error)
            remaining_coins = convert_gp_to_coins(form.remaining_funds if hasattr(form, 'remaining_funds') else budget_gp)
            return render_template('step5_equipment.html',
                                form=form,
                                starting_funds=budget_gp,
                                remaining_coins=remaining_coins,
                                remaining_funds=form.remaining_funds if hasattr(form, 'remaining_funds') else budget_gp,  # Add this for template compatibility
                                equipment=equipment,
                                format_coin_display=format_coin_display)
            
            # Process armor selection
            if form.armor.data:
                category, name = form.armor.data.split(':')
                armor_item = next((a for a in ARMOR[category] if a['name'] == name), None)
                if armor_item:
                    armor_item = {**armor_item, 'add_dex': category in ['light', 'medium']}
                    if category == 'medium':
                        armor_item['max_dex'] = 2
                    elif category == 'light':
                        armor_item['max_dex'] = None
                    equipment['armor'] = armor_item
                    # Update AC based on armor
                    equipment['armor_class'] = armor_item['ac']
                    if armor_item['add_dex']:
                        max_dex = armor_item.get('max_dex')
                        if max_dex is not None:
                            equipment['armor_class'] += min(dex_mod, max_dex)
                        else:
                            equipment['armor_class'] += dex_mod
            
            # Process shield selection
            if form.shield.data:
                shield_item = ARMOR['shield'][0]  # There's only one shield
                if shield_item:
                    equipment['shield'] = shield_item
                    equipment['armor_class'] += shield_item['ac_bonus']

            # Process weapon selections
            for field in [form.simple_melee, form.simple_ranged, form.martial_melee, form.martial_ranged]:
                for weapon_data in field.data:
                    if weapon_data:
                        category, name = weapon_data.split(':')
                        weapon_item = next((w for w in WEAPONS[category] if w['name'] == name), None)
                        if weapon_item:
                            equipment['weapons'].append({'category': category, 'name': name, **weapon_item})

    # For initial load, set up initial coins with full budget
    remaining_coins = convert_gp_to_coins(budget_gp)
    return render_template(
        "step5_equipment.html",
        form=form,
        starting_funds=budget_gp,
        remaining_coins=remaining_coins,
        remaining_funds=budget_gp,  # Add this for template compatibility
        preview=False,
        format_coin_display=format_coin_display
    )
    
# This section has been moved up to combine with the new equipment handling system

# ————— Step 6: Summary & “Begin Adventure” —————

@bp.route("/character_name", methods=["GET", "POST"])
def character_name():
    """Step for naming the character before final summary"""
    if request.method == "POST":
        character_name = request.form.get("character_name", "").strip()
        if character_name:
            session["character_name"] = character_name
            return redirect(url_for('characters.step6_summary'))
        else:
            flash("Please enter a character name.")
    
    return render_template("character_name.html", 
                         char_class=session.get("class"),
                         race=session.get("race"))

@bp.route("/step6_summary")
def step6_summary():
    if "stats" not in session or "class" not in session:
        return redirect(url_for("characters.step1_abilities"))

    # Core stats & modifiers
    stats = session.get("adjusted_stats", session.get("stats"))
    char_class = session.get("class")
    prof_bonus = PROFICIENCY_BONUS
    
    # Get spellcasting info for casters
    spellcasting_ability = None
    cast_mod = 0
    spell_save_dc = 0
    spell_attack_bonus = 0
    
    if char_class == "Wizard":
        spellcasting_ability = "intelligence"
    elif char_class == "Cleric":
        spellcasting_ability = "wisdom"
        
    if spellcasting_ability:
        ability_score = stats[spellcasting_ability]
        cast_mod = (ability_score - 10) // 2
        spells_preparable = max(1, cast_mod + 1)  # Level 1 + ability modifier (minimum 1)
        
        # Calculate spell save DC and attack bonus
        spell_save_dc = calc_spell_save_dc(cast_mod, prof_bonus)
        spell_attack_bonus = calc_spell_attack_bonus(cast_mod, prof_bonus)

    # Calculate ability modifiers
    ability_mods = {
        abbr: (score - 10) // 2
        for abbr, score in stats.items()
    }

    # Get equipment from session
    equipment = session.get("equipment", {
        'armor': None,
        'shield': None,
        'weapons': [],
        'unequipped_items': [],
        'armor_class': 10 + ability_mods['dexterity']  # Base AC if no equipment
    })

    # If AC hasn't been calculated (e.g., old session data)
    if 'armor_class' not in equipment:
        from .utils.armor_utils import calculate_ac
        equipment['armor_class'] = calculate_ac(
            armor=equipment.get('armor'),
            shield=equipment.get('shield'),
            dex_modifier=ability_mods['dexterity']
        )

    # Get remaining funds
    coins_left = session.get('coins_left', {'gp': 0})
    remaining_gp = coins_left['gp']  # Already in gold pieces

    # Calculate casting modifier if applicable
    cast_mod = ability_mods['intelligence'] if char_class == "Wizard" else \
               ability_mods['wisdom'] if char_class == "Cleric" else 0

    # Build skill modifiers list
    # Fallback: if skill_proficiencies is missing, try to use any available skills
    profs = set(session.get("skill_proficiencies") or session.get("skills") or [])
    expertise = set(session.get("expertise", []))
    print(f"DEBUG STATS: {stats}")
    print(f"DEBUG ABILITY_MODS: {ability_mods}")
    print(f"DEBUG PROFS: {profs}")
    print(f"DEBUG EXPERTISE: {expertise}")
    skills_list = []
    for skill, abbr in SKILL_ABILITIES.items():
        is_prof = skill in profs
        has_expertise = skill in expertise
        base_mod = ability_mods[abbr]
        # Expertise doubles proficiency bonus
        prof_modifier = prof_bonus * 2 if has_expertise else prof_bonus if is_prof else 0
        total_mod = base_mod + prof_modifier
        print(f"DEBUG SKILL: {skill} | Ability: {abbr} | base_mod: {base_mod} | Proficient: {is_prof} | Expertise: {has_expertise} | prof_bonus: {prof_bonus} | prof_modifier: {prof_modifier} | total_mod: {total_mod}")
        skills_list.append({
            "name": skill,
            "ability": abbr[:3].upper(),  # Just use first 3 letters for display
            "mod": total_mod,
            "proficient": is_prof,
            "expertise": has_expertise
        })
    
    # Calculate passive perception
    perception_prof = "Perception" in profs
    passive_perception = 10 + ability_mods['wisdom'] + (prof_bonus if perception_prof else 0)

    # Check weapon proficiencies for attack bonus calculations
    from .data.equipment import has_weapon_proficiency
    
    # Check if character is proficient with any melee/ranged weapons
    melee_proficient = False
    ranged_proficient = False
    
    if equipment.get('weapons'):
        for weapon in equipment['weapons']:
            weapon_category = weapon.get('category', '')
            if has_weapon_proficiency(char_class, weapon_category):
                weapon['proficient'] = True
                # Check if this weapon can be used for melee or ranged attacks
                properties = weapon.get('properties', [])
                if 'ranged' in weapon_category or 'thrown' in properties or 'range' in weapon.get('name', '').lower():
                    ranged_proficient = True
                else:
                    melee_proficient = True
            else:
                weapon['proficient'] = False
    
    # Also check general proficiencies based on class
    if has_weapon_proficiency(char_class, 'simple_melee') or has_weapon_proficiency(char_class, 'martial_melee'):
        melee_proficient = True
    if has_weapon_proficiency(char_class, 'simple_ranged') or has_weapon_proficiency(char_class, 'martial_ranged'):
        ranged_proficient = True

    # Create spell lookup dictionaries
    def create_spell_lookup():
        lookup = {}
        # Add wizard spells (2-tuple format: id, name)
        for spell_id, spell_name in wizard_cantrips + wizard_level1_spells:
            lookup[spell_id] = spell_name
        # Add cleric cantrips (3-tuple format: id, name, concentration)
        for spell_data in cleric_cantrips:
            if len(spell_data) == 3:
                spell_id, spell_name, concentration = spell_data
                lookup[spell_id] = spell_name
            else:
                spell_id, spell_name = spell_data
                lookup[spell_id] = spell_name
        # Add level 1 cleric spells (2-tuple format: id, name)
        for spell_id, spell_name in level1_cleric_spells:
            lookup[spell_id] = spell_name
        return lookup
    
    spell_lookup = create_spell_lookup()
    
    # Convert stored spell IDs back to names for display
    cantrip_names = []
    for cantrip_data in session.get("cantrips", []):
        # Handle different data types that might be stored
        if isinstance(cantrip_data, (list, tuple)):
            # If it's a tuple/list, extract the ID (first element) or name (second element)
            if len(cantrip_data) >= 2:
                spell_id = cantrip_data[0]
                spell_name = cantrip_data[1]  # Use the actual spell name if available
            else:
                spell_id = cantrip_data[0]
                spell_name = spell_lookup.get(spell_id, spell_id)
        elif isinstance(cantrip_data, str):
            # Parse tuple strings like "('light', 'Light', False)"
            if cantrip_data.startswith("('") and "'" in cantrip_data:
                parts = cantrip_data.replace("('", "").replace("')", "").split("', '")
                spell_id = parts[0]
                spell_name = parts[1] if len(parts) > 1 else spell_lookup.get(spell_id, spell_id)
            else:
                spell_id = cantrip_data
                spell_name = spell_lookup.get(spell_id, cantrip_data)
        else:
            spell_name = str(cantrip_data)
        
        # Clean up the spell name
        if isinstance(spell_name, str) and '_' in spell_name:
            spell_name = spell_name.replace('_', ' ').title()
        cantrip_names.append(spell_name)
    
    level1_spell_names = []
    for spell_data in session.get("level1_spells", []):
        # Handle different data types that might be stored
        if isinstance(spell_data, (list, tuple)):
            # If it's a tuple/list, extract the ID (first element) or name (second element)
            if len(spell_data) >= 2:
                spell_id = spell_data[0]
                spell_name = spell_data[1]  # Use the actual spell name if available
            else:
                spell_id = spell_data[0]
                spell_name = spell_lookup.get(spell_id, spell_id)
        elif isinstance(spell_data, str):
            # Parse tuple strings like "('command', 'Command')"
            if spell_data.startswith("('") and "'" in spell_data:
                parts = spell_data.replace("('", "").replace("')", "").split("', '")
                spell_id = parts[0]
                spell_name = parts[1] if len(parts) > 1 else spell_lookup.get(spell_id, spell_id)
            else:
                spell_id = spell_data
                spell_name = spell_lookup.get(spell_id, spell_data)
        else:
            spell_name = str(spell_data)
        
        # Clean up the spell name
        if isinstance(spell_name, str) and '_' in spell_name:
            spell_name = spell_name.replace('_', ' ').title()
        level1_spell_names.append(spell_name)

    # Store computed data in session for PDF generation
    session["skills_list"] = sorted(skills_list, key=lambda x: x["name"])
    session["passive_perception"] = passive_perception
    session["spell_save_dc"] = spell_save_dc
    session["spell_attack_bonus"] = spell_attack_bonus

    # For Wizards and Clerics, show summary without spells, then redirect to spells page
    if char_class in ["Wizard", "Cleric"]:
        # Render summary without spells, then redirect to spells page
        resp = render_template(
            "summary.html",
            character_name=session.get("character_name"),
            race=session.get("race"),
# Pass all relevant character summary data to the summary.html template for rendering
            char_class=char_class,  # Character's class (e.g., Fighter, Wizard)
            class_features=CLASS_FEATURES.get(char_class, []),  # List of class features
            primary_ability=session.get("primary_ability"),  # Main ability for the class
            fighting_style=session.get("fighting_style"),  # Chosen fighting style (if any)
            max_hp=session.get("max_hp"),  # Calculated max HP
            CLASS_HIT_DIE=CLASS_HIT_DIE,  # Hit die mapping for all classes
            constitution_modifier=session.get("constitution_modifier"),  # Constitution modifier
            spellcasting_ability=spellcasting_ability,  # Spellcasting ability (if any)
            spell_save_dc=spell_save_dc,  # Spell save DC (if any)
            spell_attack_bonus=spell_attack_bonus,  # Spell attack bonus (if any)
            # Only pass cleric spells if class is Cleric
            level1_cleric_spells=level1_cleric_spells if char_class == "Cleric" else None,
            spells_preparable=spells_preparable if char_class == "Cleric" else None,
            stats=stats,  # Final stats (STR, DEX, etc.)
            ability_mods=ability_mods,  # Ability modifiers
            skill_proficiencies=profs,  # List of proficient skills
            skills_list=sorted(skills_list, key=lambda x: x["name"]),  # All skills, sorted by name
            passive_perception=passive_perception,  # Calculated passive perception
            prof_bonus=prof_bonus,  # Proficiency bonus
            equipment=equipment,  # Equipment dictionary
            coins_left=coins_left,  # Remaining coins
            melee_proficient=melee_proficient,  # Whether character is proficient with melee weapons
            ranged_proficient=ranged_proficient,  # Whether character is proficient with ranged weapons
            cast_mod=cast_mod  # Spellcasting modifier (if any)
        )
        # After rendering the summary, redirect to the spells summary page after a short delay
        from flask import redirect, url_for  # Import redirect and url_for for navigation
        session["cantrip_names"] = cantrip_names  # Store selected cantrips in session
        session["level1_spell_names"] = level1_spell_names  # Store selected level 1 spells in session
        # Return the rendered summary plus a script to redirect to spells summary after 2 seconds
        return resp + "<script>setTimeout(function(){ window.location='" + url_for('characters.spells_summary') + "'; }, 2000);</script>"
    else:
        # If not a spellcaster, render the summary page directly with all relevant data
        return render_template(
            "summary.html",  # Template for character summary
            character_name=session.get("character_name"),
            race=session.get("race"),
            char_class=char_class,
            class_features=CLASS_FEATURES.get(char_class, []),
            primary_ability=session.get("primary_ability"),
            fighting_style=session.get("fighting_style"),
            max_hp=session.get("max_hp"),
            CLASS_HIT_DIE=CLASS_HIT_DIE,
            constitution_modifier=session.get("constitution_modifier"),
            spellcasting_ability=spellcasting_ability,
            spell_save_dc=spell_save_dc,
            spell_attack_bonus=spell_attack_bonus,
            cantrips=cantrip_names,  # List of cantrips (if any)
            level1_spells=level1_spell_names,  # List of level 1 spells (if any)
            level1_cleric_spells=level1_cleric_spells if char_class == "Cleric" else None,
            spells_preparable=spells_preparable if char_class == "Cleric" else None,
            stats=stats,
            ability_mods=ability_mods,
            skill_proficiencies=profs,
            skills_list=sorted(skills_list, key=lambda x: x["name"]),
            passive_perception=passive_perception,
            prof_bonus=prof_bonus,
            equipment=equipment,
            coins_left=coins_left,
            melee_proficient=melee_proficient,
            ranged_proficient=ranged_proficient,
            cast_mod=cast_mod
        )
# Route for spells summary page for Wizards/Clerics
@bp.route("/spells_summary")
def spells_summary():
    # Get the character's class from the session
    char_class = session.get("class")
    # Render the spells_summary.html template with all relevant spellcasting and character data
    return render_template(
        "spells_summary.html",  # Template for spells summary
        character_name=session.get("character_name"),  # Character's name
        race=session.get("race"),  # Character's race
        char_class=char_class,  # Character's class
        class_features=CLASS_FEATURES.get(char_class, []),  # List of class features
        primary_ability=session.get("primary_ability"),  # Main ability for the class
        fighting_style=session.get("fighting_style"),  # Chosen fighting style (if any)
        max_hp=session.get("max_hp"),  # Calculated max HP
        CLASS_HIT_DIE=CLASS_HIT_DIE,  # Hit die mapping for all classes
        constitution_modifier=session.get("constitution_modifier"),  # Constitution modifier
        spellcasting_ability=session.get("spellcasting_ability"),  # Spellcasting ability (if any)
        spell_save_dc=session.get("spell_save_dc"),  # Spell save DC (if any)
        spell_attack_bonus=session.get("spell_attack_bonus"),  # Spell attack bonus (if any)
        cantrips=session.get("cantrip_names", []),  # List of selected cantrips
        level1_spells=session.get("level1_spell_names", []),  # List of selected level 1 spells
        stats=session.get("adjusted_stats", session.get("stats")),  # Final stats (may be adjusted)
        ability_mods=session.get("ability_mods"),  # Ability modifiers
        skill_proficiencies=session.get("skill_proficiencies"),  # List of proficient skills
        skills_list=session.get("skills_list", []),  # All skills
        passive_perception=session.get("passive_perception"),  # Calculated passive perception
        prof_bonus=2,  # Proficiency bonus (hardcoded for level 1)
        equipment=session.get("equipment", {}),  # Equipment dictionary
        coins_left=session.get("coins_left", {"gp": 0}),  # Remaining coins
        melee_proficient=session.get("melee_proficient", False),  # Melee proficiency
        ranged_proficient=session.get("ranged_proficient", False),  # Ranged proficiency
        cast_mod=session.get("cast_mod", 0)  # Spellcasting modifier
    )
