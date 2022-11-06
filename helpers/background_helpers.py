import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def background_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_background_library(id_in):
    xml_out = ''

    id_in += 1
    lib_id = 'l' + str(id_in).rjust(3, '0')

    xml_out += (f'\t\t\t\t<{lib_id}-background>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Backgrounds</name>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_classfeatlist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.backgrounds@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t</{lib_id}-background>\n')

    return xml_out, id_in


def create_background_table(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''
    previous_group = ''

    # Backgrounds List
    # This controls the list that appears when you click on a Library menu

    xml_out += (f'\t\t<backgrounds>\n')
    xml_out += (f'\t\t\t<description type="string">Backgrounds</description>\n')
    xml_out += (f'\t\t\t<groups>\n')

    # Create individual item entries
    for background_dict in sorted(list_in, key=background_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', background_dict["name"])
        group_camel = name_camel[0:1].upper()

        # Check for new Group
        if group_camel != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</backgrounds{previous_group}>\n')

            # Open new Group
            xml_out += (f'\t\t\t\t<backgrounds{group_camel}>\n')
            xml_out += (f'\t\t\t\t\t<description type="string">{group_camel}</description>\n')
            xml_out += ('\t\t\t\t\t<powers>\n')

        # Backgrounds list entry
        xml_out += (f'\t\t\t\t\t\t<background{name_camel}>\n')
        xml_out += (f'\t\t\t\t\t\t\t<source type="string">{background_dict["name"]}</source>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.backgrounds.{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t\t</background{name_camel}>\n')

        previous_group = group_camel

    # Close final Group
    xml_out += ('\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t</backgrounds{previous_group}>\n')

    xml_out += (f'\t\t\t</groups>\n')
    xml_out += (f'\t\t</backgrounds>\n')

    return xml_out


def create_background_desc(list_in):
    backgrounds_out = ''

    if not list_in:
        return xml_out

    section_str = ''
    entry_str = ''
    name_lower = ''

    # Create individual item entries
    backgrounds_out += ('\t\t<backgrounds>\n')
    for background_dict in sorted(list_in, key=background_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', background_dict["name"])

        backgrounds_out += f'\t\t\t<{name_lower}>\n'
        backgrounds_out += f'\t\t\t\t<name type="string">{background_dict["name"]}</name>\n'
        backgrounds_out += '\t\t\t\t<source type="string">Background</source>\n'
        if background_dict["flavor"] != '':
            backgrounds_out += f'\t\t\t\t<flavor type="string">{background_dict["flavor"]}</flavor>\n'
        backgrounds_out += f'\t\t\t\t<description type="formattedtext">'
        if background_dict["description"] != '':
            backgrounds_out += f'{background_dict["description"]}'
        if background_dict["published"] != '':
            backgrounds_out += f'{background_dict["published"]}'
        backgrounds_out += f'</description>\n'
        if background_dict["prerequisite"] != '':
            backgrounds_out += (f'\t\t\t\t<prerequisite type="string">{background_dict["prerequisite"]}</prerequisite>\n')
        if background_dict["shortdescription"] != '':
            backgrounds_out += (f'\t\t\t\t<shortdescription type="string">{background_dict["shortdescription"]}</shortdescription>\n')
        backgrounds_out += f'\t\t\t</{name_lower}>\n'

    backgrounds_out += ('\t\t</backgrounds>\n')

    return backgrounds_out


def extract_background_db(db_in):
    backgrounds_out = []

    print('\n\n\n=========== BACKGROUNDS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

#        if name_str not in ['Auspicious Birth']:
#            continue
#        print(name_str)

        description_str = ''
        flavor_str = ''
        prerequisite_str = '' # prerequisite is the Prerequisite column on the list
        published_str = ''
        shortdescription_str = '' # shortdescription is the Benefit column on the list
        
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

        # Name
        name_tag = parsed_html.find('h1', class_='player').extract()
        if name_tag:
            name_str = name_tag.text

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

        # Prerequisite / Short Description (Benefit) / Description
        for desc in desc_list:
            if prerequisite_tag := re.search(r'^Prerequisite:\s*(.*)\s*$', desc):
                prerequisite_str = prerequisite_tag.group(1)
            elif shortdescription_tag := re.search(r'^Associated Skills:\s*(.*)\s*$', desc):
                shortdescription_str += desc
            elif shortdescription_tag := re.search(r'^Benefit:\s*(.*)\s*$', desc):
                if shortdescription_str != '':
                    shortdescription_str += '.\\n'
                shortdescription_str += desc
            description_str += ('<p>' + desc + '</p>').strip()
        # bold the Prerequisite, Type & Campaign Setting headings
        description_str = re.sub(r'(Campaign Setting:|Prerequisite:|Type:)', r'<b>\1</b>', description_str)            
        # italicize the Associated Skills Benefit headings
        description_str = re.sub(r'(Associated Skills:|Benefit:)', r'<i>\1</i>', description_str)            

        export_dict = {}
        export_dict["description"] = description_str
        export_dict["flavor"] = flavor_str
        export_dict["name"] = name_str
        export_dict["prerequisite"] = prerequisite_str
        export_dict["published"] = published_str
        export_dict["shortdescription"] = shortdescription_str

        # Append a copy of generated item dictionary
        backgrounds_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(backgrounds_out)) + ' entries exported.')

    return backgrounds_out
