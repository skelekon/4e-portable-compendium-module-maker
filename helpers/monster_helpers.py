import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

# This function return levels for all 25 conjured monsters since it's lacking in their original description/type
def get_conjured_level(name):
    if 'Shuffling Zombie' in name:
        return 'Level 0 Conjured'
    elif 'Onyx Dog' in name:
        return 'Level 4 Conjured'
    elif 'Obsidian Steed' in name:
        return 'Level 4 Conjured'
    elif 'Opal Carp' in name:
        return 'Level 6 Conjured'
    elif 'Pearl Sea Horse' in name:
        return 'Level 8 Conjured'
    elif 'Jade Macetail Behemeth' in name:
        return 'Level 8 Conjured'
    elif 'Conjured Critter (Gray Bag)' in name:
        return 'Level 8 Conjured'
    elif 'Marble Elephant' in name:
        return 'Level 10 Conjured'
    elif 'Jade Sea Snake' in name:
        return 'Level 10 Conjured'
    elif 'Ivory Goat of Travail' in name:
        return 'Level 10 Conjured'
    elif 'Ebony Fly' in name:
        return 'Level 10 Conjured'
    elif 'Bloodstone Spider' in name:
        return 'Level 10 Conjured'
    elif 'Golden Lion' in name:
        return 'Level 12 Conjured'
    elif 'Amber Monkey' in name:
        return 'Level 13 Conjured'
    elif 'Emerald Frog' in name:
        return 'Level 14 Conjured'
    elif 'Tantron' in name:
        return 'Level 16 Conjured Brute'
    elif 'Mercury Wasp Swarm' in name:
        return 'Level 16 Conjured'
    elif 'Serpentine Owl' in name:
        return 'Level 17 Conjured'
    elif 'Conjured Beast (Rust Bag)' in name:
        return 'Level 18 Conjured'
    elif 'Bronze Griffon' in name:
        return 'Level 19 Conjured'
    elif 'Guenhwyvar' in name:
        return 'Level 21 Conjured Skirmisher'
    elif 'Electrum Serpent' in name:
        return 'Level 21 Conjured'
    elif 'Tourmaline Turtle' in name:
        return 'Level 23 Conjured'
    elif 'Coral Dragon' in name:
        return 'Level 25 Conjured'
    elif 'Conjured Beast (Vermilion Bag)' in name:
        return 'Level 28 Conjured'
    else:
        return ''

# this allows for variable sorting by overwriting the GroupID value
def monster_list_sorter(entry_in):
    group_id = entry_in["group_id"]
    name = entry_in["name"]

    return (group_id, name)

def create_monster_library(tier_list, name_in):
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
        xml_out += (f'\t\t\t\t\t\t<recordname>lists.npc.{class_lower}_{tier_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</librarylink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{name_in}{tier_str}</name>\n')
        xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


