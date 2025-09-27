# dnd_builder/data/skills/all_skills.py
# This module defines all available skills in the game, with their governing ability and descriptions.
# The ALL_SKILLS dictionary is used to populate skill selection forms and provide tooltips or help text.

ALL_SKILLS = {
    "Acrobatics": {
        "ability": "dex",
        "description": "Your Dexterity (Acrobatics) check covers your attempt to stay on your feet in a tricky situation, including maintaining balance, tumbling, and stunts."
    },
    "Animal Handling": {
        "ability": "wis",
        "description": "Your Wisdom (Animal Handling) check determines your ability to calm down a domesticated animal, keep a mount from getting spooked, or intuit an animal's intentions."
    },
    "Arcana": {
        "ability": "int",
        "description": "Your Intelligence (Arcana) check measures your knowledge about spells, magical items, eldritch symbols, magical traditions, the planes of existence, and the inhabitants of those planes."
    },
    "Athletics": {
        "ability": "str",
        "description": "Your Strength (Athletics) check covers difficult situations you encounter while climbing, jumping, or swimming."
    },
    "Deception": {
        "ability": "cha",
        "description": "Your Charisma (Deception) check determines whether you can convincingly hide the truth, either verbally or through your actions."
    },
    "History": {
        "ability": "int",
        "description": "Your Intelligence (History) check measures your ability to recall lore about historical events, legendary people, ancient kingdoms, past disputes, recent wars, and lost civilizations."
    },
    "Insight": {
        "ability": "wis",
        "description": "Your Wisdom (Insight) check decides whether you can determine the true intentions of a creature, such as when searching out a lie or predicting someone's next move."
    },
    "Intimidation": {
        "ability": "cha",
        "description": "Your Charisma (Intimidation) check determines whether you can influence others through overt threats, hostile actions, and physical violence."
    },
    "Investigation": {
        "ability": "int",
        "description": "Your Intelligence (Investigation) check allows you to look around for clues and make deductions based on those clues."
    },
    "Medicine": {
        "ability": "wis",
        "description": "Your Wisdom (Medicine) check lets you try to stabilize a dying companion or diagnose an illness."
    },
    "Nature": {
        "ability": "int",
        "description": "Your Intelligence (Nature) check measures your ability to recall lore about terrain, plants and animals, the weather, and natural cycles."
    },
    "Perception": {
        "ability": "wis",
        "description": "Your Wisdom (Perception) check lets you spot, hear, or otherwise detect the presence of something. It measures your general awareness of your surroundings."
    },
    "Performance": {
        "ability": "cha",
        "description": "Your Charisma (Performance) check determines how well you can delight an audience with music, dance, acting, storytelling, or some other form of entertainment."
    },
    "Persuasion": {
        "ability": "cha",
        "description": "Your Charisma (Persuasion) check influences someone or a group of people with tact, social graces, or good nature."
    },
    "Religion": {
        "ability": "int",
        "description": "Your Intelligence (Religion) check measures your ability to recall lore about deities, rites and prayers, religious hierarchies, holy symbols, and the practices of secret cults."
    },
    "Sleight of Hand": {
        "ability": "dex",
        "description": "Your Dexterity (Sleight of Hand) check determines whether you can perform any manual trickery, such as planting something on someone else or concealing an object on your person."
    },
    "Stealth": {
        "ability": "dex",
        "description": "Your Dexterity (Stealth) check determines how well you can conceal yourself from enemies, slink past guards, slip away without being noticed, or sneak up on someone without being seen or heard."
    },
    "Survival": {
        "ability": "wis",
        "description": "Your Wisdom (Survival) check helps you follow tracks, hunt wild game, guide your group through frozen wastelands, identify signs that owlbears live nearby, predict the weather, or avoid quicksand and other natural hazards."
    }
}

# Each skill entry includes the ability score it uses and a description for UI/help purposes.
