import settings

import re
import sys
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

from helpers.mod_helpers import check_all_dbs
from helpers.mod_helpers import parse_argv
from helpers.mod_helpers import mi_other_list
from helpers.mod_helpers import create_module
from helpers.mod_helpers import create_mi_desc
from helpers.mod_helpers import create_mi_library
from helpers.mod_helpers import create_mi_table

from helpers.alchemy_helpers import extract_alchemy_list
from helpers.alchemy_helpers import create_alchemy_item_library
from helpers.alchemy_helpers import create_formula_library
from helpers.alchemy_helpers import create_alchemy_item_table
from helpers.alchemy_helpers import create_formula_table
from helpers.alchemy_helpers import create_formula_desc

from helpers.ritual_helpers import extract_ritual_list
from helpers.ritual_helpers import create_ritual_library
from helpers.ritual_helpers import create_ritual_table
from helpers.ritual_helpers import create_ritual_desc

from helpers.feat_helpers import extract_feat_list
from helpers.feat_helpers import create_feat_library
from helpers.feat_helpers import create_feat_table
from helpers.feat_helpers import create_feat_desc

from helpers.power_helpers import extract_power_list
from helpers.power_helpers import create_power_library
from helpers.power_helpers import create_power_table
from helpers.power_helpers import create_power_desc

from helpers.armor_helpers import armor_list_sorter
from helpers.armor_helpers import create_armor_reference
from helpers.armor_helpers import create_armor_library
from helpers.armor_helpers import create_armor_table
from helpers.armor_helpers import extract_armor_list

from helpers.equipment_helpers import equipment_list_sorter
from helpers.equipment_helpers import create_equipment_reference
from helpers.equipment_helpers import create_equipment_library
from helpers.equipment_helpers import create_equipment_table
from helpers.equipment_helpers import extract_equipment_list

from helpers.weapons_helpers import weapons_list_sorter
from helpers.weapons_helpers import create_weapons_reference
from helpers.weapons_helpers import create_weapons_library
from helpers.weapons_helpers import create_weapons_table
from helpers.weapons_helpers import extract_weapons_list

from helpers.mi_armor_helpers import extract_mi_armor_list

from helpers.mi_other_helpers import extract_mi_other_list

from helpers.mi_weaplements_helpers import extract_mi_weaplements_list

from helpers.monster_helpers import extract_monster_list
from helpers.monster_helpers import create_monster_library
from helpers.monster_helpers import create_monster_table
from helpers.monster_helpers import create_monster_desc

if __name__ == '__main__':

    # Check all db files are present
    check_all_dbs()

    # Parse the command line arguments to set all needed values
    argv_dict = parse_argv(sys.argv)

