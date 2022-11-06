import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.create_db import create_db

# this allows for variable sorting by overwriting the GroupID value
def disease_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


# This creates the top-level menus when you select a Module
def create_disease_library(id_in):
    xml_out = ''

    id_in += 1
    lib_id = 'l' + str(id_in).rjust(3, '0')

    xml_out += (f'\t\t\t\t<{lib_id}-diseases>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Diseases</name>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.diseases@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t</{lib_id}-diseases>\n')

    return xml_out, id_in


# This controls the table that appears when you click on a Library menu
def create_disease_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''

    # Races List
    # This controls the table that appears when you click on a Library menu

    xml_out += ('\t\t<diseases>\n')
    xml_out += (f'\t\t\t<name type="string">Diseases</name>\n')
    xml_out += ('\t\t\t<index>\n')

    # Create individual item entries
    for disease_dict in sorted(list_in, key=disease_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', disease_dict["name"])

        # Races list entry
        xml_out += (f'\t\t\t\t<disease{name_camel}>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{disease_dict["name"]}</name>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_disease</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.diseases.{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t</disease{name_camel}>\n')

    xml_out += ('\t\t\t</index>\n')
    xml_out += ('\t\t</diseases>\n')

    return xml_out


def create_disease_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    xml_out += ('\t\t<diseases>\n')
    for disease_dict in sorted(list_in, key=disease_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', disease_dict["name"])

        xml_out += (f'\t\t\t<{name_camel}>\n')
        xml_out += (f'\t\t\t\t<name type="string">{disease_dict["name"]}</name>\n')
        if disease_dict["flavor"] != '':
            xml_out += (f'\t\t\t\t<flavor type="string">{disease_dict["flavor"]}</flavor>\n')
        if disease_dict["level"] != '':
            xml_out += (f'\t\t\t\t<level type="number">{disease_dict["level"]}</level>\n')
        if disease_dict["stable"] != '':
            xml_out += (f'\t\t\t\t<stable type="number">{disease_dict["stable"]}</stable>\n')
        if disease_dict["improve"] != '':
            xml_out += (f'\t\t\t\t<improve type="number">{disease_dict["improve"]}</improve>\n')
        if disease_dict["stage000"] != '':
            xml_out += (f'\t\t\t\t<stage000 type="string">{disease_dict["stage000"]}</stage000>\n')
        if disease_dict["stage001"] != '':
            xml_out += (f'\t\t\t\t<stage001 type="string">{disease_dict["stage001"]}</stage001>\n')
        if disease_dict["stage002"] != '':
            xml_out += (f'\t\t\t\t<stage002 type="string">{disease_dict["stage002"]}</stage002>\n')
        if disease_dict["stage003"] != '':
            xml_out += (f'\t\t\t\t<stage003 type="string">{disease_dict["stage003"]}</stage003>\n')
        if disease_dict["stage004"] != '':
            xml_out += (f'\t\t\t\t<stage004 type="string">{disease_dict["stage004"]}</stage004>\n')
        if disease_dict["stage005"] != '':
            xml_out += (f'\t\t\t\t<stage005 type="string">{disease_dict["stage005"]}</stage005>\n')
        xml_out += (f'\t\t\t</{name_camel}>\n')

    xml_out += ('\t\t</diseases>\n')

    return xml_out


def extract_disease_db(db_in):
    diseases_out = []

    print('\n\n\n=========== DISEASES ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')
        level_str =  row["Level"].replace('\\', '')

#        if name_str not in ['Meenlock Corruption']:
#            continue
#        print(name_str)

        description_str = ''
        flavor_str = ''
        improve_str = ''
        published_str = ''
        stable_str = ''
        stage000_str = ''
        stage001_str = ''
        stage002_str = ''
        stage003_str = ''
        stage004_str = ''
        stage005_str = ''
        
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
        if flavor_tag := parsed_html.select_one('.flavor > i'):
            flavor_str = flavor_tag.text.strip()

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
            elif idx < len(raw_list) - 1 and (raw_list[idx + 1].strip())[0] == ':':
                desc_list.append(raw_str + raw_list[idx + 1])
                skip_flag = True
            else:
                desc_list.append(raw_str)

        # Parse the combined strings to get the remaining fields
        for desc in desc_list:
            if label_match := re.search(r'^\s*(.*?)\s*:\s*(.*?)\s*$', desc):
                if label_match.group(1) == 'Stage 0':
                    stage000_str = label_match.group(2)
                elif label_match.group(1) == 'Stage 1':
                    stage001_str = label_match.group(2)
                elif label_match.group(1) == 'Stage 2':
                    stage002_str = label_match.group(2)
                elif label_match.group(1) == 'Stage 3':
                    stage003_str = label_match.group(2)
                elif label_match.group(1) == 'Stage 4':
                    stage004_str = label_match.group(2)
                elif label_match.group(1) == 'Stage 5':
                    stage005_str = label_match.group(2)
                elif label_match.group(2) == 'No Change':
                    stable_str = re.sub(r'[^0-9].*$', '', label_match.group(1))
                elif label_match.group(2) == 'The stage of the disease decreases by one.':
                    improve_str = re.sub(r'[^0-9].*$', '', label_match.group(1))


        export_dict = {}
        export_dict["flavor"] = flavor_str
        export_dict["improve"] = improve_str
        export_dict["level"] = level_str
        export_dict["name"] = name_str
        export_dict["published"] = published_str
        export_dict["stable"] = stable_str
        export_dict["stage000"] = stage000_str
        export_dict["stage001"] = stage001_str
        export_dict["stage002"] = stage002_str
        export_dict["stage003"] = stage003_str
        export_dict["stage004"] = stage004_str
        export_dict["stage005"] = stage005_str

        # Append a copy of generated item dictionary
        diseases_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(diseases_out)) + ' entries exported.')

    return diseases_out
