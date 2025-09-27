# dnd_builder/utils.py
# --------------------
# This module provides utility functions for spellcasting calculations.
#
# Each function is now commented for clarity and maintainability.

def calc_spell_save_dc(cast_mod: int, prof_bonus: int) -> int:
    """
    Calculate the Spell Save DC for a spellcaster.
    Formula: Spell Save DC = 8 + proficiency bonus + casting ability modifier
    Args:
        cast_mod (int): The character's spellcasting ability modifier (e.g., INT, WIS, CHA mod)
        prof_bonus (int): The character's proficiency bonus
    Returns:
        int: The calculated Spell Save DC
    """
    # Add 8 (base), proficiency bonus, and casting modifier
    return 8 + prof_bonus + cast_mod


def calc_spell_attack_bonus(cast_mod: int, prof_bonus: int) -> int:
    """
    Calculate the Spell Attack Bonus for a spellcaster.
    Formula: Spell Attack Bonus = proficiency bonus + casting ability modifier
    Args:
        cast_mod (int): The character's spellcasting ability modifier
        prof_bonus (int): The character's proficiency bonus
    Returns:
        int: The calculated Spell Attack Bonus
    """
    # Add proficiency bonus and casting modifier
    return prof_bonus + cast_mod
