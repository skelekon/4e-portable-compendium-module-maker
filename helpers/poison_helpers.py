import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def poison_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_poison_library(id_in):
    xml_out = ''

    id_in += 1
    lib_id = 'l' + str(id_in).rjust(3, '0')

    xml_out += (f'\t\t\t\t<{lib_id}-poison>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Poisons</name>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.poisons@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t</{lib_id}-poison>\n')

    return xml_out, id_in


def create_poison_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''
    previous_group = ''

    # Poisons List
    # This controls the list that appears when you click on a Library menu

    xml_out += (f'\t\t<poisons>\n')
    xml_out += (f'\t\t\t<name type="string">Poisons</name>\n')
    xml_out += (f'\t\t\t<index>\n')

    # Create individual item entries
    for poison_dict in sorted(list_in, key=poison_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', poison_dict["name"])

        # Poisons list entry
        xml_out += (f'\t\t\t\t<{name_camel}>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{poison_dict["name"]}</name>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_poison</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.poisons.{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t</{name_camel}>\n')

    xml_out += (f'\t\t\t</index>\n')
    xml_out += (f'\t\t</poisons>\n')

    return xml_out


def create_poison_cards(list_in):
    poisons_out = ''

    if not list_in:
        return xml_out

    section_str = ''
    entry_str = ''
    name_lower = ''

    # Create individual item entries
    poisons_out += ('\t\t<poisons>\n')
    for poison_dict in sorted(list_in, key=poison_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', poison_dict["name"])

        poisons_out += f'\t\t\t<{name_lower}>\n'
        poisons_out += f'\t\t\t\t<name type="string">{poison_dict["name"]}</name>\n'
        if poison_dict["flavor"] != '':
            poisons_out += f'\t\t\t\t<flavor type="string">{poison_dict["flavor"]}</flavor>\n'
        if poison_dict["level"] != '':
            poisons_out += f'\t\t\t\t<level type="number">{poison_dict["level"]}</level>\n'
        if poison_dict["cost"] != '':
            poisons_out += f'\t\t\t\t<cost type="number">{poison_dict["cost"]}</cost>\n'
        if poison_dict["attack"] != '':
            poisons_out += (f'\t\t\t\t<attack type="string">{poison_dict["attack"]}</attack>\n')
        if poison_dict["description"] != '':
            poisons_out += (f'\t\t\t\t<formattedpoisonblock type="formattedtext">{poison_dict["description"]}</formattedpoisonblock>\n')
        poisons_out += f'\t\t\t</{name_lower}>\n'

    poisons_out += ('\t\t</poisons>\n')

    return poisons_out


def extract_poison_db(db_in):
    poisons_out = []

    print('\n\n\n=========== POISONS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str = row["Name"].replace('\\', '')

#        if name_str not in ['Bat', 'Cat']:
#            continue
#        print(name_str)

        attack_str = ''
        cost_str = ''
        description_str = ''
        flavor_str = ''
        level_str = ''
        published_str = ''
        
        # Flavor
        if flavor_tag := parsed_html.select_one('#detail > p > i'):
            flavor_str = flavor_tag.text
            flavor_tag.decompose()

        # Build list of strings for Prerequisite / Short Description (Benefit) / Description
        detail_div = parsed_html.find('div', id='detail')

        # Copy detail strings to a list of strings
        raw_list = []
        for div in detail_div.strings:
            if div.replace('\n', '').strip() != '':
                raw_list.append(re.sub(r'&', r'&amp;', div))

        # Combine consecutive items where an item ends with a ':'
        desc_list = []
        skip_flag = False;
        for idx, raw_str in enumerate(raw_list):
            if skip_flag:
                skip_flag = False
            elif idx < len(raw_list) - 1 and (raw_list[idx].strip())[-1] == ':':
                desc_list.append(raw_str + raw_list[idx + 1])
                skip_flag = True
            else:
                desc_list.append(raw_str)

        # Level / Cost / Attack / Description
        for desc in desc_list:
            if desc == name_str or desc == 'Poison':
                continue
            elif re.search(r'Level\s+[0-9]+', desc) != None:
                level_str = re.sub(r'[^0-9]', '', desc)
            elif re.search(r'[0-9]+\s+gp', desc) != None:
                cost_str = re.sub(r'[^0-9]', '', desc)
            elif re.search(r'^Attack:', desc) != None:
                attack_str = re.sub(r'^Attack:', '', desc).strip()
            elif re.search(r'^\s*(Aftereffect:|.*?Failed Saving Throw:|Secondary Attack:)', desc) != None:
                attack_str += '\\n' + desc.strip()
            else:
                description_str += ('<p>' + desc + '</p>').strip()

        # bold Special heading
        description_str = re.sub(r'(Special:)', r'<b>\1</b>', description_str)            

        # combine the 'Published in' footer tags
        if published_match := re.match(r'^(.*)(<p>Published in .*)$', description_str):
            description_str = published_match.group(1) + re.sub(r'</p><p>', '', published_match.group(2))
            
        export_dict = {}
        export_dict["attack"] = attack_str
        export_dict["cost"] = cost_str
        export_dict["description"] = description_str
        export_dict["flavor"] = flavor_str
        export_dict["level"] = level_str
        export_dict["name"] = name_str

        # Append a copy of generated item dictionary
        poisons_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(poisons_out)) + ' entries exported.')

    return poisons_out
