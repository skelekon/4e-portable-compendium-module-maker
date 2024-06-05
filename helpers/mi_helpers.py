import settings

import copy
import re

def mi_other_list():

    # This returns a list of all the different types of 'Other' Magic Items so that they can be iterated
    out_list = []
    mi_other_dict = {}

    mi_other_dict["arg"] = 'mi_alchemical'
    mi_other_dict["filter"] = 'Alchemical Item'
    mi_other_dict["literal"] = 'Alchemical Items'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_alternative'
    mi_other_dict["filter"] = 'Alternative Reward'
    mi_other_dict["literal"] = 'Alternative Rewards'
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
    mi_other_dict["literal"] = 'Companions'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_consumable'
    mi_other_dict["filter"] = 'Consumable'
    mi_other_dict["literal"] = 'Consumables'
    out_list.append(copy.deepcopy(mi_other_dict))

    mi_other_dict["arg"] = 'mi_familiar'
    mi_other_dict["filter"] = 'Familiar'
    mi_other_dict["literal"] = 'Familiars'
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
    mi_other_dict["literal"] = 'Mounts'
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
    mi_other_dict["literal"] = 'Wondrous Items'
    out_list.append(copy.deepcopy(mi_other_dict))

    return out_list

def mi_list_sorter(entry_in):
    name = entry_in["name"]
    return (name)

