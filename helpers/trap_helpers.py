import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

# this allows for variable sorting by overwriting the GroupID value
def trap_list_sorter(entry_in):
    group_id = entry_in["group_id"]
    name = entry_in["name"]

    return (group_id, name)


# This creates the top-level menus when you select a Module
def create_trap_library(tier_list, name_in):
    xml_out = ''
    class_lower = re.sub('[^a-zA-Z0-9_]', '', name_in).lower()

    for t in tier_list:

        if t != '' and len(tier_list) > 1:
            tier_str = ' (' + t + ')'
        else:
            tier_str = ''

        tier_lower = re.sub('[^a-zA-Z0-9_]', '', t).lower()

        settings.lib_id += 1

        xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
        xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_classmonsterlist</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>lists.traps.{class_lower}_{tier_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</librarylink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{name_in}{tier_str}</name>\n')
        xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


# This controls the table that appears when you click on a Library menu
def create_trap_list(list_in, tier_list, name_in):
    xml_out = ''

    if not list_in:
        return xml_out

    class_lower = re.sub('[^a-zA-Z0-9_]', '', name_in).lower()

    # Populate the sort order and sub-heading fields according to which table is being built
    if re.search(r'Traps By Letter', name_in):
        for trap_dict in list_in:
            trap_dict["group_id"] = re.sub('[^a-zA-Z0-9_]', '', trap_dict["name"])[0:1].lower()
            trap_dict["group_str"] = re.sub('[^a-zA-Z0-9_]', '', trap_dict["name"])[0:1].upper()
    elif re.search(r'Traps By Level( |$)', name_in):
        for trap_dict in list_in:
            # Generate Level values
            level_str = re.sub('[^0-9]', '', trap_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            level_id = level_str.rjust(2, '0')

            trap_dict["group_id"] = level_id
            trap_dict["group_str"] = 'Level ' + level_str
    elif re.search(r'Traps By Level/Role', name_in):
        for trap_dict in list_in:
            # Generate Level values
            level_str = re.sub('[^0-9]', '', trap_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            level_id = level_str.rjust(2, '0')

            trap_dict["group_id"] =  level_id + re.sub('[^a-zA-Z0-9_]', '', trap_dict["levelrole"])
            trap_dict["group_str"] = trap_dict["levelrole"]
    elif re.search(r'Traps By Role/Level', name_in):
        for trap_dict in list_in:
            # Generate Level values
            level_str = re.sub('[^0-9]', '', trap_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            level_id = level_str.rjust(2, '0')

            # Generate Role/Modifier/Leader values
            role_str = ''
            modifier_str = ''
            leader_str = ''
            # Leader in this list is the PC type not the (Leader) NPC subtype
            if role_match:= re.search(r'(Artillery|Brute|Controller|Lurker|Skirmisher|Soldier|Conjured|Defender|Leader$|Striker)', trap_dict["levelrole"], re.IGNORECASE):
                role_str = role_match.group(1).title()
            if modifier_match:= re.search(r'(Minion|Elite|Solo)', trap_dict["levelrole"], re.IGNORECASE):
                modifier_str = modifier_match.group(1).title()
            if leader_match:= re.search(r'(\(Leader\))', trap_dict["levelrole"], re.IGNORECASE):
                leader_str = leader_match.group(1).title()

            role_id = re.sub('[^a-zA-Z0-9_]', '', role_str)[0:3]
            modifier_id = re.sub('[^a-zA-Z0-9_]', '', modifier_str)[0:3].ljust(3, '-')
            leader_id = re.sub('[^a-zA-Z0-9_]', '', leader_str)[0:3].ljust(3, '-')

            trap_dict["group_id"] =  role_id + level_id + modifier_id + leader_id
            trap_dict["group_str"] = (role_str + ' Level ' + level_str + ' ' + modifier_str + ' ' + leader_str).strip()

    # Loop through the Tier list that has been built for this export
    for t in tier_list:
        section_id = 0

        # Set up a label suffix for the current Tier
        if t != '' and len(tier_list) > 1:
            tier_str = ' (' + t + ')'
        else:
            tier_str = ''

        tier_lower = re.sub('[^a-zA-Z0-9_]', '', t).lower()

        previous_group = ''

        # Trap List

        # Open new Class (new Table)
        xml_out += (f'\t\t\t<{class_lower}_{tier_lower}>\n')
        xml_out += (f'\t\t\t\t<description type="string">{name_in}{tier_str}</description>\n')
        xml_out += ('\t\t\t\t<groups>\n')
        group_flag = False

        # Create individual item entries
        for trap_dict in sorted(list_in, key=trap_list_sorter):

            # only process Items for the current Tier
            level_str = re.sub('[^0-9]', '', trap_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            if t == '':
                trap_tier = ''
            elif int(level_str) <= 10:
                trap_tier = 'Heroic'
            elif int(level_str) <= 20:
                trap_tier = 'Paragon'
            else:
                trap_tier = 'Epic'

            # only output items for the correct tier
            if trap_tier == t:
                group_flag = True

                # format name to be link target
                name_lower = re.sub('[^a-zA-Z0-9_]', '', trap_dict["name"]).lower()

                # Check for new Group
                if trap_dict["group_id"] != previous_group:

                    # Close previous Group
                    if previous_group != '':
                        xml_out += ('\t\t\t\t\t\t</monsters>\n')
                        xml_out += (f'\t\t\t\t\t</traps_{previous_group}>\n')

                    # Open new Group
                    xml_out += (f'\t\t\t\t\t<traps_{trap_dict["group_id"]}>\n')
                    xml_out += (f'\t\t\t\t\t\t<description type="string">{trap_dict["group_str"]}</description>\n')
                    xml_out += ('\t\t\t\t\t\t<monsters>\n')

                # Trap list entry
                xml_out += (f'\t\t\t\t\t\t\t<{name_lower}_{trap_dict["trap_id"]:0>3}>\n')
                xml_out += ('\t\t\t\t\t\t\t\t<link type="windowreference">\n')
                xml_out += ('\t\t\t\t\t\t\t\t\t<class>npc</class>\n')
                xml_out += (f'\t\t\t\t\t\t\t\t\t<recordname>reference.npcs.{name_lower}_{trap_dict["trap_id"]:0>3}@{settings.library}</recordname>\n')
                xml_out += ('\t\t\t\t\t\t\t\t</link>\n')
                xml_out += (f'\t\t\t\t\t\t\t\t\t<name>{trap_dict["name"]}</name>\n')
                xml_out += (f'\t\t\t\t\t\t\t</{name_lower}_{trap_dict["trap_id"]:0>3}>\n')

                previous_group = trap_dict["group_id"]

        # Close final Group if there was at least one entry
        if group_flag:
            xml_out += ('\t\t\t\t\t\t</monsters>\n')
            xml_out += (f'\t\t\t\t\t</traps_{previous_group}>\n')

        # Close final Class
        xml_out += ('\t\t\t\t</groups>\n')
        xml_out += (f'\t\t\t</{class_lower}_{tier_lower}>\n')

    return xml_out


def create_trap_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Reset the sort order so they are written in Name order
    for trap_dict in list_in:
        trap_dict["group_id"] = ''
        trap_dict["group_str"] = ''

    # Create individual item entries
    for trap_dict in sorted(list_in, key=trap_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', trap_dict["name"]).lower()

        xml_out += (f'\t\t\t<{name_lower}_{trap_dict["trap_id"]:0>3}>\n')
        xml_out += (f'\t\t\t\t<xp type="number">{trap_dict["xp"]}</xp>\n')
        if trap_dict["ac"] != '':
            xml_out += (f'\t\t\t\t<ac type="number">{trap_dict["ac"]}</ac>\n')
        else:
            xml_out += ('\t\t\t\t<ac type="number">0</ac>\n')
        if trap_dict["counters"] != '':
            xml_out += (f'\t\t\t\t<countermeasures>\n{trap_dict["counters"]}\t\t\t\t</countermeasures>\n')
        else:
            xml_out += ('\t\t\t\t<countermeasures />\n')
        if trap_dict["detect"] != '':
            xml_out += (f'\t\t\t\t<detect type="string">{trap_dict["detect"]}</detect>\n')
        if trap_dict["flavor"] != '':
            xml_out += (f'\t\t\t\t<flavor type="string">{trap_dict["flavor"]}</flavor>\n')
        if trap_dict["fortitude"] != '':
            xml_out += (f'\t\t\t\t<fortitude type="number">{trap_dict["fortitude"]}</fortitude>\n')
        else:
            xml_out += ('\t\t\t\t<fortitude type="number">0</fortitude>\n')
        if trap_dict["hp"] != '':
            xml_out += (f'\t\t\t\t<hp type="string">{trap_dict["hp"]}</hp>\n')
        if trap_dict["init"] != '':
            xml_out += (f'\t\t\t\t<init type="number">{trap_dict["init"]}</init>\n')
        else:
            xml_out += ('\t\t\t\t<init type="number">0</init>\n')
        xml_out += (f'\t\t\t\t<levelrole type="string">{trap_dict["levelrole"]}</levelrole>\n')
        xml_out += (f'\t\t\t\t<name type="string">{trap_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t<npctype type="string">Trap</npctype>\n')
        if trap_dict["powers"] != '':
            xml_out += (f'\t\t\t\t<powers>\n{trap_dict["powers"]}\t\t\t\t</powers>\n')
        else:
            xml_out += ('\t\t\t\t<powers />\n')
        if trap_dict["reflex"] != '':
            xml_out += (f'\t\t\t\t<reflex type="number">{trap_dict["reflex"]}</reflex>\n')
        else:
            xml_out += ('\t\t\t\t<reflex type="number">0</reflex>\n')
        if trap_dict["speed"] != '':
            xml_out += (f'\t\t\t\t<speed type="string">{trap_dict["speed"]}</speed>\n')
        if trap_dict["specialdefenses"] != '':
            xml_out += (f'\t\t\t\t<specialdefenses type="string">{trap_dict["specialdefenses"]}</specialdefenses>\n')
        if trap_dict["published"] != '':
            xml_out += (f'\t\t\t\t<text type="formattedtext">{trap_dict["published"]}</text>\n')
        if trap_dict["trapdesc"] != '':
            xml_out += (f'\t\t\t\t<trapdesc type="string">{trap_dict["trapdesc"]}</trapdesc>\n')
        if trap_dict["trapskills"] != '':
            xml_out += (f'\t\t\t\t<trapskills>\n{trap_dict["trapskills"]}\t\t\t\t</trapskills>\n')
        else:
            xml_out += ('\t\t\t\t<trapskills />\n')
        xml_out += (f'\t\t\t\t<type type="string">{trap_dict["type"]}</type>\n')
        xml_out += (f'\t\t\t</{name_lower}_{trap_dict["trap_id"]:0>3}>\n')

    return xml_out


def format_counter(soup_in, id_in):
    counter_out = ''
    
    text_str = (''.join(soup_in.find('p').text)).strip()

    counter_out += f'\t\t\t\t\t<id-{id_in:0>5}>\n'
    counter_out += f'\t\t\t\t\t\t<text type="string">{text_str}</text>\n'
    counter_out += f'\t\t\t\t\t</id-{id_in:0>5}>\n'

    return counter_out


def format_old_power(soup_in, id_in):
    power_out = ''
    
    # Initialize variables that are per-power entry
    action_str = ''
    flavor_str = ''
    keywords_str = ''
    pwrname_str = ''
    range_str = ''
    shortdescription_str = ''

    # Copy the components into separate tags so we can interate them without running into the next tag
    title_tag = copy.copy(soup_in.find('span', class_='trapblocktitle'))
    body_tags = copy.copy(soup_in.find_all('span', class_='trapblockbody'))

    # Power Name - anything before a bullet in the title
    pwrname_str = re.sub(r'[*•✦].*$', '', title_tag.text).strip()

    # Keywords - anything after a bullet in the title
    if keywords_match := re.search(r'[*•✦](.*$)', title_tag.text):
        keywords_str = keywords_match.group(1).strip()

    # Action
    for bdy_tag in body_tags:
        for tag in bdy_tag:
            if re.search(r'^(Free Action|Immediate Interrupt|Immediate Reaction|Minor|Move Action|Opportunity Action|Standard Action)(\s|$)', tag.text) != None:
                action_str = tag.text
                tag.decompose()

    # Short Description
    # turn the html into a text string
    shortdescription_str = '\\n'.join(map(str, body_tags))
    # replace line breaks with newlines
    shortdescription_str = re.sub(r'<br/>', r'\\n', shortdescription_str)
    # remove other tags
    shortdescription_str = re.sub(r'<.*?>', '', shortdescription_str)
    shortdescription_str = re.sub(r'(^\s*[\\n]*|[\\n]*$)', '', shortdescription_str)

    # Put Triggered Actions back into the Attack line
    if re.search(r'Attack:', shortdescription_str) != None and action_str.strip() in ['Immediate Interrupt', 'Immediate Reaction', 'Opportunity Action']:
        shortdescription_str = re.sub('Attack:', 'Attack (' + action_str + '):', shortdescription_str)
        action_str  = 'Triggered'

    # Range - split out any Ranges or Sizes
    # regex has become too complicated, so build it up piecewise
    range_pattern = '(.*?)'
    range_pattern += '('
    range_pattern += 'Area burst\s+([0-9]+ within [0-9]+|[0-9]+)'
    range_pattern += '|Close blast\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|Close burst\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|Melee reach\s+([0-9]+)'
    range_pattern += '|Melee [0-9]+ or Ranged\s+([0-9]+)'
    range_pattern += '|Melee or Ranged reach\s+([0-9]+)'
    range_pattern += '|Melee\s+([0-9]+|touch|)'
    range_pattern += '|Ranged\s+([0-9]+/[0-9]+|[0-9]+|sight)'
    range_pattern += '|Reach\s+([0-9]+)'
    range_pattern += ')'
    range_pattern += '(\s+\(.*?\)|)'
    range_pattern += '(.*?)$'
    if range_match := re.search(range_pattern,  shortdescription_str):
        range_str = re.sub(r';', '', range_match.group(2)).strip() + range_match.group(12)
        # remove leading semi-colons or newlines
        shortdescription_str = re.sub(r'^(;|\\n|)*', '', range_match.group(1).strip() + range_match.group(13).strip())
        # remove empty clauses caused by extracting Range
        shortdescription_str = re.sub(r':\s*;', ':', shortdescription_str)

    # Format the list of powers into statblocks
    power_out += f'\t\t\t\t\t<id-{id_in:0>5}>\n'
    if action_str != '':
        power_out += f'\t\t\t\t\t\t<action type="string">{action_str}</action>\n'
    if keywords_str != '':
        power_out += f'\t\t\t\t\t\t<keywords type="string">{keywords_str}</keywords>\n'
    power_out += '\t\t\t\t\t\t<link type="windowreference">\n'
    power_out += '\t\t\t\t\t\t\t<class>reference_power_custom</class>\n'
    power_out += '\t\t\t\t\t\t\t<recordname />\n'
    power_out += '\t\t\t\t\t\t</link>\n'
    power_out += f'\t\t\t\t\t\t<name type="string">{pwrname_str}</name>\n'
    if range_str != '':
        power_out += f'\t\t\t\t\t\t<range type="string">{range_str}</range>\n'
    if shortdescription_str != '':
        power_out += f'\t\t\t\t\t\t<shortdescription type="string">{shortdescription_str}</shortdescription>\n'
    power_out += f'\t\t\t\t\t</id-{id_in:0>5}>\n'

    return power_out


def format_new_power(soup_in, id_in):
    power_out = ''
#    print(soup_in)
    
    # Initialize variables that are per-power entry
    action_str = ''
    icon_str = ''
    flavor_str = ''
    keywords_str = ''
    powertype_str = ''
    pwrname_str = ''
    range_str = ''
    recharge_str = ''
    shortdescription_str = ''

    # Copy the components into separate tags so we can interate them without running into the next tag
    action_tag = copy.copy(soup_in.find('h2'))
    header_tag = copy.copy(soup_in.select_one('p', class_='th2'))
    body_tags = copy.copy(soup_in.find_all('p', class_=['thStat', 'tbod']))

    # Power Name - first element in bold tags
    if pwrname_tag := soup_in.find('b'):
        pwrname_str = pwrname_tag.text.replace('&', '&amp;')

    # Powertype - look for Power glyphs
    if powertype_img := soup_in.find_all('img'):
        for img in powertype_img:
            if 'images/symbol/S2.gif' in str(img):
                powertype_str += 'm'
            if 'images/symbol/Z2a.gif' in str(img):
                powertype_str += 'M'
            if 'images/symbol/S3.gif' in str(img):
                powertype_str += 'r'
            if 'images/symbol/Z3a.gif' in str(img):
                powertype_str += 'R'
            if 'images/symbol/Z1.gif' in str(img):
                powertype_str += 'c'
            if 'images/symbol/Z1a.gif' in str(img):
                powertype_str += 'C'
            if 'images/symbol/Z4a.gif' in str(img):
                powertype_str += 'A'
            if 'images/symbol/aura.png' in str(img):
                powertype_str += 'Z'

        if powertype_str == 'mM':
            powertype_str = 'm'

    # Action - should be in the first (action) tag
    if action_tag:
        if action_match := re.search(r'(Aura|Free|Immediate|Minor Action|Move Action|Opportunity|Standard Action|Trait|Triggered)', action_tag.text, re.IGNORECASE):
            action_str = action_match.group(1)

    # Keywords - anything in parentheses in the header tag
    if keywords_match := re.search(r'\((.*)\)', header_tag.text):
        keywords_str = keywords_match.group(1)

    # Recharge - any text after the star glyph in the header tag
    # first look for descriptive Recharge
    if recharge_img := header_tag.find('img', src=re.compile(r'/x.gif')):
        for rech_tag in recharge_img.find_all_next(text=True):
            recharge_str += rech_tag.text

    # then look for die symbols, starting from the lowest
    if recharge_img := header_tag.find('img', src=re.compile(r'/2a.gif')):
        recharge_str = 'Recharge 2-6'
    elif recharge_img := header_tag.find('img', src=re.compile(r'/3a.gif')):
        recharge_str = 'Recharge 3-6'
    elif recharge_img := header_tag.find('img', src=re.compile(r'/4a.gif')):
        recharge_str = 'Recharge 4-6'
    elif recharge_img := header_tag.find('img', src=re.compile(r'/5a.gif')):
        recharge_str = 'Recharge 5-6'
    elif recharge_img := header_tag.find('img', src=re.compile(r'/6a.gif')):
        recharge_str = 'Recharge 6'

    # If Recharge is 'Aura', change that to the Action type so that it goes under an 'Auras' heading
    # set the range to be all the text after the Aura keyword, as it's most commonly just the aura size
    if aura_match := re.search('(\s*Aura\s*)(.*)', recharge_str, re.IGNORECASE):
        action_str = 'Aura'
        range_str = aura_match.group(2)
        recharge_str = ''

    # Short Description - concatenate everything in the body tags
    for bdy_tag in body_tags:
        shortdescription_str += ' '.join(bdy_tag.stripped_strings) + '\\n'
    shortdescription_str = re.sub(r'(^;*\s*|\\n$)', '', shortdescription_str)

#    # Triggered Action - split out Immediate and Opportunity actions
#    if action_str == 'Triggered Action':
#        if trigger_match := re.search(r'^(.*?)(Immediate Interrupt|Immediate Reaction|Opportunity Action)(.*?)$', shortdescription_str):
#            action_str = trigger_match.group(2)
#            shortdescription_str = re.sub(r'(^\\n|\(\))*', '', trigger_match.group(1).strip() + trigger_match.group(3).strip())

    # Range - split out any Ranges or Sizes
    # regex has become too complicated, so build it up piecewise
    range_pattern = '(.*?)'
    range_pattern += '('
    range_pattern += 'Area burst\s+([0-9]+ within [0-9]+|[0-9]+)'
    range_pattern += '|Close blast\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|Close burst\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|Melee reach\s+([0-9]+)'
    range_pattern += '|Melee [0-9]+ or Ranged\s+([0-9]+)'
    range_pattern += '|Melee or Ranged reach\s+([0-9]+)'
    range_pattern += '|Melee\s+([0-9]+|touch|)'
    range_pattern += '|Ranged\s+([0-9]+|sight)'
    range_pattern += '|Reach\s+([0-9]+)'
    range_pattern += ')'
    range_pattern += '(\s+\(.*?\)|)'
    range_pattern += '(.*?)$'
    if range_match := re.search(range_pattern,  shortdescription_str):
        range_str = re.sub(r';', '', range_match.group(2)).strip() + range_match.group(12)
        # remove leading semi-colons or newlines
        shortdescription_str = re.sub(r'^(;|\\n|)*', '', range_match.group(1).strip() + range_match.group(13).strip())
        # remove empty clauses caused by extracting Range
        shortdescription_str = re.sub(r':\s*;', ':', shortdescription_str)

    # Format the list of powers into statblocks
    power_out += f'\t\t\t\t\t<id-{id_in:0>5}>\n'
    if action_str != '':
        power_out += f'\t\t\t\t\t\t<action type="string">{action_str}</action>\n'
    if icon_str != '':
        power_out += f'\t\t\t\t\t\t<icon type="string">{icon_str}</icon>\n'
    if keywords_str != '':
        power_out += f'\t\t\t\t\t\t<keywords type="string">{keywords_str}</keywords>\n'
    power_out += '\t\t\t\t\t\t<link type="windowreference">\n'
    power_out += '\t\t\t\t\t\t\t<class>reference_power_custom</class>\n'
    power_out += '\t\t\t\t\t\t\t<recordname />\n'
    power_out += '\t\t\t\t\t\t</link>\n'
    power_out += f'\t\t\t\t\t\t<name type="string">{pwrname_str}</name>\n'
    if powertype_str != '':
        power_out += f'\t\t\t\t\t\t<powertype type="string">{powertype_str}</powertype>\n'
    if range_str != '':
        power_out += f'\t\t\t\t\t\t<range type="string">{range_str}</range>\n'
    if recharge_str != '':
        power_out += f'\t\t\t\t\t\t<recharge type="string">{recharge_str}</recharge>\n'
    if shortdescription_str != '':
        power_out += f'\t\t\t\t\t\t<shortdescription type="string">{shortdescription_str}</shortdescription>\n'
    power_out += f'\t\t\t\t\t</id-{id_in:0>5}>\n'

    return power_out


def extract_trap_db(db_in):
    trap_out = []
    trap_id = 0

    print('\n\n\n=========== TRAPS ===========')

    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features='html.parser')

        # Retrieve the data with dedicated columns
        name_str = row["Name"].replace('\\', '')
        level_str = row["Level"].replace('\\', '')
        role_str = row["Role"].replace('\\', '')
        class_str = row["Class"].replace('\\', '')

#        if name_str not in ['Abyssal Breach', 'Animated Rapier', 'Abyssal Portal', 'Altar of Pazuzu', 'Ash Tree', 'Astral Lodestone', 'Far Realm Anomaly', 'False-Floor Pit', 'Animated Crossbow']:
#            continue
#        print('\n' + name_str)

        ac_str = ''
        counters_str = ''
        detect_str = ''
        flavor_str = ''
        fortitude_str = ''
        hp_str = ''
        init_str = ''
        levelrole_str = ''
        powers_str = ''
        published_str = ''
        reflex_str = ''
        speed_str = ''
        specialdefenses_str = ''
        trapdesc_str = ''
        trapskills_str = ''
        type_str = ''
        xp_str = ''

        # Published In
        published_tag = parsed_html.find(class_='publishedIn').extract()
        if published_tag:
            # remove p classnames
            del published_tag['class']
            # remove the a tags
            anchor_tag = published_tag.find('a')
            while anchor_tag:
                anchor_tag.replaceWithChildren()
                anchor_tag = published_tag.find('a')
            published_str = published_tag

        #####################################################################
        # OLD LAYOUT: Flavor / Perception / Trigger / Attack / Countermeasure
        #####################################################################

        # Level-Role
        level_tag = parsed_html.find('span', class_='level')
        if level_tag:
            levelrole_str = str(level_tag.next).strip()

        old_layout = False
        if levelrole_str != '':
            old_layout = True

        # Flavor
        if flavor_lbl := parsed_html.find('p', class_='flavor'):
            flavor_str = re.sub('\s\s', ' ', flavor_lbl.get_text(separator = '\\n', strip = True))

        # Type
        type_tag = parsed_html.find('span', class_='type')
        if type_tag:
            type_str = re.sub(r'\s+', ' ', type_tag.text)

        # XP
        xp_tag = parsed_html.find('span', class_='xp')
        if xp_tag:
            xp_str = str(xp_tag.next[3:])

        # Restructure the contents into a flat list of <span> tags for ease of processing
        trap_html = BeautifulSoup('', features='html.parser')
        for span_tag in parsed_html.find_all('span', class_=['traplead', 'trapblocktitle', 'trapblockbody']):
            trap_html.append(span_tag)

        # Loop through the useful_html and grab all the single occurrence fields
        current_section = ''
        previous_section = ''
        node_str = ''
        trapskills_id = 0
        node_id = 0
        counter_id = 0

        for trap_tag in trap_html:
            trap_class = trap_tag.get('class')[0]
            for tag in trap_tag:
                if tag.name in ['br', 'img'] or tag.text.strip() == '':
                    continue

                # Set which overall section we are currently in. Need to detect Attack sections to prevent them being processed until later.
                if trap_class == 'trapblocktitle':
                    if re.search(r'^(Arcana|Diplomacy|Dungeoneering|Endurance|History|Insight|Nature|Perception|Religion|Move Action|Special|Trigger|Countermeasures|.*Attack)', tag.text) != None:
                        current_section = tag.text
                else:
                    if re.search(r'^(Hazard|Trap)', tag.text) != None:
                        trapdesc_str = tag.next_sibling.text.strip()
                        current_section = ''
                    elif re.search(r'^Initiative', tag.text) != None:
                        if tag.next_sibling != None:
                            init_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                        else:
                            init_str = re.sub('[^0-9]', '', tag.text)
                        current_section = ''
                    elif re.search(r'^Speed', tag.text) != None:
                        speed_str = tag.next_sibling.text.strip()
                        current_section = ''

                    # Look for Skills & Countermeasures
                    if re.search(r'^(Arcana|Diplomacy|Dungeoneering|Endurance|History|Insight|Nature|Perception|Religion|Move Action|Special|Trigger)', current_section) != None:
                        # Beginning of new skill
                        if current_section != previous_section:
                            # Complete previous skill if already in one
                            if previous_section != '':
                                trapskills_str += node_str
                                trapskills_str += f'\t\t\t\t\t\t</nodes>\n'
                                trapskills_str += f'\t\t\t\t\t</id-{trapskills_id:0>5}>\n'
                                node_str = ''
                                node_id = 0

                            trapskills_id += 1
                            skill_lower = re.sub('[^a-zA-Z0-9_]', '', current_section)
                            trapskills_str += f'\t\t\t\t\t<id-{trapskills_id:0>5}>\n'
                            trapskills_str += f'\t\t\t\t\t\t<name type="string">{current_section}</name>\n'
                            trapskills_str += f'\t\t\t\t\t\t<nodes>\n'

                        node_id += 1
                        text_str = tag.text.strip()
                        # Split out the DC if found
                        if dc_match := re.search(r'DC ([0-9]+)[: ]*(.*)', text_str):
                            dc_str = dc_match.group(1)
                            text_str = dc_match.group(2)
                        else:
                            dc_str = '0'

                        node_str += f'\t\t\t\t\t\t\t<id-{node_id:0>5}>\n'
                        node_str += f'\t\t\t\t\t\t\t\t<dc type="number">{dc_str}</dc>\n'
                        node_str += f'\t\t\t\t\t\t\t\t<text type="string">{text_str}</text>\n'
                        node_str += f'\t\t\t\t\t\t\t</id-{node_id:0>5}>\n'
                        previous_section = current_section

                    elif title_match := re.search(r'^Countermeasures', current_section):
                        counter_id += 1
                        counters_str += f'\t\t\t\t\t<id-{counter_id:0>5}>\n'
                        counters_str += f'\t\t\t\t\t\t<text type="string">{tag.text.strip()}</text>\n'
                        counters_str += f'\t\t\t\t\t</id-{counter_id:0>5}>\n'

                        # Look for HP & Defenses in Countermeasures text
                        if defense_match := re.search(r'(\(.*?AC [0-9]+.*(hit points|hp).*?\))', tag.text):
                            if ac_match := re.search(r'AC ([0-9]*)', defense_match.group(1)):
                                ac_str = ac_match.group(1)
                            if fortitude_match := re.search(r'Fortitude ([0-9]*)', defense_match.group(1), re.IGNORECASE):
                                fortitude_str = fortitude_match.group(1)
                            elif fortitude_match := re.search(r'other defenses ([0-9]*)', defense_match.group(1), re.IGNORECASE):
                                fortitude_str = fortitude_match.group(1)
                            if hp_match := re.search(r'hp ([0-9]*)', defense_match.group(1)):
                                hp_str = hp_match.group(1)
                            elif hp_match := re.search(r'([0-9]*) hit points', defense_match.group(1)):
                                hp_str = hp_match.group(1)
                            if reflex_match := re.search(r'Reflex ([0-9]*)', defense_match.group(1), re.IGNORECASE):
                                reflex_str = reflex_match.group(1)
                            elif reflex_match := re.search(r'other defenses ([0-9]*)', defense_match.group(1), re.IGNORECASE):
                                reflex_str = reflex_match.group(1)
                            if specialdefenses_match := re.search(r'((immune|resist|vulnerable).*?)(;|\)|$|hp)', defense_match.group(1)):
                                specialdefenses_str = specialdefenses_match.group(1).strip()

        # Finish off the final trapskills
        if trapskills_str != '':
            trapskills_str += node_str
            trapskills_str += f'\t\t\t\t\t\t</nodes>\n'
            trapskills_str += f'\t\t\t\t\t</id-{trapskills_id:0>5}>\n'

        # Loop through the trap_html and build all the powers entries
        power_html = BeautifulSoup('', features='html.parser')
        in_power = False
        power_complete = False
        power_id = 0

        for pwr_tag in trap_html:
            # Break if we have reached the end of all Powers
            if pwr_tag.get('class')[0] == 'trapblocktitle' and re.search('^Countermeasures', pwr_tag.text) != None:
                break

            # Found the start of a Power
            if pwr_tag.get('class')[0] == 'trapblocktitle' and re.search('^.*Attack', pwr_tag.text) != None:
                # trigger on the start of the first power so we can know when a power has ended
                if not in_power:
                    in_power = True
                # second or later encounters with a power start signify previous power is ready to process
                else:
                    power_complete = True

            # If we have reached the start of a new power, process all the details and add it to the output
            if power_complete == True:
                power_id += 1
                powers_str += format_old_power(power_html, power_id)

                # Start next power with the tag that triggered this power creation
                power_complete = False
                power_html = BeautifulSoup('', features='html.parser')
                copy_tag = copy.copy(pwr_tag)
                power_html.append(copy_tag)

            # keep adding to the power html until it gets processed
            else:
                # for some reason using .append removes the tag from the original tree and screws up the iteration
                # so we make a copy and then append that instead
                if in_power:
                    copy_tag = copy.copy(pwr_tag)
                    power_html.append(copy_tag)

        # Create the last Power
        if str(power_html) != '':
            power_id += 1
            powers_str += format_old_power(power_html, power_id)

        #####################################################################
        # NEW LAYOUT is structured more like an NPC - classes begin with 'th'
        #####################################################################

        if not old_layout:

            # Level-Role
            level_tag = parsed_html.find('span', class_='thLevel')
            if level_tag:
                levelrole_str = str(level_tag.next)
            else:
                if name_str == 'Brazier of Silver Fire':
                    levelrole_str = 'Level 7 Trap'

            # Initiative
            init_tag = parsed_html.find('span', class_='thInit')
            if init_tag:
                init_str = re.sub('[^0-9]', '', init_tag.contents[1])

            # Type - Hazard is the only valid value other than Trap
            type_tag = parsed_html.find('span', class_='thSubHead')
            if type_tag:
                type_str = type_tag.text.strip()
            if type_str == '':
                type_str = 'Trap'

            # XP
            xp_tag = parsed_html.find('span', class_='thXP')
            if xp_tag:
                xp_str = str(xp_tag.text[3:])

            # Get the main div that contains all the Trap text
            detail_div = parsed_html.find('div', id='detail')

            # Get all the <h2> & <p> tags for ease of processing
            trap_html = BeautifulSoup('', features='html.parser')
            for span_tag in detail_div.find_all(re.compile('^(h2|p)$')):
                # replace <a> tags with their text
                anchor_tag = span_tag.find('a')
                while anchor_tag:
                    anchor_tag.replaceWithChildren()
                    anchor_tag = span_tag.find('a')
                trap_html.append(span_tag)

            # Loop through the trap_html and build all the powers entries
            power_html = BeautifulSoup('', features='html.parser')
            pwr_action = None
            in_power = False
            power_complete = False
            power_id = 0
            counter_id = 0

            # Powers / Countermeasures
            for trap_tag in trap_html:
                # Grab all the single occurrence fields and then skip
                tag_skip = False
                if trap_tag.get('class')[0] == 'thStat':
                    for tag in trap_tag:
                        if isinstance(tag, Tag):
                            if tag.text == 'AC':
                                ac_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                                tag_skip = True
                                continue
                            elif tag.text == 'Detect':
                                detect_str = tag.next_sibling.text.strip()
                                tag_skip = True
                                continue
                            elif tag.text == 'Fortitude':
                                fortitude_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                                tag_skip = True
                                continue
                            elif tag.text == 'HP':
                                hp_str = tag.next_sibling.text.strip()
                                tag_skip = True
                                continue
                            elif tag.text == 'Initiative':
                                init_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                                tag_skip = True
                                continue
                            elif tag.text == 'Reflex':
                                reflex_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                                tag_skip = True
                                continue
                            elif tag.text == 'Immune':
                                specialdefenses_str += ';' if specialdefenses_str != '' else ''
                                specialdefenses_str += 'Immune ' + tag.next_sibling.text.strip()
                                tag_skip = True
                                continue
                            elif tag.text == 'Resist':
                                specialdefenses_str += ';' if specialdefenses_str != '' else ''
                                specialdefenses_str += 'Resist ' + tag.next_sibling.text.strip()
                                tag_skip = True
                                continue
                            elif tag.text == 'Vulnerable':
                                specialdefenses_str += ';' if specialdefenses_str != '' else ''
                                specialdefenses_str += 'Vulnerable ' + tag.next_sibling.text.strip()
                                tag_skip = True
                                continue
                            elif tag.text == 'Speed':
                                speed_str = tag.next_sibling.text.strip()
                                tag_skip = True
                                continue
                if tag_skip:
                    continue

                # Grab the latest action tag to start every subsequent power until replaced by the next one
                if trap_tag.name == 'h2':
                    pwr_action = copy.copy(trap_tag)

                # Found the start of a power (Action h2 or flavor alt)
                if trap_tag.get('class')[0] in ['th2', 'thBody', 'publishedIn']:
                    # trigger on the start of the first power so we can know when a power has ended
                    if in_power == False:
                        in_power = True
                        if pwr_action:
                            power_html.append(pwr_action)

                    # second or later encounters with a power start signify previous power is ready to process
                    else:
                        power_complete = True

                # If we have reached the start of a new power, process all the details and add it to the output
                if power_complete == True:
                    # Countermeasures have a different parser
                    if power_html.find('h2', class_='thHead').text != 'Countermeasures':
                        power_id += 1
                        powers_str += format_new_power(power_html, power_id)
                    else:
                        counter_id += 1
                        counters_str += format_counter(power_html, counter_id)

                    # Break if we have reached the end of all Powers
                    if trap_tag.get('class')[0] == 'publishedIn':
                        break

                    # Start next power with the tag that triggered this power creation
                    power_complete = False
                    power_html = BeautifulSoup('', features='html.parser')
                    if pwr_action is not None:
                        power_html.append(pwr_action)
                    copy_tag = copy.copy(trap_tag)
                    power_html.append(copy_tag)

                # keep adding to the power html until it gets processed
                else:
                    # for some reason using .append removes the tag from the original tree and screws up the iteration
                    # so we make a copy and then append that instead
                    if trap_tag.name != 'h2':
                        copy_tag = copy.copy(trap_tag)
                        power_html.append(copy_tag)

            # Create the last Power
            if str(power_html) != '':
                # Countermeasures have a different parser
                if power_html.find('h2', class_='thHead').text != 'Countermeasures':
                    power_id += 1
                    powers_str += format_new_power(power_html, power_id)
                else:
                    counter_id += 1
                    counters_str += format_counter(power_html, counter_id)

        # OUTPUT BOTH LAYOUTS

        # Fix up double semi-colons in SpecialDefenses
        specialdefenses_str = re.sub(r';+', r'; ', specialdefenses_str)

        level_str = re.sub('[^0-9]', '', levelrole_str)
        if level_str.strip() == '':
            level_str = '0'
        if int(level_str) >= settings.min_lvl and int(level_str) <= settings.max_lvl:
            export_dict = {}

            # Append this to Trap card links to make them distinct, as there are multiple traps that have the same name
            trap_id += 1

            # These will be set by create_trap_table to control list creation
            export_dict["group_id"] = ''
            export_dict["group_str"] = ''

            export_dict["ac"] = ac_str
            export_dict["counters"] = counters_str
            export_dict["detect"] = detect_str
            export_dict["flavor"] = flavor_str
            export_dict["fortitude"] = fortitude_str
            export_dict["hp"] = hp_str
            export_dict["init"] = init_str
            export_dict["levelrole"] = levelrole_str
            export_dict["name"] = name_str
            export_dict["powers"] = powers_str
            export_dict["published"] = published_str
            export_dict["reflex"] = reflex_str
            export_dict["specialdefenses"] = specialdefenses_str
            export_dict["speed"] = speed_str
            export_dict["trapdesc"] = trapdesc_str
            export_dict["trapskills"] = trapskills_str
            export_dict["trap_id"] = trap_id
            export_dict["type"] = type_str
            export_dict["xp"] = xp_str

            # Append a copy of generated item dictionary
            trap_out.append(export_dict)

    print(str(len(db_in)) + ' entries checked.')
    print(str(len(trap_out)) + ' entries exported.')

    return trap_out