# This controls the table that appears when you click on a Library menu
def create_monster_list(list_in, tier_list, name_in):
    xml_out = ''

    if not list_in:
        return xml_out

    class_lower = re.sub('[^a-zA-Z0-9_]', '', name_in).lower()

    # Populate the sort order and sub-heading fields according to which table is being built
    if re.search(r'NPCs By Letter', name_in):
        for monster_dict in list_in:
            monster_dict["group_id"] = re.sub('[^a-zA-Z0-9_]', '', monster_dict["name"])[0:1].lower()
            monster_dict["group_str"] = re.sub('[^a-zA-Z0-9_]', '', monster_dict["name"])[0:1].upper()
    elif re.search(r'NPCs By Level( |$)', name_in):
        for monster_dict in list_in:
            # Generate Level values
            level_str = re.sub('[^0-9]', '', monster_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            level_id = level_str.rjust(2, '0')

            monster_dict["group_id"] = level_id
            monster_dict["group_str"] = 'Level ' + level_str
    elif re.search(r'NPCs By Level/Role', name_in):
        for monster_dict in list_in:
            # Generate Level values
            level_str = re.sub('[^0-9]', '', monster_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            level_id = level_str.rjust(2, '0')

            monster_dict["group_id"] =  level_id + re.sub('[^a-zA-Z0-9_]', '', monster_dict["levelrole"])
            monster_dict["group_str"] = monster_dict["levelrole"]
    elif re.search(r'NPCs By Role/Level', name_in):
        for monster_dict in list_in:
            # Generate Level values
            level_str = re.sub('[^0-9]', '', monster_dict["levelrole"])
            if level_str == '':
                level_str = '0'
            level_id = level_str.rjust(2, '0')

            # Generate Role/Modifier/Leader values
            role_str = ''
            modifier_str = ''
            leader_str = ''
            # Leader in this list is the PC type not the (Leader) NPC subtype
            if role_match:= re.search(r'(Artillery|Brute|Controller|Lurker|Skirmisher|Soldier|Conjured|Defender|Leader$|Striker)', monster_dict["levelrole"], re.IGNORECASE):
                role_str = role_match.group(1).title()
            if modifier_match:= re.search(r'(Minion|Elite|Solo)', monster_dict["levelrole"], re.IGNORECASE):
                modifier_str = modifier_match.group(1).title()
            if leader_match:= re.search(r'(\(Leader\))', monster_dict["levelrole"], re.IGNORECASE):
                leader_str = leader_match.group(1).title()

            role_id = re.sub('[^a-zA-Z0-9_]', '', role_str)[0:3]
            modifier_id = re.sub('[^a-zA-Z0-9_]', '', modifier_str)[0:3].ljust(3, '-')
            leader_id = re.sub('[^a-zA-Z0-9_]', '', leader_str)[0:3].ljust(3, '-')

            monster_dict["group_id"] =  role_id + level_id + modifier_id + leader_id
            monster_dict["group_str"] = (role_str + ' Level ' + level_str + ' ' + modifier_str + ' ' + leader_str).strip()

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

        # Monster List

        # Open new Class (new Table)
        xml_out += (f'\t\t\t<{class_lower}_{tier_lower}>\n')
        xml_out += (f'\t\t\t\t<description type="string">{name_in}{tier_str}</description>\n')
        xml_out += ('\t\t\t\t<groups>\n')
        group_flag = False

        # Create individual item entries
        for monster_dict in sorted(list_in, key=monster_list_sorter):

            # only process Items for the current Tier
            level_str = re.sub('[^0-9]', '', monster_dict["levelrole"])
            if t == '':
                npc_tier = ''
            elif int(level_str) <= 10:
                npc_tier = 'Heroic'
            elif int(level_str) <= 20:
                npc_tier = 'Paragon'
            else:
                npc_tier = 'Epic'

            # only output items for the correct tier
            if npc_tier == t:
                group_flag = True

                # format name to be link target
                name_lower = re.sub('[^a-zA-Z0-9_]', '', monster_dict["name"]).lower()

                # Check for new Group
                if monster_dict["group_id"] != previous_group:

                    # Close previous Group
                    if previous_group != '':
                        xml_out += ('\t\t\t\t\t\t</monsters>\n')
                        xml_out += (f'\t\t\t\t\t</npcs_{previous_group}>\n')

                    # Open new Group
                    xml_out += (f'\t\t\t\t\t<npcs_{monster_dict["group_id"]}>\n')
                    xml_out += (f'\t\t\t\t\t\t<description type="string">{monster_dict["group_str"]}</description>\n')
                    xml_out += ('\t\t\t\t\t\t<monsters>\n')

                # Monster list entry
                xml_out += (f'\t\t\t\t\t\t\t<{name_lower}>\n')
                xml_out += ('\t\t\t\t\t\t\t\t<link type="windowreference">\n')
                xml_out += ('\t\t\t\t\t\t\t\t\t<class>npc</class>\n')
                xml_out += (f'\t\t\t\t\t\t\t\t\t<recordname>reference.npcs.{name_lower}@{settings.library}</recordname>\n')
                xml_out += ('\t\t\t\t\t\t\t\t</link>\n')
                xml_out += (f'\t\t\t\t\t\t\t</{name_lower}>\n')

                previous_group = monster_dict["group_id"]

        # Close final Group if there was at least one entry
        if group_flag:
            xml_out += ('\t\t\t\t\t\t</monsters>\n')
            xml_out += (f'\t\t\t\t\t</npcs_{previous_group}>\n')

        # Close final Class
        xml_out += ('\t\t\t\t</groups>\n')
        xml_out += (f'\t\t\t</{class_lower}_{tier_lower}>\n')

    return xml_out


def create_monster_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Reset the sort order so they are written in Name order
    for monster_dict in list_in:
        monster_dict["group_id"] = ''
        monster_dict["group_str"] = ''

    # Create individual item entries
    for monster_dict in sorted(list_in, key=monster_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', monster_dict["name"]).lower()

        xml_out += (f'\t\t\t<{name_lower}>\n')
        xml_out += (f'\t\t\t\t<ac type="number">{monster_dict["ac"]}</ac>\n')
        xml_out += (f'\t\t\t\t<alignment type="string">{monster_dict["alignment"]}</alignment>\n')
        if monster_dict["ap"] != '':
            xml_out += (f'\t\t\t\t<ap type="number">{monster_dict["ap"]}</ap>\n')
        else:
            xml_out += ('\t\t\t\t<ap type="number">0</ap>\n')
        xml_out += (f'\t\t\t\t<charisma type="number">{monster_dict["charisma"]}</charisma>\n')
        xml_out += (f'\t\t\t\t<constitution type="number">{monster_dict["constitution"]}</constitution>\n')
        xml_out += (f'\t\t\t\t<dexterity type="number">{monster_dict["dexterity"]}</dexterity>\n')
        if monster_dict["equipment"] != '':
            xml_out += (f'\t\t\t\t<equipment type="string">{monster_dict["equipment"]}</equipment>\n')
        xml_out += (f'\t\t\t\t<fortitude type="number">{monster_dict["fortitude"]}</fortitude>\n')
        xml_out += (f'\t\t\t\t<hp type="string">{monster_dict["hp"]}</hp>\n')
        xml_out += (f'\t\t\t\t<init type="number">{monster_dict["init"]}</init>\n')
        xml_out += (f'\t\t\t\t<intelligence type="number">{monster_dict["intelligence"]}</intelligence>\n')
        if monster_dict["languages"] != '':
            xml_out += (f'\t\t\t\t<languages type="string">{monster_dict["languages"]}</languages>\n')
        xml_out += (f'\t\t\t\t<levelrole type="string">{monster_dict["levelrole"]}</levelrole>\n')
        xml_out += (f'\t\t\t\t<name type="string">{monster_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t<npctype type="string">NPC</npctype>\n')
        if monster_dict["perceptionval"] != '':
            xml_out += (f'\t\t\t\t<perceptionval type="number">{monster_dict["perceptionval"]}</perceptionval>\n')
        xml_out += (f'\t\t\t\t<powers>\n{monster_dict["powers"]}\t\t\t\t</powers>\n')
        xml_out += (f'\t\t\t\t<reflex type="number">{monster_dict["reflex"]}</reflex>\n')
        xml_out += (f'\t\t\t\t<save type="number">{monster_dict["save"]}</save>\n')
        if monster_dict["senses"] != '':
            xml_out += (f'\t\t\t\t<senses type="string">{monster_dict["senses"]}</senses>\n')
        if monster_dict["specialdefenses"] != '':
            xml_out += (f'\t\t\t\t<specialdefenses type="string">{monster_dict["specialdefenses"]}</specialdefenses>\n')
        xml_out += (f'\t\t\t\t<speed type="string">{monster_dict["speed"]}</speed>\n')
        if monster_dict["skills"] != '':
            xml_out += (f'\t\t\t\t<skills type="string">{monster_dict["skills"]}</skills>\n')
        xml_out += (f'\t\t\t\t<strength type="number">{monster_dict["strength"]}</strength>\n')
        if monster_dict["published"] != '':
            xml_out += (f'\t\t\t\t<text type="formattedtext">{monster_dict["published"]}</text>\n')
        xml_out += (f'\t\t\t\t<type type="string">{monster_dict["type"]}</type>\n')
        xml_out += (f'\t\t\t\t<will type="number">{monster_dict["will"]}</will>\n')
        xml_out += (f'\t\t\t\t<wisdom type="number">{monster_dict["wisdom"]}</wisdom>\n')
        xml_out += (f'\t\t\t\t<xp type="number">{monster_dict["xp"]}</xp>\n')
        xml_out += (f'\t\t\t</{name_lower}>\n')

    return xml_out


def format_power(soup_in, id_in):
#    print('\nCREATE POWER')
#    print(soup_in)
    power_out = ''
    
    # Initialize variables that are per-power entry
    action_str = ''
    icon_str = ''
    description_str = ''
    flavor_str = ''
    keywords_str = ''
    powertype_str = ''
    pwrname_str = ''
    range_str = ''
    recharge_str = ''
    shortdescription_str = ''
    sustain_str = ''
    trigger_str = ''

    # Assume there are 2 power layouts:
    # Layout 1 has Action Headers, Keywords in parentheses and Recharge after the X glyph
    # Layout 2 has no Action Headers, Action & Recharge in parentheses and Keywords after the X glyph
    layout_1 = False

    # Copy the components into separate tags so we can interate them without running into the next tag
    action_tag = copy.copy(soup_in.find('h2'))
    header_tag = copy.copy(soup_in.find('p', class_='flavor alt'))
    body_tag = copy.copy(soup_in.find_all('p', class_='flavorIndent'))
#    print(action_tag)
#    print(header_tag)
#    print(body_tag)

    # Power Name
    if pwrname_tag := soup_in.find('b'):
        pwrname_str = pwrname_tag.text.replace('&', '&amp;')
#        print(pwrname_str)

    # Powertype
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
    # may be in its own tag in Layout 1
    if action_tag:
        if action_match := re.search(r'(Trait|Standard|Move|Minor|Free|Triggered)', action_tag.text, re.IGNORECASE):
            action_str = action_match.group(1)
            layout_1 = True
    # may be in parentheses after the power name
    if action_str == '':
        if action_match := re.search(r'(Free.*?|Immediate.*?|Minor.*?|Move.*?|Opportunity.*?|Standard.*?)(,|when|;|\))', header_tag.text, re.IGNORECASE):
            action_str += action_match.group(1).title()
            layout_1 = False

    # Trait is default if no Action defined
    if action_str == 'Trait':
        action_str = ''

    # Keywords
    # may be in parentheses in Layout 1
    if layout_1:
        if keywords_match := re.search(r'\((.*)\)', header_tag.text):
            keywords_str = keywords_match.group(1)
    # may be after star symbol in Layout 2
    elif keyword_img := header_tag.find('img', src=re.compile(r'/x.gif')):
        for kwd_tag in keyword_img.find_next_siblings():
            keywords_str += ''.join(kwd_tag.text.lower())

    # Recharge
    # first look for descriptive Recharge
    if layout_1:
        if recharge_img := header_tag.find('img', src=re.compile(r'/x.gif')):
            for rech_tag in recharge_img.find_all_next(text=True):
                recharge_str += rech_tag.text
            recharge_str = recharge_str.strip()
    else:
        # Layout 2
        if recharge_match := re.search(r'(Recharge.*?)[,)$]', header_tag.text, re.IGNORECASE):
            recharge_str += recharge_match.group(1).capitalize()
        elif recharge_match := re.search(r'(At-will|Daily|Encounter)', header_tag.text, re.IGNORECASE):
            recharge_str = recharge_match.group(1).title()

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

    # Sustain
    if sustain_match := re.search(r'(Sustain.*?)[,)$]', header_tag.text, re.IGNORECASE):
        sustain_str += sustain_match.group(1).title() + '\\n'

    # Trigger
    # if recharge_str doesn't contain when (otherwise we will recapture the when clause)
    if re.search(r'When', recharge_str, re.IGNORECASE) is None:
        if trigger_match := re.search(r'(When.*?)[,;)$]', header_tag.text, re.IGNORECASE):
            trigger_str += 'Trigger: ' + trigger_match.group(1)[0:1].upper() + trigger_match.group(1)[1:] + '\\n'

    # If Recharge is 'Aura', change that to the Action type so that it goes under an 'Auras' heading
    # set the range to be all the text after the Aura keyword, as it's most commonly just the aura size
    if aura_match := re.search('(^Aura\s*)(.*)', recharge_str, re.IGNORECASE):
        action_str = 'Aura'
        range_str = aura_match.group(2)
        recharge_str = ''

    # Short Description
    for bdy_tag in body_tag:
        shortdescription_str += ''.join(bdy_tag.stripped_strings) + '\\n'
    shortdescription_str = re.sub(r'(^;*\s*|\\n$)', '', shortdescription_str)
    # Capitalize the first letter to fix Layout 2 Auras
    shortdescription_str = shortdescription_str[0:1].upper() + shortdescription_str[1:]

    # Range - split out any Ranges or Sizes
    # regex has become too complicated, so build it up piecewise
    range_pattern = '(.*?)'
    range_pattern += '('
    range_pattern += 'Area burst\s+([0-9]+ within [0-9]+,? centered.*?;|[0-9]+,? centered.*?;|[0-9]+ within [0-9]+|[0-9]+)'
    range_pattern += '|Close blast\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|Close burst\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|Melee reach\s+([0-9]+)'
    range_pattern += '|Melee [0-9]+ or Ranged\s+([0-9]+)'
    range_pattern += '|Melee or Ranged reach\s+([0-9]+)'
    range_pattern += '|Melee\s+([0-9]+|touch|)'
    range_pattern += '|Ranged\s+([0-9]+/[0-9]+|[0-9]+|sight)'
    range_pattern += '|Range\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += '|[Rr]each\s+([0-9]+; targets.*?;|[0-9]+)'
    range_pattern += ')'
    range_pattern += '(\s+\(.*?\)|)'
    range_pattern += '(.*?)$'
    if range_match := re.search(range_pattern,  shortdescription_str):
        range_str = re.sub(r';$', '', range_match.group(2)).strip().capitalize() + range_match.group(13)
        # remove leading semi-colons or newlines
        shortdescription_str = re.sub(r'^(;|\\n|)*', '', range_match.group(1).strip() + range_match.group(14).strip())
        # remove empty clauses caused by extracting Range
        shortdescription_str = re.sub(r':\s*;', ':', shortdescription_str)

    # Fix up Triggered actions for Layout 2
    if not layout_1 and trigger_str != '':
        if action_str == 'Free':
            action_str = 'Triggered'
            shortdescription_str = '(Free Action):' + shortdescription_str
        elif action_str == 'Immediate Interrupt':
            action_str = 'Triggered'
            shortdescription_str = '(Immediate Interrupt):' + shortdescription_str
        elif action_str == 'Immediate Reaction':
            action_str = 'Triggered'
            shortdescription_str = '(Immediate Reaction):' + shortdescription_str

    # Prepend any Sustain or Trigger info
    shortdescription_str = (sustain_str + trigger_str + shortdescription_str).strip()

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


def extract_monster_db(db_in):
    monster_out = []

    print('\n\n\n=========== MONSTERS ===========')

    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features='html.parser')

        # Retrieve the data with dedicated columns
        name_str = row["Name"].replace('\\', '')
        exp_str = row["XP"].replace('\\', '')
        level_str = row["Level"].replace('\\', '')
        role_str = row["Role"].replace('\\', '')

#        if name_str not in ['Torog', 'Ancient Earthquake Dragon', 'Bullywug Leaper', 'Berbalang', 'Demogorgon', 'Abalach-Re, Sorcerer-Queen', 'Ancient Red Dragon', 'Balor', 'Aboleth Overseer', 'Adult Black Dragon', 'Astral Stalker', 'Shuffling Zombie', 'Dark Naga', 'Angel of Valor Legionnaire', 'Berbalang', 'Decrepit Skeleton', 'Ogrémoch', 'Yuan-ti Abomination']:
#            continue
#        print('\n' + name_str)

        action_str = ''
        alignment_str = ''
        ap_str = ''
        description_str = ''
        equipment_str = ''
        flavor_str = ''
        hp_str = ''
        init_str = ''
        languages_str = ''
        levelrole_str = ''
        perceptionval_str = ''
        powers_str = ''
        published_str = ''
        save_str = ''
        senses_str = ''
        skills_str = ''
        speed_str = ''
        specialdefenses_str = ''
        type_str = ''
        xp_str = ''

        ac_str = ''
        fortitude_str = ''
        reflex_str = ''
        will_str = ''

        strength_str = ''
        dexterity_str = ''
        wisdom_str = ''
        constitution_str = ''
        intelligence_str = ''
        charisma_str = ''

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
            # put it in a string and separate entries with <p> tags
            published_str = str(published_tag)
            published_str = re.sub(r'(page\(s\)[0-9, ]*), ', r'\1</p><p>', published_str)
            published_str = re.sub(r'(Dungeon Magazine [0-9]+), ([^p])', r'\1</p><p>\2', published_str)
            

        # Level-Role
        level_tag = parsed_html.find('span', class_='level')
        if level_tag:
            levelrole_str = str(level_tag.next)
        else:
            levelrole_str = get_conjured_level(name_str)

        # Type
        type_tag = parsed_html.find('span', class_='type')
        if type_tag:
            type_str = re.sub(r'\s+', ' ', type_tag.text)

        # XP
        xp_tag = parsed_html.find('span', class_='xp')
        if xp_tag:
            xp_str = str(xp_tag.next[4:])

        # Get all the Power tags
        detail_div = parsed_html.find('div', id='detail')

        # Restructure the contents into a flat list of <h2>, <p> and <td> tags for ease of processing
        useful_html = BeautifulSoup('', features='html.parser')
        for div_tag in detail_div.find_all(re.compile('^(h2|p|td)$')):
            # remove nested <p> tags as they will also be returned in the outer loop
            for sub_tag in div_tag.find_all('p', class_=re.compile(r'(flavor|flavor alt|flavorIndent|publishedIn)')):
                sub_tag.extract()
            # replace <a> tags with their text
            anchor_tag = div_tag.find('a')
            while anchor_tag:
                anchor_tag.replaceWithChildren()
                anchor_tag = div_tag.find('a')
            useful_html.append(div_tag)

        # Loop through the useful_html and grab all the single occurrence fields
        for use_tag in useful_html:
            for tag in use_tag:
                if isinstance(tag, Tag):
                    if tag.text == 'AC':
                        ac_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                    if tag.text == 'Action Points':
                        ap_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                    if tag.text == 'Fortitude':
                        fortitude_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                    if tag.text == 'HP':
                        hp_str = tag.next_sibling.text.strip()
                        if hp_str[0:2] != '1;':
                            hp_str = hp_str + ' Bloodied ' + str(int(re.sub('[^0-9]', '', hp_str)) // 2)
                    if tag.text == 'Perception':
                        if tag.next_sibling:
                            perceptionval_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                    if tag.text == 'Senses':
                        senses_str = tag.next_sibling.text.strip()
                    if tag.text == 'Initiative':
                        init_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                    if tag.text == 'Reflex':
                        reflex_str = re.sub('[^0-9]', '', tag.next_sibling.text)
                    if tag.text == 'Saving Throws':
                        save_str = re.sub('[^0-9+]', '', tag.next_sibling.text)
                    if tag.text == 'Immune':
                        specialdefenses_str += ';' if specialdefenses_str != '' else ''
                        specialdefenses_str += 'Immune ' + tag.next_sibling.text.strip()
                    if tag.text == 'Resist':
                        specialdefenses_str += ';' if specialdefenses_str != '' else ''
                        specialdefenses_str += 'Resist ' + tag.next_sibling.text.strip()
                    if tag.text == 'Vulnerable':
                        specialdefenses_str += ';' if specialdefenses_str != '' else ''
                        specialdefenses_str += 'Vulnerable ' + tag.next_sibling.text.strip()
                    if tag.text == 'Speed':
                        speed_str = tag.next_sibling.text.strip()
                    if tag.text == 'Will':
                        will_str = re.sub('[^0-9]', '', tag.next_sibling)
                    if tag.text == 'Alignment':
                        alignment_str = tag.next_sibling.text.strip().lower()
                    if tag.text == 'Equipment':
                        equipment_str = ''.join(tag.find_next_siblings(string=True))
                        equipment_str = re.sub(r'(^\s*:\s*|[\.\s]*$)', '', equipment_str)
                    if tag.text.strip() == 'Languages':
                        languages_str = tag.next_sibling.text.strip()
                    if tag.text == 'Skills':
                        skills_str = tag.next_sibling.text.strip()
                    if tag.text == 'Str':
                        strength_str = re.sub(r'(^\s|\s\(.*$)', '', tag.next_sibling)
                    if tag.text == 'Con':
                        constitution_str = re.sub(r'(^\s|\s\(.*$)', '', tag.next_sibling)
                    if tag.text == 'Dex':
                        dexterity_str = re.sub(r'(^\s|\s\(.*$)', '', tag.next_sibling)
                    if tag.text == 'Int':
                        intelligence_str = re.sub(r'(^\s|\s\(.*$)', '', tag.next_sibling)
                    if tag.text == 'Wis':
                        wisdom_str = re.sub(r'(^\s|\s\(.*$)', '', tag.next_sibling)
                    if tag.text == 'Cha':
                        charisma_str = re.sub(r'(^\s|\s\(.*$)', '', tag.next_sibling)
                    if tag.text == 'Description':
                        description_str = tag.next_sibling.text.strip()
                # if we haven't hit a 'Senses' label yet, grab senses that are just by themself without any label
                if senses_str == '' and re.search(r'(All-around|Blindsight|Darkvision|Low-light vision|Truesight|Tremorsense)', tag.text, flags=re.IGNORECASE):
                    senses_str = tag.text

        # Split out PerceptionVal if it is in with Senses
        if perception_match := re.search(r'(Perception\s*\+*)([0-9]*)\s*[,;]*\s*(.*)', senses_str):
            perceptionval_str = perception_match.group(2)
            senses_str = perception_match.group(3)
        # capitalize only the first letter of each special sense
        senses_str = re.sub(r'(All-around|Blindsight|Darkvision|Low-light vision|Truesight|Tremorsense)', lambda match: match.group(0).capitalize(), senses_str, flags=re.IGNORECASE)

        # Fix up double semi-colons in SpecialDefenses
        specialdefenses_str = re.sub(r';+', r';', specialdefenses_str)

        # Loop through the useful_html and build all the powers entries
        power_html = BeautifulSoup('', features='html.parser')
        pwr_action = None
        aura_tag = None
        in_power = False
        power_complete = False
        power_id = 0

#        print('\nPWR_TAGS')
#        for pwr_tag in useful_html:
#            print(pwr_tag)

        for pwr_tag in useful_html:
            # Skip the initial header stats as they don't contain Powers information
            if pwr_tag.has_attr('class') and 'flavor' in pwr_tag.get('class') and 'alt' not in pwr_tag.get('class'):

                # if we find an Aura in the header section, construct it like other powers so it can be processed with them
                for a_tag in pwr_tag:
                    if aura_match := re.search(r'aura\s*([0-9]+)(.*)', a_tag.text, re.IGNORECASE):
                        aura_head = aura_match.group(1)
                        aura_body = aura_match.group(2)
                        aura_name = a_tag.previous_sibling.text
                        aura_kwds = ''
                        if kwds_match := re.search(r'(\(.*?\))', a_tag.text):
                            aura_kwds = kwds_match.group(1)
                        aura_tag = BeautifulSoup('<h2>Traits</h2><p class="flavor alt"><img src="images/symbol/aura.png"/><b>' + aura_name + '</b>'\
                                                 + aura_kwds + ' <img src="images/symbol/x.gif"/> <b>Aura</b> ' + aura_head + '</p><p class="flavorIndent">' + aura_body +\
                                                 '</p>', features='html.parser')
                        power_id += 1
                        powers_str += format_power(aura_tag, power_id)

                continue

            # Skip the bodytable fields as they don't contain Powers information
            if pwr_tag.name == 'td':
                continue

            # Grab the latest action tag to start every subsequent power until replaced by the next one
            if pwr_tag.name == 'h2':
                pwr_action = copy.copy(pwr_tag)

            # Found the start of a power (Action h2 or flavor alt)
            if pwr_tag.has_attr('class') and 'flavor' in pwr_tag.get('class') and 'alt' in pwr_tag.get('class'):
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
                power_id += 1
                powers_str += format_power(power_html, power_id)

                # Break if we have reached the end of all Powers
                if 'flavor' in pwr_tag.get('class') and 'alt' not in pwr_tag.get('class'):
                    break
                elif 'Str' in pwr_tag.text and 'Dex' in pwr_tag.text and 'Wis' in pwr_tag.text:
                    break

                # Start next power with the tag that triggered this power creation
                power_complete = False
                power_html = BeautifulSoup('', features='html.parser')
                if pwr_action is not None:
                    power_html.append(pwr_action)
                copy_tag = copy.copy(pwr_tag)
                power_html.append(copy_tag)

            # keep adding to the power html until it gets processed
            else:
                # for some reason using .append removes the tag from the original tree and screws up the iteration
                # so we make a copy and then append that instead
                if pwr_tag.name != 'h2':
                    copy_tag = copy.copy(pwr_tag)
                    power_html.append(copy_tag)

        level_str = re.sub('[^0-9]', '', levelrole_str)
        if int(level_str) >= settings.min_lvl and int(level_str) <= settings.max_lvl:
            export_dict = {}
            # These will be set by create_monster_table to control list creation
            export_dict["group_id"] = ''
            export_dict["group_str"] = ''

            export_dict["alignment"] = alignment_str
            export_dict["ap"] = ap_str
            export_dict["equipment"] = equipment_str
            export_dict["hp"] = hp_str
            export_dict["init"] = init_str
            export_dict["languages"] = languages_str
            export_dict["levelrole"] = levelrole_str
            export_dict["name"] = name_str
            export_dict["perceptionval"] = perceptionval_str
            export_dict["powers"] = powers_str
            export_dict["published"] = published_str
            export_dict["save"] = save_str
            export_dict["senses"] = senses_str
            export_dict["skills"] = skills_str
            export_dict["specialdefenses"] = specialdefenses_str
            export_dict["speed"] = speed_str
            export_dict["type"] = type_str
            export_dict["xp"] = xp_str

            export_dict["ac"] = ac_str
            export_dict["fortitude"] = fortitude_str
            export_dict["reflex"] = reflex_str
            export_dict["will"] = will_str

            export_dict["strength"] = strength_str
            export_dict["constitution"] = constitution_str
            export_dict["dexterity"] = dexterity_str
            export_dict["intelligence"] = intelligence_str
            export_dict["wisdom"] = wisdom_str
            export_dict["charisma"] = charisma_str

            # Append a copy of generated item dictionary
            monster_out.append(export_dict)

    print(str(len(db_in)) + ' entries checked.')
    print(str(len(monster_out)) + ' entries exported.')

    return monster_out
