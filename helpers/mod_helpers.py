import re
import copy
import optparse

def parse_argv(args_in):

    # Set up all the command line options and extract to 'options'
    parser = optparse.OptionParser()
    parser.set_defaults(filename='4E_Compendium', library='4E Compendium', min=0, max=99)
    parser.add_option('-f', '--filename', action='store', dest='filename', help='create library at FILE', metavar='FILE')
    parser.add_option('-l', '--library', action='store', dest='library', help='Fantasy Grounds\' internal name for the Library', metavar='LIBRARY')
    parser.add_option('--min', action='store', dest='min', help='only include magic items of this level and above')
    parser.add_option('--max', action='store', dest='max', help='only include magic items of this level and below')
    parser.add_option('-p', '--powers', action='store_true', dest='powers', help='outputs Power information')
    parser.add_option('-i', '--items', action='store_true', dest='items', help='include all item types (= --mundane & --magic)')
    parser.add_option('--mundane', action='store_true', dest='mundane', help='include all mundane items in the Library')
    parser.add_option('--magic', action='store_true', dest='magic', help='include all magic items in the Library')
    parser.add_option('-t', '--tiers', action='store_true', dest='tiers', help='divide Magic Armor, Implements and Weapons into Tiers (recommended)')
    parser.add_option('-a', '--all', action='store_true', dest='all', help='includes everything (WARNING very large library)')

    
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
    out_dict["min"] = int(options.min)
    out_dict["max"] = int(options.max)
    out_dict["powers"] = options.powers if options.powers != None else False
    out_dict["tiers"] = options.tiers if options.powers != None else False
    out_dict["items"] = options.items if options.items != None else False
    out_dict["mundane"] = options.mundane if options.mundane != None else False
    out_dict["magic"] = options.magic if options.magic != None else False

    # Note these options are more granular than is currently offered by the switches
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

    # If -all is specified then default all to True
    if options.all == True:
        out_dict["powers"] = True
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


def mi_other_list():
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

def write_definition(filepath_in, library_in):
    definition_str = (f'<?xml version="1.0" encoding="iso-8859-1"?>\n<root version="2.2">\n\t<name>{library_in}</name>\n\t<author>skelekon</author>\n\t<ruleset>4E</ruleset>\n</root>')

    with open(filepath_in, mode='w', encoding='UTF-8', errors='strict', buffering=1) as file:
        file.write(definition_str)
    return

def write_client(filepath_in, xml_in):
    with open(filepath_in, mode='w', encoding='UTF-8', errors='strict', buffering=1) as file:
        file.write(xml_in)

    return

def mi_list_sorter(entry_in):
    name = entry_in["name"]
    return (name)

def create_mi_library(id_in, tier_list, library_in, name_in, item_in):
    xml_out = ''
    for t in tier_list:

        if t != '':
            tier_str = ' (' + t + ')'
        else:
            tier_str = ''

        id_in += 1
        menu_str = 'a' + '0000'[0:len('0000')-len(str(id_in))] + str(id_in)

        xml_out += (f'\t\t\t\t<{menu_str}magicitems>\n')
        xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_classmagicitemtablelist</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>magicitemlists.core{item_in.lower()}{t.lower()}@{library_in}</recordname>\n')
        xml_out += ('\t\t\t\t\t</librarylink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{name_in}{tier_str}</name>\n')
        xml_out += (f'\t\t\t\t</{menu_str}magicitems>\n')

    return xml_out, id_in

