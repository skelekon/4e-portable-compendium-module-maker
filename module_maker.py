import settings

import re
import sys
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

from helpers.mod_helpers import check_all_dbs
from helpers.mod_helpers import parse_argv
from helpers.mod_helpers import create_module

from helpers.mi_helpers import mi_other_list
from helpers.mi_helpers import create_mi_desc
from helpers.mi_helpers import create_mi_library
from helpers.mi_helpers import create_mi_table

from helpers.monster_helpers import extract_monster_db
from helpers.monster_helpers import create_monster_library
from helpers.monster_helpers import create_monster_table
from helpers.monster_helpers import create_monster_desc

from helpers.trap_helpers import extract_trap_db
from helpers.trap_helpers import create_trap_library
from helpers.trap_helpers import create_trap_list
from helpers.trap_helpers import create_trap_cards

from helpers.disease_helpers import extract_disease_db
from helpers.disease_helpers import create_disease_library
from helpers.disease_helpers import create_disease_list
from helpers.disease_helpers import create_disease_cards

from helpers.races_helpers import extract_races_db
from helpers.races_helpers import create_races_library
from helpers.races_helpers import create_races_list
from helpers.races_helpers import create_races_desc

from helpers.classes_helpers import extract_classes_db
from helpers.classes_helpers import create_classes_library
from helpers.classes_helpers import create_classes_table
from helpers.classes_helpers import create_classes_desc

from helpers.background_helpers import extract_background_db
from helpers.background_helpers import create_background_library
from helpers.background_helpers import create_background_table
from helpers.background_helpers import create_background_desc

from helpers.heroic_helpers import extract_heroic_db
from helpers.heroic_helpers import create_heroic_library
from helpers.heroic_helpers import create_heroic_table
from helpers.heroic_helpers import create_heroic_desc

from helpers.paragon_helpers import extract_paragon_db
from helpers.paragon_helpers import create_paragon_library
from helpers.paragon_helpers import create_paragon_table
from helpers.paragon_helpers import create_paragon_desc

from helpers.epic_helpers import extract_epic_db
from helpers.epic_helpers import create_epic_library
from helpers.epic_helpers import create_epic_table
from helpers.epic_helpers import create_epic_desc

from helpers.feat_helpers import extract_feat_db
from helpers.feat_helpers import create_feat_library
from helpers.feat_helpers import create_feat_table
from helpers.feat_helpers import create_feat_desc

from helpers.power_helpers import extract_power_db
from helpers.power_helpers import create_power_library
from helpers.power_helpers import create_power_table
from helpers.power_helpers import create_power_desc

from helpers.alchemy_helpers import extract_alchemy_db
from helpers.alchemy_helpers import create_alchemy_item_library
from helpers.alchemy_helpers import create_formula_library
from helpers.alchemy_helpers import create_alchemy_item_table
from helpers.alchemy_helpers import create_formula_table
from helpers.alchemy_helpers import create_formula_desc

from helpers.ritual_helpers import extract_ritual_db
from helpers.ritual_helpers import create_ritual_library
from helpers.ritual_helpers import create_ritual_table
from helpers.ritual_helpers import create_ritual_desc

from helpers.armor_helpers import create_armor_reference
from helpers.armor_helpers import extract_armor_db
from helpers.armor_helpers import create_armor_library
from helpers.armor_helpers import create_armor_table

from helpers.weapons_helpers import create_weapons_reference
from helpers.weapons_helpers import extract_weapons_db
from helpers.weapons_helpers import create_weapons_library
from helpers.weapons_helpers import create_weapons_table

from helpers.equipment_helpers import create_equipment_reference
from helpers.equipment_helpers import extract_equipment_db
from helpers.equipment_helpers import create_equipment_library
from helpers.equipment_helpers import create_equipment_table

from helpers.familiar_helpers import extract_familiar_db
from helpers.familiar_helpers import create_familiar_library
from helpers.familiar_helpers import create_familiar_list
from helpers.familiar_helpers import create_familiar_cards

from helpers.mi_armor_helpers import extract_mi_armor_db

from helpers.mi_other_helpers import extract_mi_other_db

