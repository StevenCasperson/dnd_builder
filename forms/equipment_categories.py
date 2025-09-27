# dnd_builder/forms/equipment_categories.py
# This module defines a subform for special equipment categories in the equipment selection process.
from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, BooleanField, FormField
from wtforms.validators import Optional

# SpecialEquipmentForm is a subform for selecting special equipment (tools, instruments, foci, etc.)
class SpecialEquipmentForm(FlaskForm):
    """Form fields for special equipment categories that need dynamic menus"""
    class Meta:
        # CSRF is handled by the parent form, so disable it here
        csrf = False
    
    # Tools selection
    has_tools = BooleanField('Tools')
    tool_selection = SelectField('Select Tool', choices=[
        ('thieves_tools', "Thieves' Tools (25 gp)"),
        ('herbalism_kit', "Herbalism Kit (5 gp)"),
        ('disguise_kit', "Disguise Kit (25 gp)"),
        ('forgery_kit', "Forgery Kit (15 gp)"),
        ('poisoners_kit', "Poisoner's Kit (50 gp)")
    ], validators=[Optional()])
    
    # Musical Instruments selection
    has_musical_instrument = BooleanField('Musical Instrument')
    musical_instrument_selection = SelectField('Select Instrument', choices=[
        ('flute', "Flute (2 gp)"),
        ('horn', "Horn (3 gp)"),
        ('lute', "Lute (35 gp)"),
        ('lyre', "Lyre (30 gp)"),
        ('pan_flute', "Pan Flute (12 gp)"),
        ('drums', "Drums (6 gp)")
    ], validators=[Optional()])
    
    # Arcane Focus selection
    has_arcane_focus = BooleanField('Arcane Focus')
    arcane_focus_selection = SelectField('Select Arcane Focus', choices=[
        ('crystal', "Crystal (10 gp)"),
        ('orb', "Orb (20 gp)"),
        ('rod', "Rod (10 gp)"),
        ('staff', "Staff (5 gp)"),
        ('wand', "Wand (10 gp)")
    ], validators=[Optional()])
    
    # Holy Symbol selection
    has_holy_symbol = BooleanField('Holy Symbol')
    holy_symbol_selection = SelectField('Select Holy Symbol', choices=[
        ('amulet', "Amulet (5 gp)"),
        ('emblem', "Emblem (5 gp)"),
        ('reliquary', "Reliquary (5 gp)")
    ], validators=[Optional()])
    
    # Ammunition selection
    has_ammunition = BooleanField('Ammunition')
    ammunition_selection = SelectField('Select Ammunition', choices=[
        ('arrows', "Arrows (20) (1 gp)"),
        ('crossbow_bolts', "Crossbow Bolts (20) (1 gp)"),
        ('sling_bullets', "Sling Bullets (20) (4 cp)")
    ], validators=[Optional()])
    
    # Spell Scroll fields (for selecting spell scrolls by class and level)
    has_spell_scroll = BooleanField('Spell Scroll')
    spell_scroll_level = SelectField('Spell Level', 
                                   choices=[('0', 'Cantrip (30 gp)'), ('1', '1st Level (50 gp)')],
                                   validators=[Optional()])
    spell_scroll_class = SelectField('Spell Class',
                                   choices=[('wizard', 'Wizard'), ('cleric', 'Cleric')],
                                   validators=[Optional()])
    spell_selection = SelectField('Select Spell', choices=[], validators=[Optional()])

# This subform is used within the main EquipmentForm to handle dynamic and class-specific equipment options.
# It allows the user to select special items, spell scrolls, and other gear that require additional logic or menus.
