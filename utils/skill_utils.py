# dnd_builder/utils/skill_utils.py
# Utility functions for calculating skill and ability modifiers in the D&D character builder.

def calculate_ability_modifier(score: int) -> int:
    """Calculate the ability score modifier.
    Args:
        score (int): The ability score (e.g., 14 for Dexterity)
    Returns:
        int: The modifier (e.g., +2 for 14)
    """
    return (score - 10) // 2

def calculate_skill_modifier(ability_score: int, is_proficient: bool, prof_bonus: int = 2) -> int:
    """
    Calculate the total modifier for a skill.
    ability_score: The relevant ability score (not the modifier)
    is_proficient: Whether the character is proficient in this skill
    prof_bonus: Proficiency bonus (default +2 for level 1)
    """
    ability_mod = calculate_ability_modifier(ability_score)
    return ability_mod + (prof_bonus if is_proficient else 0)

def calculate_passive_perception(wisdom_score: int, perception_proficient: bool) -> int:
    """
    Calculate passive perception score.
    Formula: 10 + Wisdom modifier + (proficiency bonus if proficient in Perception)
    Args:
        wisdom_score (int): The character's Wisdom score
        perception_proficient (bool): Whether the character is proficient in Perception
    Returns:
        int: The passive perception value
    """
    wisdom_mod = calculate_ability_modifier(wisdom_score)
    prof_bonus = 2  # Level 1 proficiency bonus
    perception_mod = calculate_skill_modifier(wisdom_score, perception_proficient, prof_bonus)
    return 10 + perception_mod

# These functions are used to compute skill bonuses, ability modifiers, and passive perception for display and validation.
