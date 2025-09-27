# Import FlaskForm for form creation, SelectMultipleField for multiple selection fields, SubmitField for the submit button,
# and validators for form validation.
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, ValidationError
from wtforms.validators import DataRequired
# Import spell data for populating choices
from ..data.spells import level1_spells, cleric_cantrips, level1_cleric_spells

# SpellForm is used for selecting cantrips and spells for a spellcasting character (e.g., Wizard)
class SpellForm(FlaskForm):
    # Field for selecting 3 cantrips
    cantrips = SelectMultipleField(
        "Choose 3 Known Cantrips",
        choices=cantrips,  # This should be set to the appropriate cantrip list
        validators=[DataRequired()]
    )
    # Field for selecting 6 level 1 spells for the spellbook
    spellbook = SelectMultipleField(
        "Add 6 Spells to Your Spellbook",
        choices=level1_spells,  # This should be set to the appropriate spell list
        validators=[DataRequired()]
    )
    # Submit button
    submit = SubmitField("Next")

    # Custom validator to ensure exactly 3 cantrips are selected
    def validate_cantrips(self, field):
        if len(field.data) != 3:
            raise ValidationError("You must select exactly 3 cantrips.")

    # Custom validator to ensure exactly 6 spells are selected for the spellbook
    def validate_spellbook(self, field):
        if len(field.data) != 6:
            raise ValidationError("You must add exactly 6 spells.")

# This form enforces D&D rules for spell selection, ensuring the correct number of cantrips and spells are chosen.
# The choices for cantrips and spells should be set appropriately when the form is instantiated.
