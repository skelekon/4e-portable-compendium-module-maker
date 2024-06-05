import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def heroic_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_heroic_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_classfeatlist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.heroicthemes@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Heroic Themes</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_heroic_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    previous_group = ''

    # Heroic Themes List
    # This controls the list that appears when you click on a Library menu
    # Start a new group for each first letter

    xml_out += (f'\t\t<heroicthemes>\n')
    xml_out += (f'\t\t\t<description type="string">Heroic Themes</description>\n')
    xml_out += (f'\t\t\t<groups>\n')

    # Create individual item entries
    for heroic_dict in sorted(list_in, key=heroic_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', heroic_dict["name"]).lower()
        group_letter = name_lower[0:1]

        # Check for new Group
        if group_letter != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</heroicthemes_{previous_group}>\n')

            # Open new Group
            xml_out += (f'\t\t\t\t<heroicthemes_{group_letter}>\n')
            xml_out += (f'\t\t\t\t<description type="string">{group_letter.upper()}</description>\n')
            xml_out += ('\t\t\t\t\t<powers>\n')

        # Heroic Themes list entry
        xml_out += (f'\t\t\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>reference.heroicthemes.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
#        xml_out += (f'\t\t\t\t\t\t\t<name type="string">{heroic_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t\t\t</{name_lower}>\n')

        previous_group = group_letter

    # Close final Group
    xml_out += ('\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t</heroicthemes_{previous_group}>\n')

    xml_out += (f'\t\t\t</groups>\n')
    xml_out += (f'\t\t</heroicthemes>\n')

    return xml_out


def create_heroic_cards(list_in):
    heroic_out = ''
    featuredesc_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    heroic_out += ('\t\t<heroicthemes>\n')
    for heroic_dict in sorted(list_in, key=heroic_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', heroic_dict["name"]).lower()

        heroic_out += f'\t\t\t<{name_lower}>\n'
        heroic_out += f'\t\t\t\t<description type="formattedtext">\n'
        if heroic_dict["description"] != '':
            heroic_out += f'{heroic_dict["description"]}'
        if heroic_dict["features"] != '':
            heroic_out += f'{heroic_dict["features"]}'
        if heroic_dict["powers"] != '':
            heroic_out += f'{heroic_dict["powers"]}'
        if heroic_dict["published"] != '':
            heroic_out += f'{heroic_dict["published"]}'
        heroic_out += f'\n\t\t\t\t</description>\n'
        if heroic_dict["flavor"] != '':
            heroic_out += f'\t\t\t\t<flavor type="string">{heroic_dict["flavor"]}</flavor>\n'
        heroic_out += f'\t\t\t\t<name type="string">{heroic_dict["name"]}</name>\n'
        if heroic_dict["prerequisite"] != '':
            heroic_out += (f'\t\t\t\t<prerequisite type="string">{heroic_dict["prerequisite"]}</prerequisite>\n')
#        xml_out += (f'\t\t\t\t<shortdescription type="string">{heroic_dict["shortdescription"]}</shortdescription>\n')
        heroic_out += '\t\t\t\t<source type="string">Heroic Theme</source>\n'
        heroic_out += f'\t\t\t</{name_lower}>\n'

        # Create all Required Power entries
        featuredesc_out += heroic_dict["featuredesc"]

    heroic_out += ('\t\t</heroicthemes>\n')

    return heroic_out, featuredesc_out


def create_feature(feature_dict, pathname_in):
    link_out = ''
    featuredesc_out = ''

    # Parse the feature name to determine the various fields for the Feature card
    heading_str = re.sub(r'\([0-9].*?level\)', '', feature_dict["name"], re.IGNORECASE).strip()
    prerequisites_str = pathname_in + ' Heroic Theme'
    if level_match :=re.search(r'\(([0-9].*?level)\)', feature_dict["name"], re.IGNORECASE):
        level_str = level_match.group(1)
        prerequisites_str += ', ' + level_str
    else:
        level_str = ''

    pathname_lower = re.sub('[^a-zA-Z0-9_]', '', pathname_in).lower()
    feature_lower = re.sub('[^a-zA-Z0-9_]', '', feature_dict["name"]).lower()
    feature_desc = clean_formattedtext(feature_dict["desc"])

    link_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.features.{pathname_lower}{feature_lower}@{settings.library}">{feature_dict["name"]}</link>\n')

    featuredesc_out += f'\t\t\t<{pathname_lower}{feature_lower}>\n'
    featuredesc_out += f'\t\t\t\t<description type="formattedtext"><p><b>Prerequisite:</b>{prerequisites_str}</p>{feature_desc}</description>\n'
    featuredesc_out += f'\t\t\t\t<name type="string">{heading_str}</name>\n'
    featuredesc_out += f'\t\t\t\t<prerequisite type="string">{prerequisites_str}</prerequisite>\n'
    featuredesc_out += f'\t\t\t\t<source type="string">{pathname_in} Feature</source>\n'
    featuredesc_out += f'\t\t\t</{pathname_lower}{feature_lower}>\n'
    
    return link_out, featuredesc_out


def create_power(power_dict, name_in):
    power_out = ''
    power_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"]).lower()
    power_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.powers.{power_lower}@{settings.library}">{power_dict["name"]}</link>\n')

    return power_out


def extract_heroic_db(db_in):
    heroic_out = []

    print('\n\n\n=========== HEROIC THEMES ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

#        if name_str not in ['Alchemist']:
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
        # these are the unique Features and Powers for each Heroic Theme
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
                # bold indicates the start of a Feature
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
                    settings.heroic_power_list.append(pwr_name)
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
        heroic_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(heroic_out)) + ' entries exported.')

    return heroic_out
