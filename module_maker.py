import os
import sys
import shutil
import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

from helpers.mod_helpers import parse_argv
from helpers.mod_helpers import mi_other_list
from helpers.mod_helpers import write_definition
from helpers.mod_helpers import write_client
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


if __name__ == '__main__':

    # Parse the command line arguments to set all needed values
    argv_dict = parse_argv(sys.argv)

##    # temp settings for testing
##    argv_dict["filename"] = '4E_Powers'
##    argv_dict["library"] = '4E Powers'
##    argv_dict["min"] = 0
##    argv_dict["max"] = 99
##    argv_dict["powers"] = True
##    argv_dict["tiers"] = True
##    argv_dict["armor"] = False
##    argv_dict["equipment"] = False
##    argv_dict["weapons"] = False
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

##    print(argv_dict)

    # Pull Items data from Portable Compendium
    item_db = []
    try:
        item_db = create_db('ddiItem.sql', "','")
    except:
        print('Error reading data source.')
    print(f'{len(item_db)} Items recovered')

    if not item_db:
        print('NO DATA FOUND IN SOURCES, MAKE SURE YOU HAVE COPIED YOUR 4E PORTABLE COMPENDIUM DATA TO SOURCES!')
        input('Press enter to close.')
        sys.exit(0)

    # Pull Powers data from Portable Compendium
    power_db = []
    try:
        power_db = create_db('ddiPower.sql', "','")
    except:
        print('Error reading data source.')
    print(f'{len(power_db)} Powers recovered')

    if not power_db:
        print('NO DATA FOUND IN SOURCES, MAKE SURE YOU HAVE COPIED YOUR 4E PORTABLE COMPENDIUM DATA TO SOURCES!')
        input('Press enter to close.')
        sys.exit(0)

    # Counter the determines the order of Library menu items
    # Note that mundane items increment this before calling the library proc
    # Magic Items & Powers increment it inside as they can create a variable number of menu items
    menu_id = 0

    # Create a tier_list depending on whether the 'tiers' option is set or not
    if argv_dict["tiers"] == True:
        tier_list = ['Heroic', 'Paragon', 'Epic']
    else:
        tier_list = ['']
    empty_tier_list = ['']


    # Check if any magic items are being extracted as we'll need a <magicitemlist>
    mi_flag = False
    for arg in argv_dict:
        if re.search(r'^mi_', arg) and argv_dict[arg] == True:
            mi_flag = True

    # Set a suffix for Magic Items menu items if a level restriction is in place
    if argv_dict["min"] != 0 or argv_dict["max"] != 99:
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
        menu_id += 1
        menu_str = 'a' + '0000'[0:len('0000')-len(str(menu_id))] + str(menu_id)

        # Extract all the Armor data into a list
        armor_list = extract_armor_list(item_db)

        # Call the three functions to generate the _ref, _lib & _tbl xml
        armor_ref = create_armor_reference(armor_list)
        armor_lib = create_armor_library(menu_str, argv_dict["library"], 'Items - Armor')
        armor_tbl = create_armor_table(armor_list, argv_dict["library"])
    else:
        armor_ref = ''
        armor_lib = ''
        armor_tbl = ''
    

    #===========================
    # EQUIPMENT
    #===========================

    if argv_dict["equipment"] == True:
        menu_id += 1
        menu_str = 'a' + '0000'[0:len('0000')-len(str(menu_id))] + str(menu_id)

        # Extract all the Equipment data into a list
        equipment_list = extract_equipment_list(item_db)

        # Call the three functions to generate the _ref, _lib & _tbl xml
        equipment_ref = create_equipment_reference(equipment_list)
        equipment_lib = create_equipment_library(menu_str, argv_dict["library"], 'Items - Equipment')
        equipment_tbl = create_equipment_table(equipment_list, argv_dict["library"])
    else:
        equipment_ref = ''
        equipment_lib = ''
        equipment_tbl = ''

    #===========================
    # WEAPONS
    #===========================

    if argv_dict["weapons"] == True:
        menu_id += 1
        menu_str = 'a' + '0000'[0:len('0000')-len(str(menu_id))] + str(menu_id)

        # Extract all the Equipment data into a list
        weapons_list = extract_weapons_list(item_db)

        # Call the three functions to generate the _ref, _lib & _tbl xml
        weapons_ref = create_weapons_reference(weapons_list)
        weapons_lib = create_weapons_library(menu_str, argv_dict["library"], 'Items - Weapons')
        weapons_tbl = create_weapons_table(weapons_list, argv_dict["library"])
    else:
        weapons_ref = ''
        weapons_lib = ''
        weapons_tbl = ''

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
    # POWERS
    #===========================

    power_lib = ''
    power_tbl = ''
    power_desc = ''

    if argv_dict["powers"] == True:
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
    export_xml += equipment_lib
    export_xml += weapons_lib
    export_xml += mi_armor_lib
    export_xml += mi_implements_lib
    export_xml += mi_weapons_lib
    export_xml += mi_other_lib_xml
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
    if argv_dict["powers"] == True:
        export_xml += ('\t<powerlists>\n')
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
    if mi_flag == True or argv_dict["powers"]:
        export_xml +=('\t<powerdesc>\n')
        export_xml += mi_armor_power
        export_xml += mi_implements_power
        export_xml += mi_weapons_power
        export_xml += mi_other_power_xml
        export_xml += power_desc
        export_xml +=('\t</powerdesc>\n')

    # CLOSE
    export_xml +=('</root>\n')

    # Fix up all the dodgy characters in one go
    export_xml = re.sub('[—|–]', '-', export_xml)
    export_xml = re.sub('’', '\'', export_xml)
    export_xml = re.sub('[“”]', '"', export_xml)

    # Write FG XML database files
    write_client('export/module_maker/data/client.xml',export_xml)
    print('\nclient.xml written')

    # Write FG XML database files
    write_definition('export/module_maker/data/definition.xml',argv_dict["library"])
    print('\ndefinition.xml written.')

    try:
        os.remove(f'export/module_maker/{argv_dict["filename"]}.mod')
    except FileNotFoundError:
        print('Cleanup not needed.')
    try:
        shutil.make_archive(f'export/module_maker/{argv_dict["filename"]}', 'zip', 'export/module_maker/data/')
        os.rename(f'export/module_maker/{argv_dict["filename"]}.zip', f'export/module_maker/{argv_dict["filename"]}.mod')
        print('\nDatabase added and module generated!')
        print('You can find it in the \'export\\module_maker\' folder\n')
    except Exception as e:
        print(f"Error creating zipped .mod file:\n{e}")
        print('\nManually zip the contents of the \'export\\module_maker\\data\' folder to create the mod.')
        print(f'Rename the complete filename (including path) to \'{argv_dict["filename"]}.mod\'.\n')

    input('Press enter to close.')
