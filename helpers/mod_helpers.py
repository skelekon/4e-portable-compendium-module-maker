import settings

import copy
import optparse
import os
import re
import shutil
import sys
from zipfile import ZipFile, ZIP_DEFLATED

def check_all_dbs():
    file_list = ['sql\ddiClass.sql', 'sql\ddiEpicDestiny.sql', 'sql\ddiFeat.sql', 'sql\ddiItem.sql', 'sql\ddiParagonPath.sql', 'sql\ddiMonster.sql',\
                 'sql\ddiPower.sql', 'sql\ddiRace.sql', 'sql\ddiRitual.sql']
    for f in file_list:
        if not os.path.isfile(f):
            print('Missing File: ' + f)
            sys.exit(0)

    return

def parse_argv(args_in):

    # Set up all the command line options and extract to 'options'
    parser = optparse.OptionParser()
    parser.set_defaults(filename='4E_Compendium', library='4E Compendium', min=0, max=99)
    parser.add_option('--filename', action='store', dest='filename', help='create library at FILE', metavar='FILE')
    parser.add_option('--library', action='store', dest='library', help='Fantasy Grounds\' internal name for the Library', metavar='LIBRARY')
    parser.add_option('--min', action='store', dest='min', help='export items of this level and above. Applies to NPCs, Alchemical Items, Rituals, Martial Practices and Powers.')
    parser.add_option('--max', action='store', dest='max', help='export items of this level and below. Applies to NPCs, Alchemical Items, Rituals, Martial Practices and Powers.')
    parser.add_option('-n', '--npcs', action='store_true', dest='npcs', help='export all NPCs (Monsters)')
    parser.add_option('-a', '--alchemy', action='store_true', dest='alchemy', help='exports Alchemical Item information')
    parser.add_option('-r', '--rituals', action='store_true', dest='rituals', help='exports Ritual information')
    parser.add_option('-m', '--martial', action='store_true', dest='martial', help='exports Martial Practice information')
    parser.add_option('-f', '--feats', action='store_true', dest='feats', help='exports Feat information')
    parser.add_option('-p', '--powers', action='store_true', dest='powers', help='exports Power information')
    parser.add_option('-t', '--tiers', action='store_true', dest='tiers', help='divide Magic Armor, Implements and Weapons, NPCs into Tiers')
    parser.add_option('-i', '--items', action='store_true', dest='items', help='export all item types (= --mundane & --magic)')
    parser.add_option('--mundane', action='store_true', dest='mundane', help='export all mundane items')
    parser.add_option('--magic', action='store_true', dest='magic', help='export all magic items')

    