from helpers.mi_weaplements_helpers import extract_mi_weaplements_db

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
##    settings.diseases = True
##    settings.races = True
##    settings.classes = True
##    settings.backgrounds = True
##    settings.heroic = True
##    settings.paragon = True
##    settings.epic = True
##    settings.feats = True
##    settings.powers = True
##    settings.basic = True
##    settings.alchemy = True
##    settings.rituals = True
##    settings.practices = True
##    settings.armor = True
##    settings.weapons = True
##    settings.equipment = True
##    settings.familiars = True
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
    menu_id = 0

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
    if settings.magic or settings.items or settings.armor or settings.weapons or settings.equipment:
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
        monster_list_concat += ('\t\t<npcs>\n')
        for tbl_name in monster_tbl_list:
            monster_lib, menu_id = create_monster_library(menu_id, tier_list, tbl_name + suffix_str)
            monster_list = create_monster_table(monster_extract, tier_list, tbl_name + suffix_str)
            monster_lib_concat += monster_lib
            monster_list_concat += monster_list
        monster_list_concat += ('\t\t</npcs>\n')

        monster_cards = create_monster_desc(monster_extract)

    #===========================
    # TRAPS
    #===========================

    traps_lib_concat = ''
    traps_list_concat = ''
    traps_cards = ''
    traps_tbl_list = ['Traps By Letter', 'Traps By Level']#, 'Traps By Level/Role', 'Traps By Role/Level']

    if settings.traps:
        # Pull Traps data from Portable Compendium
        traps_db = []
        try:
            traps_db = create_db('sql\ddiTrap.sql', "','")
        except:
            print('Error reading Trap data source.')
    
        if not traps_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        # Only need to get the list of traps once
        traps_extract = extract_trap_db(traps_db)

        # Loop through the different traps list types to build the library menus and lists
        traps_list_concat += ('\t\t<traps>\n')
        for tbl_name in traps_tbl_list:
            traps_lib, menu_id = create_trap_library(menu_id, tier_list, tbl_name + suffix_str)
            traps_list = create_trap_list(traps_extract, tier_list, tbl_name + suffix_str)
            traps_lib_concat += traps_lib
            traps_list_concat += traps_list
        traps_list_concat += ('\t\t</traps>\n')

        trap_cards = create_trap_cards(traps_extract)

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
        disease_lib, menu_id = create_disease_library(menu_id)
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
        races_lib, menu_id = create_races_library(menu_id)
        races_list = create_races_list(races_extract)
        races_cards, racefeatures_cards = create_races_desc(races_extract)

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
        classes_lib, menu_id = create_classes_library(menu_id)
        classes_list = create_classes_table(classes_extract)
        classes_cards, classfeatures_cards = create_classes_desc(classes_extract)

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
        background_lib, menu_id = create_background_library(menu_id)
        background_list = create_background_table(background_extract)
        background_cards = create_background_desc(background_extract)

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
        heroic_lib, menu_id = create_heroic_library(menu_id)
        heroic_list = create_heroic_table(heroic_extract)
        heroic_cards, heroicfeatures_cards = create_heroic_desc(heroic_extract)

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
        paragon_lib, menu_id = create_paragon_library(menu_id)
        paragon_list = create_paragon_table(paragon_extract)
        paragon_cards, paragonfeatures_cards = create_paragon_desc(paragon_extract)

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
        epic_lib, menu_id = create_epic_library(menu_id)
        epic_list = create_epic_table(epic_extract)
        epic_cards, epicfeatures_cards = create_epic_desc(epic_extract)

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
        familiar_lib, menu_id = create_familiar_library(menu_id)
        familiar_list = create_familiar_list(familiar_extract)
        familiar_cards = create_familiar_cards(familiar_extract)

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
        feat_lib, menu_id = create_feat_library(menu_id, feat_extract)
        feat_list = create_feat_table(feat_extract)
        feat_cards = create_feat_desc(feat_extract)

    #===========================
    # POWERS
    #===========================

    power_lib = ''
    power_list = ''
    power_cards = ''

    if settings.powers or settings.feats or settings.races or settings.classes or settings.heroic or settings.paragon or settings.epic:
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
        power_lib, menu_id = create_power_library(menu_id, power_extract, suffix_str)
        power_list = create_power_table(power_extract)
        power_cards = create_power_desc(power_extract)

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
        alchemy_lib, menu_id = create_formula_library(menu_id, alchemy_extract, 'Alchemical Formulas' + suffix_str)
        alchemy_item_lib, menu_id = create_alchemy_item_library(menu_id, alchemy_extract, 'Alchemical Items')
        formulas_list = create_formula_table(alchemy_extract)
        alchemy_item_list = create_alchemy_item_table(alchemy_extract)
        alchemy_cards, alchemy_mi_cards, alchemy_power = create_formula_desc(alchemy_extract)

    #===========================
    # RITUALS
    #===========================

    ritual_lib = ''
    ritual_list = ''
    ritual_cards = ''

    if settings.rituals:
        ritual_extract = extract_ritual_db(ritual_db, 'Ritual')
        ritual_lib, menu_id = create_ritual_library(menu_id, ritual_extract, 'Rituals' + suffix_str)
        ritual_list = create_ritual_table(ritual_extract, 'Rituals' + suffix_str)
        ritual_cards = create_ritual_desc(ritual_extract)

    #===========================
    # MARTIAL PRACTICES
    #===========================

    practice_lib = ''
    practice_list = ''
    practice_cards = ''

    if settings.practices:
        practice_extract = extract_ritual_db(ritual_db, 'Practice')
        practice_lib, menu_id = create_ritual_library(menu_id, practice_extract, 'Martial Practices' + suffix_str)
        practice_list = create_ritual_table(practice_extract, 'Martial Practices' + suffix_str)
        practice_cards = create_ritual_desc(practice_extract)

    #===========================
    # ARMOR
    #===========================

    armor_lib = ''
    armor_list = ''
    armor_cards = ''

    if settings.armor:

        # Extract all the Armor data into a list
        armor_extract = extract_armor_db(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        armor_lib, menu_id = create_armor_library(menu_id, 'Items - Armor')
        armor_list = create_armor_table(armor_extract)
        armor_cards = create_armor_reference(armor_extract)

    #===========================
    # WEAPONS
    #===========================

    weapons_lib = ''
    weapons_list = ''
    weapons_cards = ''

    if settings.weapons:
        weapons_extract = extract_weapons_db(item_db)
        weapons_lib, menu_id = create_weapons_library(menu_id, 'Items - Weapons')
        weapons_list = create_weapons_table(weapons_extract)
        weapons_cards = create_weapons_reference(weapons_extract)

    #===========================
    # EQUIPMENT
    #===========================

    equipment_lib = ''
    equipment_list = ''
    equipment_cards = ''

    if settings.equipment:
        equipment_extract = extract_equipment_db(item_db)
        equipment_lib, menu_id = create_equipment_library(menu_id, 'Items - Equipment')
        equipment_list = create_equipment_table(equipment_extract)
        equipment_cards = create_equipment_reference(equipment_extract)

    #===========================
    # MAGIC ARMOR
    #===========================

    mi_armor_lib = ''
    mi_armor_list = ''
    mi_armor_cards = ''
    mi_armor_power = ''

    if settings.mi_armor:
        mi_armor_list = extract_mi_armor_db(item_db)
        mi_armor_lib, menu_id = create_mi_library(menu_id, tier_list, 'Magic Items - Armor' + suffix_str, 'Armor')
        mi_armor_list = create_mi_table(mi_armor_list, tier_list, 'Armor')
        mi_armor_cards, mi_armor_power = create_mi_desc(mi_armor_list)

    #===========================
    # MAGIC IMPLEMENTS
    #===========================

    mi_implements_lib = ''
    mi_implements_list = ''
    mi_implements_cards = ''
    mi_implements_power = ''

    if settings.mi_implements:
        mi_implements_list = extract_mi_weaplements_db(item_db, 'Implement')
        mi_implements_lib, menu_id = create_mi_library(menu_id, tier_list, 'Magic Items - Implements' + suffix_str, 'Implements')
        mi_implements_list = create_mi_table(mi_implements_list, tier_list, 'Implements')
        mi_implements_cards, mi_implements_power = create_mi_desc(mi_implements_list)

    #===========================
    # MAGIC WEAPONS
    #===========================

    mi_weapons_lib = ''
    mi_weapons_list = ''
    mi_weapons_cards = ''
    mi_weapons_power = ''

    if settings.mi_weapons:
        mi_weapons_list = extract_mi_weaplements_db(item_db, 'Weapon')
        mi_weapons_lib, menu_id = create_mi_library(menu_id, tier_list, 'Magic Items - Weapons' + suffix_str, 'Weapons')
        mi_weapons_list = create_mi_table(mi_weapons_list, tier_list, 'Weapons')
        mi_weapons_cards, mi_weapons_power = create_mi_desc(mi_weapons_list)

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
            mi_other_list = extract_mi_other_db(item_db, mi["filter"])
            mi_other_lib, menu_id = create_mi_library(menu_id, empty_tier_list, 'Magic Items - ' + mi["literal"] + suffix_str, mi["literal"])
            mi_other_list = create_mi_table(mi_other_list, empty_tier_list, mi["literal"])
            mi_other_cards, mi_other_power = create_mi_desc(mi_other_list)

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
    export_xml += (f'\t\t\t<name type="string">{settings.library}</name>\n')
    export_xml += ('\t\t\t<categoryname type="string">4E Core</categoryname>\n')
    export_xml += ('\t\t\t<entries>\n')

    export_xml += monster_lib_concat
    export_xml += traps_lib_concat
    export_xml += disease_lib
    export_xml += races_lib
    export_xml += classes_lib
    export_xml += background_lib
    export_xml += heroic_lib
    export_xml += paragon_lib
    export_xml += epic_lib
    export_xml += familiar_lib
    export_xml += feat_lib
    export_xml += power_lib
    export_xml += alchemy_lib
    export_xml += alchemy_item_lib
    export_xml += ritual_lib
    export_xml += practice_lib
    export_xml += armor_lib
    export_xml += weapons_lib
    export_xml += equipment_lib
    export_xml += mi_armor_lib
    export_xml += mi_implements_lib
    export_xml += mi_weapons_lib
    export_xml += mi_other_lib_concat

    export_xml += ('\t\t\t</entries>\n')
    export_xml += ('\t\t</lib4ecompendium>\n')
    export_xml += ('\t</library>\n')

######################### LISTS #########################
# These are the lists that appears when you click on a Library menu

    if settings.static:
        export_xml += ('\t<lists static="true">\n')
    else:
        export_xml += ('\t<lists>\n')

    export_xml += monster_list_concat
    export_xml += traps_list_concat
    export_xml += disease_list
    export_xml += races_list
    export_xml += classes_list
    export_xml += background_list
    export_xml += heroic_list
    export_xml += paragon_list
    export_xml += epic_list
    export_xml += feat_list
    export_xml += power_list
    export_xml += formulas_list
    export_xml += alchemy_item_list
    export_xml += ritual_list
    export_xml += practice_list
    export_xml += armor_list
    export_xml += weapons_list
    export_xml += equipment_list
    export_xml += familiar_list
    export_xml += mi_armor_list
    export_xml += mi_implements_list
    export_xml += mi_weapons_list
    export_xml += mi_other_list_concat

    export_xml += ('\t</lists>\n')

######################### CARDS #########################

    # REFERENCE
    # anything inside the <reference><items> etc tags will appear in the sidebar menus for Items, NPCs, Feats & Powers
    # static="true" suppresses empty Description boxes in Races, Classes, Paragon Paths & Epic Destinies
    if settings.static:
        export_xml += ('\t<reference static="true">\n')
    else:
        export_xml += ('\t<reference>\n')

    # NPCS / TRAPS
    if settings.npcs or settings.traps:
        export_xml += ('\t\t<npcs>\n')
        export_xml += monster_cards
        export_xml += trap_cards
        export_xml += ('\t\t</npcs>\n')

    #DISEASES
    export_xml += disease_cards

    # RACES / CLASSES/ BACKGROUNDS / HEROIC THEMES / PARAGON PATHS / EPIC DESTINIES
    export_xml += races_cards
    export_xml += classes_cards
    export_xml += background_cards
    export_xml += heroic_cards
    export_xml += paragon_cards
    export_xml += epic_cards
    export_xml += familiar_cards

    # FEATURES
    if settings.races or settings.classes or settings.heroic or settings.paragon or settings.epic:
        export_xml += ('\t\t<features>\n')
        export_xml += racefeatures_cards
        export_xml += classfeatures_cards
        export_xml += heroicfeatures_cards
        export_xml += paragonfeatures_cards
        export_xml += epicfeatures_cards
        export_xml += ('\t\t</features>\n')

    # FEATS
    export_xml += feat_cards

    # POWERDESC
    # These are the individual cards for Character, Feat or Item Powers
    if settings.magic or settings.items or settings.feats or settings.powers or settings.alchemy or settings.races \
       or settings.classes or settings.heroic or settings.paragon or settings.epic:
        export_xml += ('\t\t<powers>\n')
        export_xml += mi_armor_power
        export_xml += mi_implements_power
        export_xml += mi_weapons_power
        export_xml += mi_other_power_concat
        export_xml += power_cards
        export_xml += alchemy_power
        export_xml += ('\t\t</powers>\n')

    # ITEMS
    if settings.items or settings.armor or settings.weapons or settings.equipment or settings.mundane or settings.magic or settings.alchemy:
        export_xml +=('\t\t<items>\n')
        export_xml += armor_cards
        export_xml += weapons_cards
        export_xml += equipment_cards
        export_xml += mi_armor_cards
        export_xml += mi_implements_cards
        export_xml += mi_weapons_cards
        export_xml += mi_other_cards_concat
        export_xml += alchemy_mi_cards
        export_xml +=('\t\t</items>\n')

    # RITUALS
    if settings.alchemy or settings.rituals or settings.practices:
        export_xml += ('\t\t<rituals>\n')
        export_xml += alchemy_cards
        export_xml += ritual_cards
        export_xml += practice_cards
        export_xml += ('\t\t</rituals>\n')

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

    create_module(export_xml)