##    # override settings for testing
##    argv_dict["filename"] = '4E_Items'
##    argv_dict["library"] = '4E Items'
##    argv_dict["min"] = 0
##    argv_dict["max"] = 5
##    argv_dict["npcs"] = True
##    argv_dict["feats"] = True
##    argv_dict["powers"] = True
##    argv_dict["basic"] = True
##    argv_dict["alchemy"] = True
##    argv_dict["rituals"] = True
##    argv_dict["practices"] = True
##    argv_dict["armor"] = True
##    argv_dict["equipment"] = True
##    argv_dict["weapons"] = True
##    argv_dict["tiers"] = True
##    argv_dict["mi_armor"] = True
##    argv_dict["mi_implements"] = True
##    argv_dict["mi_weapons"] = True
##    argv_dict["mi_alchemical"] = True
##    argv_dict["mi_alternative"] = True
##    argv_dict["mi_ammunition"] = True
##    argv_dict["mi_arms"] = True
##    argv_dict["mi_companion"] = True
##    argv_dict["mi_consumable"] = True
##    argv_dict["mi_familiar"] = True
##    argv_dict["mi_feet"] = True
##    argv_dict["mi_hands"] = True
##    argv_dict["mi_head"] = True
##    argv_dict["mi_head_neck"] = True
##    argv_dict["mi_mount"] = True
##    argv_dict["mi_neck"] = True
##    argv_dict["mi_ring"] = True
##    argv_dict["mi_waist"] = True
##    argv_dict["mi_wondrous"] = True

    # Set global variables so they don't need to be passed everywhere
    settings.library = argv_dict["library"]
    settings.min_lvl = argv_dict["min"]
    settings.max_lvl = argv_dict["max"]

    # Counter the determines the order of Library menu items
    menu_id = 0

    tier_list = []
    # Create a tier_list depending on whether the 'tiers' option is set or not
    # only include Tiers that overlap with the selected Min/Max level range
    if argv_dict["tiers"]:
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
    if argv_dict["min"] <= 1 and argv_dict["max"] == 10:
        suffix_str = ' (Heroic)'
    elif argv_dict["min"] == 11 and argv_dict["max"] == 20:
        suffix_str = ' (Paragon)'
    elif argv_dict["min"] == 21 and argv_dict["max"] >= 30:
        suffix_str = ' (Epic)'
    elif argv_dict["min"] != 0 or argv_dict["max"] != 99:
        if argv_dict["min"] == argv_dict["max"]:
            suffix_str = f' (Level {argv_dict["min"]})'
        else:
            suffix_str = f' (Levels {argv_dict["min"]}-{argv_dict["max"]})'
    else:
        suffix_str = ''

    # Check if any magic items are being exported as we'll need a <magicitemlist>
    mi_flag = False
    for arg in argv_dict:
        if re.search(r'^mi_', arg) and argv_dict[arg]:
            mi_flag = True

    # Check if any magic or mundane items are being exported as we need to read the item database
    if mi_flag or argv_dict["armor"] or argv_dict["weapons"] or argv_dict["equipment"]:
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
    if argv_dict["alchemy"] or argv_dict["rituals"] or argv_dict["practices"]:
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

    monster_lib_xml = ''
    monster_tbl_xml = ''
    monster_desc = ''
    monster_tbl_list = ['NPCs By Letter', 'NPCs By Level', 'NPCs By Level/Role', 'NPCs By Role/Level']

    if argv_dict["npcs"]:
        # Pull Powers data from Portable Compendium
        monster_db = []
        try:
            monster_db = create_db('sql\ddiMonster.sql', "','")
        except:
            print('Error reading Power data source.')
    
        if not monster_db:
            print('NO DATA FOUND. MAKE SURE PORTABLE COMPENDIUM DATA IS IN THE SQL SUBDIRECTORY!')
            input('Press enter to close.')
            sys.exit(0)

        # Only need to get the list of monsters once
        monster_list = extract_monster_list(monster_db)

        # Loop through the different monster table types to build the library menus and tables
        for tbl_name in monster_tbl_list:
            monster_lib, menu_id = create_monster_library(menu_id, tier_list, tbl_name + suffix_str)
            monster_tbl = create_monster_table(monster_list, tier_list, tbl_name + suffix_str)
            monster_lib_xml += monster_lib
            monster_tbl_xml += monster_tbl

        monster_desc = create_monster_desc(monster_list)

    #===========================
    # ALCHEMY
    #===========================

    alchemy_lib = ''
    alchemy_tbl = ''
    alchemy_item_lib = ''
    alchemy_item_tbl = ''
    alchemy_desc = ''
    alchemy_mi_desc = ''
    alchemy_power = ''

    if argv_dict["alchemy"]:
        alchemy_list = extract_alchemy_list(ritual_db, 'Formula')
        alchemy_lib, menu_id = create_formula_library(menu_id, alchemy_list, 'Alchemical Formulas' + suffix_str)
        alchemy_item_lib, menu_id = create_alchemy_item_library(menu_id, alchemy_list, 'Alchemical Items')
        alchemy_tbl = create_formula_table(alchemy_list)
        alchemy_item_tbl = create_alchemy_item_table(alchemy_list)
        alchemy_desc, alchemy_mi_desc, alchemy_power = create_formula_desc(alchemy_list)

    #===========================
    # RITUALS
    #===========================

    ritual_lib = ''
    ritual_tbl = ''
    ritual_desc = ''

    if argv_dict["rituals"]:
        ritual_list = extract_ritual_list(ritual_db, 'Ritual')
        ritual_lib, menu_id = create_ritual_library(menu_id, ritual_list, 'Rituals' + suffix_str)
        ritual_tbl = create_ritual_table(ritual_list, 'Rituals' + suffix_str)
        ritual_desc = create_ritual_desc(ritual_list)

    #===========================
    # MARTIAL PRACTICES
    #===========================

    practice_lib = ''
    practice_tbl = ''
    practice_desc = ''

    if argv_dict["practices"]:
        practice_list = extract_ritual_list(ritual_db, 'Practice')
        practice_lib, menu_id = create_ritual_library(menu_id, practice_list, 'Martial Practices' + suffix_str)
        practice_tbl = create_ritual_table(practice_list, 'Martial Practices' + suffix_str)
        practice_desc = create_ritual_desc(practice_list)

    #===========================
    # ARMOR
    #===========================

    if argv_dict["armor"]:

        # Extract all the Armor data into a list
        armor_list = extract_armor_list(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        armor_lib, menu_id = create_armor_library(menu_id, 'Items - Armor')
        armor_tbl = create_armor_table(armor_list)
        armor_ref = create_armor_reference(armor_list)
    else:
        armor_ref = ''
        armor_lib = ''
        armor_tbl = ''
    

    #===========================
    # WEAPONS
    #===========================

    if argv_dict["weapons"]:

        # Extract all the Equipment data into a list
        weapons_list = extract_weapons_list(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        weapons_lib, menu_id = create_weapons_library(menu_id, 'Items - Weapons')
        weapons_tbl = create_weapons_table(weapons_list)
        weapons_ref = create_weapons_reference(weapons_list)
    else:
        weapons_ref = ''
        weapons_lib = ''
        weapons_tbl = ''

    #===========================
    # EQUIPMENT
    #===========================

    if argv_dict["equipment"]:

        # Extract all the Equipment data into a list
        equipment_list = extract_equipment_list(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        equipment_lib, menu_id = create_equipment_library(menu_id, 'Items - Equipment')
        equipment_tbl = create_equipment_table(equipment_list)
        equipment_ref = create_equipment_reference(equipment_list)
    else:
        equipment_ref = ''
        equipment_lib = ''
        equipment_tbl = ''

    #===========================
    # MAGIC ARMOR
    #===========================

    if argv_dict["mi_armor"]:

        # Extract all the Equipment data into a list
        mi_armor_list = extract_mi_armor_list(item_db)

        # Call the three functions to generate the _ref, _lib & _tbl xml
        mi_armor_lib, menu_id = create_mi_library(menu_id, tier_list, 'Magic Items - Armor' + suffix_str, 'Armor')
        mi_armor_tbl = create_mi_table(mi_armor_list, tier_list, 'Armor')
        mi_armor_desc, mi_armor_power = create_mi_desc(mi_armor_list)
    else:
        mi_armor_desc = ''
        mi_armor_power = ''
        mi_armor_lib = ''
        mi_armor_tbl = ''

    #===========================
    # MAGIC IMPLEMENTS
    #===========================

    if argv_dict["mi_implements"]:

        # Extract all the Equipment data into a list
        mi_implements_list = extract_mi_weaplements_list(item_db, 'Implement')

        # Call the three functions to generate the _desc, _power, _lib & _tbl xml
        mi_implements_lib, menu_id = create_mi_library(menu_id, tier_list, 'Magic Items - Implements' + suffix_str, 'Implement')
        mi_implements_tbl = create_mi_table(mi_implements_list, tier_list, 'Implement')
        mi_implements_desc, mi_implements_power = create_mi_desc(mi_implements_list)
    else:
        mi_implements_desc = ''
        mi_implements_power = ''
        mi_implements_lib = ''
        mi_implements_tbl = ''

    #===========================
    # MAGIC WEAPONS
    #===========================

    if argv_dict["mi_weapons"]:

        # Extract all the Equipment data into a list
        mi_weapons_list = extract_mi_weaplements_list(item_db, 'Weapon')

        # Call the three functions to generate the _desc, _power, _lib & _tbl xml
        mi_weapons_lib, menu_id = create_mi_library(menu_id, tier_list, 'Magic Items - Weapons' + suffix_str, 'Weapon')
        mi_weapons_tbl = create_mi_table(mi_weapons_list, tier_list, 'Weapon')
        mi_weapons_desc, mi_weapons_power = create_mi_desc(mi_weapons_list)
    else:
        mi_weapons_desc = ''
        mi_weapons_power = ''
        mi_weapons_lib = ''
        mi_weapons_tbl = ''

    #===========================
    # MAGIC OTHER
    #===========================

    mi_other_desc_xml = ''
    mi_other_power_xml = ''
    mi_other_lib_xml = ''
    mi_other_tbl_xml = ''

    # Get a list of details for all the 'other' item types
    mi_other_list = mi_other_list()

    # Loop through all the different types of 'other' magic items
    # this is so they will each get their own menu item
    for mi in mi_other_list:

        if argv_dict[mi["arg"]]:

            # Extract all the Equipment data into a list
            mi_other_list = extract_mi_other_list(item_db, mi["filter"], argv_dict["alchemy"])

            # Call the three functions to generate the _ref, _lib & _tbl xml
            mi_other_lib, menu_id = create_mi_library(menu_id, empty_tier_list, 'Magic Items - ' + mi["literal"] + suffix_str, mi["literal"])
            mi_other_tbl = create_mi_table(mi_other_list, empty_tier_list, mi["literal"])
            mi_other_desc, mi_other_power = create_mi_desc(mi_other_list)

            # Concatenate all the results together
            mi_other_lib_xml += mi_other_lib
            mi_other_tbl_xml += mi_other_tbl
            if mi_other_desc_xml != '':
                mi_other_desc_xml += '\n'
            mi_other_desc_xml += mi_other_desc
            if mi_other_power_xml != '':
                mi_other_power_xml += '\n'
            mi_other_power_xml += mi_other_power

    #===========================
    # FEATS
    #===========================

    feat_lib = ''
    feat_tbl = ''
    feat_desc = ''

    if argv_dict["feats"]:
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

        feat_list = extract_feat_list(feat_db)
        feat_lib, menu_id = create_feat_library(menu_id, feat_list)
        feat_tbl = create_feat_table(feat_list)
        feat_desc = create_feat_desc(feat_list)

    #===========================
    # POWERS
    #===========================

    power_lib = ''
    power_tbl = ''
    power_desc = ''

    if argv_dict["powers"]:
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

        power_list = extract_power_list(power_db, argv_dict["basic"])
        power_lib, menu_id = create_power_library(menu_id, power_list, suffix_str)
        power_tbl = create_power_table(power_list)
        power_desc = create_power_desc(power_list)

    #===========================
    # XML
    #===========================

    # OPEN
    export_xml =('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    export_xml +=('<root version="2.2">\n')

    # LIBRARY
    # These control the right-hand menu on the Modules screen
    export_xml += ('\t<library>\n')
    export_xml += ('\t\t<lib4ecompendium>\n')
    export_xml += (f'\t\t\t<name type="string">{argv_dict["library"]}</name>\n')
    export_xml += ('\t\t\t<categoryname type="string">4E Core</categoryname>\n')
    export_xml += ('\t\t\t<entries>\n')

    export_xml += monster_lib_xml
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
    export_xml += mi_other_lib_xml
    export_xml += feat_lib
    export_xml += power_lib

    export_xml += ('\t\t\t</entries>\n')
    export_xml += ('\t\t</lib4ecompendium>\n')
    export_xml += ('\t</library>\n')

    # TABLES
    # These control the tables that appears when you click on a Library menu

    # MONSTERLISTS
    # this is the table of Rituals
    if argv_dict["npcs"]:
        export_xml += ('\t<monsterlists>\n')
        export_xml += monster_tbl_xml
        export_xml += ('\t</monsterlists>\n')

    # tables for mundane items - the start and end tags are in the data string
    export_xml += armor_tbl
    export_xml += weapons_tbl
    export_xml += equipment_tbl

    # ALCCHEMYLISTS
    # this is the table of Alchemical Formulas
    if argv_dict["alchemy"]:
        export_xml += ('\t<formulalists>\n')
        export_xml += alchemy_tbl
        export_xml += ('\t</formulalists>\n')

    # RITUALLISTS
    # this is the table of Rituals
    if argv_dict["rituals"]:
        export_xml += ('\t<rituallists>\n')
        export_xml += ritual_tbl
        export_xml += ('\t</rituallists>\n')

    # PRACTICELISTS
    # this is the table of Rituals
    if argv_dict["practices"]:
        export_xml += ('\t<practicelists>\n')
        export_xml += practice_tbl
        export_xml += ('\t</practicelists>\n')

    # MAGICITEMLISTS
    # these are tables of magic items
    if mi_flag or argv_dict["alchemy"]:
        export_xml += ('\t<magicitemlists>\n')
        export_xml += mi_armor_tbl
        export_xml += mi_implements_tbl
        export_xml += mi_weapons_tbl
        export_xml += mi_other_tbl_xml
        export_xml += alchemy_item_tbl
        export_xml += ('\t</magicitemlists>\n')

    # FEAT LISTS
    # these are tables of character feats
    if argv_dict["feats"]:
        export_xml += ('\t<featlists>\n')
        export_xml += feat_tbl
        export_xml += ('\t</featlists>\n')

    # POWER LISTS
    # these are tables of character powers
    if argv_dict["powers"]:
        export_xml += ('\t<powerlists>\n')
        export_xml += power_tbl
        export_xml += ('\t</powerlists>\n')

    # RITUALDESC
    # these are the individual ritual cards
    if argv_dict["alchemy"] or argv_dict["rituals"] or argv_dict["practices"]:
        export_xml += ('\t<ritualdesc>\n')
        export_xml += alchemy_desc
        export_xml += ritual_desc
        export_xml += practice_desc
        export_xml += ('\t</ritualdesc>\n')

    # REFERENCE
    # anything inside the <reference> tags will appear in the sidebar menus for Items, NPCs & Feats
    export_xml += ('\t<reference>\n')
    export_xml +=('\t\t<items>\n')

    # ITEMS
    # These are the individual cards for mundane items that appear when you click on a table entry
    if argv_dict["weapons"] or argv_dict["armor"] or argv_dict["equipment"]:
        export_xml += armor_ref
        export_xml += weapons_ref
        export_xml += equipment_ref

    # MAGIC ITEMS
    # These are the individual cards for magic items that appear when you click on an Item table entry
    if mi_flag or argv_dict["alchemy"]:
        export_xml += mi_armor_desc
        export_xml += mi_implements_desc
        export_xml += mi_weapons_desc
        export_xml += mi_other_desc_xml
        export_xml += alchemy_mi_desc

    export_xml +=('\t\t</items>\n')

    # NPCS
    # these are the individual cards for NPCs
    if argv_dict["npcs"]:
        export_xml += ('\t\t<npcs>\n')
        export_xml += monster_desc
        export_xml += ('\t\t</npcs>\n')

    # FEATS
    # These are the individual cards for Feats
    if argv_dict["feats"]:
        export_xml += ('\t\t<feats>\n')
        export_xml += feat_desc
        export_xml += ('\t\t</feats>\n')

    export_xml += ('\t</reference>\n')

    # POWERDESC
    # These are the individual cards for character, feat or item Powers
    if mi_flag or argv_dict["feats"] or argv_dict["powers"] or argv_dict["alchemy"]:
        export_xml += ('\t<powerdesc>\n')
        export_xml += mi_armor_power
        export_xml += mi_implements_power
        export_xml += mi_weapons_power
        export_xml += mi_other_power_xml
        export_xml += power_desc
        export_xml += alchemy_power
        export_xml += ('\t</powerdesc>\n')

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

    create_module(export_xml, argv_dict["filename"], argv_dict["npcs"])
