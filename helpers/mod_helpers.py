import settings

import copy
import optparse
import os
import re
import shutil
import sys
from zipfile import ZipFile, ZIP_DEFLATED

def title_format(text_in):
    text_out = ''
    text_out = re.sub(r'[A-Za-z]+(\'[A-Za-z]+)?', lambda word: word.group(0).capitalize(), text_in)
    return text_out

def clean_formattedtext(text_in):
    text_out = text_in
    # assume that colons should be in-line
    text_out = re.sub('</p>\s*<p>\s*:', ':', text_out)
    # assume that italics should be in-line
    text_out = re.sub('</p>\s*<p><i>', '<i>', text_out)
    text_out = re.sub('</i></p>\s*<p>', '</i>', text_out)
    # turn <br/> into new <p> as line breaks inside <p> don't render in formattedtext
    text_out = re.sub(r'(\s*<br/>\s*)', r'</p><p>', text_out)
    # get rid of empty paragraphs
    text_out = re.sub('<p>\s*</p>', '', text_out)
    # get rid of mutliple linebreaks
    text_out = re.sub('\n+', '\n', text_out)
    # replace <th> with <td><b> as FG appear to not render <th> correctly
    text_out = re.sub(r'<th>', r'<td><b>', text_out)
    text_out = re.sub(r'</th>', r'</b></td>', text_out)
    # escape &
    text_out = re.sub(r'&', r'&amp;', text_out)

    return text_out

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
    parser.add_option('-t', '--tiers', action='store_true', dest='tiers', help='divide Magic Armor, Implements and Weapons, NPCs into Tiers')
    parser.add_option('-n', '--npcs', action='store_true', dest='npcs', help='export all NPCs (Monsters)')
    parser.add_option('-r', '--races', action='store_true', dest='races', help='export Races information')
    parser.add_option('-c', '--classes', action='store_true', dest='classes', help='export Classes information')
    parser.add_option('-f', '--feats', action='store_true', dest='feats', help='exports Feat information')
    parser.add_option('-p', '--powers', action='store_true', dest='powers', help='exports Power information')
    parser.add_option('-b', '--basic', action='store_true', dest='basic', help='include Basic Attacks in Power export')
    parser.add_option('-a', '--alchemy', action='store_true', dest='alchemy', help='exports Alchemical Item information')
    parser.add_option('-u', '--rituals', action='store_true', dest='rituals', help='exports Ritual information')
    parser.add_option('-m', '--martial', action='store_true', dest='martial', help='exports Martial Practice information')
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
    settings.filename = options.filename
    settings.library = options.library
    settings.min_lvl = int(options.min) if int(options.min) >= 0 else 0
    settings.max_lvl = int(options.max) if int(options.min) <= 99 else 99
    settings.tiers = options.tiers if options.tiers != None else False
    settings.npcs = options.npcs if options.npcs != None else False
    settings.races = options.races if options.races != None else False
    settings.classes = options.classes if options.classes != None else False
    settings.feats = options.feats if options.feats != None else False
    settings.powers = options.powers if options.powers != None else False
    settings.basic = options.basic if options.basic != None else False
    settings.alchemy = options.alchemy if options.alchemy != None else False
    settings.rituals = options.rituals if options.rituals != None else False
    settings.practices = options.martial if options.martial != None else False
    settings.items = options.items if options.items != None else False
    settings.mundane = options.mundane if options.mundane != None else False
    settings.magic = options.magic if options.magic != None else False

    # Note these are currently internal/debug options that are more granular than is currently offered by the switches
    settings.armor = False
    settings.equipment = False
    settings.weapons = False
    settings.mi_armor = False
    settings.mi_implements = False
    settings.mi_weapons = False
    settings.mi_alchemical = False
    settings.mi_alternative = False
    settings.mi_ammunition = False
    settings.mi_arms = False
    settings.mi_companion = False
    settings.mi_consumable = False
    settings.mi_familiar = False
    settings.mi_feet = False
    settings.mi_hands = False
    settings.mi_head = False
    settings.mi_head_neck = False
    settings.mi_mount = False
    settings.mi_neck = False
    settings.mi_ring = False
    settings.mi_waist = False
    settings.mi_wondrous = False

    # If --mundane is specified then set mundane items to True
    if options.mundane == True:
        settings.armor = True
        settings.equipment = True
        settings.weapons = True

    # If --magic  is specified then set magic items to True
    if options.magic == True:
        settings.tiers = True
        settings.mi_armor = True
        settings.mi_implements = True
        settings.mi_weapons = True
        settings.mi_alchemical = True
        settings.mi_alternative = True
        settings.mi_ammunition = True
        settings.mi_arms = True
        settings.mi_companion = True
        settings.mi_consumable = True
        settings.mi_familiar = True
        settings.mi_feet = True
        settings.mi_hands = True
        settings.mi_head = True
        settings.mi_head_neck = True
        settings.mi_mount = True
        settings.mi_neck = True
        settings.mi_ring = True
        settings.mi_waist = True
        settings.mi_wondrous = True

    # If --items is specified then set all items to True
    if options.items == True:
        settings.tiers = True
        settings.armor = True
        settings.equipment = True
        settings.weapons = True
        settings.mi_armor = True
        settings.mi_implements = True
        settings.mi_weapons = True
        settings.mi_alchemical = True
        settings.mi_alternative = True
        settings.mi_ammunition = True
        settings.mi_arms = True
        settings.mi_companion = True
        settings.mi_consumable = True
        settings.mi_familiar = True
        settings.mi_feet = True
        settings.mi_hands = True
        settings.mi_head = True
        settings.mi_head_neck = True
        settings.mi_mount = True
        settings.mi_neck = True
        settings.mi_ring = True
        settings.mi_waist = True
        settings.mi_wondrous = True
    return

