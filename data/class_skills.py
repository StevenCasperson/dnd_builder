# dnd_builder/data/class_skills.py
# This module defines the available skill proficiencies for each D&D character class.
# The CLASS_SKILLS dictionary maps class names to lists of skills that can be chosen during character creation.

CLASS_SKILLS = {
    "Fighter": [
        # Fighters can choose from these skills
        "Acrobatics",
        "Animal Handling",
        "Athletics",
        "History",
        "Insight",
        "Intimidation",
        "Perception",
        "Persuasion",
        "Survival",
    ],
    "Rogue": [
        # Rogues have a broader skill selection
        "Acrobatics",
        "Athletics",
        "Deception",
        "Insight",
        "Intimidation",
        "Investigation",
        "Perception",
        "Performance",
        "Persuasion",
        "Sleight of Hand",
        "Stealth",
    ],
    "Cleric": [
        # Clerics can choose from these skills
        "History",
        "Insight",
        "Medicine",
        "Persuasion",
        "Religion",
    ],
    "Wizard": [
        # Wizards can choose from these skills
        "Arcana",
        "History",
        "Investigation",
        "Medicine",
        "Religion",
    ],
}

# This mapping is used to populate skill selection forms and enforce class-specific skill rules.
