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
        return classes_out, featuredesc_out

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
        if classes_dict["traits"] != '':
            classes_out += f'\t\t\t\t<traits>\n{classes_dict["traits"]}\t\t\t\t</traits>\n'
        features_xml = create_features(classes_dict["class_feature_list"], classes_dict["name"])
        if features_xml != '':
            classes_out += f'\t\t\t\t<features>\n{features_xml}\t\t\t\t</features>\n'
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
    # Remove lone colon at start of description
    feature_desc = re.sub('^<p>\s*:\s*', '<p>', feature_dict["desc"])
    feature_desc = clean_formattedtext(feature_desc)

    link_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.features.{name_lower}{feature_lower}@{settings.library}">{feature_dict["name"]}</link>\n')

    featuredesc_out += f'\t\t\t<{name_lower}{feature_lower}>\n'
    featuredesc_out += f'\t\t\t\t<description type="formattedtext">{feature_desc}</description>\n'
    featuredesc_out += f'\t\t\t\t<name type="string">{feature_dict["name"]}</name>\n'
    featuredesc_out += f'\t\t\t\t<prerequisite type="string">{name_in} Class</prerequisite>\n'
    featuredesc_out += f'\t\t\t\t<source type="string">{name_in} Feature</source>\n'
    featuredesc_out += f'\t\t\t</{name_lower}{feature_lower}>\n'
    
    return link_out, featuredesc_out

TRAIT_NAMES = ['Role', 'Power Source', 'Key Abilities', 'Armor Proficiencies', 'Weapon Proficiencies',
               'Implement', 'Bonus to Defense', 'Hit Points at 1st Level', 'Hit Points per Level Gained',
               'Healing Surges per Day', 'Trained Skills', 'Extra Trained Skill']


def create_traits(traits_in, classskilllist=None):
    traits_out = ''

    if len(traits_in) == 0:
        return traits_out

    for trait in traits_in:
        trait_lower = re.sub('[^a-zA-Z0-9_]', '', trait["name"]).lower()

        traits_out += f'\t\t\t\t\t<{trait_lower}>\n'
        traits_out += f'\t\t\t\t\t\t<name type="string">{trait["name"]}</name>\n'
        if trait["name"] == "Hit Points per Level Gained":
            traits_out += f'\t\t\t\t\t\t<text type="number">{trait["text"]}</text>\n'
        else:
            traits_out += f'\t\t\t\t\t\t<text type="string">{trait["text"]}</text>\n'
        traits_out += f'\t\t\t\t\t</{trait_lower}>\n'

        if trait["name"] == "Trained Skills" and classskilllist:
            traits_out += '\t\t\t\t\t<classskilllist>\n'
            for idx, skill in enumerate(classskilllist, start=1):
                traits_out += f'\t\t\t\t\t\t<id-{idx:0>5}>\n'
                traits_out += f'\t\t\t\t\t\t\t<name type="string">{skill["name"]}</name>\n'
                traits_out += f'\t\t\t\t\t\t\t<statname type="string">{skill["statname"]}</statname>\n'
                traits_out += f'\t\t\t\t\t\t</id-{idx:0>5}>\n'
            traits_out += '\t\t\t\t\t</classskilllist>\n'

    return traits_out


def create_power_tags(ftr, indent):
    xml = ''
    for tag_name, key in [('powersgiven', 'powers_given'), ('poweroptions', 'power_options')]:
        if key in ftr and len(ftr[key]) > 0:
            xml += f'{indent}<{tag_name}>\n'
            for pwr_idx, pwr in enumerate(ftr[key], start=1):
                pwr_desc = re.sub(r'^<p>\s*:\s*', '<p>', pwr["desc"])
                pwr_desc = clean_formattedtext(pwr_desc)

                power_lower = re.sub('[^a-zA-Z0-9_]', '', pwr["name"]).lower()
                xml += f'{indent}\t<id-{pwr_idx:0>5}>\n'
                xml += f'{indent}\t\t<link type="windowreference">\n'
                xml += f'{indent}\t\t\t<class>powerdesc</class>\n'
                xml += f'{indent}\t\t\t<recordname>reference.powers.{power_lower}@{settings.library}</recordname>\n'
                xml += f'{indent}\t\t</link>\n'
                xml += f'{indent}\t\t<name type="string">{pwr["name"]}</name>\n'
                xml += f'{indent}\t\t<description type="formattedtext">{pwr_desc}</name>\n'
                xml += f'{indent}\t</id-{pwr_idx:0>5}>\n'
            xml += f'{indent}</{tag_name}>\n'
    return xml


