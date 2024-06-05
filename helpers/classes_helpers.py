import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.mod_helpers import title_format
from helpers.mod_helpers import clean_formattedtext

def classes_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_classes_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.classes@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Classes</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_classes_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Classes List
    # This controls the table that appears when you click on a Library menu

    xml_out += ('\t\t<classes>\n')
    xml_out += (f'\t\t\t<name type="string">Classes</name>\n')
    xml_out += ('\t\t\t<index>\n')

    # Create individual item entries
    for classes_dict in sorted(list_in, key=classes_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', classes_dict["name"]).lower()

        # Classes list entry
        xml_out += (f'\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.classes.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{classes_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t</{name_lower}>\n')

    xml_out += ('\t\t\t</index>\n')
    xml_out += ('\t\t</classes>\n')

    return xml_out


def create_classes_cards(list_in):
    classes_out = ''
    featuredesc_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    classes_out += ('\t\t<classes>\n')
    for classes_dict in sorted(list_in, key=classes_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', classes_dict["name"]).lower()

        classes_out += f'\t\t\t<{name_lower}>\n'
        classes_out += f'\t\t\t\t<description type="formattedtext">\n'
        if classes_dict["description"] != '':
            classes_out += f'{classes_dict["description"]}'
        if classes_dict["features"] != '':
            classes_out += f'{classes_dict["features"]}'
        if classes_dict["powers"] != '':
            classes_out += f'{classes_dict["powers"]}'
        if classes_dict["published"] != '':
            classes_out += f'{classes_dict["published"]}'
#        xml_out += (f'\t\t\t\t<shortdescription type="string">{classes_dict["shortdescription"]}</shortdescription>\n')
        classes_out += f'\n\t\t\t\t</description>\n'
        classes_out += f'\t\t\t\t<name type="string">{classes_dict["name"]}</name>\n'
        classes_out += '\t\t\t\t<source type="string">Class</source>\n'
        classes_out += f'\t\t\t</{name_lower}>\n'

        # Create all Required Power entries
        featuredesc_out += classes_dict["featuredesc"]

    classes_out += ('\t\t</classes>\n')

    return classes_out, featuredesc_out


def create_feature(feature_dict, name_in):
    link_out = ''
    featuredesc_out = ''

    name_lower = re.sub('[^a-zA-Z0-9_]', '', name_in).lower()
    feature_lower = re.sub('[^a-zA-Z0-9_]', '', feature_dict["name"]).lower()
    feature_desc = clean_formattedtext(feature_dict["desc"])

    link_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.features.{name_lower}{feature_lower}@{settings.library}">{feature_dict["name"]}</link>\n')

    featuredesc_out += f'\t\t\t<{name_lower}{feature_lower}>\n'
    featuredesc_out += f'\t\t\t\t<description type="formattedtext">{feature_desc}</description>\n'
    featuredesc_out += f'\t\t\t\t<name type="string">{feature_dict["name"]}</name>\n'
    featuredesc_out += f'\t\t\t\t<prerequisite type="string">{name_in} Class</prerequisite>\n'
    featuredesc_out += f'\t\t\t\t<source type="string">{name_in} Feature</source>\n'
    featuredesc_out += f'\t\t\t</{name_lower}{feature_lower}>\n'
    
    return link_out, featuredesc_out


def create_power(power_dict, name_in):
    xml_out = ''
    power_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"]).lower()
    xml_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.powers.{power_lower}@{settings.library}">{power_dict["name"]}</link>\n')

    return xml_out


def extract_classes_db(db_in):
    classes_out = []

    print('\n\n\n=========== CLASSES ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

#        if name_str not in ['Bard (Skald)']:#'Fighter (Knight)', 'Cleric (Templar)', 'Wizard (Arcanist)', 'Hybrid Druid (Sentinel)', 'Warlock (Binder)', 'Ardent', 'Avenger']:
#            continue
#        print(name_str)

        description_str = ''
        features_str = ''
        featuredesc_str = ''
        powers_str = ''
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

        # Traits
        # these are the elements common to all Classes
        if trait_block := parsed_html.select_one('.flavor > blockquote'):
            # loop through the <b> elements as they are the headings
            for b in trait_block.find_all('b'):
                if re.sub('\s*:\s*$', '', b.text) in ['Role', 'Power Source', 'Key Abilities', 'Armor Proficiencies', 'Weapon Proficiencies', 'Implement',\
                                                   'Bonus to Defense', 'Hit Points at 1st Level', 'Hit Points per Level Gained', 'Healing Surges per Day',\
                                                   'Trained Skills', 'Extra Trained Skill', 'Build Options', 'Class features', 'Hybrid Talent Options']:
                    # start a <p> with the heading value
                    description_str += '<p>' + str(b)
                    # keep grabbing fields for the description until we hit the next <b>
                    for tag in b.next_siblings:
                        if tag.name == 'b':
                            break
                        else:
                            description_str += str(tag)
                    description_str += '</p>\n'
                    # turn <br/> into new <p> as line breaks inside <p> don't render in formattedtext
                    description_str = re.sub(r'(^\s*<br/>|<br/>\s*$)', r'', description_str)
                    # get rid of empty paragraphs
                    description_str = description_str.replace('<p></p>', '')

        # Description
        if desc_block := parsed_html.find('p', class_='flavor'):
            for tag in desc_block.next_siblings:
                # stop at Class Features, as they are processed separately
                if tag.name == 'h3' and re.search(r'CLASS FEATURES', tag.text) != None:
                    break
                if tag.name in ['b', 'h3']:
                    description_str += '<p><b>' + tag.text + '</b></p>\n'
                elif tag.name  == 'i':
                    description_str += '<p><i>' + re.sub(r'<br/>', r'\\n', str(tag).strip()) + '</i></p>\n'
                else:
                    description_str += '<p>' + str(tag).strip() + '</p>\n'


        # Features
        # these are the unique features for each Class (excluding powers)
        feature_list = []
        in_feature = False
        in_power = False
        if feature_block := parsed_html.find('h3', text=re.compile('CLASS FEATURES')).previous_sibling:
            for tag in feature_block.next_siblings:
                # skip these if found as they are part of a Power description
                if isinstance(tag, Tag) and tag.has_attr('class') and tag.attrs.get('class')[0] in ['flavor', 'powerstat']:
                        continue
                if tag.name == 'h3':
                    description_str += '<p><b>' + tag.text + '</b></p>\n'
                elif tag.name == 'b':
                    # if we are already in a feature then this is the end
                    if in_feature:
                        feature_dict["desc"] += '</p>'
                        ftr_link, ftr_desc = create_feature(feature_dict, name_str)
                        description_str += ftr_link
                        featuredesc_str += ftr_desc
                        feature_list.append(copy.copy(feature_dict))
                        in_feature = False
                    # work out whether this is just text or the start of a new feature
                    if tag.text.isupper():
                        description_str += '<p><b>' + title_format(tag.text) + '</b></p>\n'
                    else:
                        # start capturing the feature details
                        in_feature = True
                        feature_dict = {}
                        feature_dict["name"] = tag.text
                        feature_dict["desc"] = '<p>'
                # found a power so just create a link to it (the Powers parser will create the actual Power card)
                elif isinstance(tag, Tag) and tag.select_one('.atwillpower, .encounterpower, .dailypower'):
                    h1 = tag.find('h1', class_=re.compile(r'(atwillpower|encounterpower|dailypower)'))
                    in_power = True
                # some classes like Fighter (Knight) don't wrap the power in a <p>
                elif isinstance(tag, Tag) and tag.has_attr('class') and tag.attrs.get('class')[0] in ['atwillpower', 'encounterpower', 'dailypower']:
                    h1 = tag
                    in_power = True
                else:
                    if in_feature:
                        feature_dict["desc"] += str(tag)
                    else:
                        # .replace is to fix a one borked <br/> tag in Hybrid Druid (Sentinel)
                        description_str += '<p>' + str(tag).replace(' <<br=""', '') + '</p>\n'

                if in_power:
                    # if we are already in a feature then this is the end
                    if in_feature:
                        feature_dict["desc"] += '</p>'
                        ftr_link, ftr_desc = create_feature(feature_dict, name_str)
                        description_str += ftr_link
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
                    settings.classes_power_list.append(pwr_name)
                    pwr_link = create_power(power_dict, name_str)
                    description_str += pwr_link
                    in_power = False

        description_str = clean_formattedtext(description_str)

        export_dict = {}
        export_dict["description"] = description_str
        export_dict["features"] = features_str
        export_dict["featuredesc"] = featuredesc_str
        export_dict["name"] = name_str
        export_dict["powers"] = powers_str
        export_dict["published"] = published_str
        export_dict["shortdescription"] = shortdescription_str

        # Append a copy of generated item dictionary
        classes_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(classes_out)) + ' entries exported.')

    return classes_out
