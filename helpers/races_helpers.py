import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.mod_helpers import clean_formattedtext

def races_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_races_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.races@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">Races</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_races_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Races List
    # This controls the table that appears when you click on a Library menu

    xml_out += ('\t\t<races>\n')
    xml_out += (f'\t\t\t<name type="string">Races</name>\n')
    xml_out += ('\t\t\t<index>\n')

    # Create individual item entries
    for races_dict in sorted(list_in, key=races_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', races_dict["name"]).lower()

        # Races list entry
        xml_out += (f'\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.races.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{races_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t</{name_lower}>\n')

    xml_out += ('\t\t\t</index>\n')
    xml_out += ('\t\t</races>\n')

    return xml_out


def create_races_cards(list_in):
    races_out = ''
    featuredesc_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    races_out += ('\t\t<races>\n')
    for races_dict in sorted(list_in, key=races_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', races_dict["name"]).lower()

        races_out += f'\t\t\t<{name_lower}>\n'
        races_out += f'\t\t\t\t<description type="formattedtext">\n'
        if races_dict["description"] != '':
            races_out += f'{races_dict["description"]}'
#        if races_dict["features"] != '':
#            races_out += f'{races_dict["features"]}'
#        if races_dict["powers"] != '':
#            races_out += f'{races_dict["powers"]}'
        if races_dict["published"] != '':
            races_out += f'{races_dict["published"]}'
        races_out += f'\n\t\t\t\t</description>\n'
        if races_dict["flavor"] != '':
            races_out += f'\t\t\t\t<flavor type="string">{races_dict["flavor"]}</flavor>\n'
        races_out += f'\t\t\t\t<name type="string">{races_dict["name"]}</name>\n'
#        xml_out += (f'\t\t\t\t<shortdescription type="string">{races_dict["shortdescription"]}</shortdescription>\n')
        races_out += '\t\t\t\t<source type="string">Race</source>\n'
        races_out += f'\t\t\t</{name_lower}>\n'

        # Create all Required Power entries
        featuredesc_out += races_dict["featuredesc"]

    races_out += ('\t\t</races>\n')

    return races_out, featuredesc_out

def create_features(features_in, name_in, heading_in):
    listlink_out = ''
    featuredesc_out = ''

    if len(features_in) == 0:
        return listlink_out, featuredesc_out

    name_lower = re.sub('[^a-zA-Z0-9_]', '', name_in).lower()
    
    listlink_out += f'<p><b>{heading_in}</b></p>\n'
    listlink_out += '\t\t\t\t<listlink>\n'

    for ftr in features_in:
        feature_lower = re.sub('[^a-zA-Z0-9_]', '', ftr["name"]).lower()
        listlink_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.features.{name_lower}{feature_lower}@{settings.library}">{ftr["name"]}</link>\n')

        featuredesc_out += f'\t\t\t<{name_lower}{feature_lower}>\n'
        featuredesc_out += f'\t\t\t\t<description type="formattedtext">{ftr["desc"]}</description>\n'
        featuredesc_out += f'\t\t\t\t<name type="string">{ftr["name"]}</name>\n'
        featuredesc_out += f'\t\t\t\t<prerequisite type="string">{name_in} Race</prerequisite>\n'
#        featuredesc_out += f'\t\t\t\t<shortdescription type="string">{ftr["shortdesc"]}</shortdescription>\n'
        featuredesc_out += f'\t\t\t\t<source type="string">{name_in} Feature</source>\n'
        featuredesc_out += f'\t\t\t</{name_lower}{feature_lower}>\n'

    listlink_out += '\t\t\t\t</listlink>\n'
    
    return listlink_out, featuredesc_out

def create_powers(powers_in):
    xml_out = ''
    if len(powers_in) == 0:
        return xml_out

    previous_type = ''
    
    for pwr in powers_in:
        power_lower = re.sub('[^a-zA-Z0-9_]', '', pwr["name"]).lower()
        if pwr["type"] != previous_type:
            # Close previous Type
            if previous_type != '':
                xml_out += '\t\t\t\t</listlink>\n'

            # Open new Type
            xml_out += f'<p><b>{pwr["type"]}</b></p>\n'
            previous_type = pwr["type"]
            xml_out += '\t\t\t\t<listlink>\n'

        xml_out += (f'\t\t\t\t\t<link class="powerdesc" recordname="reference.powers.{power_lower}@{settings.library}">{pwr["name"]}</link>\n')
    # Close last Type
    xml_out += '\t\t\t\t</listlink>\n'
    
    return xml_out

def extract_races_db(db_in):
    races_out = []

    print('\n\n\n=========== RACES ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

#        if name_str not in ['Bladeling', 'Bozak Draconian', 'Gold Dwarf', 'Kapak Draconian', 'Llewyrr Elf', 'Moon Elf (Eladrin)', 'Shield Dwarf', 'Sun Elf (Eladrin)', 'Wild Elf', 'Wood Elf']:
#            continue
#        print(name_str)

        description_str = ''
        features_str = ''
        featuredesc_str = ''
        featurehead_str = ''
        flavor_str = ''
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

        subrace_flag = False
        if name_str in ['Bozak Draconian', 'Gold Dwarf', 'Kapak Draconian', 'Llewyrr Elf', 'Moon Elf (Eladrin)', 'Shield Dwarf',\
                        'Sun Elf (Eladrin)', 'Wild Elf', 'Wood Elf']:
            subrace_flag = True

        if not subrace_flag:
            # Flavor
            if flavor_tag := parsed_html.select_one('#detail > i'):
                flavor_str = flavor_tag.text

            # Traits
            feature_list = []
            if traits_block := parsed_html.select_one('.flavor > blockquote'):
                description_str += '<p><b>RACIAL TRAITS</b></p>\n'
                for b in traits_block.find_all('b'):
                    # these are the elements common to all Races
                    if b.text in ['Average Height', 'Average Weight', 'Ability scores', 'Size', 'Speed', 'Vision', 'Languages', 'Skill Bonuses']:
                        description_str += '<p>' + str(b)
                        description_str += b.next_sibling + '</p>\n'
                    # otherwise assume it is a Racial Feature
                    else:
                        feature_dict = {}
                        feature_dict["name"] = b.text
                        feature_dict["desc"] = f'<p><b>Prerequisite:</b> {name_str}</p><p><b>{b.text}</b>'
                        feature_dict["shortdesc"] = ''
                        # keep grabbing fields for the description until we hit the next <b>
                        for ftrtag in b.next_siblings:
                            if ftrtag.name == 'b':
                                break
                            elif ftrtag.name == 'br':
                                continue
                            else:
                                feature_dict["desc"] += re.sub(r'^\s*:\s*', '', str(ftrtag))

                        feature_dict["desc"] += '</p>'
                        # remove tags
                        feature_dict["shortdesc"] = re.sub('<.*?>', '', feature_dict["desc"].replace('</p><p>', '\n'))

                        feature_list.append(copy.copy(feature_dict))

            features_str, featuredesc_str = create_features(feature_list, name_str, name_str + ' Features')
            description_str += features_str

            # Powers
            power_list = []
            power_h1 = parsed_html.find_all('h1', class_=re.compile(r'(atwillpower|encounterpower|dailypower)'))
            for h1 in power_h1:
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
                settings.races_power_list.append(pwr_name)
                power_list.append(copy.copy(power_dict))

            # Format the list of links to powers
            powers_str = create_powers(power_list)
            description_str += powers_str

            # Description
            if desc_block := parsed_html.select_one('.flavor'):
                for tag in desc_block.next_siblings:
                    # skip image bullets
                    if tag.name == 'img':
                        continue
                    # skip these if found as they are part of a Power description
                    elif isinstance(tag, Tag) and tag.select_one('.atwillpower, .encounterpower, .dailypower'):
                        continue
                    elif isinstance(tag, Tag) and tag.has_attr('class') and tag.attrs.get('class')[0] in ['atwillpower', 'encounterpower', 'dailypower', 'flavor', 'powerstat']:
                        continue
                    elif tag.name == 'h3':
                        description_str += '<p><b>' + tag.text + '</b></p>\n'
                    else:
                        description_str += '<p>' + str(tag).strip() + '</p>\n'
        else:
            # Sub Races
            features_block = BeautifulSoup('', features="html.parser")
            feature_list = []
            in_features = False

            # Description
            if desc_block := parsed_html.select_one('#detail'):
                for tag in desc_block.children:
                    if not in_features:
                        # skip main Race heading
                        if tag.name == 'h1':
                            continue
                        # skip image bullets
                        elif tag.name == 'img':
                            continue
                        elif tag.name == 'h3':
                            if re.search(r' Benefits$', tag.text, flags = re.IGNORECASE) != None:
                                featurehead_str = name_str + ' Benefits'
                                in_features = True
                            else:
                                description_str += '<p><b>' + tag.text + '</b></p>\n'
                        else:
                            description_str += '<p>' + str(tag).strip() + '</p>\n'
                    else:
                        features_block.append(copy.copy(tag))

            if features_block != None:
                for b in features_block.find_all('b'):
                    feature_dict = {}
                    feature_dict["name"] = re.sub(r'[\s:]*$', '', b.text)
                    feature_dict["desc"] = f'<p><b>Prerequisite:</b> {name_str}</p><p><b>{b.text}</b>'
                    feature_dict["shortdesc"] = ''
                    # keep grabbing fields for the description until we hit the next <b>
                    for ftrtag in b.next_siblings:
                        if ftrtag.name == 'b':
                            break
                        elif ftrtag.name == 'br':
                            feature_dict["desc"] += '\\n'
                            continue
                        else:
                            feature_dict["desc"] += re.sub(r'^\s*:\s*', '', str(ftrtag))

                    feature_dict["desc"] += '</p>'
                    # remove tags and copy
                    feature_dict["shortdesc"] = re.sub('<.*?>', '', feature_dict["desc"].replace('</p><p>', '\n'))
                    feature_list.append(copy.copy(feature_dict))

            features_str, featuredesc_str = create_features(feature_list, name_str, featurehead_str)
            description_str += features_str

            if name_str == 'Bozak Draconian':
                settings.races_power_list.append('Concussive Vengeance')
                description_str += '<p><b>Bozak Draconian Racial Attack </b></p>\n'
                description_str += '\t\t\t<listlink>\n'
                description_str += f'\t\t\t\t<link class="powerdesc" recordname="reference.powers.concussivevengeance@{settings.library}">Concussive Vengeance</link>\n'
                description_str += '\t\t\t</listlink>\n'
            elif name_str == 'Kapak Draconian':
                settings.races_power_list.append('Toxic Saliva')
                settings.races_power_list.append('Acidic Revenge')
                description_str += '<p><b>Kapak Draconian Racial Utility </b></p>\n'
                description_str += '\t\t\t<listlink>\n'
                description_str += f'\t\t\t\t<link class="powerdesc" recordname="reference.powers.toxicsaliva@{settings.library}">Toxic Saliva</link>\n'
                description_str += '\t\t\t</listlink>\n'
                description_str += '<p><b>Kapak Draconian Racial Attack </b></p>\n'
                description_str += '\t\t\t<listlink>\n'
                description_str += f'\t\t\t\t<link class="powerdesc" recordname="reference.powers.acidicrevenge@{settings.library}">Acidic Revenge</link>\n'
                description_str += '\t\t\t</listlink>\n'


        description_str = clean_formattedtext(description_str)
        
        export_dict = {}
        export_dict["description"] = description_str
        export_dict["features"] = features_str
        export_dict["featuredesc"] = featuredesc_str
        export_dict["flavor"] = flavor_str
        export_dict["name"] = name_str
        export_dict["powers"] = powers_str
        export_dict["published"] = published_str
        export_dict["shortdescription"] = shortdescription_str

        # Append a copy of generated item dictionary
        races_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(races_out)) + ' entries exported.')

    return races_out
