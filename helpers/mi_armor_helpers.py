import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.mi_helpers import multi_level
from helpers.mi_helpers import power_construct
from helpers.mi_helpers import powers_format
from helpers.mi_helpers import props_format

def extract_mi_armor_db(db_in):
    mi_armor_out = []

    print('\n\n\n=========== MAGIC ARMOR ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row['Txt']
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row['Name'].replace('\\', '')
        category_str = row['Category'].replace('\\', '')
        rarity_str =  row['Rarity'].replace('\\', '')

#        if name_str not in ['Dilatory Armor']:
#            continue
#        print(name_str)

        bonus_str = ''
        cat_str = ''
        class_str = ''
        cost_str = ''
        critical_str = ''
        enhancement_str = ''
        flavor_str = ''
        group_str = ''
        level_str = ''
        mitype_str = ''
        powers_str = ''
        prerequisite_str = ''
        properties_str = ''
        props_str = ''
        section_id = 100
        special_str = ''
        subclass_str = ''

        # Class
        if (re.search('^(Armor)$', category_str) and re.search('^(Common|Uncommon|Rare)', rarity_str)):
            class_str = category_str
            mitype_str = 'armor'
            section_id = 1

        if section_id < 99:
##            print(str(i) + ' ' + name_str)

            # Bonus / Cost / Level
            multi_bonus = True
            try:
                multi_list = multi_level(parsed_html)
            except:
                multi_bonus = False
                multi_list = []
                multi_dict = {}
                multi_dict['bonus'] = ''
                multi_dict['cost'] = ''
                multi_dict['level'] = '0'
                multi_list.append(copy.deepcopy(multi_dict))

            # Enhancement
            if enhancement_lbl := parsed_html.find(string=re.compile('^(Enhancement|Enhancement Bonus):$')):
                enhancement_str = enhancement_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True)

            # Flavor
            if flavor_lbl := parsed_html.find('p', class_='miflavor'):
                flavor_str = re.sub('\s\s', ' ', flavor_lbl.get_text(separator = '\\n', strip = True))

            # Cat/Subclass (Armor)
            if cat_lbl := parsed_html.find(string='Armor: '):
                cat_str = re.sub('\s\s', ' ', cat_lbl.parent.next_sibling.strip()).title().replace(' Or ', ' or ')
                subclass_str = cat_str

            # Powers
            powerdesc_str, mipowers_str = powers_format(parsed_html, name_str)

            # Prerequisite
            if prerequisite_lbl := parsed_html.find(string=re.compile('^(Prerequisite|Requirement):$')):
                prerequisite_str = prerequisite_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True)

            # Properties
            if properties_lbl := parsed_html.find(string=re.compile('^(Property|Properties)')):
                props_list = []
                if properties_lbl.parent.next_sibling.name == 'ul':
                    for li in properties_lbl.parent.next_sibling:
                        properties_str = li.text.strip()
                        props_list.append(properties_str)
                else:
                    properties_str = re.sub('\s\s', ' ', properties_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True))
                    properties_str = re.sub(r':\\n', ': ', properties_str)
                    props_list.append(properties_str)
                props_str = props_format(props_list)

            # Special (Published In)
            if special_lbl := parsed_html.find('p', class_='publishedIn'):
                special_str = re.sub('\s\s', ' ', special_lbl.text)

            # Build the item entry
            previous_name = ''
            for item in multi_list:
                if int(item["level"]) >= settings.min_lvl and int(item["level"]) <= settings.max_lvl:
                    export_dict = {}
                    export_dict['bonus'] = item['bonus']
                    export_dict['cat'] = cat_str
                    export_dict['class'] = class_str
                    export_dict['cost'] = item['cost']
                    export_dict['critical'] = critical_str
                    export_dict['enhancement'] = enhancement_str
                    export_dict['flavor'] = flavor_str
                    export_dict['group'] = group_str
                    export_dict['level'] = item['level']
                    export_dict['mipowers'] = mipowers_str
                    export_dict['mitype'] = mitype_str
                    # append bonus if it exists, else append level for multi-items
                    if item["bonus"] != '':
                        export_dict['name'] = name_str + ' ' + item["bonus"]
                    elif len(multi_list) > 1:
                        export_dict['name'] = name_str + ' (Level ' + item["level"].rjust(2, ' ') + ')'
                    else:
                        export_dict['name'] = name_str
                    # only output powerdesc once for each named item as it will be the same for all levels
                    if name_str != previous_name:
                        export_dict['powerdesc'] = powerdesc_str
                        powerdesc_flag = True
                    else:
                        export_dict['powerdesc'] = ''
                    export_dict['powers'] = powers_str
                    export_dict['prerequisite'] = prerequisite_str
                    export_dict['props'] = props_str
                    export_dict['section_id'] = section_id
                    export_dict['special'] = special_str
                    export_dict['subclass'] = subclass_str

                    # Append a copy of generated item dictionary
                    mi_armor_out.append(copy.deepcopy(export_dict))
                    previous_name = name_str

    print(str(len(db_in)) + " entries parsed.")
    print(str(len(mi_armor_out)) + " entries exported.")

    return mi_armor_out