##    parser.add_option('--armor', action='store_true', dest='armor', help='include mundane Armor items in the Library')
##    parser.add_option('--equipment', action='store_true', dest='equipment', help='include mundane Equipment items in the Library')
##    parser.add_option('--weapons', action='store_true', dest='weapons', help='include mundane Weapon items in the Library')
##    parser.add_option('--mi_armor', action='store_true', dest='mi_armor', help='include Magic Armor items in the Library')
##    parser.add_option('--mi_implements', action='store_true', dest='mi_implements', help='include Magic Implements items in the Library')
##    parser.add_option('--mi_weapons', action='store_true', dest='mi_weapons', help='include Magic Weapon items in the Library')
##    parser.add_option('--mi_other', action='store_true', dest='mi_other', help='includes all Other Magic item (overrides the following)')
##    parser.add_option('--mi_alchemical', action='store_true', dest='mi_alchemical', help='includes Alchemical items in the Library')
##    parser.add_option('--mi_alternative', action='store_true', dest='mi_alternative', help='includes Alternative Rewards in the Library')
##    parser.add_option('--mi_ammunition', action='store_true', dest='mi_ammunition', help='includes Ammunition in the Library')
##    parser.add_option('--mi_arms', action='store_true', dest='mi_arms', help='includes Arms Slot items in the Library')
##    parser.add_option('--mi_companion', action='store_true', dest='mi_companion', help='includes Companions in the Library')
##    parser.add_option('--mi_consumable', action='store_true', dest='mi_consumable', help='includes Consumable items in the Library')
##    parser.add_option('--mi_familiar', action='store_true', dest='mi_familiar', help='includes Familiars in the Library')
##    parser.add_option('--mi_feet', action='store_true', dest='mi_feet', help='includes Feet Slot items in the Library')
##    parser.add_option('--mi_hands', action='store_true', dest='mi_hands', help='includes Hands Slot items in the Library')
##    parser.add_option('--mi_head', action='store_true', dest='mi_head', help='includes Head Slot in the Library')
##    parser.add_option('--mi_head_neck', action='store_true', dest='mi_head_neck', help='includes Nead and Neck Slot items in the Library')
##    parser.add_option('--mi_mount', action='store_true', dest='mi_mount', help='includes Mount items in the Library')
##    parser.add_option('--mi_neck', action='store_true', dest='mi_neck', help='includes Neck SLot items in the Library')
##    parser.add_option('--mi_ring', action='store_true', dest='mi_ring', help='includes Ring Slot items in the Library')
##    parser.add_option('--mi_waist', action='store_true', dest='mi_waist', help='includes Waist Slot items in the Library')
##    parser.add_option('--mi_wondrous', action='store_true', dest='mi_wondrous', help='includes Wondrous Items in the Library')
    (options, args) = parser.parse_args()

    # Copy all values from options except 'all' and 'mi_other'
    out_dict = {}
    out_dict["filename"] = options.filename
    out_dict["library"] = options.library
    out_dict["min"] = int(options.min) if int(options.min) >= 0 else 0
    out_dict["max"] = int(options.max) if int(options.min) <= 99 else 99
    out_dict["npcs"] = options.npcs if options.npcs != None else False
    out_dict["alchemy"] = options.alchemy if options.alchemy != None else False
    out_dict["rituals"] = options.rituals if options.rituals != None else False
    out_dict["practices"] = options.martial if options.martial != None else False
    out_dict["feats"] = options.feats if options.feats != None else False
    out_dict["powers"] = options.powers if options.powers != None else False
    out_dict["tiers"] = options.tiers if options.tiers != None else False
    out_dict["items"] = options.items if options.items != None else False
    out_dict["mundane"] = options.mundane if options.mundane != None else False
    out_dict["magic"] = options.magic if options.magic != None else False

    # Note these are currently internal/debug options that are more granular than is currently offered by the switches
    out_dict["armor"] = False
    out_dict["equipment"] = False
    out_dict["weapons"] = False
    out_dict["mi_armor"] = False
    out_dict["mi_implements"] = False
    out_dict["mi_weapons"] = False
    out_dict["mi_alchemical"] = False
    out_dict["mi_alternative"] = False
    out_dict["mi_ammunition"] = False
    out_dict["mi_arms"] = False
    out_dict["mi_companion"] = False
    out_dict["mi_consumable"] = False
    out_dict["mi_familiar"] = False
    out_dict["mi_feet"] = False
    out_dict["mi_hands"] = False
    out_dict["mi_head"] = False
    out_dict["mi_head_neck"] = False
    out_dict["mi_mount"] = False
    out_dict["mi_neck"] = False
    out_dict["mi_ring"] = False
    out_dict["mi_waist"] = False
    out_dict["mi_wondrous"] = False

    # If --mundane is specified then set mundane items to True
    if options.mundane == True:
        out_dict["armor"] = True
        out_dict["equipment"] = True
        out_dict["weapons"] = True

    # If --magic  is specified then set magic items to True
    if options.magic == True:
        out_dict["tiers"] = True
        out_dict["mi_armor"] = True
        out_dict["mi_implements"] = True
        out_dict["mi_weapons"] = True
        out_dict["mi_alchemical"] = True
        out_dict["mi_alternative"] = True
        out_dict["mi_ammunition"] = True
        out_dict["mi_arms"] = True
        out_dict["mi_companion"] = True
        out_dict["mi_consumable"] = True
        out_dict["mi_familiar"] = True
        out_dict["mi_feet"] = True
        out_dict["mi_hands"] = True
        out_dict["mi_head"] = True
        out_dict["mi_head_neck"] = True
        out_dict["mi_mount"] = True
        out_dict["mi_neck"] = True
        out_dict["mi_ring"] = True
        out_dict["mi_waist"] = True
        out_dict["mi_wondrous"] = True

    # If --items is specified then set all items to True
    if options.items == True:
        out_dict["tiers"] = True
        out_dict["armor"] = True
        out_dict["equipment"] = True
        out_dict["weapons"] = True
        out_dict["mi_armor"] = True
        out_dict["mi_implements"] = True
        out_dict["mi_weapons"] = True
        out_dict["mi_alchemical"] = True
        out_dict["mi_alternative"] = True
        out_dict["mi_ammunition"] = True
        out_dict["mi_arms"] = True
        out_dict["mi_companion"] = True
        out_dict["mi_consumable"] = True
        out_dict["mi_familiar"] = True
        out_dict["mi_feet"] = True
        out_dict["mi_hands"] = True
        out_dict["mi_head"] = True
        out_dict["mi_head_neck"] = True
        out_dict["mi_mount"] = True
        out_dict["mi_neck"] = True
        out_dict["mi_ring"] = True
        out_dict["mi_waist"] = True
        out_dict["mi_wondrous"] = True

    return out_dict


