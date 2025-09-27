# dnd_builder/utils/currency_utils.py
# Utility functions for converting and formatting D&D currency denominations.
# Handles conversion between copper, silver, gold, and platinum pieces.

def convert_to_coins(total_cp):
    """
    Convert a total number of copper pieces into appropriate coin denominations.
    Returns a dictionary with the number of each type of coin.
    1 pp = 10 gp = 100 sp = 1000 cp
    """
    # Ensure we're working with integers
    total_cp = int(total_cp)
    coins = {'pp': 0, 'gp': 0, 'sp': 0, 'cp': 0}
    
    # Convert to platinum first
    coins['pp'], remainder = divmod(total_cp, 1000)
    # Convert remainder to gold
    coins['gp'], remainder = divmod(remainder, 100)
    # Convert remainder to silver
    coins['sp'], coins['cp'] = divmod(remainder, 10)
    
    return coins

def convert_gp_to_coins(total_gp):
    """
    Convert a total number of gold pieces into appropriate coin denominations.
    Returns a dictionary with the number of each type of coin.
    1 pp = 10 gp, 1 gp = 10 sp, 1 sp = 10 cp
    """
    coins = {'pp': 0, 'gp': 0, 'sp': 0, 'cp': 0}
    
    # Convert to platinum first (10 gp = 1 pp)
    coins['pp'] = int(total_gp // 10)
    remainder_gp = total_gp % 10
    
    # Convert remainder to gold
    coins['gp'] = int(remainder_gp)
    fractional_gp = remainder_gp - coins['gp']
    
    # Convert fractional gold to silver (1 gp = 10 sp)
    total_sp = fractional_gp * 10
    coins['sp'] = int(total_sp)
    fractional_sp = total_sp - coins['sp']
    
    # Convert fractional silver to copper (1 sp = 10 cp)
    coins['cp'] = int(fractional_sp * 10)
    
    return coins

def format_coin_display(coins):
    """
    Format a coin dictionary into a display string.
    Only includes denominations that have a value.
    Handles missing denominations gracefully.
    """
    parts = []
    if coins.get('pp', 0) > 0:
        parts.append(f"{int(coins['pp'])} pp")
    if coins.get('gp', 0) > 0:
        parts.append(f"{int(coins['gp'])} gp")
    if coins.get('sp', 0) > 0:
        parts.append(f"{int(coins['sp'])} sp")
    if coins.get('cp', 0) > 0:
        parts.append(f"{int(coins['cp'])} cp")
    return ", ".join(parts) if parts else "0 cp"

def get_cost_in_cp(cost_dict):
    """
    Convert a cost dictionary {pp, gp, sp, cp} into total copper pieces.
    """
    total = 0
    total += cost_dict.get('pp', 0) * 1000  # 1 pp = 1000 cp
    total += cost_dict.get('gp', 0) * 100   # 1 gp = 100 cp
    total += cost_dict.get('sp', 0) * 10    # 1 sp = 10 cp
    total += cost_dict.get('cp', 0)
    return total

# These functions are used throughout the app for currency math, display, and validation.