def create_features(features_in, class_name=''):
    features_out = ''

    if len(features_in) == 0:
        return features_out

    for idx, ftr in enumerate(features_in, start=1):
        feature_desc = re.sub(r'^<p>\s*:\s*', '<p>', ftr["desc"])
        feature_desc = clean_formattedtext(feature_desc)

        features_out += f'\t\t\t\t\t<id-{idx:0>5}>\n'
        features_out += f'\t\t\t\t\t\t<shortcut type="windowreference">\n'
        features_out += f'\t\t\t\t\t\t\t<class />\n'
        features_out += f'\t\t\t\t\t\t\t<recordname />\n'
        features_out += f'\t\t\t\t\t\t</shortcut>\n'
        features_out += f'\t\t\t\t\t\t<level type="number">1</level>\n'
        features_out += f'\t\t\t\t\t\t<name type="string">{ftr["name"]}</name>\n'
        features_out += f'\t\t\t\t\t\t<description type="formattedtext">{feature_desc}</description>\n'

        if "subfeatures" in ftr and len(ftr["subfeatures"]) > 0:
            features_out += '\t\t\t\t\t\t<subfeatures>\n'
            for sub_idx, sub_ftr in enumerate(ftr["subfeatures"], start=1):
                sub_desc = re.sub(r'^<p>\s*:\s*', '<p>', sub_ftr["desc"])
                sub_desc = clean_formattedtext(sub_desc)

                name_lower = re.sub('[^a-zA-Z0-9_]', '', class_name).lower()
                feature_lower = re.sub('[^a-zA-Z0-9_]', '', sub_ftr["name"]).lower()
                features_out += f'\t\t\t\t\t\t\t<id-{sub_idx:0>5}>\n'
                features_out += '\t\t\t\t\t\t\t\t<link type="windowreference">\n'
                features_out += f'\t\t\t\t\t\t\t\t\t<class>powerdesc</class>\n'
                features_out += f'\t\t\t\t\t\t\t\t\t<recordname>reference.features.{name_lower}{feature_lower}@{settings.library}</recordname>\n'
                features_out += '\t\t\t\t\t\t\t\t</link>\n'
                features_out += f'\t\t\t\t\t\t\t\t<level type="number">1</level>\n'
                features_out += f'\t\t\t\t\t\t\t\t<name type="string">{sub_ftr["name"]}</name>\n'
                features_out += f'\t\t\t\t\t\t\t\t<description type="formattedtext">{sub_desc}</description>\n'
                features_out += create_power_tags(sub_ftr, '\t\t\t\t\t\t\t\t')
                features_out += f'\t\t\t\t\t\t\t</id-{sub_idx:0>5}>\n'
            features_out += '\t\t\t\t\t\t</subfeatures>\n'

        if "subfeatureoptions" in ftr and len(ftr["subfeatureoptions"]) > 0:
            features_out += '\t\t\t\t\t\t<subfeaturechoices>\n'
            for sub_idx, sub_ftr in enumerate(ftr["subfeatureoptions"], start=1):
                sub_desc = re.sub(r'^<p>\s*:\s*', '<p>', sub_ftr["desc"])
                sub_desc = clean_formattedtext(sub_desc)

                name_lower = re.sub('[^a-zA-Z0-9_]', '', class_name).lower()
                feature_lower = re.sub('[^a-zA-Z0-9_]', '', sub_ftr["name"]).lower()
                features_out += f'\t\t\t\t\t\t\t<id-{sub_idx:0>5}>\n'
                features_out += '\t\t\t\t\t\t\t\t<link type="windowreference">\n'
                features_out += f'\t\t\t\t\t\t\t\t\t<class>powerdesc</class>\n'
                features_out += f'\t\t\t\t\t\t\t\t\t<recordname>reference.features.{name_lower}{feature_lower}@{settings.library}</recordname>\n'
                features_out += '\t\t\t\t\t\t\t\t</link>\n'
                features_out += f'\t\t\t\t\t\t\t\t<level type="number">1</level>\n'
                features_out += f'\t\t\t\t\t\t\t\t<name type="string">{sub_ftr["name"]}</name>\n'
                features_out += f'\t\t\t\t\t\t\t\t<description type="formattedtext">{sub_desc}</description>\n'
                features_out += create_power_tags(sub_ftr, '\t\t\t\t\t\t\t\t')
                features_out += f'\t\t\t\t\t\t\t</id-{sub_idx:0>5}>\n'
            features_out += '\t\t\t\t\t\t</subfeaturechoices>\n'

        features_out += create_power_tags(ftr, '\t\t\t\t\t\t')
        features_out += f'\t\t\t\t\t</id-{idx:0>5}>\n'

    return features_out


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

        # if name_str not in ['Sorcerer']:#, 'Hybrid Druid', 'Runepriest', 'Hybrid Fighter', 'Hybrid Ranger', 'Hybrid Rogue']:
        #     continue
        # print(name_str)

        description_str = ''
        features_str = ''
        featuredesc_str = ''
        powers_str = ''
        published_str = ''
        shortdescription_str = ''
        traits_str = ''
        
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
        traits_list = []
        if trait_block := parsed_html.select_one('.flavor > blockquote'):
            # loop through the <b> elements as they are the headings
            for b in trait_block.find_all('b'):
                trait_name = re.sub('\s*:\s*$', '', b.text)
                if trait_name in TRAIT_NAMES + ['Build Options', 'Class features', 'Hybrid Talent Options']:
                    # start a <p> with the heading value
                    description_str += '<p>' + str(b)
                    trait_text_parts = []
                    # keep grabbing fields for the description until we hit the next <b>
                    for tag in b.next_siblings:
                        if tag.name == 'b':
                            break
                        else:
                            description_str += str(tag)
                            if trait_name in TRAIT_NAMES:
                                trait_text_parts.append(str(tag))
                    description_str += '</p>\n'
                    # turn <br/> into new <p> as line breaks inside <p> don't render in formattedtext
                    description_str = re.sub(r'(^\s*<br/>|<br/>\s*$)', r'', description_str)
                    # get rid of empty paragraphs
                    description_str = description_str.replace('<p></p>', '')
                    if trait_name in TRAIT_NAMES:
                        trait_text = ''.join(trait_text_parts).lstrip(': ').strip()
                        traits_list.append({'name': trait_name, 'text': trait_text})

        # Class Skills list (parsed from the "Class Skills:" paragraph)
        classskills_list = []
        class_skills_tag = parsed_html.find('i', string=re.compile(r'Class Skills'))
        if class_skills_tag:
            skills_text = ''
            for sibling in class_skills_tag.next_siblings:
                skills_text += str(sibling)
            skills_text = skills_text.lstrip(': ').rstrip('.')
            for match in re.finditer(r'([^,(]+?)\s*\((\w+)\)', skills_text):
                classskills_list.append({'name': match.group(1).strip(), 'statname': match.group(2).strip()})

        traits_str = create_traits(traits_list, classskills_list)

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
        feature_list = [] #Used for the description section of the class
        class_feature_list = []  #Used for the separate feature tags
        in_feature = False
        in_power = False
        in_class_feature = False
        if feature_block := parsed_html.find('h3', text=re.compile('CLASS FEATURES')).previous_sibling:
            for tag in feature_block.next_siblings:
                # skip these if found as they are part of a Power description
                if isinstance(tag, Tag) and tag.has_attr('class') and tag.attrs.get('class')[0] in ['flavor', 'powerstat']:
                        continue
                if tag.name == 'h3':
                    description_str += '<p><b>' + tag.text + '</b></p>\n'
                elif tag.name == 'b' or tag.text in ['Suggested Combinations', 'Selecting Druid Powers', name_str.upper() + ' OVERVIEW']:
                    # if we are already in a feature then this is the end
                    if in_feature:
                        feature_dict["desc"] += '</p>'
                        ftr_link, ftr_desc = create_feature(feature_dict, name_str)
                        description_str += ftr_link
                        featuredesc_str += ftr_desc
                        feature_list.append(copy.copy(feature_dict))
                        in_feature = False
                    # work out whether this is just text or the start of a new feature
                    if tag.text.isupper() or tag.text in ['Suggested Combinations', 'Selecting Druid Powers']:
                        description_str += '<p><b>' + title_format(tag.text) + '</b></p>\n'
                        if in_class_feature:
                            class_feature_dict["desc"] += '</p>'
                            class_feature_list.append(copy.copy(class_feature_dict))                        
                        class_feature_dict = {}
                        class_feature_dict["name"] =  title_format(tag.text)
                        class_feature_dict["desc"] = "<p>"
                        class_feature_dict["powers_given"] = []
                        class_feature_dict["power_options"] = []
                        in_class_feature = True
                    # Sorcerer also has some paragraphs that look like features
                    elif name_str == 'Sorcerer' and tag.text in ['Cosmic Magic', 'Dragon Magic', 'Storm Magic', 'Wild Magic']:
                        description_str += '<p><b>' + title_format(tag.text) + '</b></p>\n'
                    else:
                        # close out the class feature if we're in one
                        if in_class_feature:
                            class_feature_dict["desc"] += '</p>'
                            class_feature_list.append(copy.copy(class_feature_dict))
                            in_class_feature = False
                        # start capturing the feature details
                        in_feature = True
                        feature_dict = {}
                        feature_dict["name"] = tag.text
                        feature_dict["desc"] = '<p>'
                        feature_dict["parent"] = class_feature_dict["name"]
                        feature_dict["powers_given"] = []
                        feature_dict["power_options"] = []
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
                        if in_class_feature:
                            class_feature_dict["desc"] += str(tag).replace(' <<br=""', '')
                        # .replace is to fix a one borked <br/> tag in Hybrid Druid (Sentinel)
                        description_str += '<p>' + str(tag).replace(' <<br=""', '') + '</p>\n'

                if in_power:
                    # if we are already in a feature then this is the end
                    was_in_feature = in_feature
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
                    # Add power link to feature/class feature descriptions
                    power_lower = re.sub('[^a-zA-Z0-9_]', '', pwr_name).lower()
                    feature_pwr_link = f'<link class="powerdesc" recordname="reference.powers.{power_lower}@{settings.library}">{pwr_name}</link>'
                    power_entry = {"name": pwr_name}
                    if was_in_feature and len(feature_list) > 0:
                        feature_list[-1]["desc"] += '\n' + feature_pwr_link
                        if re.search(r'[Yy]ou gain\b.*?\bpowers?\b.*?\bof your choice\b', feature_list[-1]["desc"]):
                            feature_list[-1]["power_options"].append(power_entry)
                        else:
                            feature_list[-1]["powers_given"].append(power_entry)
                    elif in_class_feature:
                        class_feature_dict["desc"] += '\n' + feature_pwr_link
                        if re.search(r'[Yy]ou gain\b.*?\bpowers?\b.*?\bof your choice\b', class_feature_dict["desc"]):
                            class_feature_dict["power_options"].append(power_entry)
                        else:
                            class_feature_dict["powers_given"].append(power_entry)
                    in_power = False

        # if we are still in a feature then close out the final one
        if in_feature:
            feature_dict["desc"] += '</p>'
            ftr_link, ftr_desc = create_feature(feature_dict, name_str)
            description_str += ftr_link
            featuredesc_str += ftr_desc
            feature_list.append(copy.copy(feature_dict))
            in_feature = False
        if in_class_feature:
            class_feature_dict["desc"] += '</p>'
            class_feature_list.append(copy.copy(class_feature_dict))
            in_class_feature = False

        description_str = clean_formattedtext(description_str)

        # Post-process class_feature_list to nest sub-features under parent features
        # If the parent feature has a description which contains "choose...following", those subfeatures are filed into subfeatureoptions
        # Otherwise, it is filed into just normal subfeatures
        # Sub-features are pulled from feature_list in order
        for ftr in class_feature_list:
            j = 0  # tracks position in feature_list across all iterations
            ftr["subfeatureoptions"] = []
            ftr["subfeatures"] = []
            while j < len(feature_list):
                if feature_list[j]["parent"] == ftr["name"] and feature_list[j]["name"] != ftr["name"]:
                    if re.search(r'[Cc]hoose\b.*\bfollowing\b', ftr["desc"]):
                        ftr["subfeatureoptions"].append(feature_list[j])
                    else:
                        ftr["subfeatures"].append(feature_list[j])
                j += 1

        export_dict = {}
        export_dict["description"] = description_str
        export_dict["features"] = features_str
        export_dict["feature_list"] = feature_list
        export_dict["featuredesc"] = featuredesc_str
        export_dict["name"] = name_str
        export_dict["powers"] = powers_str
        export_dict["published"] = published_str
        export_dict["shortdescription"] = shortdescription_str
        export_dict["traits"] = traits_str
        export_dict["class_feature_list"] = class_feature_list

        # Append a copy of generated item dictionary
        classes_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(classes_out)) + ' entries exported.')

    return classes_out