def create_module(xml_in, filename_in, dm_module_in):

    # Use db.xml for DM only modules so they are not player readable
    if dm_module_in:
        db_filename = 'db.xml'
    else:
        db_filename = 'client.xml'

    # Write FG XML client file
    with open(db_filename, mode='w', encoding='iso-8859-1', errors='strict', buffering=1) as file:
        file.write(xml_in)
    print(f'\n{db_filename} written')

    # Write FG XML definition file
    definition_str = (f'<?xml version="1.0" encoding="iso-8859-1"?>\n<root version="2.2">\n\t<name>{settings.library}</name>\n\t<author>skelekon</author>\n\t<ruleset>4E</ruleset>\n</root>')
    with open('definition.xml', mode='w', encoding='iso-8859-1', errors='strict', buffering=1) as file:
        file.write(definition_str)
    print('\ndefinition.xml written.')

    try:
        with ZipFile(f'{filename_in}.mod', 'w', compression=ZIP_DEFLATED) as modzip:
            modzip.write(db_filename)
            modzip.write('definition.xml')
            if os.path.isfile('thumbnail.png'):
                modzip.write('thumbnail.png')

        print(f'\n{filename_in}.mod generated!')
        print('\nMove it to your Fantasy Grounds\modules directory')
    except Exception as e:
        print(f'\nError creating zipped .mod file:\n{e}')

    return

def mi_other_list():

    # This returns a list of all the different types of 'Other' Magic Items so that they can be iterated
    out_list = []
    mi_other_dict = {}

    mi_other_dict["arg"] = 'mi_alchemical'
    mi_other_dict["filter"] = 'Alchemical Item'
    mi_other_dict["literal"] = 'Alchemical Item'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_alternative'
    mi_other_dict["filter"] = 'Alternative Reward'
    mi_other_dict["literal"] = 'Alternative Reward'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_ammunition'
    mi_other_dict["filter"] = 'Ammunition'
    mi_other_dict["literal"] = 'Ammunition'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_arms'
    mi_other_dict["filter"] = 'Arms'
    mi_other_dict["literal"] = 'Arms Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_companion'
    mi_other_dict["filter"] = 'Companion'
    mi_other_dict["literal"] = 'Companion'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_consumable'
    mi_other_dict["filter"] = 'Consumable'
    mi_other_dict["literal"] = 'Consumable'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_familiar'
    mi_other_dict["filter"] = 'Familiar'
    mi_other_dict["literal"] = 'Familiar'
    out_list.append(copy.deepcopy(mi_other_dict))
    
    mi_other_dict["arg"] = 'mi_feet'
    mi_other_dict["filter"] = 'Feet'
    mi_other_dict["literal"] = 'Feet Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_hands'
    mi_other_dict["filter"] = 'Hands'
    mi_other_dict["literal"] = 'Hands Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_head'
    mi_other_dict["filter"] = 'Head'
    mi_other_dict["literal"] = 'Head Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_head_neck'
    mi_other_dict["filter"] = 'Head and Neck'
    mi_other_dict["literal"] = 'Head and Neck Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_neck'
    mi_other_dict["filter"] = 'Neck'
    mi_other_dict["literal"] = 'Neck Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_mount'
    mi_other_dict["filter"] = 'Mount'
    mi_other_dict["literal"] = 'Mount'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_ring'
    mi_other_dict["filter"] = 'Ring'
    mi_other_dict["literal"] = 'Ring Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_waist'
    mi_other_dict["filter"] = 'Waist'
    mi_other_dict["literal"] = 'Waist Slot'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_wondrous'
    mi_other_dict["filter"] = 'Wondrous'
    mi_other_dict["literal"] = 'Wondrous Item'
    out_list.append(copy.deepcopy(mi_other_dict))

    return out_list

