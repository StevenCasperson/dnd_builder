# dnd_builder/data/equipment/adventuring_gear.py
# This module defines special equipment categories and options for the D&D character builder.
# It provides dictionaries for ammunition, arcane foci, holy symbols, musical instruments, tools, and standard adventuring gear.

# Ammunition options for ranged weapons
AMMUNITION_OPTIONS = {
    "arrows": {
        "name": "Arrows (20)",
        "cost": {"gp": 1}
    },
    "bolts": {
        "name": "Crossbow Bolts (20)",
        "cost": {"gp": 1}
    },
    "needles": {
        "name": "Blowgun Needles (50)",
        "cost": {"gp": 1}
    }
}

# Arcane focus options for spellcasters
ARCANE_FOCUS_OPTIONS = {
    "crystal": {
        "name": "Crystal",
        "cost": {"gp": 10}
    },
    "orb": {
        "name": "Orb",
        "cost": {"gp": 20}
    },
    "rod": {
        "name": "Rod",
        "cost": {"gp": 10}
    },
    "staff": {
        "name": "Staff",
        "cost": {"gp": 5}
    },
    "wand": {
        "name": "Wand",
        "cost": {"gp": 10}
    }
}

# Holy symbol options for divine spellcasters
HOLY_SYMBOL_OPTIONS = {
    'amulet': {'name': 'Amulet', 'cost': {'gp': 5}},
    'emblem': {'name': 'Emblem', 'cost': {'gp': 5}}, 
    'reliquary': {'name': 'Reliquary', 'cost': {'gp': 5}}
}

# Musical instrument options for bards and other classes
MUSICAL_INSTRUMENT_OPTIONS = {
    'bagpipes': {'name': 'Bagpipes', 'cost': {'gp': 30}},
    'drum': {'name': 'Drum', 'cost': {'gp': 6}},
    'dulcimer': {'name': 'Dulcimer', 'cost': {'gp': 25}},
    'flute': {'name': 'Flute', 'cost': {'gp': 2}},
    'lute': {'name': 'Lute', 'cost': {'gp': 35}},
    'lyre': {'name': 'Lyre', 'cost': {'gp': 30}},
    'horn': {'name': 'Horn', 'cost': {'gp': 3}},
    'pan_flute': {'name': 'Pan Flute', 'cost': {'gp': 12}},
    'shawm': {'name': 'Shawm', 'cost': {'gp': 2}},
    'viol': {'name': 'Viol', 'cost': {'gp': 30}}
}

# Tool options for various backgrounds and classes
TOOL_OPTIONS = {
    'alchemists_supplies': {'name': "Alchemist's Supplies", 'cost': {'gp': 50}},
    'brewers_supplies': {'name': "Brewer's Supplies", 'cost': {'gp': 20}},
    'calligraphers_supplies': {'name': "Calligrapher's Supplies", 'cost': {'gp': 10}},
    'carpenters_tools': {'name': "Carpenter's Tools", 'cost': {'gp': 8}},
    'cartographers_tools': {'name': "Cartographer's Tools", 'cost': {'gp': 15}},
    'cobblers_tools': {'name': "Cobbler's Tools", 'cost': {'gp': 5}},
    'cooks_utensils': {'name': "Cook's Utensils", 'cost': {'gp': 2}},
    'glassblowers_tools': {'name': "Glassblower's Tools", 'cost': {'gp': 30}},
    'jewelers_tools': {'name': "Jeweler's Tools", 'cost': {'gp': 25}},
    'leatherworkers_tools': {'name': "Leatherworker's Tools", 'cost': {'gp': 5}},
    'masons_tools': {'name': "Mason's Tools", 'cost': {'gp': 10}},
    'painters_supplies': {'name': "Painter's Supplies", 'cost': {'gp': 10}},
    'potters_tools': {'name': "Potter's Tools", 'cost': {'gp': 10}},
    'smiths_tools': {'name': "Smith's Tools", 'cost': {'gp': 20}},
    'tinkers_tools': {'name': "Tinker's Tools", 'cost': {'gp': 50}},
    'weavers_tools': {'name': "Weaver's Tools", 'cost': {'gp': 1}},
    'woodcarvers_tools': {'name': "Woodcarver's Tools", 'cost': {'gp': 1}},
    'disguise_kit': {'name': 'Disguise Kit', 'cost': {'gp': 25}},
    'forgery_kit': {'name': 'Forgery Kit', 'cost': {'gp': 15}},
    'herbalism_kit': {'name': 'Herbalism Kit', 'cost': {'gp': 5}},
    'navigators_tools': {'name': "Navigator's Tools", 'cost': {'gp': 25}},
    'poisoners_kit': {'name': "Poisoner's Kit", 'cost': {'gp': 50}},
    'thieves_tools': {'name': "Thieves' Tools", 'cost': {'gp': 25}}
}

