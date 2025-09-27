# dnd_builder/data/equipment/armor.py
# This module defines all armor and shield options for the D&D character builder.
# Each armor type is represented as a list of dictionaries with stats and properties.

ARMOR = {
    "light": [
        # Light armor options: allow full Dexterity bonus, low weight
        {
            "name": "Padded",
            "cost": {"gp": 5},
            "ac": 11,
            "add_dex": True,  # Add full Dex modifier
            "max_dex": None,  # No max Dex
            "stealth_disadvantage": True,  # Disadvantage on Stealth
            "weight": 8,
            "type": "light"
        },
        {
            "name": "Leather",
            "cost": {"gp": 10},
            "ac": 11,
            "add_dex": True,
            "max_dex": None,
            "stealth_disadvantage": False,
            "weight": 10,
            "type": "light"
        },
        {
            "name": "Studded Leather",
            "cost": {"gp": 45},
            "ac": 12,
            "add_dex": True,
            "max_dex": None,
            "stealth_disadvantage": False,
            "weight": 13,
            "type": "light"
        }
    ],
    "medium": [
        # Medium armor: max +2 Dex bonus, moderate weight
        {
            "name": "Hide",
            "cost": {"gp": 10},
            "ac": 12,
            "add_dex": True,
            "max_dex": 2,
            "stealth_disadvantage": False,
            "weight": 12,
            "type": "medium"
        },
        {
            "name": "Chain Shirt",
            "cost": {"gp": 50},
            "ac": 13,
            "add_dex": True,
            "max_dex": 2,
            "stealth_disadvantage": False,
            "weight": 20,
            "type": "medium"
        },
        {
            "name": "Scale Mail",
            "cost": {"gp": 50},
            "ac": 14,
            "add_dex": True,
            "max_dex": 2,
            "stealth_disadvantage": True,
            "weight": 45,
            "type": "medium"
        },
        {
            "name": "Breastplate",
            "cost": {"gp": 400},
            "ac": 14,
            "add_dex": True,
            "max_dex": 2,
            "stealth_disadvantage": False,
            "weight": 20,
            "type": "medium"
        },
        {
            "name": "Half Plate",
            "cost": {"gp": 750},
            "ac": 15,
            "add_dex": True,
            "max_dex": 2,
            "stealth_disadvantage": True,
            "weight": 40,
            "type": "medium"
        }
    ],
    "heavy": [
        # Heavy armor: no Dex bonus, high weight, some require Strength
        {
            "name": "Ring Mail",
            "cost": {"gp": 30},
            "ac": 14,
            "add_dex": False,
            "max_dex": 0,
            "stealth_disadvantage": True,
            "weight": 40,
            "type": "heavy"
        },
        {
            "name": "Chain Mail",
            "cost": {"gp": 75},
            "ac": 16,
            "add_dex": False,
            "max_dex": 0,
            "stealth_disadvantage": True,
            "weight": 55,
            "type": "heavy",
            "strength_requirement": 13  # Minimum Strength to avoid speed penalty
        },
        {
            "name": "Splint",
            "cost": {"gp": 200},
            "ac": 17,
            "add_dex": False,
            "max_dex": 0,
            "stealth_disadvantage": True,
            "weight": 60,
            "type": "heavy",
            "strength_requirement": 15
        },
        {
            "name": "Plate",
            "cost": {"gp": 1500},
            "ac": 18,
            "add_dex": False,
            "max_dex": 0,
            "stealth_disadvantage": True,
            "weight": 65,
            "type": "heavy",
            "strength_requirement": 15
        }
    ],
    "shield": [
        # Shields: add +2 AC, can be used by most classes
        {
            "name": "Shield",
            "cost": {"gp": 10},
            "ac_bonus": 2,
            "weight": 6,
            "type": "shield"
        }
    ]
}

# This dictionary is used to populate armor selection forms, validate choices, and calculate AC and encumbrance.
