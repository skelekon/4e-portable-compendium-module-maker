import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def terrain_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_terrain_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.terrain@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Terrain</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_terrain_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Terrain List
    # This controls the list that appears when you click on a Library menu

    xml_out += (f'\t\t<terrain>\n')
    xml_out += (f'\t\t\t<name type="string">Terrain</name>\n')
    xml_out += (f'\t\t\t<index>\n')

    # Create individual item entries
    for terrain_dict in sorted(list_in, key=terrain_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', terrain_dict["name"]).lower()

        # Terrain list entry
        xml_out += (f'\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.terrain.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{terrain_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t</{name_lower}>\n')

    xml_out += (f'\t\t\t</index>\n')
    xml_out += (f'\t\t</terrain>\n')

    return xml_out


def create_terrain_cards(list_in):
    terrain_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    terrain_out += ('\t\t<terrain>\n')
    for terrain_dict in sorted(list_in, key=terrain_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', terrain_dict["name"]).lower()

        terrain_out += f'\t\t\t<{name_lower}>\n'
        terrain_out += f'\t\t\t\t<description type="formattedtext">'
        if terrain_dict["description"] != '':
            terrain_out += f'{terrain_dict["description"]}'
        if terrain_dict["published"] != '':
            terrain_out += f'{terrain_dict["published"]}'
        terrain_out += f'</description>\n'
        terrain_out += f'\t\t\t\t<name type="string">{terrain_dict["name"]}</name>\n'
        if terrain_dict["type"] != '':
            terrain_out += f'\t\t\t\t<source type="string">{terrain_dict["type"]}</source>\n'
        terrain_out += f'\t\t\t</{name_lower}>\n'

    terrain_out += ('\t\t</terrain>\n')

    return terrain_out


def extract_terrain_db(db_in):
    terrain_out = []

    print('\n\n\n=========== TERRAIN ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row['Name'].replace('\\', '')
        type_str =  row['type'].replace('\\', '')

#        if name_str not in ['Auspicious Birth']:
#            continue
#        print(name_str)

        description_str = ''
        published_str = ''
        
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

        # Build list of detail strings
        detail_div = parsed_html.find('div', id='detail')

        # Copy detail strings to a list of strings
        raw_list = []
        for div in detail_div.strings:
            if div.replace('\n', '').strip() != '' and not re.search('Tier$', div):
                raw_list.append(re.sub(r'&', r'&amp;', div))

        # Combine consecutive items where an item ends with a ':'
        desc_list = []
        skip_flag = False;
        for idx, raw_str in enumerate(raw_list):
            if skip_flag:
                skip_flag = False
            elif idx < len(raw_list) - 1 and raw_list[idx].strip() in ['Attack:', 'Check:', 'Effect:', 'Failure:', 'Hit:', 'Miss:', 'Requirement:', 'Special:', 'Success:', 'Target:', 'Usage:']:
                desc_list.append(raw_str + raw_list[idx + 1])
                skip_flag = True
            else:
                desc_list.append(raw_str)

        # Prerequisite / Short Description (Benefit) / Description
        for desc in desc_list:
            if desc == name_str:
                continue
            description_str += ('<p>' + desc + '</p>').strip()
        # bold the Prerequisite, Type & Campaign Setting headings
        description_str = re.sub(r'(At-Will Terrain|Attack:|Check:|Effect:|Failure:|Free Action|Hit:|Minor Action|Miss:|Move Action|Requirement:|Single-Use Terrain|Special:|Standard Action|Success:|Target:|Usage:)', r'<b>\1</b>', description_str)            

        export_dict = {}
        export_dict["description"] = description_str
        export_dict["name"] = name_str
        export_dict["published"] = published_str
        export_dict["type"] = type_str

        # Append a copy of generated item dictionary
        terrain_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(terrain_out)) + ' entries exported.')

    return terrain_out
