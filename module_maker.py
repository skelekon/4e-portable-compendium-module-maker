import settings

import re
import sys
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

from helpers.mod_helpers import check_all_dbs
from helpers.mod_helpers import parse_argv
from helpers.mod_helpers import create_module

from helpers.monster_helpers import extract_monster_db
from helpers.monster_helpers import create_monster_library
from helpers.monster_helpers import create_monster_list
from helpers.monster_helpers import create_monster_cards

from helpers.trap_helpers import extract_trap_db
from helpers.trap_helpers import create_trap_library
from helpers.trap_helpers import create_trap_list
from helpers.trap_helpers import create_trap_cards

from helpers.terrain_helpers import extract_terrain_db
from helpers.terrain_helpers import create_terrain_library
from helpers.terrain_helpers import create_terrain_list
from helpers.terrain_helpers import create_terrain_cards

from helpers.disease_helpers import extract_disease_db
from helpers.disease_helpers import create_disease_library
from helpers.disease_helpers import create_disease_list
from helpers.disease_helpers import create_disease_cards

from helpers.races_helpers import extract_races_db
from helpers.races_helpers import create_races_library
from helpers.races_helpers import create_races_list
from helpers.races_helpers import create_races_cards

from helpers.classes_helpers import extract_classes_db
from helpers.classes_helpers import create_classes_library
from helpers.classes_helpers import create_classes_list
from helpers.classes_helpers import create_classes_cards

from helpers.background_helpers import extract_background_db
from helpers.background_helpers import create_background_library
from helpers.background_helpers import create_background_list
from helpers.background_helpers import create_background_cards

from helpers.heroic_helpers import extract_heroic_db
from helpers.heroic_helpers import create_heroic_library
from helpers.heroic_helpers import create_heroic_list
from helpers.heroic_helpers import create_heroic_cards

from helpers.paragon_helpers import extract_paragon_db
from helpers.paragon_helpers import create_paragon_library
from helpers.paragon_helpers import create_paragon_list
from helpers.paragon_helpers import create_paragon_cards

from helpers.epic_helpers import extract_epic_db
from helpers.epic_helpers import create_epic_library
from helpers.epic_helpers import create_epic_list
from helpers.epic_helpers import create_epic_cards

from helpers.familiar_helpers import extract_familiar_db
from helpers.familiar_helpers import create_familiar_library
from helpers.familiar_helpers import create_familiar_list
from helpers.familiar_helpers import create_familiar_cards

from helpers.deities_helpers import extract_deities_db
from helpers.deities_helpers import create_deities_library
from helpers.deities_helpers import create_deities_list
from helpers.deities_helpers import create_deities_cards

from helpers.feat_helpers import extract_feat_db
from helpers.feat_helpers import create_feat_library
from helpers.feat_helpers import create_feat_list
from helpers.feat_helpers import create_feat_cards

from helpers.power_helpers import extract_power_db
from helpers.power_helpers import create_power_library
from helpers.power_helpers import create_power_list
from helpers.power_helpers import create_power_cards

from helpers.alchemy_helpers import extract_alchemy_db
from helpers.alchemy_helpers import create_alchemy_item_library
from helpers.alchemy_helpers import create_formula_library
from helpers.alchemy_helpers import create_alchemy_item_list
from helpers.alchemy_helpers import create_formula_list
from helpers.alchemy_helpers import create_formula_cards

from helpers.ritual_helpers import extract_ritual_db
from helpers.ritual_helpers import create_ritual_library
from helpers.ritual_helpers import create_ritual_list
from helpers.ritual_helpers import create_ritual_cards

from helpers.poison_helpers import extract_poison_db
from helpers.poison_helpers import create_poison_library
from helpers.poison_helpers import create_poison_list
from helpers.poison_helpers import create_poison_cards

from helpers.armor_helpers import extract_armor_db
from helpers.armor_helpers import create_armor_library
from helpers.armor_helpers import create_armor_list
from helpers.armor_helpers import create_armor_cards

