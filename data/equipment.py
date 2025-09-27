# dnd_builder/data/equipment.py
# This module provides references to the equipment package and defines common equipment data for the app.
# It includes ammunition, spell focuses, holy symbols, and common adventuring gear.

from .equipment.weapons import WEAPONS  # Weapon data for the app
from .equipment.armor import ARMOR      # Armor data for the app

# Ammunition options for ranged weapons
AMMUNITION = {
    "arrows": {
        "name": "Arrows (20)",
        "cost": {"gp": 1},
        "weight": 1
    },
    "crossbow_bolts": {
        "name": "Crossbow Bolts (20)",
        "cost": {"gp": 1},
        "weight": 1.5
    },
    "sling_bullets": {
        "name": "Sling Bullets (20)",
        "cost": {"cp": 4},
        "weight": 1.5
    },
    "blowgun_needles": {
        "name": "Blowgun Needles (50)",
        "cost": {"gp": 1},
        "weight": 1
    }
}

# Arcane focus items for spellcasters
ARCANE_FOCUS = {
    "crystal": {
        "name": "Crystal",
        "cost": {"gp": 10},
        "weight": 1
    },
    "orb": {
        "name": "Orb",
        "cost": {"gp": 20},
        "weight": 3
    },
    "rod": {
        "name": "Rod",
        "cost": {"gp": 10},
        "weight": 2
    },
    "staff": {
        "name": "Staff",
        "cost": {"gp": 5},
        "weight": 4
    },
    "wand": {
        "name": "Wand",
        "cost": {"gp": 10},
        "weight": 1
    }
}

# Holy symbol options for divine spellcasters
HOLY_SYMBOL = {
    "amulet": {
        "name": "Amulet",
        "cost": {"gp": 5},
        "weight": 1
    },
    "emblem": {
        "name": "Emblem",
        "cost": {"gp": 5},
        "weight": 0
    },
    "reliquary": {
        "name": "Reliquary",
        "cost": {"gp": 5},
        "weight": 2
    }
}

# Common adventuring gear with names, costs, and weights
ADVENTURING_GEAR = {
    "acid": {
        "name": "Acid (vial)",
        "cost": {"gp": 25},
        "weight": 1
    },
    "alchemists_fire": {
        "name": "Alchemist's Fire (flask)",
        "cost": {"gp": 50},
        "weight": 1
    },
    "antitoxin": {
        "name": "Antitoxin (vial)",
        "cost": {"gp": 50},
        "weight": 0
    },
    "vial": {
        "name": "Vial",
        "cost": {"gp": 1},
        "weight": 0
    },
    "waterskin": {
        "name": "Waterskin",
        "cost": {"sp": 2},
        "weight": 5
    }
}

# This module is used to provide equipment data for forms, validation, and PDF output.
