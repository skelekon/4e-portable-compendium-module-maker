import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def paragon_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_paragon_library(id_in):
    xml_out = ''

    id_in += 1
    lib_id = 'l' + str(id_in).rjust(3, '0')

    xml_out += (f'\t\t\t\t<{lib_id}-paragon>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Paragon Paths</name>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_classfeatlist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.paragonpaths@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t</{lib_id}-paragon>\n')

    return xml_out, id_in


def create_paragon_table(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''
    previous_group = ''

    # Paragon Paths List
    # This controls the list that appears when you click on a Library menu

    xml_out += (f'\t\t<paragonpaths>\n')
    xml_out += (f'\t\t\t<description type="string">Paragon Paths</description>\n')
    xml_out += (f'\t\t\t<groups>\n')

    # Create individual item entries
    for paragon_dict in sorted(list_in, key=paragon_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', paragon_dict["name"])
        group_camel = name_camel[0:1].upper()

        # Check for new Group
        if group_camel != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</paragonpaths{previous_group}>\n')

            # Open new Group
            xml_out += (f'\t\t\t\t<paragonpaths{group_camel}>\n')
            xml_out += (f'\t\t\t\t\t<description type="string">{group_camel}</description>\n')
            xml_out += ('\t\t\t\t\t<powers>\n')

        # Paragon Paths list entry
        xml_out += (f'\t\t\t\t\t\t<paragon{name_camel}>\n')
        xml_out += (f'\t\t\t\t\t\t\t<source type="string">{paragon_dict["name"]}</source>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.paragonpaths.{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t\t</paragon{name_camel}>\n')

        previous_group = group_camel

    # Close final Group
    xml_out += ('\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t</paragonpaths{previous_group}>\n')

    xml_out += (f'\t\t\t</groups>\n')
    xml_out += (f'\t\t</paragonpaths>\n')

    return xml_out


def create_paragon_desc(list_in):
    paragon_out = ''
    featuredesc_out = ''

    if not list_in:
        return xml_out

    section_str = ''
    entry_str = ''
    name_lower = ''

    # Create individual item entries
    paragon_out += ('\t\t<paragonpaths>\n')
    for paragon_dict in sorted(list_in, key=paragon_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', paragon_dict["name"])

        paragon_out += f'\t\t\t<{name_lower}>\n'
        paragon_out += f'\t\t\t\t<name type="string">{paragon_dict["name"]}</name>\n'
        paragon_out += '\t\t\t\t<source type="string">Paragon Path</source>\n'
        if paragon_dict["prerequisite"] != '':
            paragon_out += (f'\t\t\t\t<prerequisite type="string">{paragon_dict["prerequisite"]}</prerequisite>\n')
        if paragon_dict["flavor"] != '':
            paragon_out += f'\t\t\t\t<flavor type="string">{paragon_dict["flavor"]}</flavor>\n'
        paragon_out += f'\t\t\t\t<description type="formattedtext">\n'
        if paragon_dict["description"] != '':
            paragon_out += f'{paragon_dict["description"]}'
        if paragon_dict["features"] != '':
            paragon_out += f'{paragon_dict["features"]}'
        if paragon_dict["powers"] != '':
            paragon_out += f'{paragon_dict["powers"]}'
        if paragon_dict["published"] != '':
            paragon_out += f'{paragon_dict["published"]}'
#        xml_out += (f'\t\t\t\t<shortdescription type="string">{paragon_dict["shortdescription"]}</shortdescription>\n')
        paragon_out += f'\n\t\t\t\t</description>\n'
        paragon_out += f'\t\t\t</{name_lower}>\n'

        # Create all Required Power entries
        featuredesc_out += paragon_dict["featuredesc"]

    paragon_out += ('\t\t</paragonpaths>\n')

    return paragon_out, featuredesc_out


def create_feature(feature_dict, pathname_in):
    link_out = ''
    featuredesc_out = ''

    # Parse the feature name to determine the various fields for the Feature card
    heading_str = re.sub(r'\([0-9].*?level\)', '', feature_dict["name"], re.IGNORECASE).strip()
    prerequisites_str = pathname_in + ' Paragon Path'
    if level_match :=re.search(r'\(([0-9].*?level)\)', feature_dict["name"], re.IGNORECASE):
        level_str = level_match.group(1)
        prerequisites_str += ', ' + level_str
    else:
        level_str = ''

    pathname_camel = re.sub('[^a-zA-Z0-9_]', '', pathname_in)
    feature_camel = re.sub('[^a-zA-Z0-9_]', '', feature_dict["name"])
    feature_desc = clean_formattedtext(feature_dict["desc"])

    link_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.features.{pathname_camel}{feature_camel}@{settings.library}">{feature_dict["name"]}</link>\n')

    featuredesc_out += f'\t\t\t<{pathname_camel}{feature_camel}>\n'
    featuredesc_out += f'\t\t\t\t<name type="string">{heading_str}</name>\n'
    featuredesc_out += f'\t\t\t\t<source type="string">{pathname_in} Feature</source>\n'
    featuredesc_out += f'\t\t\t\t<prerequisite type="string">{prerequisites_str}</prerequisite>\n'
    featuredesc_out += f'\t\t\t\t<description type="formattedtext"><p><b>Prerequisite:</b>{prerequisites_str}</p>{feature_desc}</description>\n'
    featuredesc_out += f'\t\t\t</{pathname_camel}{feature_camel}>\n'
    
    return link_out, featuredesc_out


def create_power(power_dict, name_in):
    xml_out = ''
    power_camel = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"])
    xml_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.powers.{power_camel}@{settings.library}">{power_dict["name"]}</link>\n')

    return xml_out


def extract_paragon_db(db_in):
    paragon_out = []

    print('\n\n\n=========== PARAGON PATHS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

#        if name_str not in ['Zephyr Warchief', 'Feytouched']:
#            continue
#        print(name_str)

        description_str = ''
        features_str = ''
        featuredesc_str = ''
        flavor_str = ''
        powers_str = ''
        prerequisite_str = ''
        published_str = ''
        shortdescription_str = ''
        
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

        # Features / Powers
        # these are the unique Features and Powers for each Paragon Path
        feature_list = []
        in_prerequisite = False
        in_feature = False
        in_power = False
        if feature_block := parsed_html.find('h1', class_='player'):
            for tag in feature_block.next_siblings:
                # skip this - it is just the PATH FEATURES heading
                if tag.name == 'h3' and tag.text.isupper():
                    continue
                # skip these if found as they are part of a Power description (the Powers parser will get them from ddiPower.sql)
                if isinstance(tag, Tag) and tag.has_attr('class') and tag.attrs.get('class')[0] in ['flavor', 'powerstat']:
                    continue
                # Flavor
                # don't want italics if they are a Power flavor
                if isinstance(tag, Tag) and not tag.select_one('.atwillpower, .encounterpower, .dailypower'):
                    if flavor_str == '' and tag.select_one('i'):
                        flavor_str = tag.text
                        continue
                # Prerequisite
                # skip the first tag after encountering Prerequisite as we have already grabbed it
                if in_prerequisite:
                    in_prerequisite = False
                    continue
                elif tag.text[0:12] == 'Prerequisite':
                    prerequisite_str = tag.next_sibling.strip()
                    description_str += f'<p><b>Prerequisite:</b>{prerequisite_str}</p>\n'
                    in_prerequisite = True
                    continue
                if tag.name == 'b':
                    # if we are already in a feature then this is the end
                    if in_feature:
                        feature_dict["desc"] += '</p>'
                        ftr_link, ftr_desc = create_feature(feature_dict, name_str)
                        features_str += ftr_link
                        featuredesc_str += ftr_desc
                        feature_list.append(copy.copy(feature_dict))
                        in_feature = False
                    # start capturing the feature details
                    in_feature = True
                    feature_dict = {}
                    feature_dict["name"] = tag.text
                    feature_dict["desc"] = '<p>'
                # found a power so just create a link to it (the Powers parser will create the actual Power card)
                elif isinstance(tag, Tag) and tag.select_one('.atwillpower, .encounterpower, .dailypower'):
                    h1 = tag.find('h1', class_=re.compile(r'(atwillpower|encounterpower|dailypower)'))
                    in_power = True
                else:
                    # remove leading colon and append to feature or description
                    if in_feature:
                        feature_dict["desc"] += re.sub(r'^\s*:+\s*', '', str(tag))
                    else:
                        description_str += '<p>' + re.sub(r'^\s*:+\s*', '', str(tag)) + '</p>\n'

                if in_power:
                    # if we are already in a feature then this is the end
                    if in_feature:
                        feature_dict["desc"] += '</p>'
                        ftr_link, ftr_desc = create_feature(feature_dict, name_str)
                        features_str += ftr_link
                        featuredesc_str += ftr_desc
                        feature_list.append(copy.copy(feature_dict))
                        in_feature = False
                    pwr_type = ''
                    pwr_name = ''
                    for item in h1:
                        if isinstance(item, NavigableString):
                            pwr_name = item
                        else:
                            pwr_type = item.text
                    power_dict = {}
                    power_dict["type"] = pwr_type
                    power_dict["name"] = pwr_name
                    settings.paragon_power_list.append(pwr_name)
                    pwr_link = create_power(power_dict, name_str)
                    powers_str += pwr_link
                    in_power = False

        description_str = clean_formattedtext(description_str)

        # Add a heading to Features section
        if features_str != '':
            features_str = f'<p><b>{name_str.upper()} PATH FEATURES</b></p>\n' + features_str

        # Add a heading to Powers section
        if powers_str != '':
            powers_str = f'<p><b>{name_str.upper()} POWERS</b></p>\n' + powers_str


        export_dict = {}
        export_dict["description"] = description_str
        export_dict["features"] = features_str
        export_dict["featuredesc"] = featuredesc_str
        export_dict["flavor"] = flavor_str
        export_dict["name"] = name_str
        export_dict["powers"] = powers_str
        export_dict["prerequisite"] = prerequisite_str
        export_dict["published"] = published_str
        export_dict["shortdescription"] = shortdescription_str

        # Append a copy of generated item dictionary
        paragon_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(paragon_out)) + ' entries exported.')

    return paragon_out
