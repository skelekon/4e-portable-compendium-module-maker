import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

def library_list_sorter(entry_in):
    class_id = entry_in["class_id"]

    return (class_id)


def feat_list_sorter(entry_in):
    class_id = entry_in["class_id"]
    name = entry_in["name"]

    return (class_id, name)


def create_feat_library(id_in, list_in):
    xml_out = ''

    if not list_in:
        return xml_out, id_in

    previous_class = ''
    for feat_dict in sorted(list_in, key=library_list_sorter):
        if feat_dict["class"] != previous_class:
            previous_class = feat_dict["class"]
            class_camel = re.sub('[^a-zA-Z0-9_]', '', feat_dict["class"])

            id_in += 1
            lib_id = 'l' + str(id_in).rjust(3, '0')

            xml_out += (f'\t\t\t\t<{lib_id}-feats{class_camel}>\n')
            xml_out += (f'\t\t\t\t\t<name type="string">Feats - {feat_dict["class"]}</name>\n')
            xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
            xml_out += ('\t\t\t\t\t\t<class>reference_classfeatlist</class>\n')
            xml_out += (f'\t\t\t\t\t\t<recordname>lists.feats.{class_camel}@{settings.library}</recordname>\n')
            xml_out += ('\t\t\t\t\t</librarylink>\n')
            xml_out += (f'\t\t\t\t</{lib_id}-feats{class_camel}>\n')
    return xml_out, id_in