def create_mi_table(list_in, tier_list, library_in, type_in):
    xml_out = ''

    if not list_in:
        return xml_out

    type_lower = re.sub('[^a-zA-Z0-9_]', '', type_in.lower())

    for t in tier_list:
        section_id = 0

        if t != '':
            tier_str = ' (' + t + ')'
        else:
            tier_str = ''

        # Item List part
        # This controls the table that appears when you click on a Library menu
        xml_out += (f'\t\t<core{type_lower}{t.lower()}>\n')
        xml_out += (f'\t\t\t<description type="string">Magic Item Table{tier_str}</description>\n')
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

            if item_tier == t:

                level_str = "000"[0:len("000")-len(str(entry_dict["level"]))] + str(entry_dict["level"])
                name_lower = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"].lower())
                #Check for new section
                if entry_dict["section_id"] != section_id:
                    section_id = entry_dict["section_id"]
                    if section_id != 1:
                        section_str = "000"[0:len("000")-len(str(section_id - 1))] + str(section_id - 1)
                        xml_out += ('\t\t\t\t\t</items>\n')
                        xml_out += (f'\t\t\t\t</section{section_str}>\n')
                    section_str = "000"[0:len("000")-len(str(section_id))] + str(section_id)
                    xml_out += (f'\t\t\t\t<section{section_str}>\n')
                    xml_out += (f'\t\t\t\t\t<description type="string">Armor</description>\n')
                    xml_out += ('\t\t\t\t\t<items>\n')

                xml_out += (f'\t\t\t\t\t\t<a{level_str}{name_lower}>\n')
                xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
                xml_out += ('\t\t\t\t\t\t\t\t<class>referencemagicitem</class>\n')
                xml_out += (f'\t\t\t\t\t\t\t\t<recordname>magicitemdesc.{name_lower}_{level_str}@{library_in}</recordname>\n')
                xml_out += ('\t\t\t\t\t\t\t</link>\n')
                xml_out += (f'\t\t\t\t\t\t\t<name type="string">{entry_dict["name"]} {entry_dict["bonus"]}</name>\n')
                xml_out += (f'\t\t\t\t\t\t\t<cat type="string">{entry_dict["cat"]}</cat>\n')
                xml_out += (f'\t\t\t\t\t\t\t<level type="number">{entry_dict["level"]}</level>\n')
                xml_out += (f'\t\t\t\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
                xml_out += (f'\t\t\t\t\t\t</a{level_str}{name_lower}>\n')

        # Close out the last section
        xml_out += ('\t\t\t\t\t</items>\n')
        xml_out += (f'\t\t\t\t</section{section_str}>\n')

        # Close out Item List part
        xml_out += ('\t\t\t</groups>\n')
        xml_out += (f'\t\t</core{type_lower}{t.lower()}>\n')

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
        level_str = "000"[0:len("000")-len(str(entry_dict["level"]))] + str(entry_dict["level"])
        name_lower = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"].lower())

        # Create all Required Power entries
        power_out += entry_dict["powerdesc"]

        mi_out += (f'\t\t<{name_lower}_{level_str}>\n')
        mi_out += (f'\t\t\t<name type="string">{entry_dict["name"]} {entry_dict["bonus"]}</name>\n')
        mi_out += (f'\t\t\t<class type="string">{entry_dict["class"]}</class>\n')
        if entry_dict["subclass"] != '':
            mi_out += (f'\t\t\t<subclass type="string">{entry_dict["subclass"]}</subclass>\n')
        mi_out += (f'\t\t\t<level type="number">{entry_dict["level"]}</level>\n')
        mi_out += (f'\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
        mi_out += (f'\t\t\t<bonus type="number">{entry_dict["bonus"]}</bonus>\n')
        mi_out += (f'\t\t\t<flavor type="string">{entry_dict["flavor"]}</flavor>\n')
        mi_out += (f'\t\t\t<enhancement type="string">{entry_dict["enhancement"]}</enhancement>\n')
        if entry_dict["critical"] != '':
            mi_out += (f'\t\t\t<critical type="string">{entry_dict["critical"]}</critical>\n')
        mi_out += (f'\t\t\t<powers>{entry_dict["mipowers"]}</powers>\n')
        mi_out += (f'\t\t\t<props>{entry_dict["props"]}</props>\n')
        mi_out += (f'\t\t\t<formatteditemblock type="formattedtext">{entry_dict["flavor"]}\n\t\t\t\t</formatteditemblock>\n')
        mi_out += (f'\t\t\t<mitype type="string">{entry_dict["mitype"]}</mitype>\n')
        mi_out += (f'\t\t</{name_lower}_{level_str}>\n')

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
        recharge_test = re.search(r'(At-will Attack|At-Will Attack|At-will Utillity|At-Will Utility|At-will|At-Will|Consumable|Daily Attack|Daily Utility|Daily|Encounter|Healing Surge)', line)
        if recharge_test != None:
            recharge_str = recharge_test.group(1)

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

def powers_format(soup_in, name_in, library_in):
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
    magicitemsdesc_out = '\n'
    for power in powers_list:
        id += 1
        recharge_alpha = re.sub('[^a-zA-Z0-9_]', '', power["recharge"])
        entry_id = "000"[0:len("000")-len(str(id))] + str(id)

        powerdesc_out += f'\t\t<item{name_alpha}Power-{entry_id}>\n'
        powerdesc_out += f'\t\t\t<name type="string">{name_in} Power - {power["recharge"]}</name>\n'
        if power["recharge"] != '':
            powerdesc_out += f'\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["keywords"] != '':
            powerdesc_out += f'\t\t\t<keywords type="string">{power["keywords"]}</keywords>\n'
        if power["action"] != '':
            powerdesc_out += f'\t\t\t<action type="string">{power["action"]}</action>\n'
        powerdesc_out += f'\t\t\t<source type="string">Item</source>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t<description type="formattedtext">{power["shortdescription"]}</description>\n'
            powerdesc_out += f'\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        powerdesc_out += '\t\t\t<class type="string">Item</class>\n'
        powerdesc_out += '\t\t\t<level type="number">0</level>\n'
        powerdesc_out += '\t\t\t<type type="string">Item</type>\n'
##        if power["shortdescription"] != '':
##            powerdesc_out += f'\t\t\t<flavor type="string">{power["shortdescription"]}</flavor>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t<effect type="formattedtext">{power["shortdescription"]}</effect>\n'
        powerdesc_out += f'\t\t</item{name_alpha}Power-{entry_id}>\n'

        magicitemsdesc_out += f'\t\t\t\t<id-{entry_id}>\n'
        magicitemsdesc_out += f'\t\t\t\t\t<name type="string">Power - {power["recharge"]}</name>\n'
        if power["recharge"] != '':
            magicitemsdesc_out += f'\t\t\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["action"] != '':
            magicitemsdesc_out += f'\t\t\t\t\t<action type="string">{power["action"]}</action>\n'
        if power["shortdescription"] != '':
            magicitemsdesc_out += f'\t\t\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        magicitemsdesc_out += '\t\t\t\t\t<link type="windowreference">\n'
        magicitemsdesc_out += '\t\t\t\t\t\t<class>powerdesc</class>\n'
        magicitemsdesc_out += f'\t\t\t\t\t\t<recordname>powerdesc.item{name_alpha}Power-{entry_id}@{library_in}</recordname>\n'
        magicitemsdesc_out += '\t\t\t\t\t</link>\n'
        magicitemsdesc_out += f'\t\t\t\t</id-{entry_id}>\n'

    magicitemsdesc_out += '\t\t\t'

    return re.sub('^\s*$', '', powerdesc_out), re.sub('^\s*$', '', magicitemsdesc_out)

def props_format(props_in):
    id = 0

    # Split the input at each \n into a list of properties
    props_list = re.split(r'\\n', props_in)

    # Loop though properties list to create all the tags
    props_out = '\n'
    for p in props_list:
        id += 1
        entrry_id = "00000"[0:len("00000")-len(str(id))] + str(id)
        props_out += f'\t\t\t\t<id-{entrry_id}>\n'
        props_out += f'\t\t\t\t\t<shortdescription type="string">{p}</shortdescription>\n'
        props_out += f'\t\t\t\t</id-{entrry_id}>\n'
    props_out += '\t\t\t'

    return re.sub('^\s*$', '', props_out)
