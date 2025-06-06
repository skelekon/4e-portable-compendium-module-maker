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
        if races_dict["published"] != '':
            races_out += f'{races_dict["published"]}'
        races_out += f'\n\t\t\t\t</description>\n'
        if races_dict["traits"] != '':
            races_out += f'\t\t\t\t<traits>\n{races_dict["traits"]}\t\t\t\t</traits>\n'
        if races_dict["features"] != '':
            races_out += f'\t\t\t\t<features>\n{races_dict["featuredesc"]}\t\t\t\t</features>\n'        
        if races_dict["powers"] != '':
           races_out += f'\t\t\t\t<powers>\n{races_dict["powerslib"]}\t\t\t\t</powers>\n'        
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

        featuredesc_out += f'\t\t\t\t\t<{name_lower}{feature_lower}>\n'
        featuredesc_out += f'\t\t\t\t\t\t<description type="formattedtext">{ftr["text"]}</description>\n'
        featuredesc_out += f'\t\t\t\t\t\t<name type="string">{ftr["name"]}</name>\n'
        featuredesc_out += f'\t\t\t\t\t\t<prerequisite type="string">{name_in} Race</prerequisite>\n'
#        featuredesc_out += f'\t\t\t\t<shortdescription type="string">{ftr["shortdesc"]}</shortdescription>\n'
        featuredesc_out += f'\t\t\t\t\t\t<source type="string">{name_in} Feature</source>\n'
        featuredesc_out += f'\t\t\t\t\t</{name_lower}{feature_lower}>\n'

    listlink_out += '\t\t\t\t</listlink>\n'
    
    return listlink_out, featuredesc_out

def create_traits(traits_in):
    traits_out = ''

    if len(traits_in) == 0:
        return traits_out

    for trait in traits_in:
        trait_lower = re.sub('[^a-zA-Z0-9_]', '', trait["name"]).lower()

        traits_out += f'\t\t\t\t\t<{trait_lower}>\n'
        traits_out += f'\t\t\t\t\t\t<name type="string">{trait["name"]}</name>\n'
        traits_out += f'\t\t\t\t\t\t<text type="formattedtext">{trait["text"]}</text>\n'
        traits_out += f'\t\t\t\t\t</{trait_lower}>\n'
    
    return traits_out    

def create_powers(powers_in):
    xml_out = ''
    powerdesc_out = ''
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

