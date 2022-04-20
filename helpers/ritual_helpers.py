import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .create_db import create_db

from .mod_helpers import mi_list_sorter
from .mod_helpers import multi_level

def ritual_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)

def create_ritual_library(id_in, library_in, list_in, name_in):
    xml_out = ''

    if not list_in:
        return xml_out, id_in


    id_in += 1
    entry_id = '0000'[0:len('0000')-len(str(id_in))] + str(id_in)

    xml_out += (f'\t\t\t\t<a{entry_id}rituals>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_rituallist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>rituallists@{library_in}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">{name_in}</name>\n')
    xml_out += (f'\t\t\t\t</a{entry_id}rituals>\n')

    return xml_out, id_in

def create_ritual_table(list_in, library_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''

    # Ritual List
    # This controls the table that appears when you click on a Library menu

    xml_out += ('\t\t<description type="string">Rituals</description>\n')
    xml_out += ('\t\t<groups>\n')

    # Create individual item entries
    for ritual_dict in sorted(list_in, key=ritual_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', ritual_dict["name"])

        # Rituals list entry
        xml_out += (f'\t\t\t<ritual{name_camel}>\n')
        xml_out += ('\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t<class>reference_ritual</class>\n')
        xml_out += (f'\t\t\t\t\t<recordname>ritualdesc.ritual{name_camel}@{library_in}</recordname>\n')
        xml_out += ('\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t<source type="string">{ritual_dict["name"]}</source>\n')
        xml_out += (f'\t\t\t</ritual{name_camel}>\n')

    xml_out += ('\t\t</groups>\n')

    return xml_out

def create_ritual_desc(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''

    # Create individual item entries
    for ritual_dict in sorted(list_in, key=ritual_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', ritual_dict["name"])

        xml_out += (f'\t\t<ritual{name_camel}>\n')
        xml_out += (f'\t\t\t<name type="string">{ritual_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t<category type="string">{ritual_dict["category"]}</category>\n')
        xml_out += (f'\t\t\t<component type="string">{ritual_dict["component"]}</component>\n')
        xml_out += (f'\t\t\t<details type="formattedtext">{ritual_dict["details"]}</details>\n')
        xml_out += (f'\t\t\t<duration type="string">{ritual_dict["duration"]}</duration>\n')
        xml_out += (f'\t\t\t<flavor type="string">{ritual_dict["flavor"]}</flavor>\n')
        xml_out += (f'\t\t\t<level type="string">{ritual_dict["level"]}</level>\n')
        xml_out += (f'\t\t\t<prerequisite type="string">{ritual_dict["prerequisite"]}</prerequisite>\n')
        xml_out += (f'\t\t\t<price type="string">{ritual_dict["price"]}</price>\n')
        xml_out += (f'\t\t\t<skill type="string">{ritual_dict["skill"]}</skill>\n')
        xml_out += (f'\t\t\t<time type="string">{ritual_dict["time"]}</time>\n')
        xml_out += (f'\t\t</ritual{name_camel}>\n')

    return xml_out

def extract_ritual_list(db_in, library_in, min_lvl, max_lvl, filter_in):
    ritual_out = []

    print('\n\n\n=========== RITUALS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')
        
        category_str = ''
        class_str = ''
        component_str = ''
        details_str = ''
        duration_str = ''
        flavor_str = ''
        level_str = ''
        price_str = ''
        prerequisite_str = ''
        published_str = ''
        section_id = 100
        skill_str =  ''
        time_str = ''

        # Component
        if component_tag := parsed_html.find(string=re.compile('^Component')):
            component_str = re.sub(':\w*', '', component_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

        if re.search(r'(See Alchemical Item|See below|See the item\'s price)', component_str):
            class_str = 'Alchemical Formulas'
        else:
            class_str = 'Rituals'

        if (re.search(f'^({filter_in})$', class_str)):
            section_id = 1

        if section_id < 100:

            # Category
            if category_tag := parsed_html.find(string=re.compile('^Category')):
                category_str = re.sub(':\w*', '', category_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Duration
            if duration_tag := parsed_html.find(string=re.compile('^Duration')):
                duration_str = re.sub(':\w*', '', duration_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Flavor
            if flavor_tag := parsed_html.select_one('#detail > i'):
                flavor_str = flavor_tag.text

            # Level
            if level_tag := parsed_html.find(string=re.compile('^Level')):
                level_str = re.sub(':\w*', '', level_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Prerequisite
            prerequisite_tag = parsed_html.find(string=re.compile('^Prerequisite'))
            if prerequisite_tag:
                prerequisite_str = re.sub(':\w*', '', prerequisite_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Price
            if price_tag := parsed_html.find(string=re.compile('^Market Price')):
                price_str = re.sub(':\w*', '', price_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Skill
            if skill_tag := parsed_html.find(string=re.compile('^Key Skill')):
                skill_str = re.sub(':\w*', '', skill_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Time
            if time_tag := parsed_html.find(string=re.compile('^Time')):
                time_str = re.sub(':\w*', '', time_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Details
            if detail_tag := parsed_html.find('div', id='detail'):
                for tag in detail_tag.find_all(recursive=False):
                    if tag.name in ['h1', 'i']:
                        continue
                    # skip if this contains the ritual info
                    if tag.find(class_='ritualstats'):
                        continue
                    del tag['class']
                    # remove the a tag
                    if anchor_tag := tag.find('a'):
                        anchor_tag.replaceWithChildren()
                    # append details
                    details_str += str(tag)
            # replace <th> with <td><b> as FG appear to not render <th> correctly
            details_str = re.sub(r'<th>', r'<td><b>', details_str)
            details_str = re.sub(r'</th>', r'</b></td>', details_str)

            export_dict = {}
            export_dict["category"] = category_str
            export_dict["component"] = component_str
            export_dict["details"] = details_str
            export_dict["duration"] = duration_str
            export_dict["flavor"] = flavor_str
            export_dict["level"] = level_str
            export_dict["name"] = name_str
            export_dict["prerequisite"] = prerequisite_str
            export_dict["price"] = price_str
            export_dict["skill"] = skill_str
            export_dict["time"] = time_str

            # Append a copy of generated item dictionary
            ritual_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(ritual_out)) + ' entries exported.')

    return ritual_out
