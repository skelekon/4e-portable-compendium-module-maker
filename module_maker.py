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

from helpers.power_helpers import extract_power_list
from helpers.power_helpers import create_power_library
from helpers.power_helpers import create_power_table
from helpers.power_helpers import create_power_desc

from helpers.feat_helpers import extract_feat_list
from helpers.feat_helpers import create_feat_library
from helpers.feat_helpers import create_feat_table
from helpers.feat_helpers import create_feat_desc


if __name__ == '__main__':

    # Check all db files are present
    check_all_dbs()

    # Parse the command line arguments to set all needed values
    argv_dict = parse_argv(sys.argv)

##    # temp settings for testing
##    argv_dict["filename"] = '4E_Weapons'
##    argv_dict["library"] = '4E Weapons'
##    argv_dict["min"] = 0
##    argv_dict["max"] = 10
##    argv_dict["powers"] = True
##    argv_dict["feats"] = True
##    argv_dict["tiers"] = False
##    argv_dict["armor"] = True
##    argv_dict["equipment"] = True
##    argv_dict["weapons"] = True
##    argv_dict["mi_armor"] = False
##    argv_dict["mi_implements"] = False
##    argv_dict["mi_weapons"] = False
##    argv_dict["mi_alchemical"] = False
##    argv_dict["mi_alternative"] = False
##    argv_dict["mi_ammunition"] = False
##    argv_dict["mi_arms"] = False
##    argv_dict["mi_companion"] = False
##    argv_dict["mi_consumable"] = False
##    argv_dict["mi_familiar"] = False
##    argv_dict["mi_feet"] = False
##    argv_dict["mi_hands"] = False
##    argv_dict["mi_head"] = False
##    argv_dict["mi_head_neck"] = False
##    argv_dict["mi_mount"] = False
##    argv_dict["mi_neck"] = False
##    argv_dict["mi_ring"] = False
##    argv_dict["mi_waist"] = False
##    argv_dict["mi_wondrous"] = False

    # Pull Items data from Portable Compendium
    item_db = []
    try:
        item_db = create_db('sql\ddiItem.sql', "','")
    except:
        print('Error reading Item data source.')

    if not item_db:
        print('NO DATA FOUND IN SOURCES, MAKE SURE YOU HAVE COPIED YOUR 4E PORTABLE COMPENDIUM DATA TO SOURCES!')
        input('Press enter to close.')
        sys.exit(0)

    # Counter the determines the order of Library menu items
    menu_id = 0

    # Create a tier_list depending on whether the 'tiers' option is set or not
    if argv_dict["tiers"] == True:
        tier_list = ['Heroic', 'Paragon', 'Epic']
    else:
        tier_list = ['']
    # this is always empty for 'other' magic items
    empty_tier_list = ['']

    # Check if any magic items are being extracted as we'll need a <magicitemlist>
    mi_flag = False
    for arg in argv_dict:
        if re.search(r'^mi_', arg) and argv_dict[arg] == True:
            mi_flag = True

    # Set a suffix for Magic Items menu items if a level restriction is in place
    if (argv_dict["min"] == 0 or argv_dict["min"] == 1) and argv_dict["max"] == 10:
            suffix_str = f' (Heroic)'
    elif argv_dict["min"] == 11 and argv_dict["max"] == 20:
            suffix_str = f' (Paragon)'
    elif argv_dict["min"] == 21 and (argv_dict["max"] == 30 or argv_dict["max"] == 99):
            suffix_str = f' (Epic)'
    elif argv_dict["min"] != 0 or argv_dict["max"] != 99:
        if argv_dict["min"] == argv_dict["max"]:
            suffix_str = f' (Level {argv_dict["min"]})'
        else:
            suffix_str = f' (Levels {argv_dict["min"]}-{argv_dict["max"]})'
    else:
        suffix_str = ''

    #===========================
    # ARMOR
    #===========================

    if argv_dict["armor"] == True:

        # Extract all the Armor data into a list
        armor_list = extract_armor_list(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        armor_lib, menu_id = create_armor_library(menu_id, argv_dict["library"], 'Items - Armor')
        armor_tbl = create_armor_table(armor_list, argv_dict["library"])
        armor_ref = create_armor_reference(armor_list)
    else:
        armor_ref = ''
        armor_lib = ''
        armor_tbl = ''
    

    #===========================
    # WEAPONS
    #===========================

    if argv_dict["weapons"] == True:

        # Extract all the Equipment data into a list
        weapons_list = extract_weapons_list(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        weapons_lib, menu_id = create_weapons_library(menu_id, argv_dict["library"], 'Items - Weapons')
        weapons_tbl = create_weapons_table(weapons_list, argv_dict["library"])
        weapons_ref = create_weapons_reference(weapons_list)
    else:
        weapons_ref = ''
        weapons_lib = ''
        weapons_tbl = ''

    #===========================
    # EQUIPMENT
    #===========================

    if argv_dict["equipment"] == True:

        # Extract all the Equipment data into a list
        equipment_list = extract_equipment_list(item_db)

        # Call the three functions to generate the _lib, _tbl & _ref xml
        equipment_lib, menu_id = create_equipment_library(menu_id, argv_dict["library"], 'Items - Equipment')
        equipment_tbl = create_equipment_table(equipment_list, argv_dict["library"])
        equipment_ref = create_equipment_reference(equipment_list)
    else:
        equipment_ref = ''
        equipment_lib = ''
        equipment_tbl = ''

    #===========================
    # MAGIC ARMOR
    #===========================

    if argv_dict["mi_armor"] == True:

        # Extract all the Equipment data into a list
        mi_armor_list = extract_mi_armor_list(item_db, argv_dict["library"], argv_dict["min"], argv_dict["max"])

        # Call the three functions to generate the _ref, _lib & _tbl xml
        mi_armor_lib, menu_id = create_mi_library(menu_id, tier_list, argv_dict["library"], 'Magic Items - Armor' + suffix_str, 'Armor')
        mi_armor_tbl = create_mi_table(mi_armor_list, tier_list, argv_dict["library"], 'Armor')
        mi_armor_desc, mi_armor_power = create_mi_desc(mi_armor_list)
    else:
        mi_armor_desc = ''
        mi_armor_power = ''
        mi_armor_lib = ''
        mi_armor_tbl = ''

    #===========================
    # MAGIC IMPLEMENTS
    #===========================

    if argv_dict["mi_implements"] == True:

        # Extract all the Equipment data into a list
        mi_implements_list = extract_mi_weaplements_list(item_db, argv_dict["library"], argv_dict["min"], argv_dict["max"], 'Implement')

        # Call the three functions to generate the _desc, _power, _lib & _tbl xml
        mi_implements_lib, menu_id = create_mi_library(menu_id, tier_list, argv_dict["library"], 'Magic Items - Implements' + suffix_str, 'Implement')
        mi_implements_tbl = create_mi_table(mi_implements_list, tier_list, argv_dict["library"], 'Implement')
        mi_implements_desc, mi_implements_power = create_mi_desc(mi_implements_list)
    else:
        mi_implements_desc = ''
        mi_implements_power = ''
        mi_implements_lib = ''
        mi_implements_tbl = ''

    #===========================
    # MAGIC WEAPONS
    #===========================

    if argv_dict["mi_weapons"] == True:

        # Extract all the Equipment data into a list
        mi_weapons_list = extract_mi_weaplements_list(item_db, argv_dict["library"], argv_dict["min"], argv_dict["max"], 'Weapon')

        # Call the three functions to generate the _desc, _power, _lib & _tbl xml
        mi_weapons_lib, menu_id = create_mi_library(menu_id, tier_list, argv_dict["library"], 'Magic Items - Weapons' + suffix_str, 'Weapon')
        mi_weapons_tbl = create_mi_table(mi_weapons_list, tier_list, argv_dict["library"], 'Weapon')
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

        if argv_dict[mi["arg"]] == True:

            # Extract all the Equipment data into a list
            mi_other_list = extract_mi_other_list(item_db, argv_dict["library"], argv_dict["min"], argv_dict["max"], mi["filter"])

            # Call the three functions to generate the _ref, _lib & _tbl xml
            mi_other_lib, menu_id = create_mi_library(menu_id, empty_tier_list, argv_dict["library"], 'Magic Items - ' + mi["literal"] + suffix_str, mi["literal"])
            mi_other_tbl = create_mi_table(mi_other_list, empty_tier_list, argv_dict["library"], mi["literal"])
            mi_other_desc, mi_other_power = create_mi_desc(mi_other_list)

            # Concatenate all the results together
            if mi_other_lib_xml != '':
                mi_other_lib_xml += '\n'
            mi_other_lib_xml += mi_other_lib
            if mi_other_tbl_xml != '':
                mi_other_tbl_xml += '\n'
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

    if argv_dict["feats"] == True:
        # Pull Feats data from Portable Compendium
        feat_db = []
        try:
            feat_db = create_db('sql\ddiFeat.sql', "','")
        except:
            print('Error reading Feat data source.')

        if not feat_db:
            print('NO DATA FOUND IN SOURCES, MAKE SURE YOU HAVE COPIED YOUR 4E PORTABLE COMPENDIUM DATA TO SOURCES!')
            input('Press enter to close.')
            sys.exit(0)

        feat_list = extract_feat_list(feat_db, argv_dict["library"], argv_dict["min"], argv_dict["max"])
        feat_lib, menu_id = create_feat_library(menu_id, argv_dict["library"], feat_list, 'feats')
        feat_tbl = create_feat_table(feat_list, argv_dict["library"])
        feat_desc = create_feat_desc(feat_list)

    #===========================
    # POWERS
    #===========================

    power_lib = ''
    power_tbl = ''
    power_desc = ''

    if argv_dict["powers"] == True:
        # Pull Powers data from Portable Compendium
        power_db = []
        try:
            power_db = create_db('sql\ddiPower.sql', "','")
        except:
            print('Error reading Power data source.')
    
        if not power_db:
            print('NO DATA FOUND IN SOURCES, MAKE SURE YOU HAVE COPIED YOUR 4E PORTABLE COMPENDIUM DATA TO SOURCES!')
            input('Press enter to close.')
            sys.exit(0)

        power_list = extract_power_list(power_db, argv_dict["library"], argv_dict["min"], argv_dict["max"])
        power_lib, menu_id = create_power_library(menu_id, argv_dict["library"], power_list, 'Powers')
        power_tbl = create_power_table(power_list, argv_dict["library"])
        power_desc = create_power_desc(power_list)

    #===========================
    # XML
    #===========================

    # OPEN
    export_xml =('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    export_xml +=('<root version="2.9">\n')

    # LIBRARY
    # These control the right-hand menu on the Modules screen
    export_xml +=('\t<library>\n')
    export_xml +=('\t\t<lib4ecompendium>\n')
    export_xml +=(f'\t\t\t<name type="string">{argv_dict["library"]}</name>\n')
    export_xml +=('\t\t\t<categoryname type="string">4E Core</categoryname>\n')
    export_xml +=('\t\t\t<entries>\n')

    export_xml += armor_lib
    export_xml += weapons_lib
    export_xml += equipment_lib
    export_xml += mi_armor_lib
    export_xml += mi_implements_lib
    export_xml += mi_weapons_lib
    export_xml += mi_other_lib_xml
    export_xml += feat_lib
    export_xml += power_lib

    export_xml +=('\t\t\t</entries>\n')
    export_xml += ('\t\t</lib4ecompendium>\n')
    export_xml +=('\t</library>\n')

    # TABLES
    # These control the tables that appears when you click on a Library menu

    # tables for mundane items - the start and end tags are in the data string
    export_xml += weapons_tbl
    export_xml += armor_tbl
    export_xml += equipment_tbl

    # MAGICITEMLISTS
    # these are tables of magic items
    if mi_flag == True:
        export_xml += ('\t<magicitemlists>\n')
        export_xml += mi_armor_tbl
        export_xml += mi_implements_tbl
        export_xml += mi_weapons_tbl
        export_xml += mi_other_tbl_xml
        export_xml += ('\t</magicitemlists>\n')

    # POWERLIST
    # these are tables of character powers
    if argv_dict["feats"] == True or argv_dict["powers"] == True:
        export_xml += ('\t<powerlists>\n')
        export_xml += feat_tbl
        export_xml += power_tbl
        export_xml += ('\t</powerlists>\n')

    # REFERENCE
    # These are the individual cards for mundane items that appear when you click on a table entry
    if argv_dict["weapons"] == True or argv_dict["armor"] == True or argv_dict["equipment"] == True:
        export_xml +=('\t<reference static="true">\n')
        export_xml += weapons_ref
        export_xml += armor_ref
        export_xml += equipment_ref
        export_xml +=('\t</reference>\n')

    # MAGICITEMDESC
    # These are the individual cards for magic items that appear when you click on an Item table entry
    if mi_flag == True:
        export_xml +=('\t<magicitemdesc>\n')
        export_xml += mi_armor_desc
        export_xml += mi_implements_desc
        export_xml += mi_weapons_desc
        export_xml += mi_other_desc_xml
        export_xml +=('\t</magicitemdesc>\n')

    # POWERDESC
    # These are the individual cards for character or item Powers
    if mi_flag == True or argv_dict["feats"] or argv_dict["powers"]:
        export_xml +=('\t<powerdesc>\n')
        export_xml += mi_armor_power
        export_xml += mi_implements_power
        export_xml += mi_weapons_power
        export_xml += mi_other_power_xml
        export_xml += feat_desc
        export_xml += power_desc
        export_xml +=('\t</powerdesc>\n')

    # CLOSE
    export_xml +=('</root>\n')

    # Fix up all the dodgy characters before we export
    export_xml = export_xml.replace(u'\xa0', ' ')   # &nbsp;
    export_xml = re.sub('[—−‑–]', '-', export_xml)  # hyphens
    export_xml = re.sub('’', '\'', export_xml)      # single quotes
    export_xml = re.sub('[“”]', '"', export_xml)    # double marks
    export_xml = re.sub('[×]', 'x', export_xml)     # x's
    export_xml = re.sub('[•✦]', '-', export_xml)    # bullets

    create_module(export_xml, argv_dict["filename"], argv_dict["library"])

    input('Press enter to close.')