def mi_list_sorter(entry_in):
    name = entry_in["name"]
    return (name)

def create_mi_library(id_in, tier_list, name_in, item_in):
    xml_out = ''
    item_camel = re.sub('[^a-zA-Z0-9_]', '', item_in)

    for t in tier_list:

        if t != '' and len(tier_list) > 1:
            tier_str = ' (' + t + ')'
        else:
            tier_str = ''

        tier_camel = re.sub('[^a-zA-Z0-9_]', '', t)

        id_in += 1
        lib_id = 'l' + str(id_in).rjust(3, '0')

        xml_out += (f'\t\t\t\t<{lib_id}-magicitems>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{name_in}{tier_str}</name>\n')
        xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_classmagicitemtablelist</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>magicitemlists.mi{item_camel}{tier_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</librarylink>\n')
        xml_out += (f'\t\t\t\t</{lib_id}-magicitems>\n')

    return xml_out, id_in

def create_mi_table(list_in, tier_list, item_in):
    xml_out = ''

    if not list_in:
        return xml_out

    item_camel = re.sub('[^a-zA-Z0-9_]', '', item_in)

    # Loop through the Tier list that has been built for this export
    for t in tier_list:
        section_id = 0

        # Set up a label suffix for the current Tier
        if t != '' and len(tier_list) > 1:
            tier_str = ' (' + t + ')'
        else:
            tier_str = ''

        tier_camel = re.sub('[^a-zA-Z0-9_]', '', t)

        # Open Item List
        # This controls the table that appears when you click on a Library menu
        xml_out += (f'\t\t<mi{item_camel}{tier_camel}>\n')
        xml_out += (f'\t\t\t<description type="string">Magic Item Table</description>\n')
        xml_out += ('\t\t\t<groups>\n')

        # Create individual item entries
        for entry_dict in sorted(list_in, key=mi_list_sorter):

            # only process Items for the current Tier
            if t == '':
                item_tier = ''
            elif int(entry_dict["level"]) <= 10:
                item_tier = 'Heroic'
            elif int(entry_dict["level"]) <= 20:
                item_tier = 'Paragon'
            else:
                item_tier = 'Epic'

            level_str = str(entry_dict["level"]).rjust(2, '0')
            name_camel = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"])
            # Remove '(Level nn)' as the table alreasy has a level column
            name_display = re.sub(r'\s*\(Level\s*[0-9]*\)', '', entry_dict["name"])

            #Check for new section
            if entry_dict["section_id"] != section_id:
                section_id = entry_dict["section_id"]

                # Close previous Section
                if section_id != 1:
                    section_str = str(section_id - 1).rjust(3, '0')
                    xml_out += ('\t\t\t\t\t</items>\n')
                    xml_out += (f'\t\t\t\t</section{section_str}>\n')

                # Open new Section
                section_str = str(section_id).rjust(3, '0')
                xml_out += (f'\t\t\t\t<section{section_str}>\n')
                xml_out += (f'\t\t\t\t\t<description type="string">{item_in}{tier_str}</description>\n')
                xml_out += ('\t\t\t\t\t<items>\n')

            # only output items for the correct tier
            if item_tier == t:

                xml_out += (f'\t\t\t\t\t\t<mi{level_str}-{name_camel}>\n')
                xml_out += (f'\t\t\t\t\t\t\t<name type="string">{name_display}</name>\n')
                xml_out += (f'\t\t\t\t\t\t\t<cat type="string">{entry_dict["cat"]}</cat>\n')
                xml_out += (f'\t\t\t\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
                xml_out += (f'\t\t\t\t\t\t\t<level type="number">{entry_dict["level"]}</level>\n')
                xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
                xml_out += ('\t\t\t\t\t\t\t\t<class>referencemagicitem</class>\n')
                xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.items.{name_camel}-{level_str}@{settings.library}</recordname>\n')
                xml_out += ('\t\t\t\t\t\t\t</link>\n')
                xml_out += (f'\t\t\t\t\t\t</mi{level_str}-{name_camel}>\n')

        # Close last Section
        xml_out += ('\t\t\t\t\t</items>\n')
        xml_out += (f'\t\t\t\t</section{section_str}>\n')

        # Close Item List
        xml_out += ('\t\t\t</groups>\n')
        xml_out += (f'\t\t</mi{item_camel}{tier_camel}>\n')

    return xml_out

def multi_level(soup_in):
    multi_out = []

    # Get Bonus / Cost / Level lists for items with variable bonus
    bonus_list = soup_in.find('table', class_='magicitem').find_all('td', class_='mic2')
    cost_list = soup_in.find('table', class_='magicitem').find_all('td', class_='mic3')
    level_list = soup_in.find('table', class_='magicitem').find_all('td', class_='mic1')

    # Loop through the lists to create a dictionary
    # critical will be completed later in the calling function
    idx = max(len(bonus_list), len(cost_list), len(level_list))
    for item in range(idx):
        multi_dict = {}
        multi_dict['bonus'] = ''
        multi_dict['cost'] = ''
        multi_dict['level'] = ''
        multi_dict['critical'] = ''

        if bonus_str := bonus_list[item].string:
            multi_dict['bonus'] = bonus_str
        if cost_str := cost_list[item].string:
            multi_dict['cost'] = cost_str
        if level_str := level_list[item].string.replace('Lvl ', ''):
            multi_dict['level'] = level_str

        # Append dictionary to output list
        multi_out.append(copy.deepcopy(multi_dict))

    return multi_out

def create_mi_desc(list_in):
    mi_out = ''
    power_out = ''

    if not list_in:
        return mi_out, power_out

    section_str = ''
    entry_str = ''
    name_lower = ''

    # Create individual item entries
    for entry_dict in sorted(list_in, key=mi_list_sorter):
        # Don't make item cards if the item is a duplicate of an Alchemy Item
        if entry_dict["mitype"] == 'other' and entry_dict["alchemy_flag"]:
            continue
        
        level_str = str(entry_dict["level"]).rjust(2, '0')
        name_camel = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"])

        # Create all Required Power entries
        power_out += entry_dict["powerdesc"]

        mi_out += (f'\t\t\t<{name_camel}-{level_str}>\n')
        mi_out += (f'\t\t\t\t<name type="string">{entry_dict["name"]}</name>\n')
        mi_out += (f'\t\t\t\t<bonus type="number">{entry_dict["bonus"]}</bonus>\n')
        mi_out += (f'\t\t\t\t<class type="string">{entry_dict["class"]}</class>\n')
        mi_out += (f'\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
        if entry_dict["critical"] != '':
            mi_out += (f'\t\t\t\t<critical type="string">{entry_dict["critical"]}</critical>\n')
        mi_out += (f'\t\t\t\t<enhancement type="string">{entry_dict["enhancement"]}</enhancement>\n')
        mi_out += (f'\t\t\t\t<flavor type="string">{entry_dict["flavor"]}</flavor>\n')
        mi_out += (f'\t\t\t\t<formatteditemblock type="formattedtext">{entry_dict["flavor"]}</formatteditemblock>\n')
        mi_out += (f'\t\t\t\t<level type="number">{entry_dict["level"]}</level>\n')
        mi_out += (f'\t\t\t\t<mitype type="string">{entry_dict["mitype"]}</mitype>\n')
        if entry_dict["subclass"] != '':
            mi_out += (f'\t\t\t\t<subclass type="string">{entry_dict["subclass"]}</subclass>\n')
        if entry_dict["mipowers"] != '':
            mi_out += (f'\t\t\t\t<powers>\n{entry_dict["mipowers"]}\t\t\t\t</powers>\n')
        if entry_dict["props"] != '':
            mi_out += (f'\t\t\t\t<props>\n{entry_dict["props"]}\t\t\t\t</props>\n')
        mi_out += (f'\t\t\t</{name_camel}-{level_str}>\n')

    return mi_out, power_out

def power_construct(lines_list):

    # List of keywords to be included
    keywords_list = ['Acid', 'Augmentable', 'Aura', 'Charm', 'Cold', 'Conjuration', 'Fear', 'Fire', 'Healing', 'Illusion', 'Implement',\
        'Lightning', 'Necrotic', 'Poison', 'Polymorph', 'Psychic', 'Radiant', 'Sleep', 'Summoning', 'Teleportation', 'Thunder', 'Varies', 'Weapon', 'Zone']

    action_str = ''
    keywords_str = ''
    name_str = ''
    range_str = ''
    recharge_str = ''
    shortdescription_str = ''

    # Loop through list of strings that contains all information for a single power
    for line in lines_list:

        # Action
        action_test = re.search(r'(Free Action|Free|Immediate Interrupt|Immediate Reaction|Minor Action|Minor|Move Action|Move|No Action|Standard Action|Standard)', line)
        if action_test != None:
            action_str = action_test.group(1)

        # Keyword
        # exhaustive check to avoid false positives
        for kwd in keywords_list:
            if keywords_test := re.search(kwd, line):
                keywords_str += ', ' if keywords_str != '' else ''
                keywords_str += kwd

        # Range
        # take only the first entry as some multi-level items increase range with level
        range_test = re.search(r'(Area.*?|Close.*?|Ranged.*?)[;($\.]', line)
        if range_test != None and range_str == '':
           range_str = range_test.group(1).strip()

        # Recharge
        recharge_test = re.search(r'(At-Will Attack|At-Will Utility|At-Will|Consumable|Daily Attack|Daily Utility|Daily|Encounter|Healing Surge)', line, re.IGNORECASE)
        if recharge_test != None:
            recharge_str = recharge_test.group(1).title()

        # Description
        # Check for keywords that indicate a power description line
        shortdescription_test = re.search(r'(^As|^Attack:|Effect|Hit|Level|Make|Miss|Trigger|You)', line)
        # also include any line that doesn't find an action or recharge
        if shortdescription_test != None or (action_test == None and recharge_test == None):
            if shortdescription_str != '':
                shortdescription_str += '\\n'
            shortdescription_str += re.sub('\s\s', ' ', line)

    # Create and return power as a dictionary item
    power_dict = {}
    power_dict['action'] = action_str
    power_dict['keywords'] = keywords_str
    power_dict['name'] = name_str
    power_dict['range'] = range_str
    power_dict['recharge'] = recharge_str
    power_dict['shortdescription'] = shortdescription_str

    return power_dict

def powers_format(soup_in, name_in):
    name_alpha = re.sub('[^a-zA-Z0-9_]', '', name_in)
    id = 0
    powers_list = []
    in_power = False

    # Find all tags that might contain powers information
    power_tags = soup_in.find_all(class_=['mihead', 'mistat', 'mistat indent', 'mistat indent1'])
    for tag in power_tags:
        # concatenate all the elements within each tag
        tag_str = ' '.join(map(str, tag.stripped_strings))
        # if we find the beginning of a power and one is already under construction then construct and add it to the power list and start a new item
        if re.search(r'^(Attack Power|Power|Utility Power)', tag_str) and in_power:
            power_item = power_construct(new_power)
            powers_list.append(copy.deepcopy(power_item))
            new_power = []
        # else if this is the beginning of the first power then start a new item
        elif re.search(r'^(Attack Power|Power|Utility Power)', tag_str):
            in_power = True
            new_power = []
        if in_power:
            new_power.append(tag_str)
    # construct final power and add it to the power list
    if in_power:
        power_item = power_construct(new_power)
        powers_list.append(copy.deepcopy(power_item))

    # Loop though power list to create all the tags
    powerdesc_out = ''
    magicitemsdesc_out = ''
    for power in powers_list:
        id += 1
        recharge_alpha = re.sub('[^a-zA-Z0-9_]', '', power["recharge"])
        entry_id = str(id).rjust(3, '0')

        powerdesc_out += f'\t\t<item{name_alpha}Power-{entry_id}>\n'
        powerdesc_out += f'\t\t\t<name type="string">{name_in} Power - {power["recharge"]}</name>\n'
        if power["action"] != '':
            powerdesc_out += f'\t\t\t<action type="string">{power["action"]}</action>\n'
        powerdesc_out += '\t\t\t<class type="string">Item</class>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t<description type="formattedtext">{power["shortdescription"]}</description>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t<effect type="formattedtext">{power["shortdescription"]}</effect>\n'
##        if power["shortdescription"] != '':
##            powerdesc_out += f'\t\t\t<flavor type="string">{power["shortdescription"]}</flavor>\n'
        if power["keywords"] != '':
            powerdesc_out += f'\t\t\t<keywords type="string">{power["keywords"]}</keywords>\n'
        powerdesc_out += '\t\t\t<level type="number">0</level>\n'
        if power["recharge"] != '':
            powerdesc_out += f'\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        powerdesc_out += f'\t\t\t<source type="string">Item</source>\n'
        powerdesc_out += '\t\t\t<type type="string">Item</type>\n'
        powerdesc_out += f'\t\t</item{name_alpha}Power-{entry_id}>\n'

        magicitemsdesc_out += f'\t\t\t\t\t<id-{entry_id}>\n'
        magicitemsdesc_out += f'\t\t\t\t\t\t<name type="string">Power - {power["recharge"]}</name>\n'
        if power["action"] != '':
            magicitemsdesc_out += f'\t\t\t\t\t\t<action type="string">{power["action"]}</action>\n'
        if power["recharge"] != '':
            magicitemsdesc_out += f'\t\t\t\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["shortdescription"] != '':
            magicitemsdesc_out += f'\t\t\t\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        magicitemsdesc_out += '\t\t\t\t\t\t<link type="windowreference">\n'
        magicitemsdesc_out += '\t\t\t\t\t\t\t<class>powerdesc</class>\n'
        magicitemsdesc_out += f'\t\t\t\t\t\t\t<recordname>powerdesc.item{name_alpha}Power-{entry_id}@{settings.library}</recordname>\n'
        magicitemsdesc_out += '\t\t\t\t\t\t</link>\n'
        magicitemsdesc_out += f'\t\t\t\t\t</id-{entry_id}>\n'

    return powerdesc_out, magicitemsdesc_out

def props_format(props_in):
    props_out = ''
    id = 0

    # Split the input at each \n into a list of properties
    props_list = re.split(r'\\n', props_in)

    # Loop though properties list to create all the tags
    for p in props_list:
        id += 1
        entrry_id = str(id).rjust(3, '0')
        props_out += f'\t\t\t\t<id-{entrry_id}>\n'
        props_out += f'\t\t\t\t\t<shortdescription type="string">{p}</shortdescription>\n'
        props_out += f'\t\t\t\t</id-{entrry_id}>\n'

    return props_out
