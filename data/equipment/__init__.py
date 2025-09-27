from dnd_builder.data.equipment.weapons import WEAPONS  # Import weapon data for proficiency checks

# Class proficiencies for equipment
# Maps each class to the types of armor and weapons they are proficient with
CLASS_PROFICIENCIES = {
    "Fighter": {
        "armor": ["light", "medium", "heavy", "shields"],  # Fighters can use all armor and shields
        "weapons": ["simple_melee", "simple_ranged", "martial_melee", "martial_ranged"]  # All weapon categories
    },
    "Rogue": {
        "armor": ["light"],  # Rogues can only use light armor
        "weapons": ["simple_melee", "simple_ranged", "hand crossbow", "longsword", "rapier", "shortsword"]  # Some categories and specific weapons
    },
    "Wizard": {
        "armor": [],  # Wizards have no armor proficiency
        "weapons": ["dagger", "dart", "sling", "quarterstaff", "light crossbow"]  # Only a few simple weapons
    },
    "Cleric": {
        "armor": ["light", "medium", "shields"],  # Clerics can use light/medium armor and shields
        "weapons": ["simple_melee", "simple_ranged"]  # All simple weapons
    }
}

# Function to check if a class has proficiency with a given armor type
def has_armor_proficiency(char_class: str, armor_type: str) -> bool:
    """
    Check if a character class has proficiency with an armor type.
    Args:
        char_class (str): The character's class name
        armor_type (str): The armor type (e.g., 'light', 'medium', 'heavy', 'shields')
    Returns:
        bool: True if the class is proficient, False otherwise
    """
    if not char_class:
        return False  # No class provided
    return armor_type in CLASS_PROFICIENCIES.get(char_class, {}).get("armor", [])

# Function to check if a class has proficiency with a given weapon or weapon category
def has_weapon_proficiency(char_class: str, weapon_info: str | dict) -> bool:
    """
    Check if a character class has proficiency with a weapon or weapon category.
    Args:
        char_class (str): The character's class name
        weapon_info (str | dict): Either a weapon category string (e.g. 'simple_melee')
                                 or a weapon dictionary from WEAPONS
    Returns:
        bool: True if the class is proficient, False otherwise
    """
    if not char_class:
        return False  # No class provided
    proficiencies = CLASS_PROFICIENCIES.get(char_class, {}).get("weapons", [])
    # If we're checking a category (e.g., 'simple_melee')
    if isinstance(weapon_info, str):
        return weapon_info in proficiencies
    # If we're checking a specific weapon (dict)
    # First check if they have proficiency with the whole category
    weapon_cat = None
    for cat in ['simple_melee', 'simple_ranged', 'martial_melee', 'martial_ranged']:
        if weapon_info in WEAPONS[cat]:
            weapon_cat = cat
            break
    if weapon_cat and weapon_cat in proficiencies:
        return True  # Proficient with the whole category
    # Check for specific weapon proficiencies (e.g., 'rapier')
    return weapon_info['name'].lower() in proficiencies