def create_mi_library(tier_list, name_in, item_in):
    xml_out = ''
    item_lower = re.sub('[^a-zA-Z0-9_]', '', item_in).lower()

    for t in tier_list:

        if t != '' and len(tier_list) > 1:
            tier_str = ' (' + t + ')'
            tier_lower = '_' + re.sub('[^a-zA-Z0-9_]', '', t).lower()
        else:
            tier_str = ''
            tier_lower = ''


        settings.lib_id += 1

        xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
        xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_classmagicitemtablelist</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>lists.magicitems_{item_lower}{tier_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</librarylink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{name_in}{tier_str}</name>\n')
        xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_mi_list(list_in, tier_list, item_in):
    xml_out = ''

    if not list_in:
        return xml_out

    item_lower = re.sub('[^a-zA-Z0-9_]', '', item_in).lower()

    # Loop through the Tier list that has been built for this export
    for t in tier_list:
        section_id = 0

        # Set up a label suffix for the current Tier
        if t != '' and len(tier_list) > 1:
            tier_str = ' (' + t + ')'
            tier_lower = '_' + re.sub('[^a-zA-Z0-9_]', '', t).lower()
        else:
            tier_str = ''
            tier_lower = ''


        # Open Item List
        # This controls the table that appears when you click on a Library menu
        xml_out += (f'\t\t<magicitems_{item_lower}{tier_lower}>\n')
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
            name_lower = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"]).lower()
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

                xml_out += (f'\t\t\t\t\t\t<mi{level_str}_{name_lower}>\n')
                xml_out += (f'\t\t\t\t\t\t\t<cat type="string">{entry_dict["cat"]}</cat>\n')
                xml_out += (f'\t\t\t\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
                xml_out += (f'\t\t\t\t\t\t\t<level type="number">{entry_dict["level"]}</level>\n')
                xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
                xml_out += ('\t\t\t\t\t\t\t\t<class>referencemagicitem</class>\n')
                xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.items.{name_lower}@{settings.library}</recordname>\n')
                xml_out += ('\t\t\t\t\t\t\t</link>\n')
                xml_out += (f'\t\t\t\t\t\t\t<name type="string">{name_display}</name>\n')
                xml_out += (f'\t\t\t\t\t\t</mi{level_str}_{name_lower}>\n')

        # Close last Section
        xml_out += ('\t\t\t\t\t</items>\n')
        xml_out += (f'\t\t\t\t</section{section_str}>\n')

        # Close Item List
        xml_out += ('\t\t\t</groups>\n')
        xml_out += (f'\t\t</magicitems_{item_lower}{tier_lower}>\n')

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


def create_mi_cards(list_in):
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
        name_lower = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"]).lower()

        # Create all Required Power entries
        power_out += entry_dict["powerdesc"]

        mi_out += (f'\t\t\t<{name_lower}>\n')
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
        mi_out += (f'\t\t\t\t<name type="string">{entry_dict["name"]}</name>\n')
        mi_out += (f'\t\t\t\t<mitype type="string">{entry_dict["mitype"]}</mitype>\n')
        if entry_dict["prerequisite"] != '':
            mi_out += (f'\t\t\t\t<prerequisite type="string">{entry_dict["prerequisite"]}</prerequisite>\n')
        if entry_dict["subclass"] != '':
            mi_out += (f'\t\t\t\t<subclass type="string">{entry_dict["subclass"]}</subclass>\n')
        if entry_dict["mipowers"] != '':
            mi_out += (f'\t\t\t\t<powers>\n{entry_dict["mipowers"]}\t\t\t\t</powers>\n')
        if entry_dict["props"] != '':
            mi_out += (f'\t\t\t\t<props>\n{entry_dict["props"]}\t\t\t\t</props>\n')
        else:
            mi_out += ('\t\t\t\t<props />\n')
        mi_out += (f'\t\t\t</{name_lower}>\n')

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
    name_lower = re.sub('[^a-zA-Z0-9_]', '', name_in).lower()
    powerdesc_out = ''
    mi_powerstag_out = ''
    pwr_id = 0

    for power in powers_list:
        pwr_id += 1
        recharge_alpha = re.sub('[^a-zA-Z0-9_]', '', power["recharge"])
        power_name = 'Power' if power["recharge"] == '' else 'Power - ' + power["recharge"]

        mi_powerstag_out += f'\t\t\t\t\t<id-{pwr_id:0>5}>\n'
        if power["action"] != '':
            mi_powerstag_out += f'\t\t\t\t\t\t<action type="string">{power["action"]}</action>\n'
        mi_powerstag_out += '\t\t\t\t\t\t<link type="windowreference">\n'
        mi_powerstag_out += '\t\t\t\t\t\t\t<class>powerdesc</class>\n'
        mi_powerstag_out += f'\t\t\t\t\t\t\t<recordname>reference.powers.{name_lower}_id-{pwr_id:0>5}@{settings.library}</recordname>\n'
        mi_powerstag_out += '\t\t\t\t\t\t</link>\n'
        mi_powerstag_out += f'\t\t\t\t\t\t<name type="string">{power_name}</name>\n'
        if power["recharge"] != '':
            mi_powerstag_out += f'\t\t\t\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["shortdescription"] != '':
            mi_powerstag_out += f'\t\t\t\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        mi_powerstag_out += f'\t\t\t\t\t</id-{pwr_id:0>5}>\n'

        powerdesc_out += f'\t\t\t<{name_lower}_id-{pwr_id:0>5}>\n'
        if power["action"] != '':
            powerdesc_out += f'\t\t\t\t<action type="string">{power["action"]}</action>\n'
        powerdesc_out += '\t\t\t\t<class type="string">Item</class>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t\t<description type="formattedtext">{power["shortdescription"]}</description>\n'
##        if power["shortdescription"] != '':
##            powerdesc_out += f'\t\t\t<effect type="formattedtext">{power["shortdescription"]}</effect>\n'
##        if power["shortdescription"] != '':
##            powerdesc_out += f'\t\t\t<flavor type="string">{power["shortdescription"]}</flavor>\n'
        if power["keywords"] != '':
            powerdesc_out += f'\t\t\t\t<keywords type="string">{power["keywords"]}</keywords>\n'
        powerdesc_out += '\t\t\t\t<level type="number">0</level>\n'
        powerdesc_out += f'\t\t\t\t<name type="string">{name_in} {power_name}</name>\n'
        if power["recharge"] != '':
            powerdesc_out += f'\t\t\t\t<recharge type="string">{power["recharge"]}</recharge>\n'
        if power["shortdescription"] != '':
            powerdesc_out += f'\t\t\t\t<shortdescription type="string">{power["shortdescription"]}</shortdescription>\n'
        powerdesc_out += f'\t\t\t\t<source type="string">Item</source>\n'
        powerdesc_out += '\t\t\t\t<type type="string">Item</type>\n'
        powerdesc_out += f'\t\t\t</{name_lower}_id-{pwr_id:0>5}>\n'

    return powerdesc_out, mi_powerstag_out


def props_format(props_in):
    props_out = ''
    prop_id = 0

    # Loop though properties list to create all the tags
    for prop in props_in:
        if prop.strip() == '':
            continue
        prop_id += 1
        props_out += f'\t\t\t\t\t<id-{prop_id:0>5}>\n'
        props_out += f'\t\t\t\t\t\t<shortdescription type="string">{prop}</shortdescription>\n'
        props_out += f'\t\t\t\t\t</id-{prop_id:0>5}>\n'

    return props_out