def create_feat_table(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    previous_class = ''
    previous_group = ''
    class_camel = ''

    # Feat List
    # This controls the table that appears when you click on a Library menu
    xml_out += ('\t\t<feats>\n')

    # Create individual item entries
    for feat_dict in sorted(list_in, key=feat_list_sorter):
        class_camel = re.sub('[^a-zA-Z0-9_]', '', feat_dict["class"])
        name_camel = re.sub('[^a-zA-Z0-9_]', '', feat_dict["name"])
        group_camel = name_camel[0:1].upper()

        #Check for new Class
        if class_camel != previous_class:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t\t</{previous_class}{previous_group}>\n')

            # Close previous Class
            if previous_class != '':
                xml_out += ('\t\t\t\t</groups>\n')
                xml_out += (f'\t\t\t</{previous_class}>\n')

            # Open new Class
            previous_group = group_camel
            xml_out += (f'\t\t\t<{class_camel}>\n')
            xml_out += (f'\t\t\t\t<description type="string">{feat_dict["class"]} Feats</description>\n')
            xml_out += ('\t\t\t\t<groups>\n')
    
            # Open new Group
            xml_out += (f'\t\t\t\t\t<{class_camel}{group_camel}>\n')
            xml_out += (f'\t\t\t\t\t\t<description type="string">{group_camel}</description>\n')
            xml_out += ('\t\t\t\t\t\t<powers>\n')

        # Check for new Group
        if group_camel != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t\t</{class_camel}{previous_group}>\n')

            # Open new Group if not the first entry in the table
            if previous_class != '':
                xml_out += (f'\t\t\t\t\t<{class_camel}{group_camel}>\n')
                xml_out += (f'\t\t\t\t\t\t<description type="string">{group_camel}</description>\n')
                xml_out += ('\t\t\t\t\t\t<powers>\n')

        # Feats list entry
        xml_out += (f'\t\t\t\t\t\t\t<feat{name_camel}>\n')
        xml_out += ('\t\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t\t<recordname>reference.feats.{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<source type="string">{feat_dict["name"]}</source>\n')
        xml_out += (f'\t\t\t\t\t\t\t</feat{name_camel}>\n')

        previous_class = class_camel
        previous_group = group_camel

    # Close final Group
    xml_out += ('\t\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t\t</{class_camel}{group_camel}>\n')

    # Close final Class
    xml_out += ('\t\t\t\t</groups>\n')
    xml_out += (f'\t\t\t</{class_camel}>\n')

    xml_out += ('\t\t</feats>\n')

    return xml_out


def create_feat_desc(list_in):
    feats_out = ''

    if not list_in:
        return feats_out

    section_str = ''
    entry_str = ''
    name_lower = ''

    # Create individual item entries
    feats_out += ('\t\t<feats>\n')
    for feat_dict in sorted(list_in, key=feat_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', feat_dict["name"])

        feats_out += (f'\t\t\t<{name_lower}>\n')
        feats_out += (f'\t\t\t\t<name type="string">{feat_dict["name"]}</name>\n')
        feats_out += (f'\t\t\t\t<description type="formattedtext">{feat_dict["description"]}</description>\n')
        feats_out += (f'\t\t\t\t<prerequisite type="string">{feat_dict["prerequisite"]}</prerequisite>\n')
        feats_out += (f'\t\t\t\t<shortdescription type="string">{feat_dict["shortdescription"]}</shortdescription>\n')
        if feat_dict["linkedpower"] != '':
            feats_out += (f'\t\t\t\t<linkedpowers>\n{feat_dict["linkedpower"]}\t\t\t\t</linkedpowers>\n')
        feats_out += (f'\t\t\t</{name_lower}>\n')

    feats_out += ('\t\t</feats>\n')

    return feats_out


def create_linked_power(power_in):
    power_camel = re.sub('[^a-zA-Z0-9_]', '', power_in)

    power_out = ''
    power_out += (f'\t\t\t\t\t<power{power_camel}>\n')
    power_out += ('\t\t\t\t\t\t<link type="windowreference">\n')
    power_out += ('\t\t\t\t\t\t\t<class>powerdesc</class>\n')
    power_out += (f'\t\t\t\t\t\t\t<recordname>reference.powers.{power_camel}@{settings.library}</recordname>\n')
    power_out += ('\t\t\t\t\t\t</link>\n')
    power_out += (f'\t\t\t\t\t</power{power_camel}>\n')
    
    return power_out


def extract_feat_db(db_in):
    feats_out = []

    print('\n\n\n=========== FEATS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')
        class_str =  row["Tier"].replace('\\', '')

##        if name_str != 'Anthem of Civilization':
##            continue

        class_id = ''
        description_str = ''
        linkedpower_str = ''
        prerequisite_str = ''
        published_str = ''
        shortdescription_str = ''

        # Class ID (top level sort order)
        if class_str == 'Heroic':
            class_id = 1
        elif class_str == 'Paragon':
            class_id = 2
        elif class_str == 'Epic':
            class_id = 3
        else:
            class_str = 'Other'
            class_id = 4

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
            published_str = str(published_tag)

        # Name
        name_tag = parsed_html.find('h1', class_='player').extract()
        if name_tag:
            name_str = name_tag.text

        # Build list of strings for Prerequisite / Short Description (Benefit) / Description
        detail_div = parsed_html.find('div', id='detail')

        # Copy detail strings to a list of strings
        raw_list = []
        for div in detail_div.strings:
            if div.replace('\n', '').strip() != '' and not re.search('Tier$', div):
                raw_list.append(re.sub(r'&', r'&amp;', div))

        # Combine consecutive items where next item starts with a ':'
        desc_list = []
        skip_flag = False;
        for idx, raw_str in enumerate(raw_list):
            if skip_flag:
                skip_flag = False
            elif idx < len(raw_list) - 1 and raw_list[idx + 1][0:1] == ':':
                desc_list.append(raw_str + raw_list[idx + 1])
                skip_flag = True
            else:
                desc_list.append(raw_str)

        power_list = []
        power_flag = False
        # Prerequisite / Short Description (Benefit) / Description
        for desc in desc_list:
            if re.search('Feat (Attack|Utility)', desc):
                power_flag = True
            if power_flag:
                power_list.append(desc)
            else:
                if prerequisite_tag := re.search(r'^Prerequisite:\s*(.*)\s*$', desc):
                    prerequisite_str = prerequisite_tag.group(1)
                elif shortdescription_tag := re.search(r'^Benefit:\s*(.*)\s*$', desc):
                    shortdescription_str = shortdescription_tag.group(1)
                description_str += ('<p>' + desc + '</p>').strip()
        # bold the Prerequisite & Benefit headings
        description_str = re.sub(r'(Prerequisite:|Benefit:)', r'<b>\1</b>', description_str)            

        # this presumes there is one power at most per Feat. Cahulaks Novice & Gythka Specialist have 2
        if power_flag:
            settings.feat_power_list.append(power_list[1])
            linkedpower_str = create_linked_power(power_list[1])

        export_dict = {}
        export_dict["class"] = class_str
        export_dict["class_id"] = class_id
        export_dict["description"] = description_str + published_str
        export_dict["name"] = name_str
        export_dict["linkedpower"] = linkedpower_str
        export_dict["prerequisite"] = prerequisite_str
        export_dict["shortdescription"] = shortdescription_str

        # Append a copy of generated item dictionary
        feats_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(feats_out)) + ' entries exported.')

    return feats_out
