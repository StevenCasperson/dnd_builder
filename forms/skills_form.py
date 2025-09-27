# Import FlaskForm for creating forms, SelectMultipleField for multiple selection fields, SubmitField for a submit button,
# and validators for form validation.
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, ValidationError

# Define a form for selecting skill proficiencies and expertise (for D&D characters)
class SkillsForm(FlaskForm):
    # Field for selecting multiple skill proficiencies
    skills = SelectMultipleField(
        "Choose skill proficiencies:",
        choices=[],  # Choices will be set dynamically in __init__
        validators=[DataRequired(message="Pick the required skills.")]
    )
    # Field for selecting multiple skills for Expertise (Rogues only)
    expertise = SelectMultipleField(
        "Choose 2 skills for Expertise (double proficiency bonus):",
        choices=[],  # Will be populated for Rogues
        validators=[]
    )
    # Submit button for the form
    submit = SubmitField("Next")

    def __init__(self, allowed_skills, char_class=None, *args, **kwargs):
        # Initialize the parent FlaskForm
        super().__init__(*args, **kwargs)
        self.char_class = char_class  # Store the character class
        # Build choices for the skills field from the allowed_skills list
        self.skills.choices = [(s, s) for s in allowed_skills]
        
        # Set the number of required skills and adjust labels based on class
        if char_class == 'Rogue':
            self.skills_required = 4  # Rogues pick 4 skills
            self.skills.label.text = "Choose 4 skill proficiencies:"
            # Expertise choices are set to all allowed skills (filtered by JS on the frontend)
            self.expertise.choices = [(s, s) for s in allowed_skills]
        else:
            self.skills_required = 2  # Most classes pick 2 skills
            self.skills.label.text = "Choose 2 skill proficiencies:"

    # Custom validator for the skills field
    def validate_skills(self, field):
        # Ensure the user picks exactly the required number of skills
        if len(field.data) != self.skills_required:
            if self.skills_required == 4:
                raise ValidationError("You must pick exactly four skills.")
            else:
                raise ValidationError("You must pick exactly two skills.")
    
    # Custom validator for the expertise field (Rogues only)
    def validate_expertise(self, field):
        if self.char_class == 'Rogue':
            # Rogues must pick exactly 2 skills for Expertise
            if len(field.data or []) != 2:
                raise ValidationError("Rogues must choose exactly 2 skills for Expertise.")
            # Ensure expertise skills are among the selected proficiencies
            for skill in field.data or []:
                if skill not in (self.skills.data or []):
                    raise ValidationError("You can only choose Expertise in skills you're proficient with.")

# This form is used in the character creation process to enforce D&D rules for skill selection.
# The logic ensures that only valid skill and expertise choices are accepted, with special handling for Rogues.