from helpers.weapons_helpers import extract_weapons_db
from helpers.weapons_helpers import create_weapons_library
from helpers.weapons_helpers import create_weapons_list
from helpers.weapons_helpers import create_weapons_cards

from helpers.equipment_helpers import extract_equipment_db
from helpers.equipment_helpers import create_equipment_library
from helpers.equipment_helpers import create_equipment_list
from helpers.equipment_helpers import create_equipment_cards

from helpers.mi_armor_helpers import extract_mi_armor_db
from helpers.mi_other_helpers import extract_mi_other_db
from helpers.mi_weaplements_helpers import extract_mi_weaplements_db

from helpers.mi_helpers import mi_other_list
from helpers.mi_helpers import create_mi_cards
from helpers.mi_helpers import create_mi_library
from helpers.mi_helpers import create_mi_list

if __name__ == '__main__':

    # Check all db files are present
    check_all_dbs()

    # Parse the command line arguments to set all needed values
    parse_argv(sys.argv)

##    # override settings for testing
##    settings.filename = '4E_Items'
##    settings.library = '4E Items'
##    settings.min_lvl = 0
##    settings.max_lvl = 5
##    settings.static = True
##    settings.tiers = True
##    settings.npcs = True
##    settings.traps = True
##    settings.terrain = True
##    settings.diseases = True
##    settings.races = True
##    settings.classes = True
##    settings.backgrounds = True
##    settings.heroic = True
##    settings.paragon = True
##    settings.epic = True
##    settings.familiars = True
##    settings.deities = True
##    settings.feats = True
##    settings.powers = True
##    settings.basic = True
##    settings.alchemy = True
##    settings.rituals = True
##    settings.practices = True
##    settings.poisons = True
##    settings.mundane = True
##    settings.armor = True
##    settings.weapons = True
##    settings.equipment = True
##    settings.magic = True
##    settings.mi_armor = True
##    settings.mi_implements = True
##    settings.mi_weapons = True
##    settings.mi_alchemical = True
##    settings.mi_alternative = True
##    settings.mi_ammunition = True
##    settings.mi_arms = True
##    settings.mi_companion = True
##    settings.mi_consumable = True
##    settings.mi_familiar = True
##    settings.mi_feet = True
##    settings.mi_hands = True
##    settings.mi_head = True
##    settings.mi_head_neck = True
##    settings.mi_mount = True
##    settings.mi_neck = True
##    settings.mi_ring = True
##    settings.mi_waist = True
##    settings.mi_wondrous = True

    # Counter the determines the order of Library menu items
    settings.lib_id = 0

    tier_list = []
    # Create a tier_list depending on whether the 'tiers' option is set or not
    # only include Tiers that overlap with the selected Min/Max level range
    if settings.tiers:
        if settings.min_lvl <= 10:
            tier_list.append('Heroic')
        if settings.min_lvl <= 20 and settings.max_lvl >= 11:
            tier_list.append('Paragon')
        if settings.max_lvl >= 21:
            tier_list.append('Epic')
    else:
        tier_list = ['']
    # this is always empty to use for 'other' magic items
    empty_tier_list = ['']

    # Set a suffix if a level restriction is in place
    if settings.min_lvl <= 1 and settings.max_lvl == 10:
        suffix_str = ' (Heroic)'
    elif settings.min_lvl == 11 and settings.max_lvl == 20:
        suffix_str = ' (Paragon)'
    elif settings.min_lvl == 21 and settings.max_lvl >= 30:
        suffix_str = ' (Epic)'
    elif settings.min_lvl != 0 or settings.max_lvl != 99:
        if settings.min_lvl == settings.max_lvl:
            suffix_str = f' (Level {settings.min_lvl})'
        else:
            suffix_str = f' (Levels {settings.min_lvl}-{settings.max_lvl})'
    else:
        suffix_str = ''

    # Check if any magic or mundane items are being exported as we need to read the item database
    if settings.mundane or settings.magic:
        # Pull Items data from Portable Compendium
        item_db = []
        try:
            item_db = create_db('sql\ddiItem.sql', '\',\'')
        except:
            print('Error reading Item data source.')

        if not item_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

    # Check if any types of rituals are being exported as we need to read the rituals database
    if settings.alchemy or settings.rituals or settings.practices:
        # Pull Rituals data from Portable Compendium
        ritual_db = []
        try:
            ritual_db = create_db('sql\ddiRitual.sql', "','")
        except:
            print('Error reading Ritual data source.')

        if not ritual_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

    #===========================
    # MONSTERS
    #===========================

    monster_lib_concat = ''
    monster_list_concat = ''
    monster_cards = ''
    monster_tbl_list = ['NPCs By Letter', 'NPCs By Level', 'NPCs By Level/Role', 'NPCs By Role/Level']

    if settings.npcs:
        # Pull Monsters data from Portable Compendium
        monster_db = []
        try:
            monster_db = create_db('sql\ddiMonster.sql', "','")
        except:
            print('Error reading Monster data source.')
    
        if not monster_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        # Only need to get the list of monsters once
        monster_extract = extract_monster_db(monster_db)

        # Loop through the different monster list types to build the library menus and lists
        monster_list_concat += ('\t\t<npc>\n')
        for tbl_name in monster_tbl_list:
            monster_lib = create_monster_library(tier_list, tbl_name + suffix_str)
            monster_list = create_monster_list(monster_extract, tier_list, tbl_name + suffix_str)
            monster_lib_concat += monster_lib
            monster_list_concat += monster_list
        monster_list_concat += ('\t\t</npc>\n')

        monster_cards = create_monster_cards(monster_extract)

    #===========================
    # TRAPS
    #===========================

    trap_lib_concat = ''
    trap_list_concat = ''
    trap_cards = ''
    trap_tbl_list = ['Traps By Letter', 'Traps By Level']#, 'Traps By Level/Role', 'Traps By Role/Level']

    if settings.traps:
        # Pull Traps data from Portable Compendium
        trap_db = []
        try:
            trap_db = create_db('sql\ddiTrap.sql', "','")
        except:
            print('Error reading Trap data source.')
    
        if not trap_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        # Only need to get the list of traps once
        trap_extract = extract_trap_db(trap_db)

        # Loop through the different traps list types to build the library menus and lists
        trap_list_concat += ('\t\t<traps>\n')
        for tbl_name in trap_tbl_list:
            trap_lib = create_trap_library(tier_list, tbl_name + suffix_str)
            trap_list = create_trap_list(trap_extract, tier_list, tbl_name + suffix_str)
            trap_lib_concat += trap_lib
            trap_list_concat += trap_list
        trap_list_concat += ('\t\t</traps>\n')

        trap_cards = create_trap_cards(trap_extract)

    #===========================
    # TERRAIN
    #===========================

    terrain_lib = ''
    terrain_list = ''
    terrain_cards = ''

    if settings.terrain:
        # Pull Terrain data from Portable Compendium
        terrain_db = []
        try:
            terrain_db = create_db('sql\ddiTerrain.sql', "','")
        except:
            print('Error reading Terrain data source.')
    
        if not terrain_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        terrain_extract = extract_terrain_db(terrain_db)
        terrain_lib = create_terrain_library()
        terrain_list = create_terrain_list(terrain_extract)
        terrain_cards = create_terrain_cards(terrain_extract)

    #===========================
    # DISEASES
    #===========================

    disease_lib = ''
    disease_list = ''
    disease_cards = ''

    if settings.diseases:
        # Pull Diseases data from Portable Compendium
        diseases_db = []
        try:
            diseases_db = create_db('sql\ddiDisease.sql', "','")
        except:
            print('Error reading Diseases data source.')
    
        if not diseases_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        disease_extract = extract_disease_db(diseases_db)
        disease_lib = create_disease_library()
        disease_list = create_disease_list(disease_extract)
        disease_cards = create_disease_cards(disease_extract)

    #===========================
    # RACES
    #===========================

    races_lib = ''
    races_list = ''
    races_cards = ''
    racefeatures_cards = ''

    if settings.races:
        # Pull Races data from Portable Compendium
        races_db = []
        try:
            races_db = create_db('sql\ddiRace.sql', "','")
        except:
            print('Error reading Races data source.')
    
        if not races_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        races_extract = extract_races_db(races_db)
        races_lib = create_races_library()
        races_list = create_races_list(races_extract)
        races_cards, racefeatures_cards = create_races_cards(races_extract)

    #===========================
    # CLASSES
    #===========================

    classes_lib = ''
    classes_list = ''
    classes_cards = ''
    classfeatures_cards = ''

    if settings.classes:
        # Pull Classes data from Portable Compendium
        classes_db = []
        try:
            classes_db = create_db('sql\ddiClass.sql', "','")
        except:
            print('Error reading Classes data source.')
    
        if not classes_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        classes_extract = extract_classes_db(classes_db)
        classes_lib = create_classes_library()
        classes_list = create_classes_list(classes_extract)
        classes_cards, classfeatures_cards = create_classes_cards(classes_extract)

    #===========================
    # BACKGROUNDS
    #===========================

    background_lib = ''
    background_list = ''
    background_cards = ''
    backgroundfeatures_cards = ''

    if settings.backgrounds:
        # Pull Backgrounds data from Portable Compendium
        background_db = []
        try:
            background_db = create_db('sql\ddiBackground.sql', "','")
        except:
            print('Error reading Background data source.')
    
        if not background_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        background_extract = extract_background_db(background_db)
        background_lib = create_background_library()
        background_list = create_background_list(background_extract)
        background_cards = create_background_cards(background_extract)

    #===========================
    # HEROIC THEMES
    #===========================

    heroic_lib = ''
    heroic_list = ''
    heroic_cards = ''
    heroicfeatures_cards = ''

    if settings.heroic:
        # Pull Heroic Themes data from Portable Compendium
        heroic_db = []
        try:
            heroic_db = create_db('sql\ddiTheme.sql', "','")
        except:
            print('Error reading Heroic Themes data source.')
    
        if not heroic_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        heroic_extract = extract_heroic_db(heroic_db)
        heroic_lib = create_heroic_library()
        heroic_list = create_heroic_list(heroic_extract)
        heroic_cards, heroicfeatures_cards = create_heroic_cards(heroic_extract)

    #===========================
    # PARAGON PATHS
    #===========================

    paragon_lib = ''
    paragon_list = ''
    paragon_cards = ''
    paragonfeatures_cards = ''

    if settings.paragon:
        # Pull Paragon Paths data from Portable Compendium
        paragon_db = []
        try:
            paragon_db = create_db('sql\ddiParagonPath.sql', "','")
        except:
            print('Error reading Paragon Paths data source.')
    
        if not paragon_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        paragon_extract = extract_paragon_db(paragon_db)
        paragon_lib = create_paragon_library()
        paragon_list = create_paragon_list(paragon_extract)
        paragon_cards, paragonfeatures_cards = create_paragon_cards(paragon_extract)

    #===========================
    # EPIC DESTINIES
    #===========================

    epic_lib = ''
    epic_list = ''
    epic_cards = ''
    epicfeatures_cards = ''

    if settings.epic:
        # Pull Epic Destinies data from Portable Compendium
        epic_db = []
        try:
            epic_db = create_db('sql\ddiEpicDestiny.sql', "','")
        except:
            print('Error reading Epic Destinies data source.')
    
        if not epic_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        epic_extract = extract_epic_db(epic_db)
        epic_lib = create_epic_library()
        epic_list = create_epic_list(epic_extract)
        epic_cards, epicfeatures_cards = create_epic_cards(epic_extract)

    #===========================
    # FAMILIARS
    #===========================

    familiar_lib = ''
    familiar_list = ''
    familiar_cards = ''

    if settings.familiars:
        # Pull Races data from Portable Compendium
        familiar_db = []
        try:
            familiar_db = create_db('sql\ddiCompanion.sql', "','")
        except:
            print('Error reading Familiar data source.')
    
        if not familiar_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        familiar_extract = extract_familiar_db(familiar_db)
        familiar_lib = create_familiar_library()
        familiar_list = create_familiar_list(familiar_extract)
        familiar_cards = create_familiar_cards(familiar_extract)

    #===========================
    # DEITIES
    #===========================

    deities_lib = ''
    deities_list = ''
    deities_cards = ''

    if settings.deities:
        # Pull Deities data from Portable Compendium
        deities_db = []
        try:
            deities_db = create_db('sql\ddiDeity.sql', "','")
        except:
            print('Error reading Deity data source.')
    
        if not deities_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        deities_extract = extract_deities_db(deities_db)
        deities_lib = create_deities_library()
        deities_list = create_deities_list(deities_extract)
        deities_cards = create_deities_cards(deities_extract)

    #===========================
    # FEATS
    #===========================

    feat_lib = ''
    feat_list = ''
    feat_cards = ''

    if settings.feats:
        # Pull Feats data from Portable Compendium
        feat_db = []
        try:
            feat_db = create_db('sql\ddiFeat.sql', "','")
        except:
            print('Error reading Feat data source.')

        if not feat_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        feat_extract = extract_feat_db(feat_db)
        feat_lib = create_feat_library(feat_extract)
        feat_list = create_feat_list(feat_extract)
        feat_cards = create_feat_cards(feat_extract)

    #===========================
    # POWERS
    #===========================

    power_lib = ''
    power_list = ''
    power_cards = ''

    if settings.powers or settings.basic or settings.feats or settings.races or settings.classes or settings.heroic or settings.paragon or settings.epic:
        # Pull Powers data from Portable Compendium
        power_db = []
        try:
            power_db = create_db('sql\ddiPower.sql', "','")
        except:
            print('Error reading Power data source.')
    
        if not power_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        power_extract = extract_power_db(power_db)
        power_lib = create_power_library(power_extract, suffix_str)
        power_list = create_power_list(power_extract)
        power_cards = create_power_cards(power_extract)

    #===========================
    # ALCHEMY
    #===========================

    alchemy_lib = ''
    formulas_list = ''
    alchemy_item_lib = ''
    alchemy_item_list = ''
    alchemy_cards = ''
    alchemy_mi_cards = ''
    alchemy_power = ''

    if settings.alchemy:
        alchemy_extract = extract_alchemy_db(ritual_db, 'Formula')
        alchemy_lib = create_formula_library(alchemy_extract, 'Alchemical Formulas' + suffix_str)
        alchemy_item_lib = create_alchemy_item_library(alchemy_extract, 'Alchemical Items')
        formulas_list = create_formula_list(alchemy_extract)
        alchemy_item_list = create_alchemy_item_list(alchemy_extract)
        alchemy_cards, alchemy_mi_cards, alchemy_power = create_formula_cards(alchemy_extract)

    #===========================
    # RITUALS
    #===========================

    ritual_lib = ''
    ritual_list = ''
    ritual_cards = ''

    if settings.rituals:
        ritual_extract = extract_ritual_db(ritual_db, 'Ritual')
        ritual_lib = create_ritual_library(ritual_extract, 'Rituals' + suffix_str)
        ritual_list = create_ritual_list(ritual_extract, 'Rituals' + suffix_str)
        ritual_cards = create_ritual_cards(ritual_extract)

    #===========================
    # MARTIAL PRACTICES
    #===========================

    practice_lib = ''
    practice_list = ''
    practice_cards = ''

    if settings.practices:
        practice_extract = extract_ritual_db(ritual_db, 'Practice')
        practice_lib = create_ritual_library(practice_extract, 'Martial Practices' + suffix_str)
        practice_list = create_ritual_list(practice_extract, 'Martial Practices' + suffix_str)
        practice_cards = create_ritual_cards(practice_extract)

    #===========================
    # POISONS
    #===========================

    poison_lib = ''
    poison_list = ''
    poison_cards = ''

    if settings.poisons:
        # Pull Poisons data from Portable Compendium
        poison_db = []
        try:
            poison_db = create_db('sql\ddiPoison.sql', "','")
        except:
            print('Error reading Poison data source.')
    
        if not poison_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        poison_extract = extract_poison_db(poison_db)
        poison_lib = create_poison_library()
        poison_list = create_poison_list(poison_extract)
        poison_cards = create_poison_cards(poison_extract)

    #===========================
    # ARMOR
    #===========================

    armor_lib = ''
    armor_list = ''
    armor_cards = ''

    if settings.armor:
        armor_extract = extract_armor_db(item_db)
        armor_lib = create_armor_library('Items - Armor')
        armor_list = create_armor_list(armor_extract)
        armor_cards = create_armor_cards(armor_extract)

    #===========================
    # WEAPONS
    #===========================

    weapons_lib = ''
    weapons_list = ''
    weapons_cards = ''

    if settings.weapons:
        weapons_extract = extract_weapons_db(item_db)
        weapons_lib = create_weapons_library('Items - Weapons')
        weapons_list = create_weapons_list(weapons_extract)
        weapons_cards = create_weapons_cards(weapons_extract)

    #===========================
    # EQUIPMENT
    #===========================

    equipment_lib = ''
    equipment_list = ''
    equipment_cards = ''

    if settings.equipment:
        equipment_extract = extract_equipment_db(item_db)
        equipment_lib = create_equipment_library('Items - Equipment')
        equipment_list = create_equipment_list(equipment_extract)
        equipment_cards = create_equipment_cards(equipment_extract)

    #===========================
    # MAGIC ARMOR
    #===========================

    mi_armor_lib = ''
    mi_armor_list = ''
    mi_armor_cards = ''
    mi_armor_power = ''

    if settings.mi_armor:
        mi_armor_extract = extract_mi_armor_db(item_db)
        mi_armor_lib = create_mi_library(tier_list, 'Magic Items - Armor' + suffix_str, 'Armor')
        mi_armor_list = create_mi_list(mi_armor_extract, tier_list, 'Armor')
        mi_armor_cards, mi_armor_power = create_mi_cards(mi_armor_extract)

    #===========================
    # MAGIC IMPLEMENTS
    #===========================

    mi_implements_lib = ''
    mi_implements_list = ''
    mi_implements_cards = ''
    mi_implements_power = ''

    if settings.mi_implements:
        mi_implements_extract = extract_mi_weaplements_db(item_db, 'Implement')
        mi_implements_lib = create_mi_library(tier_list, 'Magic Items - Implements' + suffix_str, 'Implements')
        mi_implements_list = create_mi_list(mi_implements_extract, tier_list, 'Implements')
        mi_implements_cards, mi_implements_power = create_mi_cards(mi_implements_extract)

    #===========================
    # MAGIC WEAPONS
    #===========================

    mi_weapons_lib = ''
    mi_weapons_list = ''
    mi_weapons_cards = ''
    mi_weapons_power = ''

    if settings.mi_weapons:
        mi_weapons_extract = extract_mi_weaplements_db(item_db, 'Weapon')
        mi_weapons_lib = create_mi_library(tier_list, 'Magic Items - Weapons' + suffix_str, 'Weapons')
        mi_weapons_list = create_mi_list(mi_weapons_extract, tier_list, 'Weapons')
        mi_weapons_cards, mi_weapons_power = create_mi_cards(mi_weapons_extract)

    #===========================
    # MAGIC OTHER
    #===========================

    mi_other_lib_concat = ''
    mi_other_list_concat = ''
    mi_other_cards_concat = ''
    mi_other_power_concat = ''

    # Get a list of details for all the 'other' item types
    mi_other_list = mi_other_list()

    # Loop through all the different types of 'other' magic items
    # this is so they will each get their own menu item
    for mi in mi_other_list:
        # get the value for this mi variable from settings
        if process_flag := eval(f'settings.{mi["arg"]}'):
            mi_other_extract = extract_mi_other_db(item_db, mi["filter"])
            mi_other_lib = create_mi_library(empty_tier_list, 'Magic Items - ' + mi["literal"] + suffix_str, mi["literal"])
            mi_other_list = create_mi_list(mi_other_extract, empty_tier_list, mi["literal"])
            mi_other_cards, mi_other_power = create_mi_cards(mi_other_extract)

            # Concatenate all the results together
            mi_other_lib_concat += mi_other_lib
            mi_other_list_concat += mi_other_list
            if mi_other_cards_concat != '':
                mi_other_cards_concat += '\n'
            mi_other_cards_concat += mi_other_cards
            if mi_other_power_concat != '':
                mi_other_power_concat += '\n'
            mi_other_power_concat += mi_other_power

    #===========================
    # XML
    #===========================

    # OPEN
    export_xml =('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    export_xml +=('<root version="2.2">\n')

######################### LIBRARY #########################
# These control the right-hand menu on the Modules screen

    export_xml += ('\t<library>\n')
    export_xml += ('\t\t<lib4ecompendium>\n')
    export_xml += ('\t\t\t<categoryname type="string">4E Compendium</categoryname>\n')
    export_xml += ('\t\t\t<entries>\n')

    export_xml += monster_lib_concat
    export_xml += trap_lib_concat
    export_xml += terrain_lib
    export_xml += disease_lib
    export_xml += races_lib
    export_xml += classes_lib
    export_xml += background_lib
    export_xml += heroic_lib
    export_xml += paragon_lib
    export_xml += epic_lib
    export_xml += familiar_lib
    export_xml += deities_lib
    export_xml += feat_lib
    export_xml += power_lib
    export_xml += alchemy_lib
    export_xml += alchemy_item_lib
    export_xml += ritual_lib
    export_xml += practice_lib
    export_xml += poison_lib
    export_xml += armor_lib
    export_xml += weapons_lib
    export_xml += equipment_lib
    export_xml += mi_armor_lib
    export_xml += mi_implements_lib
    export_xml += mi_weapons_lib
    export_xml += mi_other_lib_concat

    export_xml += ('\t\t\t</entries>\n')
    export_xml += (f'\t\t\t<name type="string">{settings.library}</name>\n')
    export_xml += ('\t\t</lib4ecompendium>\n')
    export_xml += ('\t</library>\n')

######################### LISTS #########################
# These are the lists that appears when you click on a Library menu

    if settings.static:
        export_xml += ('\t<lists static="true">\n')
    else:
        export_xml += ('\t<lists>\n')

    export_xml += alchemy_item_list
    export_xml += armor_list
    export_xml += background_list
    export_xml += classes_list
    export_xml += deities_list
    export_xml += disease_list
    export_xml += epic_list
    export_xml += equipment_list
    export_xml += familiar_list
    export_xml += feat_list
    export_xml += formulas_list
    export_xml += heroic_list
    export_xml += paragon_list
    export_xml += mi_armor_list
    export_xml += mi_implements_list
    export_xml += mi_weapons_list
    export_xml += mi_other_list_concat
    export_xml += monster_list_concat   # tag is <npc>
    export_xml += poison_list
    export_xml += power_list
    export_xml += practice_list
    export_xml += races_list
    export_xml += ritual_list
    export_xml += terrain_list
    export_xml += trap_list_concat
    export_xml += weapons_list

    export_xml += ('\t</lists>\n')

######################### CARDS #########################

    # REFERENCE
    # anything inside the <reference><items> etc tags will appear in the sidebar menus for Items, NPCs, Feats & Powers
    # static="true" suppresses empty Description boxes in Races, Classes, Paragon Paths & Epic Destinies
    if settings.static:
        export_xml += ('\t<reference static="true">\n')
    else:
        export_xml += ('\t<reference>\n')

    export_xml += background_cards
    export_xml += classes_cards
    export_xml += deities_cards
    export_xml += disease_cards
    export_xml += epic_cards
    export_xml += familiar_cards
    export_xml += feat_cards

    # FEATURES
    if settings.races or settings.classes or settings.heroic or settings.paragon or settings.epic:
        export_xml += ('\t\t<features>\n')
        export_xml += racefeatures_cards
        export_xml += classfeatures_cards
        export_xml += heroicfeatures_cards
        export_xml += paragonfeatures_cards
        export_xml += epicfeatures_cards
        export_xml += ('\t\t</features>\n')

    export_xml += heroic_cards

    # ITEMS
    if settings.mundane or settings.magic or settings.alchemy:
        export_xml +=('\t\t<items>\n')
        export_xml += armor_cards
        export_xml += weapons_cards
        export_xml += equipment_cards
        export_xml += alchemy_mi_cards
        export_xml += mi_armor_cards
        export_xml += mi_implements_cards
        export_xml += mi_weapons_cards
        export_xml += mi_other_cards_concat
        export_xml +=('\t\t</items>\n')

    # NPCS / TRAPS
    if settings.npcs or settings.traps:
        export_xml += ('\t\t<npcs>\n')
        export_xml += monster_cards
        export_xml += trap_cards
        export_xml += ('\t\t</npcs>\n')

    export_xml += paragon_cards
    export_xml += poison_cards

    # POWERDESC
    # These are the individual cards for Character, Feat or Item Powers
    if settings.magic or settings.feats or settings.powers or settings.alchemy or settings.races \
       or settings.classes or settings.heroic or settings.paragon or settings.epic:
        export_xml += ('\t\t<powers>\n')
        export_xml += power_cards
        export_xml += alchemy_power
        export_xml += mi_armor_power
        export_xml += mi_implements_power
        export_xml += mi_weapons_power
        export_xml += mi_other_power_concat
        export_xml += ('\t\t</powers>\n')

    export_xml += races_cards

    # RITUALS
    if settings.alchemy or settings.rituals or settings.practices:
        export_xml += ('\t\t<rituals>\n')
        export_xml += alchemy_cards
        export_xml += ritual_cards
        export_xml += practice_cards
        export_xml += ('\t\t</rituals>\n')

    export_xml += terrain_cards

    export_xml += ('\t</reference>\n')

    # CLOSE
    export_xml += ('</root>\n')

    # Fix up all the dodgy characters before we export
    export_xml = export_xml.replace(u'\xa0', ' ')   # &nbsp;
    export_xml = re.sub('[—−‑–]', '-', export_xml)  # hyphens
    export_xml = re.sub('[‘’]', '\'', export_xml)   # single quotes
    export_xml = re.sub('[“”]', '"', export_xml)    # double quotes
    export_xml = re.sub('[×]', 'x', export_xml)     # x's
    export_xml = re.sub('[•✦]', '-', export_xml)   # bullets
    export_xml = re.sub('[ﬂ]', 'fl', export_xml)    # ligature fl
    export_xml = re.sub('[ﬁ]', 'fi', export_xml)    # ligature fi
    export_xml = re.sub('[…]', '...', export_xml)   # horizontal ellipsis
    export_xml = re.sub('[™]', '', export_xml)      # Trademark

    create_module(export_xml)
