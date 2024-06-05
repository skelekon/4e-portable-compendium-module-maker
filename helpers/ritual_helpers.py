import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .create_db import create_db

from helpers.mi_helpers import mi_list_sorter
from helpers.mi_helpers import multi_level

def ritual_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)

def create_ritual_library(list_in, name_in):
    xml_out = ''

    if not list_in:
        return xml_out, id_in

    settings.lib_id += 1

    # Set the name of the top-level XML tag
    if re.search('(Martial Practices)', name_in):
        list_str = 'practices'
    else:
        list_str = 'rituals'

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_rituallist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.{list_str}@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">{name_in}</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out

def create_ritual_list(list_in, name_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Set the name of the top-level XML tag
    if re.search('(Martial Practices)', name_in):
        list_str = 'practices'
    else:
        list_str = 'rituals'

    # Ritual List
    # This controls the table that appears when you click on a Library menu

    xml_out += (f'\t\t<{list_str}>\n')
    xml_out += (f'\t\t\t<description type="string">{name_in}</description>\n')
    xml_out += ('\t\t\t<groups>\n')

    # Create individual item entries
    for ritual_dict in sorted(list_in, key=ritual_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', ritual_dict["name"]).lower()

        # Rituals list entry
        xml_out += (f'\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_ritual</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.rituals.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{ritual_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t</{name_lower}>\n')

    xml_out += ('\t\t\t</groups>\n')
    xml_out += (f'\t\t</{list_str}>\n')

    return xml_out

def create_ritual_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    for ritual_dict in sorted(list_in, key=ritual_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', ritual_dict["name"]).lower()

        xml_out += (f'\t\t\t<{name_lower}>\n')
        xml_out += (f'\t\t\t\t<category type="string">{ritual_dict["category"]}</category>\n')
        xml_out += (f'\t\t\t\t<component type="string">{ritual_dict["component"]}</component>\n')
        xml_out += (f'\t\t\t\t<details type="formattedtext">{ritual_dict["details"]}</details>\n')
        if ritual_dict["duration"] != '':
            xml_out += (f'\t\t\t\t<duration type="string">{ritual_dict["duration"]}</duration>\n')
        if ritual_dict["flavor"] != '':
            xml_out += (f'\t\t\t\t<flavor type="string">{ritual_dict["flavor"]}</flavor>\n')
        xml_out += (f'\t\t\t\t<level type="string">{ritual_dict["level"]}</level>\n')
        xml_out += (f'\t\t\t\t<name type="string">{ritual_dict["name"]}</name>\n')
        if ritual_dict["prerequisite"] != '':
            xml_out += (f'\t\t\t\t<prerequisite type="string">{ritual_dict["prerequisite"]}</prerequisite>\n')
        xml_out += (f'\t\t\t\t<price type="string">{ritual_dict["price"]}</price>\n')
        if ritual_dict["skill"] != '':
            xml_out += (f'\t\t\t\t<skill type="string">{ritual_dict["skill"]}</skill>\n')
        xml_out += (f'\t\t\t\t<time type="string">{ritual_dict["time"]}</time>\n')
        xml_out += (f'\t\t\t</{name_lower}>\n')

    return xml_out

def extract_ritual_db(db_in, filter_in):
    ritual_out = []

    print('\n\n\n=========== ' + filter_in.upper() + ' ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

##        if name_str not in ['Aberrant Totemic Link']:
##            continue
        
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
        skill_str =  ''
        time_str = ''

        # Category
        if category_tag := parsed_html.find(string=re.compile('^Category')):
            category_str = re.sub(':\s*', '', category_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

        # Component
        if component_tag := parsed_html.find(string=re.compile('^Component')):
            component_str = re.sub(':\s*', '', component_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

        # Classify as Martial Practice, Ritual or Alchemical Formaula
        if re.search(r'(Martial Practice)', category_str, re.IGNORECASE):
            class_str = 'Practice'
        elif re.search(r'(See Alchemical|See below|See the item\'s price)', component_str, re.IGNORECASE)\
           or name_str in ['Grayflower Perfume', 'Keen Oil', 'Panther Tears']:
            class_str = 'Formula'
        else:
            class_str = 'Ritual'

        # only Martial Practices and Rituals and handled in this module
        if (re.search(f'^({filter_in})$', class_str)):

            # Duration
            if duration_tag := parsed_html.find(string=re.compile('^Duration')):
                duration_str = re.sub(':\s*', '', duration_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Flavor
            if flavor_tag := parsed_html.select_one('#detail > i'):
                flavor_str = flavor_tag.text

            # Level
            if level_tag := parsed_html.find(string=re.compile('^Level')):
                level_str = re.sub(':\s*', '', level_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Prerequisite
            prerequisite_tag = parsed_html.find(string=re.compile('^Prerequisite'))
            if prerequisite_tag:
                prerequisite_str = re.sub(':\s*', '', prerequisite_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Price
            if price_tag := parsed_html.find(string=re.compile('^Market Price')):
                price_str = re.sub(':\s*', '', price_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Skill
            if skill_tag := parsed_html.find(string=re.compile('^Key Skill')):
                skill_str = re.sub(':\s*', '', skill_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Time
            if time_tag := parsed_html.find(string=re.compile('^Time')):
                time_str = re.sub(':\s*', '', time_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Details
            if detail_tag := parsed_html.find('div', id='detail'):
                for tag in detail_tag.find_all('p'):
                    # skip heading & flavor
                    if tag.name in ['h1', 'i']:
                        continue
                    # remove the stats tag
                    if stats_tag := tag.find(class_='ritualstats'):
                        continue
                    # remove the tag class
                    del tag['class']
                    # remove the a tag
                    if anchor_tag := tag.find('a'):
                        anchor_tag.replaceWithChildren()
                    # append details
                    details_str += str(tag)

            # turn <br/> into new <p> as line breaks inside <p> don't render in formattedtext
            details_str = re.sub(r'(^\s*<br/>|<br/>\s*$)', r'', details_str)
            details_str = re.sub(r'<br/>', r'</p><p>', details_str)

            # replace <th> with <td><b> as FG appear to not render <th> correctly
            details_str = re.sub(r'<th>', r'<td><b>', details_str)
            details_str = re.sub(r'</th>', r'</b></td>', details_str)

            if int(level_str) >= settings.min_lvl and int(level_str) <= settings.max_lvl:
                export_dict = {}
                export_dict["category"] = category_str
                export_dict["class"] = class_str
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
