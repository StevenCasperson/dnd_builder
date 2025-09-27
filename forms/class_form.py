# dnd_builder/forms/class_form.py
# This module defines the form for class selection in the character creation process.

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired, Optional

class ClassForm(FlaskForm):
    # Radio field for selecting the character's class (required)
    class_choice = RadioField("Choose your class", choices=[], validators=[DataRequired()])
    # Radio field for selecting the primary ability (only for Fighters, optional for others)
    primary_ability = RadioField("Primary Ability (for Fighter only)", 
                                choices=[('strength', 'Strength'), ('dexterity', 'Dexterity')],
                                validators=[Optional()])
    # Submit button to proceed to the next step
    submit = SubmitField("Next")

    def __init__(self, classes, *args, **kwargs):
        """
        Initialize the form with a dynamic list of class choices.
        Args:
            classes (list): List of available class names (e.g., ['Fighter', 'Wizard', ...])
        """
        super().__init__(*args, **kwargs)
        self.class_choice.choices = [(c, c) for c in classes]  # Populate class choices dynamically
