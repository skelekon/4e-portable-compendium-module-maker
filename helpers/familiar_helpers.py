import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def familiar_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_familiar_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.familiars@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Familiars</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_familiar_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Familiars List
    # This controls the list that appears when you click on a Library menu

    xml_out += (f'\t\t<familiars>\n')
    xml_out += (f'\t\t\t<name type="string">Familiars</name>\n')
    xml_out += (f'\t\t\t<index>\n')

    # Create individual item entries
    for familiar_dict in sorted(list_in, key=familiar_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', familiar_dict["name"]).lower()

        # Familiars list entry
        xml_out += (f'\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_familiar</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.familiars.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{familiar_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t</{name_lower}>\n')

    xml_out += (f'\t\t\t</index>\n')
    xml_out += (f'\t\t</familiars>\n')

    return xml_out


def create_familiar_cards(list_in):
    familiars_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    familiars_out += ('\t\t<familiars>\n')
    for familiar_dict in sorted(list_in, key=familiar_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', familiar_dict["name"]).lower()

        familiars_out += f'\t\t\t<{name_lower}>\n'
        if familiar_dict["active"] != '':
            familiars_out += (f'\t\t\t\t<active type="string">{familiar_dict["active"]}</active>\n')
        if familiar_dict["constant"] != '':
            familiars_out += f'\t\t\t\t<constant type="string">{familiar_dict["constant"]}</constant>\n'
        if familiar_dict["flavor"] != '':
            familiars_out += f'\t\t\t\t<flavor type="string">{familiar_dict["flavor"]}</flavor>\n'
        familiars_out += f'\t\t\t\t<name type="string">{familiar_dict["name"]}</name>\n'
        if familiar_dict["senses"] != '':
            familiars_out += f'\t\t\t\t<senses type="string">{familiar_dict["senses"]}</senses>\n'
        if familiar_dict["speed"] != '':
            familiars_out += (f'\t\t\t\t<speed type="string">{familiar_dict["speed"]}</speed>\n')
        familiars_out += f'\t\t\t</{name_lower}>\n'

    familiars_out += ('\t\t</familiars>\n')

    return familiars_out


def extract_familiar_db(db_in):
    familiars_out = []

    print('\n\n\n=========== FAMILIARS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str = row["Name"].replace('\\', '')
        type_str = row["Type"].replace('\\', '')

        if type_str.upper() != 'FAMILIAR':
            continue

#        if name_str not in ['Bat', 'Cat']:
#            continue
#        print(name_str)

        active_str = ''
        constant_str = ''
        description_str = ''
        flavor_str = ''
        published_str = ''
        senses_str = ''
        speed_str = ''
        
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
            published_str += str(published_tag)

        # Flavor
        if flavor_tag := parsed_html.select_one('#detail > p > i'):
            flavor_str = flavor_tag.text
            flavor_tag.decompose()

        # Build list of strings for Prerequisite / Short Description (Benefit) / Description
        detail_div = parsed_html.find('div', id='detail')

        # Copy detail strings to a list of strings
        raw_list = []
        for div in detail_div.strings:
            if div.replace('\n', '').strip() != '' and not re.search('Tier$', div):
                raw_list.append(re.sub(r'&', r'&amp;', div))

        # Senses / Speed / Constant Benefits / Active Benefits
        in_constant = False
        in_active = False
        for idx, raw_str in enumerate(raw_list):
            if constant_tag := re.search(r'^Constant Benefits', raw_str, re.IGNORECASE):
                in_constant = True
                continue
            elif constant_tag := re.search(r'^Active Benefits', raw_str, re.IGNORECASE):
                in_active = True
                in_constant = False
                continue
            elif senses_tag := re.search(r'^Senses', raw_str, re.IGNORECASE):
                senses_str = raw_list[idx + 1]
            elif speed_tag := re.search(r'^Speed', raw_str, re.IGNORECASE):
                speed_str = raw_list[idx + 1]
            elif in_constant:
                if constant_str != '':
                    constant_str += '\\n'
                constant_str += raw_str
            elif in_active:
                if active_str != '':
                    active_str += '\\n'
                active_str += raw_str

            
        export_dict = {}
        export_dict["active"] = active_str
        export_dict["constant"] = constant_str
        export_dict["flavor"] = flavor_str
        export_dict["name"] = name_str
        export_dict["senses"] = senses_str
        export_dict["speed"] = speed_str

        # Append a copy of generated item dictionary
        familiars_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(familiars_out)) + ' entries exported.')

    return familiars_out
