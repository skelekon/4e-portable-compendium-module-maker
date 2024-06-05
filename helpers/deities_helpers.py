import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def deities_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_deities_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_classfeatlist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.deities@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Deities</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_deities_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    previous_group = ''

    # Deities List
    # This controls the list that appears when you click on a Library menu
    # Start a new group for each first letter

    xml_out += (f'\t\t<deities>\n')
    xml_out += (f'\t\t\t<description type="string">Deities</description>\n')
    xml_out += (f'\t\t\t<groups>\n')

    # Create individual item entries
    for deity_dict in sorted(list_in, key=deities_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', deity_dict["name"]).lower()
        group_letter = name_lower[0:1]

        # Check for new Group
        if group_letter != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</deities_{previous_group}>\n')

            # Open new Group
            xml_out += (f'\t\t\t\t<deities_{group_letter}>\n')
            xml_out += (f'\t\t\t\t\t<description type="string">{group_letter.upper()}</description>\n')
            xml_out += ('\t\t\t\t\t<powers>\n')

        # Deities list entry
        xml_out += (f'\t\t\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.deities.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
#        xml_out += (f'\t\t\t\t\t\t\t<name type="string">{deity_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t\t\t</{name_lower}>\n')

        previous_group = group_letter

    # Close final Group
    xml_out += ('\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t</deities_{previous_group}>\n')

    xml_out += (f'\t\t\t</groups>\n')
    xml_out += (f'\t\t</deities>\n')

    return xml_out


def create_deities_cards(list_in):
    deities_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    deities_out += ('\t\t<deities>\n')
    for deity_dict in sorted(list_in, key=deities_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', deity_dict["name"]).lower()

        deities_out += f'\t\t\t<{name_lower}>\n'
        deities_out += f'\t\t\t\t<description type="formattedtext">'
        if deity_dict["description"] != '':
            deities_out += f'{deity_dict["description"]}'
        if deity_dict["published"] != '':
            deities_out += f'{deity_dict["published"]}'
        deities_out += f'</description>\n'
        if deity_dict["flavor"] != '':
            deities_out += f'\t\t\t\t<flavor type="string">{deity_dict["flavor"]}</flavor>\n'
        deities_out += f'\t\t\t\t<name type="string">{deity_dict["name"]}</name>\n'
        if deity_dict["prerequisite"] != '':
            deities_out += (f'\t\t\t\t<prerequisite type="string">{deity_dict["prerequisite"]}</prerequisite>\n')
        if deity_dict["shortdescription"] != '':
            deities_out += (f'\t\t\t\t<shortdescription type="string">{deity_dict["shortdescription"]}</shortdescription>\n')
        deities_out += '\t\t\t\t<source type="string">Deity</source>\n'
        deities_out += f'\t\t\t</{name_lower}>\n'

    deities_out += ('\t\t</deities>\n')

    return deities_out


def extract_deities_db(db_in):
    deities_out = []

    print('\n\n\n=========== DEITIES ===========')
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
            elif idx < len(raw_list) - 1 and raw_list[idx].strip() in ['Adjective:', 'Alignment:', 'Domain:', 'Dominion:', 'Gender:', 'Priests:', 'Realm:', 'Sphere:', 'Territory:', 'Type:']:
                desc_list.append(raw_str + raw_list[idx + 1])
                skip_flag = True
            else:
                desc_list.append(raw_str)

        # Prerequisite / Short Description (Benefit) / Description
        for desc in desc_list:
            if prerequisite_tag := re.search(r'^Alignment:\s*(.*)\s*$', desc):
                prerequisite_str = prerequisite_tag.group(1)
            elif shortdescription_tag := re.search(r'^Domain:\s*(.*)\s*$', desc):
                shortdescription_str += desc
            description_str += ('<p>' + desc + '</p>').strip()
        # bold the Prerequisite, Type & Campaign Setting headings
        description_str = re.sub(r'(Adjective:|Alignment:|Domain:|Dominion:|Gender:|Priests:|Realm:|Sphere:|Territory:|Type:)', r'<b>\1</b>', description_str)            

        export_dict = {}
        export_dict["description"] = description_str
        export_dict["flavor"] = flavor_str
        export_dict["name"] = name_str
        export_dict["prerequisite"] = prerequisite_str
        export_dict["published"] = published_str
        export_dict["shortdescription"] = shortdescription_str

        # Append a copy of generated item dictionary
        deities_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(deities_out)) + ' entries exported.')

    return deities_out
