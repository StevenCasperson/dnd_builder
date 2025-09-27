# dnd_builder/data/equipment/weapons.py
# This module defines all weapon options for the D&D character builder.
# Each weapon type is represented as a list of dictionaries with stats and properties.

WEAPONS = {
    "simple_melee": [
        # Simple melee weapons: easy to use, available to most classes
        {
            "name": "Sickle",
            "cost": {"gp": 1},
            "damage": "1d4",
            "damage_type": "slashing",
            "weight": 2,
            "properties": ["light"],
            "category": "simple"
        },
        {
            "name": "Club",
            "cost": {"sp": 1},
            "damage": "1d4",
            "damage_type": "bludgeoning",
            "weight": 2,
            "properties": ["light"],
            "category": "simple"
        },
        {
            "name": "Dagger",
            "cost": {"gp": 2},
            "damage": "1d4",
            "damage_type": "piercing",
            "weight": 1,
            "properties": ["finesse", "light", "thrown"],
            "range": "20/60",
            "category": "simple"
        },
        {
            "name": "Greatclub",
            "cost": {"sp": 2},
            "damage": "1d8",
            "damage_type": "bludgeoning",
            "weight": 10,
            "properties": ["two-handed"],
            "category": "simple"
        },
        {
            "name": "Handaxe",
            "cost": {"gp": 5},
            "damage": "1d6",
            "damage_type": "slashing",
            "weight": 2,
            "properties": ["light", "thrown"],
            "range": "20/60",
            "category": "simple"
        },
        {
            "name": "Light Hammer",
            "cost": {"gp": 2},
            "damage": "1d4",
            "damage_type": "bludgeoning",
            "weight": 2,
            "properties": ["light", "thrown"],
            "range": "20/60",
            "category": "simple"
        },
        {
            "name": "Mace",
            "cost": {"gp": 5},
            "damage": "1d6",
            "damage_type": "bludgeoning",
            "weight": 4,
            "properties": [],
            "category": "simple"
        },
        {
            "name": "Quarterstaff",
            "cost": {"sp": 2},
            "damage": "1d6",
            "damage_type": "bludgeoning",
            "weight": 4,
            "properties": ["versatile"],
            "versatile_damage": "1d8",
            "category": "simple"
        },
        {
            "name": "Spear",
            "cost": {"gp": 1},
            "damage": "1d6",
            "damage_type": "piercing",
            "weight": 3,
            "properties": ["thrown", "versatile"],
            "range": "20/60",
            "versatile_damage": "1d8",
            "category": "simple"
        }
    ],
    "simple_ranged": [
        # Simple ranged weapons: basic ranged options
        {
            "name": "Light Crossbow",
            "cost": {"gp": 25},
            "damage": "1d8",
            "damage_type": "piercing", 
            "weight": 5,
            "properties": ["ammunition", "loading", "two-handed"],
            "range": "80/320",
            "category": "simple"
        },
        {
            "name": "Dart",
            "cost": {"cp": 5},
            "damage": "1d4",
            "damage_type": "piercing",
            "weight": 0.25,
            "properties": ["finesse", "thrown"],
            "range": "20/60",
            "category": "simple"
        },
        {
            "name": "Shortbow",
            "cost": {"gp": 25},
            "damage": "1d6",
            "damage_type": "piercing",
            "weight": 2,
            "properties": ["ammunition", "two-handed"],
            "range": "80/320",
            "category": "simple"
        },
        {
            "name": "Sling",
            "cost": {"sp": 1},
            "damage": "1d4",
            "damage_type": "bludgeoning",
            "weight": 0,
            "properties": ["ammunition"],
            "range": "30/120",
            "category": "simple"
        }
    ],
    "martial_melee": [
        # Martial melee weapons: require training, higher damage or special properties
        {
            "name": "Flail",
            "cost": {"gp": 10},
            "damage": "1d8",
            "damage_type": "bludgeoning",
            "weight": 2,
            "properties": [],
            "category": "martial"
        },
        {
            "name": "Glaive",
            "cost": {"gp": 20},
            "damage": "1d10",
            "damage_type": "slashing",
            "weight": 6,
            "properties": ["heavy", "reach", "two-handed"],
            "category": "martial"
        },
        {
            "name": "Greataxe",
            "cost": {"gp": 30},
            "damage": "1d12",
            "damage_type": "slashing",
            "weight": 7,
            "properties": ["heavy", "two-handed"],
            "category": "martial"
        },
        {
            "name": "Greatsword",
            "cost": {"gp": 50},
            "damage": "2d6",
            "damage_type": "slashing",
            "weight": 6,
            "properties": ["heavy", "two-handed"],
            "category": "martial"
        },
        {
            "name": "Halberd",
            "cost": {"gp": 20},
            "damage": "1d10",
            "damage_type": "slashing",
            "weight": 6,
            "properties": ["heavy", "reach", "two-handed"],
            "category": "martial"
        },
        {
            "name": "Lance",
            "cost": {"gp": 10},
            "damage": "1d12",
            "damage_type": "piercing",
            "weight": 6,
            "properties": ["reach", "special"],
            "special": "Requires two hands unless mounted",
            "category": "martial"
        },
        {
            "name": "Maul",
            "cost": {"gp": 10},
            "damage": "2d6",
            "damage_type": "bludgeoning",
            "weight": 10,
            "properties": ["heavy", "two-handed"],
            "category": "martial"
        },
        {
            "name": "Morningstar",
            "cost": {"gp": 15},
            "damage": "1d8",
            "damage_type": "piercing",
            "weight": 4,
            "properties": [],
            "category": "martial"
        },
        {
            "name": "Pike",
            "cost": {"gp": 5},
            "damage": "1d10",
            "damage_type": "piercing",
            "weight": 18,
            "properties": ["heavy", "reach", "two-handed"],
            "category": "martial"
        },
        {
            "name": "Scimitar",
            "cost": {"gp": 25},
            "damage": "1d6",
            "damage_type": "slashing",
            "weight": 3,
            "properties": ["finesse", "light"],
            "category": "martial"
        },
        {
            "name": "Trident",
            "cost": {"gp": 5},
            "damage": "1d8",
            "damage_type": "piercing",
            "weight": 4,
            "properties": ["thrown", "versatile"],
            "range": "20/60",
            "versatile_damage": "1d10",
            "category": "martial"
        },
        {
            "name": "Warhammer",
            "cost": {"gp": 15},
            "damage": "1d8",
            "damage_type": "bludgeoning",
            "weight": 5,
            "properties": ["versatile"],
            "versatile_damage": "1d10",
            "category": "martial"
        },
        {
            "name": "War Pick",
            "cost": {"gp": 5},
            "damage": "1d8",
            "damage_type": "piercing",
            "weight": 2,
            "properties": ["versatile"],
            "versatile_damage": "1d10",
            "category": "martial"
        },
        {
            "name": "Whip",
            "cost": {"gp": 2},
            "damage": "1d4",
            "damage_type": "slashing",
            "weight": 3,
            "properties": ["finesse", "reach"],
            "category": "martial"
        },
        {
            "name": "Battleaxe",
            "cost": {"gp": 10},
            "damage": "1d8",
            "damage_type": "slashing",
            "weight": 4,
            "properties": ["versatile"],
            "versatile_damage": "1d10",
            "category": "martial"
        },
        {
            "name": "Longsword",
            "cost": {"gp": 15},
            "damage": "1d8",
            "damage_type": "slashing",
            "weight": 3,
            "properties": ["versatile"],
            "versatile_damage": "1d10",
            "category": "martial"
        },
        {
            "name": "Rapier",
            "cost": {"gp": 25},
            "damage": "1d8",
            "damage_type": "piercing",
            "weight": 2,
            "properties": ["finesse"],
            "category": "martial"
        },
        {
            "name": "Shortsword",
            "cost": {"gp": 10},
            "damage": "1d6",
            "damage_type": "piercing",
            "weight": 2,
            "properties": ["finesse", "light"],
            "category": "martial"
        }
    ],
    "martial_ranged": [
        # Martial ranged weapons: advanced ranged options
        {
            "name": "Blowgun",
            "cost": {"gp": 10},
            "damage": "1",
            "damage_type": "piercing",
            "weight": 1,
            "properties": ["ammunition", "loading"],
            "range": "25/100",
            "category": "martial"
        },
        {
            "name": "Hand Crossbow",
            "cost": {"gp": 75},
            "damage": "1d6",
            "damage_type": "piercing",
            "weight": 3,
            "properties": ["ammunition", "light", "loading"],
            "range": "30/120",
            "category": "martial"
        },
        {
            "name": "Heavy Crossbow",
            "cost": {"gp": 50},
            "damage": "1d10",
            "damage_type": "piercing",
            "weight": 18,
            "properties": ["ammunition", "heavy", "loading", "two-handed"],
            "range": "100/400",
            "category": "martial"
        },
        {
            "name": "Longbow",
            "cost": {"gp": 50},
            "damage": "1d8",
            "damage_type": "piercing",
            "weight": 2,
            "properties": ["ammunition", "heavy", "two-handed"],
            "range": "150/600",
            "category": "martial"
        }
    ]
}

# Each weapon entry includes name, cost, damage, damage type, weight, properties, and category.
# This dictionary is used to populate weapon selection forms, validate choices, and calculate attack/damage stats.