def create_powers_lib(powers_in):
    xml_out = ''
    powerdesc_out = ''
    if len(powers_in) == 0:
        return powerdesc_out

    previous_type = ''
    settings.power_lib_id = 0
    for pwr in powers_in:
        power_lower = re.sub('[^a-zA-Z0-9_]', '', pwr["name"]).lower()
        # if pwr["class"] != previous_type:
        #     settings.power_lib_id = 0

        settings.power_lib_id += 1
        #Open new Power Tag Description
        powerdesc_out += (f'\t\t\t\t<id-{settings.power_lib_id:0>5}>\n')
        powerdesc_out += (f'\t\t\t\t\t<abilities />\n')
        powerdesc_out += (f'\t\t\t\t\t<flavor type="string">{pwr["flavor"]}</flavor>\n')
        powerdesc_out += (f'\t\t\t\t\t<action type="string">{pwr["action"]}</action>\n')
        powerdesc_out += (f'\t\t\t\t\t<keywords type="string">{pwr["keywords"]}</keywords>\n')
        powerdesc_out += (f'\t\t\t\t\t<name type="string">{pwr["name"]}</name>\n')
        powerdesc_out += (f'\t\t\t\t\t<prepared type="number">1</prepared>\n')
        powerdesc_out += (f'\t\t\t\t\t<range type="string">{pwr["range"]}</range>\n')           
        powerdesc_out += (f'\t\t\t\t\t<recharge type="string">{pwr["recharge"]}</recharge>\n')
        powerdesc_out += (f'\t\t\t\t\t<shortdescription type="string">{pwr["shortdescription"]}</shortdescription>\n')
        powerdesc_out += (f'\t\t\t\t\t<source type="string">{pwr["class"]}</source>\n')
        powerdesc_out += (f'\t\t\t\t</id-{settings.power_lib_id:0>5}>\n')

        # previous_type = pwr["class"]
    
    return powerdesc_out    

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
        powersdesc_str = ''
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

        subrace_flag = False
        if name_str in ['Bozak Draconian', 'Gold Dwarf', 'Kapak Draconian', 'Llewyrr Elf', 'Moon Elf (Eladrin)', 'Shield Dwarf',\
                        'Sun Elf (Eladrin)', 'Wild Elf', 'Wood Elf']:
            subrace_flag = True

        if not subrace_flag:
            # Flavor
            if flavor_tag := parsed_html.select_one('#detail > i'):
                flavor_str = flavor_tag.text

            # Traits and Features
            feature_list = []
            traits_list = []
            if traits_block := parsed_html.select_one('.flavor > blockquote'):
                description_str += '<p><b>RACIAL TRAITS</b></p>\n'
                for b in traits_block.find_all('b'):
                    # these are the elements common to all Races
                    if b.text in ['Average Height', 'Average Weight', 'Ability scores', 'Size', 'Speed', 'Vision', 'Languages', 'Skill Bonuses']:
                        description_str += '<p>' + str(b)
                        description_str += b.next_sibling + '</p>\n'
                        traits_dict = {}
                        traits_dict["name"] = b.text
                        traits_dict["text"] = b.next_sibling[1:].strip()
                        traits_list.append(copy.copy(traits_dict))
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
                                feature_dict["text"] = re.sub(r'^\s*:\s*', '', str(ftrtag))

                        feature_dict["desc"] += '</p>'
                        # remove tags
                        feature_dict["shortdesc"] = re.sub('<.*?>', '', feature_dict["desc"].replace('</p><p>', '\n'))

                        feature_list.append(copy.copy(feature_dict))

            features_str, featuredesc_str = create_features(feature_list, name_str, name_str + ' Features')
            description_str += features_str
            traits_str = create_traits(traits_list)

            # Powers
            power_list = []
            powerlib_list = []
            power_h1 = parsed_html.find_all('h1', class_=re.compile(r'(atwillpower|encounterpower|dailypower)'))
            for h1 in power_h1:
                pwr_type = ''
                pwr_name = ''
                pwer_text = ''
                for item in h1:
                    pwer_text = re.sub(r'^\s*:\s*', '', str(item.text))
                    if isinstance(item, NavigableString):
                        pwr_name = item
                    else:
                        pwr_type = item.text
                power_dict = {}
                power_dict["type"] = pwr_type
                power_dict["name"] = pwr_name

                powerlib_dict = {}
                powerlib_dict["class"] = pwr_type
                powerlib_dict["name"] = pwr_name
                powerlib_dict["source"] = ''
                powerlib_dict["flavor"] = ''
                powerlib_dict["recharge"] = ''
                powerlib_dict["action"] = ''
                powerlib_dict["range"] = ''
                powerlib_dict["keywords"] = ''
                powerlib_dict["description"] = ''
                powerlib_dict["shortdescription"] = ''

                # Power Source / Name
                if source_tag := h1.select_one('span', class_='level'):
                    source_str = source_tag.text
                    power_name_str = source_tag.next_sibling.strip()
                if power_name_str == '':
                    power_name_str = basename_str
                powerlib_dict["source"] = source_str
                # Power Flavor
                if power_flavor_ptag := h1.find_next_sibling('p', class_='flavor'):
                    if power_flavor_itag := power_flavor_ptag.select_one('i') :
                        power_flavor_str = power_flavor_itag.text
                powerlib_dict["flavor"] = power_flavor_str
                # Power Recharge
                if power_recharge_ptag := h1.find_next_sibling('p', class_="powerstat"):
                    if power_recharge_btag := power_recharge_ptag.select_one('b') :
                        power_recharge_str = power_recharge_btag.text
                        # small number of powers have alternate capitalization
                        if power_recharge_str == 'At-will':
                            power_recharge_str = 'At-Will'
                        powerlib_dict["recharge"] = power_recharge_str
                # Powerstat class - this is used to find Action, Range, Keywords
                powerstat_p = h1.find_next_sibling('p', class_='powerstat')
                if powerstat_p is not None:
                    #Action
                    powerstat_br = powerstat_p.find('br')
                    action_tag = powerstat_br.find_next_sibling('b')
                    action_str = action_tag.text
                    powerlib_dict["action"] = action_str
                    #Range
                    range_tag = action_tag.find_next_sibling('b')
                    if range_tag:
                        range_next = range_tag.next_sibling
                        range_str = range_tag.text + range_next.text if range_next else range_tag.text
                    powerlib_dict["range"] = range_str
                    #Keywords
                    keywords = []
                    power_bullet = powerstat_p.find('img', attrs={'src': 'images/bullet.gif'})
                    if power_bullet:
                        for tag in power_bullet.next_siblings:
                            if tag.name == 'br':
                                break
                            elif tag.name == 'b':
                                keywords.append(tag.text)
                    keywords_str = ', '.join(keywords)
                    powerlib_dict["keywords"] = keywords_str
                    # Description
                    description_tags = []
                    for desc_tag in powerstat_p.find_all_next():
                        if desc_tag.has_attr('class'):
                            if desc_tag.get('class')[0] in ['powerstat', 'flavor', 'atwillpower', 'encounterpower', 'dailypower']:
                                description_tags.append(desc_tag)
                        # looking for Augment labels as they are not in the usual classes
                        elif desc_tag.name == 'b':
                            if re.search(r'^Augment [0-9]', desc_tag.text):
                                description_tags.append(desc_tag)
                    for tag in description_tags:
                        # remove p classnames
                        del tag['class']
                    description_str = ''.join(map(str, description_tags))
                    description_str = description_str.replace('\n', '')
                    # wrap any Augment X in <p> tags, because it's easier to do once it's a string instead of messing with tags
                    description_str = re.sub(r'(<b>Augment [0-9]</b>)', r'<p>\1</p>', description_str)
                    # power description doesn't honor <br/> tags, so replace with new paragraphs
                    description_str = re.sub('<br/>', '</p><p>', description_str)
                    description_str += published_str
                    powerlib_dict["description"] = description_str

                # wrap any Augment X in <p> tags, because it's easier to do once it's a string instead of messing with tags
                description_str = re.sub(r'(<b>Augment [0-9]</b>)', r'<p>\1</p>', description_str)
                # power description doesn't honor <br/> tags, so replace with new paragraphs
                description_str = re.sub('<br/>', '</p><p>', description_str)
                description_str += published_str

                # Short Description
                # remove tags after replacing new paragraphs with newlines
                shortdescription_str = re.sub('<.*?>', '', description_str.replace('</p><p>', '\n'))
                shortdescription_str = shortdescription_str.replace('\n', '\\n')
                powerlib_dict["shortdescription"] = shortdescription_str

                settings.races_power_list.append(pwr_name)
                power_list.append(copy.copy(power_dict))
                powerlib_list.append(copy.copy(powerlib_dict))

            # Format the list of links to powers
            powers_str = create_powers(power_list)
            powersdesc_str = create_powers_lib(powerlib_list)
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
                            feature_dict["text"] = re.sub(r'^\s*:\s*', '', str(ftrtag))

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
        export_dict["traits"] = traits_str
        export_dict["powerslib"] = powersdesc_str

        # Append a copy of generated item dictionary
        races_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(races_out)) + ' entries exported.')

    return races_out
