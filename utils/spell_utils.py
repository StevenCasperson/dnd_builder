# dnd_builder/utils/spell_utils.py
# Utility functions for calculating spell save DC and spell attack bonus in the D&D character builder.

def calc_spell_save_dc(cast_mod: int, prof_bonus: int) -> int:
    """
    Calculate the Spell Save DC for a spellcaster.
    Formula: 8 + proficiency bonus + casting ability modifier
    Args:
        cast_mod (int): The caster's ability modifier (e.g., Intelligence for Wizards)
        prof_bonus (int): The caster's proficiency bonus
    Returns:
        int: The spell save DC
    """
    return 8 + prof_bonus + cast_mod

def calc_spell_attack_bonus(cast_mod: int, prof_bonus: int) -> int:
    """
    Calculate the Spell Attack Bonus for a spellcaster.
    Formula: proficiency bonus + casting ability modifier
    Args:
        cast_mod (int): The caster's ability modifier
        prof_bonus (int): The caster's proficiency bonus
    Returns:
        int: The spell attack bonus
    """
    return prof_bonus + cast_mod

# These functions are used to compute spellcasting stats for display, validation, and PDF output.
