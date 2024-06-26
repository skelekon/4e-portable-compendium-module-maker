import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .mod_helpers import title_format

def weapons_list_sorter(entry_in):
    section_id = entry_in["section_id"]
    name = entry_in["name"]

    return (section_id, name)

def create_weapons_library(name_in):
    settings.lib_id += 1

    xml_out = ''
    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_classweapontablelist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.weapon@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">{name_in}</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out

def create_weapons_list(list_in):
    xml_out = ''
    section_id = 0

    # Open the Item List
    # This controls the table that appears when you click on a Library menu
    xml_out += ('\t\t<weapon>\n')
    xml_out += ('\t\t\t<description type="string">Weapons Table</description>\n')
    xml_out += ('\t\t\t<groups>\n')

    # Create individual item entries
    for entry_dict in sorted(list_in, key=weapons_list_sorter):
        suffix_str = ' Weapons' if entry_dict["type"] != 'Implement' else 's'
        name_lower = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"]).lower()

        # Check for new section
        if entry_dict["section_id"] != section_id:
            section_id = entry_dict["section_id"]

            # Close the previous section
            if section_id != 1:
                section_str = str(section_id - 1).rjust(3, '0')
                xml_out += ('\t\t\t\t\t</weapons>\n')
                xml_out += (f'\t\t\t\t</section{section_str}>\n')

            # Open the next section
            section_str = str(section_id).rjust(3, '0')
            xml_out += (f'\t\t\t\t<section{section_str}>\n')
            xml_out += (f'\t\t\t\t\t<description type="string">{entry_dict["prof"]} {entry_dict["type"]}{suffix_str}</description>\n')
            xml_out += (f'\t\t\t\t\t<subdescription type="string">{entry_dict["heft"]}</subdescription>\n')
            xml_out += ('\t\t\t\t\t<weapons>\n')

        xml_out += (f'\t\t\t\t\t\t<{name_lower}>\n')
        xml_out += (f'\t\t\t\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
        xml_out += (f'\t\t\t\t\t\t\t<damage type="string">{entry_dict["damage"]}</damage>\n')
        xml_out += (f'\t\t\t\t\t\t\t<group type="string">{entry_dict["group"]}</group>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>referenceweapon</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.items.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t\t\t<name type="string">{entry_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t\t\t\t<profbonus type="number">{entry_dict["profbonus"]}</profbonus>\n')
        xml_out += (f'\t\t\t\t\t\t\t<properties type="string">{entry_dict["properties"]}</properties>\n')
        xml_out += (f'\t\t\t\t\t\t\t<range type="number">{entry_dict["range"]}</range>\n')
        xml_out += (f'\t\t\t\t\t\t\t<weight type="string">{entry_dict["weight"]}</weight>\n')
        xml_out += (f'\t\t\t\t\t\t</{name_lower}>\n')

    # Close the final section
    xml_out += ('\t\t\t\t\t</weapons>\n')
    xml_out += (f'\t\t\t\t</section{section_str}>\n')

    # Close the Item List
    xml_out += ('\t\t\t</groups>\n')
    xml_out += ('\t\t</weapon>\n')

    return xml_out

def create_weapons_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    for entry_dict in sorted(list_in, key=weapons_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', entry_dict["name"]).lower()

        xml_out += (f'\t\t\t<{name_lower}>\n')
        if entry_dict["cost"] != '':
            xml_out += (f'\t\t\t\t<cost type="string">{entry_dict["cost"]}</cost>\n')
        if entry_dict["damage"] != '':
            xml_out += (f'\t\t\t\t<damage type="string">{entry_dict["damage"]}</damage>\n')
        xml_out += (f'\t\t\t\t<description type="formattedtext">{entry_dict["description"]}</description>\n')
        xml_out += (f'\t\t\t\t<flavor type="string">{entry_dict["description"]}</flavor>\n')
        xml_out += (f'\t\t\t\t<group type="string">{entry_dict["group"]}</group>\n')
        xml_out += (f'\t\t\t\t<heft type="string">{entry_dict["heft"]}</heft>\n')
        xml_out += (f'\t\t\t\t<mitype type="string">weapon</mitype>\n')
        xml_out += (f'\t\t\t\t<name type="string">{entry_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t<prof type="string">{entry_dict["prof"]}</prof>\n')
        xml_out += (f'\t\t\t\t<profbonus type="number">{entry_dict["profbonus"]}</profbonus>\n')
        if entry_dict["properties"] != '':
            xml_out += (f'\t\t\t\t<properties type="string">{entry_dict["properties"]}</properties>\n')
        if entry_dict["range"] != '':
            xml_out += (f'\t\t\t\t<range type="number">{entry_dict["range"]}</range>\n')
        else:
            xml_out += ('\t\t\t\t<range type="number">0</range>\n')
        xml_out += (f'\t\t\t\t<type type="string">{entry_dict["type"]}</type>\n')
        xml_out += (f'\t\t\t\t<weight type="number">{entry_dict["weight"]}</weight>\n')
        xml_out += (f'\t\t\t</{name_lower}>\n')

    return xml_out

def extract_weapons_db(db_in):
    weapons_out = []

    # List of possible Weapon properties
    properties_list = ['^Brutal 1', '^Brutal 2', '^Defensive', '^Heavy Thrown', '^High Crit', '^Light Thrown', '^Load Free', '^Load Minor', '^Load Move', '^Load Standard', '^Off-Hand', '^Reach[^i]', '^Small', '^Stout', '^Versatile',\
        '^Accurate', '^Blinking', '^Deadly', '^Distant', '^Empowered Crit', '^Forceful', '^Mighty', '^Mobile', '^Reaching', '^Shielding', '^Undeniable', '^Unerring', '^Unstoppable',\
        'Energized \(acid\)', 'Energized \(cold\)', 'Energized \(fire\)', 'Energized \(force\)', 'Energized \(lightning\)', 'Energized \(necrotic\)', 'Energized \(psychic\)', 'Energized \(radiant\)', 'Energized \(thunder\)']

    print('\n\n\n=========== WEAPONS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row['Txt']
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  title_format(row['Name'].replace('\\', ''))

        # Initialize the other tag data
        category_str = ''
        cost_str = ''
        damage_str = ''
        description_str = ''
        group_str = ''
        heft_str = ''
        prof_str = ''
        profbonus_str = ''
        properties_str = ''
        range_str = ''
        section_id = 100
        type_str = ''
        weight_str = ''

        # Type - Basic weapons and Superior implements
        # brute force the Type/Heft
        if type_lbl := parsed_html.find(string=re.compile('^(Simple|Military|Superior( one| two| dou|\s*$)|Improvised.*handed.*weapon)')):
            type_lbl = re.sub('\s*$', '', type_lbl)
            if type_lbl == 'Simple one-handed melee weapon':
                section_id = 1
                prof_str = 'Simple'
                type_str = 'Melee'
                heft_str = 'One-Handed'
            elif type_lbl == 'Simple two-handed melee weapon':
                section_id = 2
                prof_str = 'Simple'
                type_str = 'Melee'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Military one-handed melee weapon':
                section_id = 3
                prof_str = 'Military'
                type_str = 'Melee'
                heft_str = 'One-Handed'
            elif type_lbl == 'Military two-handed melee weapon':
                section_id = 4
                prof_str = 'Military'
                type_str = 'Melee'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Superior one-handed melee weapon':
                section_id = 5
                prof_str = 'Superior'
                type_str = 'Melee'
                heft_str = 'One-Handed'
            elif type_lbl == 'Superior two-handed melee weapon':
                section_id = 6
                prof_str = 'Superior'
                type_str = 'Melee'
                heft_str = 'Two-Handed'
            # Garotte typo
            elif type_lbl == 'Superior two-handed  weapon':
                section_id = 6
                prof_str = 'Superior'
                type_str = 'Melee'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Superior double melee weapon':
                section_id = 7
                prof_str = 'Superior'
                type_str = 'Melee'
                heft_str = 'Double'
            elif type_lbl == 'Improvised one-handed melee weapon':
                section_id = 8
                prof_str = 'Improvised'
                type_str = 'Melee'
                heft_str = 'One-Handed'
            elif type_lbl == 'Improvised two-handed melee weapon':
                section_id = 9
                prof_str = 'Improvised'
                type_str = 'Melee'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Simple one-handed ranged weapon':
                section_id = 10
                prof_str = 'Simple'
                type_str = 'Ranged'
                heft_str = 'One-Handed'
            elif type_lbl == 'Simple two-handed ranged weapon':
                section_id = 11
                prof_str = 'Simple'
                type_str = 'Ranged'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Military one-handed ranged weapon':
                section_id = 12
                prof_str = 'Military'
                type_str = 'Ranged'
                heft_str = 'One-Handed'
            elif type_lbl == 'Military two-handed ranged weapon':
                section_id = 13
                prof_str = 'Military'
                type_str = 'Ranged'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Superior one-handed ranged weapon':
                section_id = 14
                prof_str = 'Superior'
                type_str = 'Ranged'
                heft_str = 'One-Handed'
            elif type_lbl == 'Superior two-handed ranged weapon':
                section_id = 15
                prof_str = 'Superior'
                type_str = 'Ranged'
                heft_str = 'Two-Handed'
            elif type_lbl == 'Improvised one-handed ranged weapon':
                section_id = 16
                prof_str = 'Improvised'
                type_str = 'Ranged'
                heft_str = 'One-Handed'
            # there are none of these
##            elif type_lbl == 'Improvised two-handed ranged weapon':
##                section_id = 17
##                prof_str = 'Improvised'
##                type_str = 'Ranged'
##                heft_str = 'Two-Handed'
            elif type_lbl == 'Superior':
                section_id = 17
                prof_str = 'Superior'
                type_str = 'Implement'
                heft_str = 'One-Handed'
            else:
                section_id = 100
                type_str = type_lbl

        # Records to be processed
        if section_id < 100:

            # Cost
            if cost_lbl := parsed_html.find(string='Price'):
                cost_str = cost_lbl.parent.next_sibling
            elif cost_lbl := parsed_html.find(string='Cost'):
                cost_str = cost_lbl.parent.next_sibling
            elif cost_lbl := parsed_html.find(string=re.compile('^Cost:.*')):
                cost_str = cost_lbl.string

            if cost_str != '':
                cost_str = re.sub(r'(^:\s*|^\s*Cost:\s*|\.$)', '', cost_str)
##                # Divide by 100 if cost is in cp
##                if re.search(r'cp', cost_str):
##                    cost_str = '0.0' + re.sub('[^\.\d]', '', cost_str)
##                # Divide by 10 if cost is in sp
##                elif re.search(r'sp', cost_lbl):
##                    cost_str = '0.' + re.sub('[^\.\d]', '', cost_str)
##                else:
##                    cost_str = re.sub('[^\.\d]', '', cost_str)
##                # remove trailing zeroes
##                cost_str = re.sub('(\.0*$)', '', cost_str)
##                # add leading zero
##                cost_str = re.sub('(^\.)', '0.', cost_str)

            # Damage
            if damage_lbl := parsed_html.find(string='Damage'):
                damage_str = damage_lbl.parent.next_sibling.replace(': ', '')

            # Description
            # implements have a description tag
            if description_lbl := parsed_html.find(string='Description'):
                description_str = description_lbl.parent.next_sibling.replace(': ', '')
            # otherwise look for a 'detail' div
            elif detail_div := parsed_html.find('div', id='detail'):
                for el_str in detail_div.stripped_strings:
                    # if we hit these we have gone too far
                    if re.search('^(Properties|Published|' + group_str + ')', el_str):
                        break
                    # skip over these ones
                    if re.search('^(:|Cost|Damage|Group|Range|Weight|Proficient|' + name_str + '|' + type_lbl + ')', el_str):
                        continue
                    # otherwise append non-empty values to the Description
                    if re.sub('\s', '', el_str) != '':
                        description_str += '\\n' if description_str != '' else ''
                        description_str += re.sub('^[:\s]*', '', el_str)

            # Description (Published In)
            if description_lbl := parsed_html.find('p', class_='publishedIn'):
                if description_str != '':
                    description_str += '\\n'
                description_str += re.sub('\s\s', ' ', description_lbl.text)

            # clean up extraneous spaces
            description_str = re.sub('\s\s', ' ', description_str.strip())

            # Group
            if group_lbl := parsed_html.find(string='Group'):
                group_str = group_lbl.parent.next_sibling.next_sibling.next_sibling.replace(' (', '').title()

            # Proficiency Bonus
            if profbonus_lbl := parsed_html.find(string=re.compile('^Proficient:.*')):
                profbonus_str = int(profbonus_lbl.string.replace('Proficient: ', ''))

            # Properties
            # might get false positives as it's just checking each property regex against the whole text
            for prop in properties_list:
                if properties_lbl := parsed_html.find(string=re.compile(prop + '.*')):
                    properties_str += '\\n' if properties_str != '' else ''
                    properties_str += prop.replace('[^i]', '').replace('\\', '').replace('^', '')

            # Range
            # strip the heading and long range bracket
            if range_lbl := parsed_html.find(string=re.compile('^Range:.*')):
                range_str = re.sub('(Range: |-|/.*)', '', range_lbl.string)
                if range_str != '':
                    range_str = int(range_str)

            # Weight
            # might have a separate bold label
            if weight_lbl := parsed_html.find(string='Weight'):
                weight_str = weight_lbl.parent.next_sibling.replace(': ', '').replace('1/10', '0.1').replace('1/2', '0.5').replace(' lb.', '').replace(' lb', '')
            # might be inside a single tag
            elif weight_lbl := parsed_html.find(string=re.compile('^Weight:.*')):
                weight_str = weight_lbl.string.replace('Weight: ', '').replace('1–', '').replace('6–', '').replace('—', '0').replace('1/10', '0.1').replace('1/2', '0.5').replace(' lb.', '').replace(' lb', '')
            # remove trailing zeroes
            weight_str = re.sub('(\.0*$)', '', weight_str)
            # add leading zero
            weight_str = re.sub('(^\.)', '0.', weight_str)

            # Build the item dictionary
            export_dict = {}
            export_dict['cost'] = cost_str# if cost_str != '' else 0
            export_dict['damage'] = damage_str
            export_dict['description'] = description_str
            export_dict['group'] = group_str
            export_dict['heft'] = heft_str
            export_dict['name'] = name_str
            export_dict['prof'] = prof_str
            export_dict['profbonus'] = profbonus_str
            export_dict['properties'] = properties_str
            export_dict['range'] = range_str
            export_dict['section_id'] = section_id
            export_dict['type'] = type_str
            export_dict['weight'] = weight_str if weight_str != '' else 0

            # Append a copy of generated item dictionary
            weapons_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + " entries parsed.")
    print(str(len(weapons_out)) + " entries exported.")

    return weapons_out
