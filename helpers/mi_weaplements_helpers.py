import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from helpers.mi_helpers import mi_list_sorter
from helpers.mi_helpers import multi_level
from helpers.mi_helpers import power_construct
from helpers.mi_helpers import powers_format
from helpers.mi_helpers import props_format

def extract_mi_weaplements_db(db_in, filter_in):
    mi_weaplements_out = []

    print(f'\n\n\n=========== MAGIC {filter_in.upper()}S ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row['Txt']
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row['Name'].replace('\\', '')
        category_str = row['Category'].replace('\\', '')
        rarity_str =  row['Rarity'].replace('\\', '')

#        if name_str not in ['Anarusi Codex', 'Wand of Wonder']:
#            continue
#        print(name_str)

        bonus_str = ''
        cat_str = ''
        class_str = ''
        cost_str = ''
        critical_str = ''
        enhancement_str = ''
        flavor_str = ''
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
        if (re.search(f'^({filter_in})$', category_str) and re.search('^(Common|Uncommon|Rare)', rarity_str)):
            class_str = category_str
            # implements are also 'weapons'
            mitype_str = 'weapon'
            section_id = 1

        if section_id < 99:
##            print(str(i) + ' ' + name_str)

#            if name_str not in ['Blackshroud Weapon']:
#                continue

            # Bonus / Cost / Level
            multi_bonus = True
            try:
                multi_list = multi_level(parsed_html)
            except:
                multi_bonus = False
                multi_list = []
                multi_item = {}

                # hard code the 5 items that don't conform
                if name_str == 'Anarusi Codex':
                    multi_item['bonus'] = '+2'
                    multi_item['cost'] = '0'
                    multi_item['level'] = '10'
                    multi_item['critical'] = '+1d6 necrotic damage per plus and the target is weakened until the end of your next turn'
                elif name_str == 'Eberron Shard of Bleeding Wounds':
                    multi_item['bonus'] = ''
                    multi_item['cost'] = '1,000 gp'
                    multi_item['level'] = '5'
                    multi_item['critical'] = ''
                elif name_str == 'Everdare':
                    multi_item['bonus'] = '+4'
                    multi_item['cost'] = ''
                    multi_item['level'] = '17'
                    multi_item['critical'] = '+4d6 damage'
                elif name_str == 'Scepter of the Chosen Tyrant':
                    multi_item['bonus'] = '+6'
                    multi_item['cost'] = ''
                    multi_item['level'] = '28'
                    multi_item['critical'] = '+6d10 damage'
                elif name_str == 'Symbol of Revivification':
                    multi_item['bonus'] = '+6'
                    multi_item['cost'] = '3,125,000 gp'
                    multi_item['level'] = '30'
                    multi_item['critical'] = '+6d6 damage'
                else:
                    multi_item['bonus'] = ''
                    multi_item['cost'] = ''
                    multi_item['level'] = '0'
                    multi_item['critical'] = ''

                multi_list.append(copy.deepcopy(multi_item))

            # Critical
            if critical_lbl := parsed_html.find(string='Critical:'):
                critical_str = critical_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True)
                if critical_str != '':
                    if multi_bonus == True:
                        for item in multi_list:
                            item["critical"] = critical_str
                            critical_test = re.search(r'(.*)(\d)(d)(\d{1,2})(.*)per plus(.*)', item["critical"])
                            if critical_test != None:
                                item["critical"] = critical_test.group(1) + str(int(critical_test.group(2)) * int(item["bonus"])) + critical_test.group(3) + critical_test.group(4) + critical_test.group(5) + critical_test.group(6)
                            item["critical"] = re.sub('damage', 'critical damage', item["critical"])
#                            critical_test = re.search(r'(\+)(\d)(d)(\d{1,2})(.*)per plus(.*)', critical_str)
#                            critical_test = re.search(r'(\+)(\d)(d)(\d{1,2})(.*)damage(.*)per plus(.*)', critical_str)
#                            if critical_test != None:
#                                item['critical'] = critical_test.group(1) + str(int(critical_test.group(2)) * int(item["bonus"])) + critical_test.group(3) + critical_test.group(4) + critical_test.group(5) + critical_test.group(6)
#                                item['critical'] = (critical_test.group(1) + str(int(critical_test.group(2)) * int(item["bonus"])) + critical_test.group(3)\
#                                                   + critical_test.group(4) + critical_test.group(5) + 'critical damage' + critical_test.group(6) + critical_test.group(7)).strip()
#                            else:
                            

            # Enhancement
            if enhancement_lbl := parsed_html.find(string=re.compile('^(Enhancement|Enhancement Bonus):$')):
                enhancement_str = enhancement_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True).title().replace(' And ', ' and ')

            # Flavor
            if flavor_lbl := parsed_html.find('p', class_='miflavor'):
                flavor_str = re.sub('\s\s', ' ', flavor_lbl.get_text(separator = '\\n', strip = True))

            # Cat / Subclass (Weapon/Implement)
            if cat_lbl := parsed_html.find(string=f'{filter_in}: '):
                cat_str = re.sub('\s\s', ' ', cat_lbl.parent.next_sibling.strip())
                subclass_str = re.sub('\s\s', ' ', cat_lbl.parent.next_sibling.strip())

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
                    export_dict['critical'] = item["critical"]
                    export_dict['enhancement'] = enhancement_str
                    export_dict['flavor'] = flavor_str
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
                    export_dict['prerequisite'] = prerequisite_str
                    export_dict['props'] = props_str
                    export_dict['section_id'] = section_id
                    export_dict['special'] = special_str
                    export_dict['subclass'] = subclass_str

                    # Append a copy of generated item dictionary
                    mi_weaplements_out.append(copy.deepcopy(export_dict))
                    previous_name = name_str

    print(str(len(db_in)) + " entries parsed.")
    print(str(len(mi_weaplements_out)) + " entries exported.")

    return mi_weaplements_out