# Standard adventuring gear items
ADVENTURING_GEAR = {
    "acid": {"name": "Acid", "cost": {"gp": 25}},
    "alchemists_fire": {"name": "Alchemist's Fire", "cost": {"gp": 50}},
    "antitoxin": {"name": "Antitoxin", "cost": {"gp": 50}},
    "backpack": {"name": "Backpack", "cost": {"gp": 2}},
    "ball_bearings": {"name": "Ball Bearings (bag of 1000)", "cost": {"gp": 1}},
    "barrel": {"name": "Barrel", "cost": {"gp": 2}},
    "basket": {"name": "Basket", "cost": {"sp": 4}},
    "bedroll": {"name": "Bedroll", "cost": {"gp": 1}},
    "bell": {"name": "Bell", "cost": {"gp": 1}},
    "blanket": {"name": "Blanket", "cost": {"sp": 5}},
    "block_and_tackle": {"name": "Block and Tackle", "cost": {"gp": 1}},
    "book": {"name": "Book", "cost": {"gp": 25}},
    "glass_bottle": {"name": "Glass Bottle", "cost": {"gp": 2}},
    "bucket": {"name": "Bucket", "cost": {"cp": 5}},
    "burglars_pack": {"name": "Burglar's Pack", "cost": {"gp": 16}},
    "caltrops": {"name": "Caltrops (bag of 20)", "cost": {"gp": 1}},
    "candle": {"name": "Candle", "cost": {"cp": 1}},
    "crossbow_bolt_case": {"name": "Crossbow Bolt Case", "cost": {"gp": 1}},
    "map_case": {"name": "Map or Scroll Case", "cost": {"gp": 1}},
    "chain": {"name": "Chain (10 feet)", "cost": {"gp": 5}},
    "chest": {"name": "Chest", "cost": {"gp": 5}},
    "climbers_kit": {"name": "Climber's Kit", "cost": {"gp": 25}},
    "clothes_fine": {"name": "Fine Clothes", "cost": {"gp": 15}},
    "clothes_travelers": {"name": "Traveler's Clothes", "cost": {"gp": 2}},
    "component_pouch": {"name": "Component Pouch", "cost": {"gp": 25}},
    "costume": {"name": "Costume", "cost": {"gp": 5}},
    "crowbar": {"name": "Crowbar", "cost": {"gp": 2}},
    "diplomats_pack": {"name": "Diplomat's Pack", "cost": {"gp": 39}},
    "dungeoneers_pack": {"name": "Dungeoneer's Pack", "cost": {"gp": 12}},
    "entertainers_pack": {"name": "Entertainer's Pack", "cost": {"gp": 40}},
    "explorers_pack": {"name": "Explorer's Pack", "cost": {"gp": 10}},
    "flask": {"name": "Flask", "cost": {"cp": 2}},
    "grappling_hook": {"name": "Grappling Hook", "cost": {"gp": 2}},
    "healers_kit": {"name": "Healer's Kit", "cost": {"gp": 5}},
    "holy_water": {"name": "Holy Water (flask)", "cost": {"gp": 25}},
    "hunting_trap": {"name": "Hunting Trap", "cost": {"gp": 5}},
    "ink": {"name": "Ink (1 ounce bottle)", "cost": {"gp": 10}},
    "ink_pen": {"name": "Ink Pen", "cost": {"cp": 2}},
    "jug": {"name": "Jug", "cost": {"cp": 2}},
    "ladder": {"name": "Ladder (10-foot)", "cost": {"sp": 1}},
    "lamp": {"name": "Lamp", "cost": {"sp": 5}},
    "lantern_bullseye": {"name": "Bullseye Lantern", "cost": {"gp": 10}},
    "lantern_hooded": {"name": "Hooded Lantern", "cost": {"gp": 5}},
    "lock": {"name": "Lock", "cost": {"gp": 10}},
    "magnifying_glass": {"name": "Magnifying Glass", "cost": {"gp": 100}},
    "manacles": {"name": "Manacles", "cost": {"gp": 2}},
    "map": {"name": "Map", "cost": {"gp": 1}},
    "mirror": {"name": "Mirror, Steel", "cost": {"gp": 5}},
    "net": {"name": "Net", "cost": {"gp": 1}},
    "oil": {"name": "Oil (flask)", "cost": {"sp": 1}},
    "paper": {"name": "Paper (one sheet)", "cost": {"sp": 2}},
    "parchment": {"name": "Parchment (one sheet)", "cost": {"sp": 1}},
    "perfume": {"name": "Perfume (vial)", "cost": {"gp": 5}},
    "basic_poison": {"name": "Basic Poison (vial)", "cost": {"gp": 100}},
    "pole": {"name": "Pole (10-foot)", "cost": {"cp": 5}},
    "iron_pot": {"name": "Iron Pot", "cost": {"gp": 2}},
    "potion_of_healing": {"name": "Potion of Healing", "cost": {"gp": 50}},
    "pouch": {"name": "Pouch", "cost": {"sp": 5}},
    "priests_pack": {"name": "Priest's Pack", "cost": {"gp": 33}},
    "quiver": {"name": "Quiver", "cost": {"gp": 1}},
    "portable_ram": {"name": "Portable Ram", "cost": {"gp": 4}},
    "rations": {"name": "Rations (1 day)", "cost": {"sp": 5}},
    "robe": {"name": "Robes", "cost": {"gp": 1}},
    "rope_hemp": {"name": "Rope, Hemp (50 feet)", "cost": {"gp": 1}},
    "sack": {"name": "Sack", "cost": {"cp": 1}},
    "scholars_pack": {"name": "Scholar's Pack", "cost": {"gp": 40}},
    "shovel": {"name": "Shovel", "cost": {"gp": 2}},
    "signal_whistle": {"name": "Signal Whistle", "cost": {"cp": 5}},
    "iron_spikes": {"name": "Iron Spikes (10)", "cost": {"gp": 1}},
    "string": {"name": "String (10 feet)", "cost": {"sp": 1}},
    "tent": {"name": "Tent, Two-person", "cost": {"gp": 2}},
    "tinderbox": {"name": "Tinderbox", "cost": {"sp": 5}},
    "torch": {"name": "Torch", "cost": {"cp": 1}},
    "vial": {"name": "Vial", "cost": {"gp": 1}},
    "waterskin": {"name": "Waterskin", "cost": {"sp": 2}}
}

# This module is used to provide special equipment options for forms and validation in the character builder.
