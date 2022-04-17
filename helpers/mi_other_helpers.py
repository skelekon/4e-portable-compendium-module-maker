import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .mod_helpers import mi_list_sorter
from .mod_helpers import multi_level
from .mod_helpers import power_construct
from .mod_helpers import powers_format
from .mod_helpers import props_format

def extract_mi_other_list(db_in, library_in, min_lvl, max_lvl, filter_in):
    mi_other_out = []

    alt_reward_expr = re.compile('(Alternative Reward|Battle Scars|Divine Boon|Echo of Power|Elemental gift|Elemental Gift|Fey Magic Gift|Glory Boon|Grandmaster Training|Legendary Boon|Lost Rune|Primal Blessing|Psionic Talent|Secret of the Way|Sorcerer-King\'s Boon|Templar Brand|Veiled Alliance Mystery|Wanderer\'s Secret)')

    print(f'\n\n\n=========== MAGIC OTHER ({filter_in.upper()}) ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row['Txt']
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row['Name'].replace('\\', '')
        category_str = row['Category'].replace('\\', '')
        rarity_str =  row['Rarity'].replace('\\', '')

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
        if (re.search(f'^({filter_in})$', category_str) and re.search('^(Common|Uncommon|Rare)', rarity_str)):
            class_str = category_str
            mitype_str = 'other'
            section_id = 1

        if section_id < 99:
##            print(str(i) + ' ' + name_str)

            # Ensure the category_str matches the bold label to avoid false matches e.g. 'Ring'
            if re.search('(Arms|Familiar|Feet|Hands|Head|Head and Neck|Neck|Ring|Waist)', category_str):
                category_str += ' Slot'
                cat_str += ' Slot'
            elif category_str == 'Wondrous':
                category_str = 'Wondrous Item'
                cat_str = 'Wondrous Item'

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
                multi_dict['level'] = ''

                # Try to find a value for cost
                if category_str == 'Alternative Reward':
                    if cost_tag := parsed_html.find(string=alt_reward_expr):
                        if cost_lbl := cost_tag.parent.next_sibling:
                            multi_dict['cost'] = re.search(r'([\d,]*( gp)*$)', cost_lbl).group(1)
                if cost_tag := parsed_html.find(string=re.compile('^' + category_str)):
                    if re.search('^Artifact', cost_tag):
                        multi_dict['cost'] = ''
                    elif cost_lbl := cost_tag.parent.next_sibling:
                        multi_dict['cost'] = re.search(r'([\d,]*( gp)*$)', cost_lbl).group(1)

                # Try to find a value for level
                if level_lbl := parsed_html.find(id='headerlevel'):
                    multi_dict['level'] = re.search(r'(\d+)', level_lbl.string).group(1)
                # If we find a Tier just set the level to the minimum for that Tier
                elif level_lbl := parsed_html.find('span', class_='milevel'):
                    tier_str = re.search(r'(Heroic|Paragon|Epic)', level_lbl.string).group(1)
                    if tier_str == 'Heroic':
                        multi_dict['level'] = '1'
                    elif tier_str == 'Paragon':
                        multi_dict['level'] = '11'
                    elif tier_str == 'Epic':
                        multi_dict['level'] = '21'

                if multi_dict["level"] == '':
                    multi_dict["level"] = 0

                multi_list.append(copy.deepcopy(multi_dict))

            # Critical
            if critical_lbl := parsed_html.find(string='Critical:'):
                critical_str = critical_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True)

            # Enhancement
            if enhancement_lbl := parsed_html.find(string=re.compile('^(Enhancement|Enhancement Bonus):$')):
                enhancement_str = enhancement_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True)

            # Flavor
            if flavor_lbl := parsed_html.find('p', class_='miflavor'):
                flavor_str = re.sub('\s\s', ' ', flavor_lbl.get_text(separator = '\\n', strip = True))

            # Subclass (category)
            # look for a <p> that begins with the category_str
            if subclass_cat := parsed_html.find('p', class_='mistat').find(string=re.compile('^' + category_str)):
                # if the next tag contains 'Property' then there is nothing to find
                if subclass_lbl := subclass_cat.parent.next_sibling:
                    if subclass_lbl.text == 'Property':
                        subclass_str = ''
                    # otherwise try to extract a string that is different to the category_str
                    else:
                        subclass_str = re.search(r'^([a-zA-Z \(\)]*)', subclass_lbl).group(1)
                        subclass_str = '' if subclass_str == category_str else subclass_str

            # Subclass (Alternative Reward)
            # There is no 'Alternative Reward' label, so check for the Subclass using a regex
            if category_str == 'Alternative Reward':
                subclass_str = parsed_html.find(string=alt_reward_expr)
            subclass_str = re.sub('\s\s', ' ', subclass_str.strip())

            cat_str = subclass_str

            # Powers
            powerdesc_str, mipowers_str = powers_format(parsed_html, name_str, library_in)

            # Prerequisite
            if prerequisite_lbl := parsed_html.find(string=re.compile('^(Prerequisite|Requirement):$')):
                prerequisite_str = prerequisite_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True)

            # Properties
            if properties_lbl := parsed_html.find(string=re.compile('^(Property|Properties)')):
                properties_str = re.sub('\s\s', ' ', properties_lbl.parent.next_sibling.get_text(separator = '\\n', strip = True))
                properties_str = re.sub(r':\\n', ': ', properties_str)
                props_str = props_format(properties_str)

            # Special (Published In)
            if special_lbl := parsed_html.find('p', class_='publishedIn'):
                special_str = re.sub('\s\s', ' ', special_lbl.text)

            # Build the item entry
            previous_name = ''
            for item in multi_list:
                if int(item["level"]) >= min_lvl and int(item["level"]) <= max_lvl:
                    # only need to output powerdesc once for each item as it will be the same for all level versions
                    powerdesc_flag = False

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
                    mi_other_out.append(copy.deepcopy(export_dict))
                    previous_name = name_str

    print(str(len(db_in)) + " entries parsed.")
    print(str(len(mi_other_out)) + " entries exported.")

    return mi_other_out
