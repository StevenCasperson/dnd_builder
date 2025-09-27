# dnd_builder/utils/armor_utils.py
# Utility functions for calculating Armor Class (AC) in the D&D character builder.

def calculate_ac(armor=None, shield=None, dex_modifier=0):
    """Calculate Armor Class based on armor, shield, and dexterity modifier.
    
    Args:
        armor (dict): Armor item dictionary from ARMOR data structure
        shield (dict): Shield item dictionary from ARMOR data structure
        dex_modifier (int): Character's dexterity modifier
    
    Returns:
        int: The calculated Armor Class
    """
    base_ac = 10  # Base AC without armor
    
    if not armor:
        # No armor - use base AC + full dex modifier
        return base_ac + dex_modifier
        
    # Start with the armor's base AC
    total_ac = armor['ac']
    
    # Add dexterity modifier based on armor type
    if armor['add_dex']:
        if armor['max_dex'] is not None:
            # Medium armor - cap dex bonus
            dex_bonus = min(dex_modifier, armor['max_dex'])
        else:
            # Light armor - full dex bonus
            dex_bonus = dex_modifier
        total_ac += dex_bonus
    # Heavy armor - no dex bonus (handled implicitly since add_dex is False)
    
    # Add shield bonus if equipped
    if shield:
        total_ac += shield['ac_bonus']
        
    return total_ac

# This function is used to compute a character's AC for display, validation, and PDF output.
# It handles all armor types, shield bonuses, and dexterity rules per D&D 5e.
