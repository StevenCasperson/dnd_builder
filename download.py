
# dnd_builder/download.py
# -----------------------
# This module handles PDF generation and download for the D&D Character Builder app.
# It uses ReportLab to create a detailed character sheet PDF from session data.
#
# Each section, function, and block is now commented in detail for clarity and maintainability.
#
# ——— Imports ———
import io  # For in-memory byte buffer
from flask import Blueprint, session, send_file  # Flask utilities for routing, session, and file sending
from reportlab.lib import colors  # Color constants for PDF styling
from reportlab.lib.pagesizes import letter  # Standard US letter page size
from reportlab.platypus import Table, TableStyle  # Table and style classes for PDF layout


# Create a Flask Blueprint for download-related routes
bp = Blueprint("download", __name__)

@bp.route("/download/pdf")
def download_pdf():
    """
    Generate and send a PDF character sheet based on session data.
    This function builds a detailed PDF using ReportLab, including all character info, stats, equipment, spells, and more.
    """
    # Import ReportLab classes for PDF generation (imported here for hot-reload compatibility)
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch

    # Set up ReportLab styles for section headers and character text
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=15, leading=18, spaceAfter=10, fontName='Helvetica-Bold', textColor=colors.saddlebrown))  # For section headers
    styles.add(ParagraphStyle(name='CharacterText', fontSize=12, leading=15, fontName='Helvetica', textColor=colors.HexColor('#2c1810')))  # For main text

    # Create a buffer and PDF document
    buffer = io.BytesIO()  # In-memory buffer for PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    story = []  # List of flowables (content blocks) for the PDF

    # Character name (try multiple keys for compatibility)
    char_name = session.get('character_name') or session.get('name') or session.get('char_name') or 'Unnamed Hero'
    # Add character name as a centered, bold title
    story.append(Paragraph(f"<para align='center'><b>{char_name}</b></para>", styles['Title']))
    story.append(Spacer(1, 8))  # Small vertical space

    # Gather stats and equipment from session
    stats = session.get("adjusted_stats", {}) or {}  # Final stats dict
    dex_mod = (stats.get('dexterity', 10) - 10) // 2  # Dexterity modifier
    con_mod = (stats.get('constitution', 10) - 10) // 2  # Constitution modifier
    equipment = session.get('equipment', {}) or {}  # Equipment dict

    # Calculate Armor Class (AC)
    armor_class = equipment.get('armor_class')  # Use explicit AC if present
    if not armor_class:
        base_ac = 10 + dex_mod  # Default AC if no armor
        armor = equipment.get('armor')
        if armor:
            # If armor is equipped, use its AC and add DEX if allowed
            armor_class = armor.get('ac', 10) + (dex_mod if armor.get('add_dex', True) else 0)
        else:
            armor_class = base_ac

    # Get Hit Points (HP)
    hit_points = session.get('max_hp')
    # Build info table (race, class, etc.)
    info_data = [
        # Each row is a (label, value) pair for the character's summary info
        ['Race', session.get('race', 'Unknown')],
        ['Class', session.get('class', 'Unknown')],
        ['Level', '1'],
        ['Primary Ability', session.get('primary_ability', 'Unknown')],
        ['AC', str(armor_class)],
        ['HP', str(hit_points)],
        ['Speed', "25 ft" if ('dwarf' in (session.get('race') or '').lower() or 'halfling' in (session.get('race') or '').lower()) else "30 ft"]
    ]
    # Table for displaying character info (race, class, AC, etc.)
    info_table = Table(info_data, colWidths=[1.2*inch, 1.2*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.red),  # Red background for all cells
        ('TEXTCOLOR', (0,0), (-1,-1), colors.red),    # Red text (overridden below)
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),  # Bold for labels
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),       # Regular for values
        ('FONTSIZE', (0,0), (-1,-1), 12),  # All rows use font size 12
        ('GRID', (0,0), (-1,-1), 1, colors.red),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.red, colors.red]),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    # ...existing code...

    # === ABILITY SCORES: Build ability score boxes for the PDF ===
    # Create a vertical stack of boxes for each ability (Strength, Dexterity, etc.)
    # Each box shows the ability name, score, and modifier, styled with colors and fonts
    # AbilityColumn is a custom Flowable to stack the boxes vertically
    # 3. Build the ability score display boxes for the PDF
    #    - ability_order: keys for stats dict
    #    - ability_names: display names for each ability
    ability_order = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
    ability_names = ['STRENGTH', 'DEXTERITY', 'CONSTITUTION', 'INTELLIGENCE', 'WISDOM', 'CHARISMA']
    ability_boxes = []
    for i, ability in enumerate(ability_order):
        ability_name = ability_names[i]
        # Get the score for this ability (default 10 if missing)
        score = stats.get(ability, 10)
        # Calculate the modifier for this ability
        mod = (score - 10) // 2
        # Prepare the data for the 3-row box: name, score, modifier
        box_data = [
            [ability_name],
            [f"{score}"],
            [f"{'+' if mod >= 0 else ''}{mod}"]
        ]
        # Create the table for this ability's box
        ability_box = Table(box_data, colWidths=[1.32*inch], rowHeights=[0.4*inch, 0.5*inch, 0.32*inch])
        # Style the table: see comments for each row
        ability_box.setStyle(TableStyle([
            # --- Row 1: Ability Name ---
            ('BACKGROUND', (0,0), (0,0), colors.red),
            ('TEXTCOLOR', (0,0), (0,0), colors.black),
            ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (0,0), 12),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('VALIGN', (0,0), (0,0), 'MIDDLE'),
            # --- Row 2: Score ---
            ('BACKGROUND', (0,1), (0,1), colors.tan),
            ('TEXTCOLOR', (0,1), (0,1), colors.HexColor('#2c1810')),
            ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,1), (0,1), 26),
            ('ALIGN', (0,1), (0,1), 'CENTER'),
            ('VALIGN', (0,1), (0,1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,1), (0,1), 26),  # Padding for Score Row 
            # Row 3: Modifier 
            ('BACKGROUND', (0,2), (0,2), colors.HexColor('#e8dcc0')),
            ('TEXTCOLOR', (0,2), (0,2), colors.HexColor('#2c1810')),
            ('FONTNAME', (0,2), (0,2), 'Helvetica-Bold'),
            ('FONTSIZE', (0,2), (0,2), 13),
            ('ALIGN', (0,2), (0,2), 'CENTER'),
            ('VALIGN', (0,2), (0,2), 'MIDDLE'),
            # --- Box and Grid ---
            ('BOX', (0,0), (0,2), 1, colors.saddlebrown),
            ('INNERGRID', (0,0), (0,2), 0.5, colors.saddlebrown),            
            ('BOTTOMPADDING', (0,2), (0,2), 8),     # Padding for Modifier Row
        ]))
        ability_boxes.append(ability_box)
    from reportlab.platypus import Flowable
    class AbilityColumn(Flowable):
        def __init__(self, boxes):
            super().__init__()
            self.boxes = boxes
        def wrap(self, availWidth, availHeight):
            # Make the column a bit wider for left alignment
            return (1.47*inch, 2.2*inch)
        def draw(self):
            # Vertical positioning of the ability score boxes 
            # y controls how far down the boxes start relative to the title above.
            # Lower y moves the boxes further down; raise y to move them closer to the title.
            y = 1.25*inch  # Adjust this value to control vertical spacing below the title
            x = 0.38*inch  # shift right more
            box_height = 0.4 + 0.5 + 0.32  # sum of rowHeights in inches
            spacing = 0.13*inch  # extra space between boxes
            for box in self.boxes:
                box.wrapOn(self.canv, 1.32*inch, box_height*inch)
                box.drawOn(self.canv, x, y)
                y -= (box_height*inch + spacing)
    ability_column = AbilityColumn(ability_boxes)

    # Import class features for the character's class
    from .characters import CLASS_FEATURES
    char_class = session.get('class', 'Unknown')
    features = CLASS_FEATURES.get(char_class, [])

    # Build the three-column layout: Ability Scores (left), Race & Class Info (center), Class Features (right)
    # Each column is a list of flowables (tables, paragraphs, etc.)
    class_features_flow = []
    if features:
        class_features_flow.append(Paragraph("<b>Class Features</b>", styles['SectionHeader']))
        for feature in features:
            class_features_flow.append(Paragraph(f"• {feature}", styles['CharacterText']))
    # Move ability boxes directly under title, shift left, and move Class Features to right edge
    # Move the Ability Scores title to the right to center above the boxes (without moving the boxes)
    # 4. Display the Ability Scores title and the column of boxes in the PDF
    # Ability Scores Title as a Table for precise control 
    ability_title_table = Table(
        [["Ability\nScores"]],  # Each word on its own line
        colWidths=[1.32*inch],
        rowHeights=[0.6*inch]
    )
    ability_title_table.setStyle(TableStyle([
    ('TEXTCOLOR', (0,0), (0,0), colors.red),
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (0,0), 15),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('VALIGN', (0,0), (0,0), 'MIDDLE'),
        # Adjust these paddings for fine-tuned positioning 
        ('LEFTPADDING', (0,0), (0,0), 70),   # Increase to move text right
        ('RIGHTPADDING', (0,0), (0,0), 12),  # Increase to move text left
        ('TOPPADDING', (0,0), (0,0), 6),     # Increase to move text down
        ('BOTTOMPADDING', (0,0), (0,0), 6),  # Increase to move text up
    # ('BOX', (0,0), (0,0), 1, colors.white),
    ]))
    ability_scores_col = [
        ability_title_table,  # Table title for precise control
        Spacer(1, 16),        # Adjust vertical space below title
        ability_column
    ]
    from reportlab.platypus import Spacer
    race_info_col = [Spacer(1, 0), Paragraph("<para align='center'><b>Race & Class Info</b></para>", styles['SectionHeader']), Table(info_data, colWidths=[1.6*inch, 1.6*inch], style=TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BACKGROUND', (0,0), (-1,-1), colors.tan),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.red),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),

        ('FONTSIZE', (0,0), (-1,-1), 15),
    ('GRID', (0,0), (-1,-1), 1, colors.saddlebrown),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.tan, colors.HexColor('#e8dcc0')]),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))]
    # Increase right column width to push Class Features further right
    # Add a spacer column to push Class Features to the right edge
    spacer_col = ""
    # Add a left Spacer to race_info_col to shift it right to align with skills_table (2.2*inch)
    race_info_col_with_spacer = [Spacer(2.2*inch, 0)] + race_info_col[1:]
    three_col_table = Table([
        [ability_scores_col, race_info_col_with_spacer, spacer_col, class_features_flow]
    ], colWidths=[1.45*inch, 4.0*inch, 0.7*inch, 2.55*inch])
    three_col_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'CENTER'),  # spacer
        ('ALIGN', (3,0), (3,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 6),
        ('LEFTPADDING', (1,0), (1,0), 2.2*inch),  # Shift Race & Class Info right to align with skills table
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('LEFTPADDING', (2,0), (2,0), 0),
        ('RIGHTPADDING', (2,0), (2,0), 0),
    ('LEFTPADDING', (3,0), (3,0), 0.5*inch),  # Move Class Features right
        ('RIGHTPADDING', (3,0), (3,0), 0),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(three_col_table)
    story.append(Spacer(1, 12))

    # Class Features section (below two-column layout) -- already included above, so skip here

    # === SKILLS SECTION ===
    # If the character has skills, display them in a styled table
    # Each row shows the skill name, ability, modifier, and proficiency
    # Skills table
    skills_list = session.get('skills_list', []) or []
    if skills_list:
        story.append(Paragraph("<para align='center'><b>Skills</b></para>", styles['SectionHeader']))
        table_data = [["Skill", "Ability", "Mod", "Proficient"]]
        for skill in skills_list:
            table_data.append([
                skill.get("name", ""),
                skill.get("ability", ""),
                str(skill.get("mod", "")),
                "✔" if skill.get("proficient") else ""
            ])
        skills_table = Table(table_data, colWidths=[2.2*inch, 1*inch, 0.7*inch, 0.8*inch])
        skills_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d4af37')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2c1810')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 13),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
            ('BACKGROUND', (0,1), (-1,-1), colors.tan),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2c1810')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 12),
            ('ALIGN', (0,1), (-1,-1), 'LEFT'),
            ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#8b4513')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.tan, colors.HexColor('#e8dcc0')]),
        ]))
        story.append(Spacer(1, 12))
        story.append(skills_table)
        story.append(Spacer(1, 8))
        prof_bonus = 2
        # Center Proficiency Bonus and Passive Perception
        story.append(Paragraph(f"<para align='center'>Proficiency Bonus: <b>+{prof_bonus}</b></para>", styles['CharacterText']))
        passive_perception = session.get('passive_perception')
        if passive_perception:
            story.append(Paragraph(f"<para align='center'>Passive Perception: <b>{passive_perception}</b></para>", styles['CharacterText']))

    # (Removed duplicate Remaining Funds section here)

    # (Removed duplicate Spellcasting Magic section here)

    # === WEAPONS SECTION ===
    # If the character has weapons, display them in a styled table
    # Each row shows the weapon name, damage, and properties
    # Weapons section
    if weapons := equipment.get('weapons', []):
        story.append(Paragraph("⚔️ WEAPONS & ARMAMENTS ⚔️", styles['SectionHeader']))
        weapon_data = [['Weapon', 'Damage', 'Properties']]
        for weapon in weapons:
            properties_text = ', '.join(weapon.get('properties', [])) if weapon.get('properties') else 'None'
            weapon_data.append([
                weapon.get('name', 'Unknown'),
                f"{weapon.get('damage', '')} {weapon.get('damage_type', '')}".strip(),
                properties_text
            ])
        weapon_table = Table(weapon_data, colWidths=[2*inch, 1.5*inch, 2*inch])
        weapon_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d4af37')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2c1810')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f4f1e8')),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2c1810')),
            ('FONTNAME', (0,1), ( -1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#8b4513')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f4f1e8'), colors.HexColor('#e8dcc0')]),
        ]))
        story.append(weapon_table)
        story.append(Spacer(1, 15))
    
    # === SPELLS SECTION (for spellcasters) ===
    # If the character is a Wizard or Cleric, display spellcasting stats and spell lists
    # Includes spell save DC, attack bonus, spell ability, cantrips, and level 1 spells
    # SPELLCASTING SECTION (for Wizards and Clerics) 
    if session.get('class') in ["Wizard", "Cleric"]:
        from reportlab.platypus import PageBreak
        story.append(PageBreak())  # Start spellcasting section on a new page
        # Center Spellcasting Magic title using a centered Paragraph
        story.append(Paragraph("<para align='center'>🔮 SPELLCASTING MAGIC 🔮</para>", styles['SectionHeader']))
        story.append(Spacer(1, 2))

        # Spellcasting ability and stats
        spellcasting_ability = 'Intelligence' if session.get('class') == 'Wizard' else 'Wisdom'
        spell_save_dc = session.get('spell_save_dc', 'N/A')
        spell_attack_bonus = session.get('spell_attack_bonus', 0)

        # Create spell stats boxes
        spell_stat_boxes = []
        spell_stats = [
            ('SPELL SAVE DC', spell_save_dc, 'DC'),
            ('SPELL ATTACK', f"+{spell_attack_bonus}", 'ATK'),
            ('SPELL ABILITY', spellcasting_ability[:3].upper(), 'ABIL')
        ]

        for stat_name, value, abbrev in spell_stats:
            box_data = [
                [stat_name],
                [str(value)],
                [abbrev]
            ]
            spell_box = Table(box_data, colWidths=[1.6*inch], rowHeights=[0.25*inch, 0.5*inch, 0.2*inch])
            spell_box.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0,0), (0,0), colors.HexColor('#4b0082')),
                ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#e6e6fa')),
                ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (0,0), 8),
                ('ALIGN', (0,0), (0,0), 'CENTER'),
                ('VALIGN', (0,0), (0,0), 'MIDDLE'),

                # Value
                ('BACKGROUND', (0,1), (0,1), colors.HexColor('#e6e6fa')),
                ('TEXTCOLOR', (0,1), (0,1), colors.HexColor('#4b0082')),
                ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,1), (0,1), 14),
                ('ALIGN', (0,1), (0,1), 'CENTER'),
                ('VALIGN', (0,1), (0,1), 'MIDDLE'),

                # Abbrev
                ('BACKGROUND', (0,2), (0,2), colors.HexColor('#d4af37')),
                ('TEXTCOLOR', (0,2), (0,2), colors.HexColor('#4b0082')),
                ('FONTNAME', (0,2), (0,2), 'Helvetica-Bold'),
                ('FONTSIZE', (0,2), (0,2), 8),
                ('ALIGN', (0,2), (0,2), 'CENTER'),
                ('VALIGN', (0,2), (0,2), 'MIDDLE'),

                # Borders
                ('BOX', (0,0), (0,2), 2, colors.HexColor('#4b0082')),
                ('INNERGRID', (0,0), (0,2), 1, colors.HexColor('#4b0082')),
            ]))
            spell_stat_boxes.append(spell_box)

        # Display spell stat boxes, centered, with correct width for purple box
        spell_stats_row = Table([spell_stat_boxes], colWidths=[1.7*inch] * len(spell_stat_boxes))
        spell_stats_row.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(spell_stats_row)
        story.append(Spacer(1, 15))
        
        # Cantrips section
        if cantrips := session.get('cantrips'):
            cantrip_header_table = Table([['⭐ CANTRIPS (AT WILL) ⭐']], colWidths=[5.78*inch])
            cantrip_header_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor('#4b0082')),
                ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#e6e6fa')),
                ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (0,0), 12),
                ('ALIGN', (0,0), (0,0), 'CENTER'),
                ('VALIGN', (0,0), (0,0), 'MIDDLE'),
                ('BOX', (0,0), (0,0), 2, colors.HexColor('#4b0082')),
            ]))
            story.append(cantrip_header_table)
            
            # Process cantrips
            cantrip_names = []
            for cantrip in cantrips:
                if isinstance(cantrip, (list, tuple)) and len(cantrip) >= 2:
                    cantrip_names.append(cantrip[1])
                elif isinstance(cantrip, str):
                    cantrip_names.append(cantrip)
                else:
                    cantrip_names.append(str(cantrip))
            
            # Display cantrips in a box
            cantrip_text = " ◆ ".join(cantrip_names)
            cantrip_content_table = Table([[cantrip_text]], colWidths=[5.78*inch])
            cantrip_content_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f0f0ff')),
                ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#4b0082')),
                ('FONTNAME', (0,0), (0,0), 'Helvetica'),
                ('FONTSIZE', (0,0), (0,0), 10),
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('VALIGN', (0,0), (0,0), 'TOP'),
                ('BOX', (0,0), (0,0), 1, colors.HexColor('#4b0082')),
                ('LEFTPADDING', (0,0), (0,0), 8),
                ('RIGHTPADDING', (0,0), (0,0), 8),
                ('TOPPADDING', (0,0), (0,0), 6),
                ('BOTTOMPADDING', (0,0), (0,0), 6),
            ]))
            story.append(cantrip_content_table)
            story.append(Spacer(1, 10))
        
        # Level 1 Spells section
        if level1_spells := session.get('level1_spells'):
            class_name = session.get('class')
            header_text = "📚 1ST LEVEL SPELLS (SPELLBOOK) 📚" if class_name == "Wizard" else "🙏 1ST LEVEL SPELLS (PREPARED) 🙏"
            
            spell_header_table = Table([[header_text]], colWidths=[5.78*inch])
            spell_header_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor('#4b0082')),
                ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#e6e6fa')),
                ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (0,0), 12),
                ('ALIGN', (0,0), (0,0), 'CENTER'),
                ('VALIGN', (0,0), (0,0), 'MIDDLE'),
                ('BOX', (0,0), (0,0), 2, colors.HexColor('#4b0082')),
            ]))
            story.append(spell_header_table)
            
            # Process level 1 spells
            spell_names = []
            for spell in level1_spells:
                if isinstance(spell, (list, tuple)) and len(spell) >= 2:
                    spell_names.append(spell[1])
                elif isinstance(spell, str):
                    spell_names.append(spell)
                else:
                    spell_names.append(str(spell))
            
            # Display spells in a box
            spell_text = " ◆ ".join(spell_names)
            spell_content_table = Table([[spell_text]], colWidths=[5.78*inch])
            spell_content_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f0f0ff')),
                ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#4b0082')),
                ('FONTNAME', (0,0), (0,0), 'Helvetica'),
                ('FONTSIZE', (0,0), (0,0), 10),
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('VALIGN', (0,0), (0,0), 'TOP'),
                ('BOX', (0,0), (0,0), 1, colors.HexColor('#4b0082')),
                ('LEFTPADDING', (0,0), (0,0), 8),
                ('RIGHTPADDING', (0,0), (0,0), 8),
                ('TOPPADDING', (0,0), (0,0), 6),
                ('BOTTOMPADDING', (0,0), (0,0), 6),
            ]))
            story.append(spell_content_table)
        
        story.append(Spacer(1, 20))
    
    # === ADVENTURING GEAR SECTION ===
    # Display lists of adventuring gear, special equipment, and unequipped items
    # Each section is styled and can show items as a list or bullet points
    # ADVENTURING GEAR SECTION 
    gear_sections = [
        ('adventuring_gear', 'ADVENTURING GEAR'),
        ('special_equipment', 'SPECIAL EQUIPMENT'),
        ('unequipped_items', 'UNEQUIPPED ITEMS')
    ]
    
    for gear_key, gear_title in gear_sections:
        gear_items = equipment.get(gear_key, [])
        # For special_equipment, get the values (dict -> list of dicts)
        if gear_key == 'special_equipment' and isinstance(gear_items, dict):
            gear_items = list(gear_items.values())
        if gear_items:
            if gear_title in ['SPECIAL EQUIPMENT', 'ADVENTURING GEAR']:
                story.append(Paragraph(f"<para align='center'>🎒 {gear_title} 🎒</para>", styles['SectionHeader']))
            else:
                story.append(Paragraph(f"🎒 {gear_title} 🎒", styles['SectionHeader']))
            gear_text_items = []
            for i, item in enumerate(gear_items):
                if isinstance(item, dict):
                    if gear_key == 'unequipped_items':
                        item_text = f"{item.get('name', 'Unknown')} ({item.get('reason', 'No reason given')})"
                    else:
                        item_name = item.get('name', str(item))
                        lower_name = item_name.lower()
                        if lower_name in ('ammunition', 'musical instrument'):
                            specific_type = item.get('type') or item.get('subtype') or item.get('item_type')
                            if specific_type:
                                item_name = specific_type.capitalize()
                        qty = item.get('quantity') or item.get('count')
                        if qty:
                            item_text = f"{item_name} (x{qty})"
                        else:
                            item_text = item_name
                    gear_text_items.append(item_text)
                else:
                    item_text = str(item)
                    gear_text_items.append(item_text)
            # Center Brewer's Supplies if under SPECIAL EQUIPMENT
            if gear_title == 'SPECIAL EQUIPMENT' and any('brewer' in s.lower() for s in gear_text_items):
                for item_text in gear_text_items:
                    if 'brewer' in item_text.lower():
                        story.append(Paragraph(f"<para align='center'>{item_text}</para>", styles['CharacterText']))
                    else:
                        story.append(Paragraph(item_text, styles['CharacterText']))
            else:
                # Split into multiple lines if too many items
                if len(gear_text_items) <= 3:
                    gear_text = " • ".join(gear_text_items)
                    story.append(Paragraph(gear_text, styles['CharacterText']))
                else:
                    # Show as bullet list for many items
                    for item_text in gear_text_items:
                        story.append(Paragraph(f"• {item_text}", styles['CharacterText']))
            story.append(Spacer(1, 15))
    # === REMAINING FUNDS SECTION ===
    # Show the character's remaining funds in a styled box
    # Uses a custom Jinja filter for formatting coin display
    # REMAINING FUNDS SECTION 
    # Center Remaining Funds title
    story.append(Paragraph("<para align='center'>💰 REMAINING FUNDS 💰</para>", styles['SectionHeader']))
    from .utils.currency_utils import format_coin_display
    coins_left = session.get('coins_left', {})
    funds_display = format_coin_display(coins_left) if coins_left else "0 gp"
    
    # Display funds in a nice box
    funds_table = Table([[funds_display]], colWidths=[4*inch])
    funds_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#d4af37')),
        ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#2c1810')),
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (0,0), 14),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('VALIGN', (0,0), (0,0), 'MIDDLE'),
        ('BOX', (0,0), (0,0), 2, colors.HexColor('#8b4513')),
        ('TOPPADDING', (0,0), (0,0), 8),
        ('BOTTOMPADDING', (0,0), (0,0), 8),
    ]))
    story.append(funds_table)
    story.append(Spacer(1, 30))
    
    # === FOOTER ===
    # Add a decorative footer and credits to the PDF
    # FOOTER 
    story.append(Paragraph("═" * 80, styles['CharacterText']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Generated by D&D 5E Character Builder", styles['CharacterText']))
    story.append(Paragraph("Adventure awaits! 🗡️🛡️🔮", styles['CharacterText']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("═" * 80, styles['CharacterText']))
    
    # Build the PDF and send it as a downloadable file
    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="character_overview.pdf",
        mimetype="application/pdf"
    )