def create_module(xml_in):

    # Use db.xml for DM only modules so they are not player readable
    if settings.npcs:
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
        with ZipFile(f'{settings.filename}.mod', 'w', compression=ZIP_DEFLATED) as modzip:
            modzip.write(db_filename)
            modzip.write('definition.xml')
            if os.path.isfile('thumbnail.png'):
                modzip.write('thumbnail.png')

        print(f'\n{settings.filename}.mod generated!')
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
            # Remove '(Level nn)' as the table already has a level column
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
        if entry_dict["cost"] != '':
            mi_out += (f'\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
        if entry_dict["critical"] != '':
            mi_out += (f'\t\t\t\t<critical type="string">{entry_dict["critical"]}</critical>\n')
        if entry_dict["enhancement"] != '':
            mi_out += (f'\t\t\t\t<enhancement type="string">{entry_dict["enhancement"]}</enhancement>\n')
        if entry_dict["flavor"] != '':
            mi_out += (f'\t\t\t\t<flavor type="string">{entry_dict["flavor"]}</flavor>\n')
        mi_out += (f'\t\t\t\t<formatteditemblock type="formattedtext">{entry_dict["flavor"]}</formatteditemblock>\n')
        mi_out += (f'\t\t\t\t<level type="number">{entry_dict["level"]}</level>\n')
        mi_out += (f'\t\t\t\t<mitype type="string">{entry_dict["mitype"]}</mitype>\n')
        if entry_dict["prerequisite"] != '':
            mi_out += (f'\t\t\t\t<prerequisite type="string">{entry_dict["prerequisite"]}</prerequisite>\n')
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
        # include line in the description unless it is used for the Action or Recharge
        desc_flag = True

        # Action
        # take only the first entry
        action_test = re.search(r'(Free Action|Free|Immediate Interrupt|Immediate Reaction|Minor Action|Minor|Move Action|Move|No Action|Standard Action|Standard)', line)
        if action_test and action_str == '':
            action_str = action_test.group(1)
            desc_flag = False

        # Recharge
        # take only the first entry
        recharge_test = re.search(r'(At-Will Attack|At-Will Utility|At-Will|Consumable|Daily Attack|Daily Utility|Daily|Encounter|Healing Surge)', line, re.IGNORECASE)
        if recharge_test and recharge_str == '':
            recharge_str = recharge_test.group(1).title()
            desc_flag = False

        # Range
        # take only the first entry as some multi-level items increase range with level
        range_test = re.search(r'(Area.*?|Close.*?|Ranged.*?)[;($\.]', line)
        if range_test and range_str == '':
           range_str = range_test.group(1).strip()

        # Keyword
        # exhaustive check to avoid false positives
        for kwd in keywords_list:
            if keywords_test := re.search(kwd, line):
                keywords_str += ', ' if keywords_str != '' else ''
                keywords_str += kwd

        # Description
        # Check for keywords that indicate a power description line
        shortdescription_test = re.search(r'(^As|^Attack:|Effect|Hit|Level|Make|Miss|Trigger|You)', line)
        # also include any line that isn't used for Action or Recharge
        if shortdescription_test or desc_flag:
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
    powers_list = []
    in_power = False

    # Find all tags that might contain powers information
    power_tags = soup_in.find_all(class_=['mihead', 'mistat', 'mistat indent', 'mistat indent1'])
    for tag in power_tags:
        # concatenate all the elements within each tag
        tag_str = ' '.join(map(str, tag.stripped_strings))
        if re.search(r'^(Attack Power|Power|Utility Power)', tag_str):
            # trigger that we have started the first power
            if in_power == False:
                in_power = True
            # else if one is already under construction then construct and add it to the power list
            else:
                power_item = power_construct(new_power)
                powers_list.append(copy.deepcopy(power_item))

            # either way we are starting a new power
            new_power = []
        if in_power:
            new_power.append(tag_str)
    # construct final power and add it to the power list
    if in_power:
        power_item = power_construct(new_power)
        powers_list.append(copy.deepcopy(power_item))

    # Loop though power list to create all the tags
    name_camel = re.sub('[^a-zA-Z0-9_]', '', name_in)
    powerdesc_out = ''
    mi_powerstag_out = ''
    id = 0

    for power in powers_list:
        id += 1
        recharge_alpha = re.sub('[^a-zA-Z0-9_]', '', power["recharge"])
        entry_id = str(id).rjust(2, '0')
        power_name = 'Power' if power["recharge"] == '' else 'Power - ' + power["recharge"]

        mi_powerstag_out += f'\t\t\t\t\t<id-{entry_id}>\n'
        mi_powerstag_out += f'\t\t\t\t\t\t<name type="string">{power_name}</name>\n'
        if power["action"] != '':
            mi_powerstag_out += f'\t\t\t\t\t\t<action type="string">{power["action"]}</action>\n'
        if power["recharge"] != '':
            mi_powerstag_out += f'\t\t\t\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["shortdescription"] != '':
            mi_powerstag_out += f'\t\t\t\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        mi_powerstag_out += '\t\t\t\t\t\t<link type="windowreference">\n'
        mi_powerstag_out += '\t\t\t\t\t\t\t<class>powerdesc</class>\n'
        mi_powerstag_out += f'\t\t\t\t\t\t\t<recordname>powerdesc.item{name_camel}Power-{entry_id}@{settings.library}</recordname>\n'
        mi_powerstag_out += '\t\t\t\t\t\t</link>\n'
        mi_powerstag_out += f'\t\t\t\t\t</id-{entry_id}>\n'

        powerdesc_out += f'\t\t<item{name_camel}Power-{entry_id}>\n'
        powerdesc_out += f'\t\t\t<name type="string">{name_in} {power_name}</name>\n'
        if power["action"] != '':
            powerdesc_out += f'\t\t\t<action type="string">{power["action"]}</action>\n'
        powerdesc_out += '\t\t\t<class type="string">Item</class>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t<description type="formattedtext">{power["shortdescription"]}</description>\n'
##        if power["shortdescription"] != '':
##            powerdesc_out += f'\t\t\t<effect type="formattedtext">{power["shortdescription"]}</effect>\n'
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
        powerdesc_out += f'\t\t</item{name_camel}Power-{entry_id}>\n'

    return powerdesc_out, mi_powerstag_out

def props_format(props_in):
    props_out = ''
    id = 0

    # Loop though properties list to create all the tags
    for p in props_in:
        if p.strip() == '':
            continue
        id += 1
        entrry_id = str(id).rjust(3, '0')
        props_out += f'\t\t\t\t<id-{entrry_id}>\n'
        props_out += f'\t\t\t\t\t<shortdescription type="string">{p}</shortdescription>\n'
        props_out += f'\t\t\t\t</id-{entrry_id}>\n'

    return props_out
