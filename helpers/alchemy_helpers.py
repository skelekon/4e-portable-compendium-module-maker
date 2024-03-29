import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

# This returns a dictionary containing the Power details of an Alchemical Item
def create_power_desc(soup_in, name_in):
    power_out = {}

    new_power = []
    tag_str = ''

    action_expr = 'Free Action|Free|Immediate Interrupt|Immediate Reaction|Minor Action|Minor|Move Action|Move|No Action|Standard Action|Standard'

    action_str = ''
    keywords_str = ''
    description_str = ''
    recharge_str = ''
    shortdescription_str = ''

    for tag in soup_in:
        # concatenate all the elements within each tag
        tag_str += ' '.join(map(str, tag.stripped_strings))

    # Action
    action_str = match.group(1) if (match := re.search(r'(' + action_expr + ')', tag_str)) else ''

    # Keywords
    keywords_str = match.group(1) if (match := re.search(r'[•\*]\s*(.*?)\)', tag_str)) else ''

    # Recharge
    recharge_str = match.group(1) if (match := re.search(r'\((.*?)\s', tag_str)) else ''

    # Description
    shortdescription_str = match.group(2).strip() if (match := re.search(r'(' + action_str + ')\.(.*)', tag_str)) else ''
    # fancy format
    # add <p>
    description_str = '<p>' + re.sub(r'(Attack:|Effect:|Hit:|Special:)', r'</p><p>\1', shortdescription_str) + '</p>'
    # add <b>
    description_str = '<p>' + re.sub(r'(Attack:|Effect:|Hit:|Special:)', r'<b>\1</b>', description_str) + '</p>'

    power_out["action"] = action_str
    power_out["description"] = description_str
    power_out["keywords"] = keywords_str
    power_out["recharge"] =  recharge_str
    power_out["shortdescription"] = shortdescription_str

    return power_out


# This returns the XML for an indivual Alchemical Item and any associated Power
def create_mi_desc(item_dict, mi_name_in):
    mi_out = ''
    power_out = ''

    name_camel = re.sub('[^a-zA-Z0-9_]', '', mi_name_in)
    suffix_str = item_dict["level"].rjust(2, '0')

    # Fetch the Item Power information as it will be needed to complete the Item Desc block
    power_dict = create_power_desc(item_dict["power"], mi_name_in)

    # This is the Magic Item block that goes in <reference><items>
    mi_out += f'\t\t\t<{name_camel}-{suffix_str}>\n'
    mi_out += f'\t\t\t\t<name type="string">{mi_name_in}</name>\n'
    mi_out += '\t\t\t\t<class type="string">Alchemical Item</class>\n'
    mi_out += f'\t\t\t\t<level type="number">{item_dict["level"]}</level>\n'
    mi_out += f'\t\t\t\t<cost type="string">{item_dict["cost"]}</cost>\n'
    mi_out += f'\t\t\t\t<flavor type="string">{item_dict["flavor"]}</flavor>\n'
    mi_out += '\t\t\t\t<powers>\n'
    mi_out += '\t\t\t\t\t<id-001>\n'
    mi_out += '\t\t\t\t\t\t<name type="string">Power - Consumable</name>\n'
    mi_out += '\t\t\t\t\t\t<recharge type="string">Consumable</recharge>\n'
    if power_dict["keywords"] != '':
        mi_out += f'\t\t\t\t\t\t<keywords type="string">{power_dict["keywords"]}</keywords>\n'
    mi_out += f'\t\t\t\t\t\t<action type="string">{power_dict["action"]}</action>\n'
    mi_out += f'\t\t\t\t\t\t<description type="formattedtext">{power_dict["description"]}</description>\n'
    mi_out += f'\t\t\t\t\t\t<shortdescription type="string">{power_dict["shortdescription"]}</shortdescription>\n'
    mi_out += '\t\t\t\t\t\t<link type="windowreference">\n'
    mi_out += '\t\t\t\t\t\t\t<class>powerdesc</class>\n'
    mi_out += f'\t\t\t\t\t\t\t<recordname>reference.powers.alchemy{name_camel}Power-{suffix_str}@{settings.library}</recordname>\n'
    mi_out += '\t\t\t\t\t\t</link>\n'
    mi_out += '\t\t\t\t\t</id-001>\n'
    mi_out += '\t\t\t\t</powers>\n'
    mi_out += '\t\t\t\t<formatteditemblock type="formattedtext"><p></p></formatteditemblock>\n'
    mi_out += '\t\t\t\t<mitype type="string">other</mitype>\n'
    mi_out += f'\t\t\t</{name_camel}-{suffix_str}>\n'

    # This is the Item Power block that goes in <powerdesc>
    power_out += f'\t\t<alchemy{name_camel}Power-{suffix_str}>\n'
    power_out += f'\t\t\t<name type="string">{mi_name_in} Power - Consumable</name>\n'
    power_out += '\t\t\t<recharge type="string">Consumable</recharge>\n'
    if power_dict["keywords"] != '':
        power_out += f'\t\t\t<keywords type="string">{power_dict["keywords"]}</keywords>\n'
    power_out += f'\t\t\t<action type="string">{power_dict["action"]}</action>\n'
    power_out += '\t\t\t<source type="string">Item</source>\n'
    power_out += f'\t\t\t<description type="formattedtext">{power_dict["description"]}</description>\n'
    power_out += f'\t\t\t<shortdescription type="string">{power_dict["shortdescription"]}</shortdescription>\n'
    power_out += '\t\t\t<class type="string">Item</class>\n'
    power_out += f'\t\t\t<level type="number">{item_dict["level"]}</level>\n'
    power_out += '\t\t\t<type type="string">Item</type>\n'
    power_out += '\t\t\t<flavor type="formattedtext"><p><i></i></p></flavor>\n'
##    power_out += f'\t\t\t<effect type="string">{power_dict["effect"]}</effect>\n'
    power_out += f'\t\t</alchemy{name_camel}Power-{suffix_str}>\n'

    return mi_out, power_out


# Extracts details for one Alchemical Item from passed in Magic Item soup
def extract_mi_details(soup_in, name_in):

    cost_str = ''
    flavor_str = ''
    level_str  = ''
    power_soup = ''
    item_str = ''
    linklist_out = ''
    mi_name_str = ''
    mi_table_out = ''
    mi_out = ''
    power_out = ''

    # Cost
    if cost_tag := soup_in.find(string=re.compile('^Price')):
        cost_str = re.sub(':\w*', '', cost_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

    # Flavor
    if flavor_tag := soup_in.find(class_='flavor'):
        flavor_str = flavor_tag.text
        flavor_tag.extract()

    # Level
    if level_tag := soup_in.find('span', class_='milevel'):
        level_str = re.sub(r'[^0-9]', '', level_tag.text)
        level_tag.extract

    # Power
    # get the leftovers that have not been extracted
    power_soup = soup_in

    mi_name_str = name_in + ' (Level ' + level_str.rjust(2, ' ') + ')'
    mi_name_camel = re.sub('[^a-zA-Z0-9_]', '', mi_name_str)
    suffix_str = level_str.rjust(2, '0')

    # These are the links to the Alchemy Items that appear on the Alchemy Items table
    mi_table_out += f'\t\t\t\t\t\t<a{suffix_str}{mi_name_camel}>\n'
    mi_table_out += f'\t\t\t\t\t\t\t<name type="string">{name_in}</name>\n'
    mi_table_out += '\t\t\t\t\t\t\t<link type="windowreference">\n'
    mi_table_out += '\t\t\t\t\t\t\t\t<class>referencemagicitem</class>\n'
    mi_table_out += f'\t\t\t\t\t\t\t\t<recordname>reference.items.{mi_name_camel}-{suffix_str}@{settings.library}</recordname>\n'
    mi_table_out += '\t\t\t\t\t\t\t</link>\n'
    mi_table_out += '\t\t\t\t\t\t\t<cat type="string"></cat>\n'
    mi_table_out += f'\t\t\t\t\t\t\t<level type="number">{level_str}</level>\n'
    mi_table_out += f'\t\t\t\t\t\t\t<cost type="string">{cost_str}</cost>\n'
    mi_table_out += f'\t\t\t\t\t\t</a{suffix_str}{mi_name_camel}>\n'

    # These are the links to the Alchemy Items that appear on the Alchemy Formula item card
    linklist_out += f'\n\t\t\t\t\t<link class="referencemagicitem" recordname="reference.items.{mi_name_camel}-{suffix_str}@{settings.library}">Level {level_str} - {name_in}</link>'

    # Set up variables needed to create the Item Card & any Power Card
    mi_dict = {}
    mi_dict["cost"] = cost_str
    mi_dict["level"] = level_str
    mi_dict["flavor"] = flavor_str
    mi_dict["power"] = copy.copy(power_soup)

    mi_out, power_out = create_mi_desc(mi_dict, mi_name_str)

    return mi_table_out, linklist_out, mi_out, power_out


# Sort by Name
def alchemy_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


# Returns the XML for the top-level menu that leads to the Alchemical Formulas list
def create_formula_library(id_in, list_in, name_in):
    xml_out = ''

    if not list_in:
        return xml_out, id_in

    id_in += 1

    xml_out += (f'\t\t\t\t<l{id_in:0>3}-alchemyformulas>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">{name_in}</name>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_rituallist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.formulas@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t</l{id_in:0>3}-alchemyformulas>\n')

    return xml_out, id_in


# Returns the XML for the top-level menu that leads to the Alchemical Items list
def create_alchemy_item_library(id_in, list_in, name_in):
    xml_out = ''

    if not list_in:
        return xml_out, id_in

    id_in += 1

    xml_out += (f'\t\t\t\t<l{id_in:0>3}-alchemyitems>\n')
    xml_out += (f'\t\t\t\t\t<name type="string">{name_in}</name>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>reference_classmagicitemtablelist</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.alchemicalitems@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += (f'\t\t\t\t</l{id_in:0>3}-alchemyitems>\n')

    return xml_out, id_in


# Returns the XML for the second-level menu that leads to the individual Alchemical Formulas
def create_formula_table(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    name_camel = ''

    xml_out += ('\t\t<formulas>\n')
    xml_out += ('\t\t\t<description type="string">Alchemical Formulas</description>\n')
    xml_out += ('\t\t\t<groups>\n')

    # Create individual item entries
    for alchemy_dict in sorted(list_in, key=alchemy_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', alchemy_dict["name"])

        # Rituals list entry
        xml_out += (f'\t\t\t\t<alchemy{name_camel}>\n')
        xml_out += ('\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>reference_ritual</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.rituals.alchemy{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t<source type="string">{alchemy_dict["name"]}</source>\n')
        xml_out += (f'\t\t\t\t</alchemy{name_camel}>\n')

    xml_out += ('\t\t\t</groups>\n')
    xml_out += ('\t\t</formulas>\n')

    return xml_out


# Returns the XML for the second-level menu that leads to the individual Alchemical Items
def create_alchemy_item_table(list_in):
    xml_out = ''

    # Alchemy Item Table
    # This controls the table that appears when you click on a Library menu
    xml_out += ('\t\t<alchemicalitems>\n')
    xml_out += ('\t\t\t<description type="string">Alchemical Items</description>\n')
    xml_out += ('\t\t\t<groups>\n')
    xml_out += ('\t\t\t\t<section001>\n')
    xml_out += ('\t\t\t\t\t<description type="string">Alchemical Items</description>\n')
    xml_out += ('\t\t\t\t\t<items>\n')

    # Create individual item entries
    for alchemy_dict in sorted(list_in, key=alchemy_list_sorter):
        xml_out += (f'{alchemy_dict["mi_table"]}')

    xml_out += ('\t\t\t\t\t</items>\n')
    xml_out += ('\t\t\t\t</section001>\n')
    xml_out += ('\t\t\t</groups>\n')
    xml_out += ('\t\t</alchemicalitems>\n')

    return xml_out


# Returns the XML for the Ritual Cards for all Alchemical Formula
def create_formula_desc(list_in):
    xml_out = ''
    mi_out = ''
    power_out = ''

    if not list_in:
        return xml_out

    # Create individual Alchemy Formula ritual cards
    for alchemy_dict in sorted(list_in, key=alchemy_list_sorter):
        name_camel = re.sub('[^a-zA-Z0-9_]', '', alchemy_dict["name"])

        xml_out += (f'\t\t<alchemy{name_camel}>\n')
        xml_out += (f'\t\t\t<name type="string">{alchemy_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t<category type="string">{alchemy_dict["category"]}</category>\n')
        xml_out += (f'\t\t\t<component type="string">{alchemy_dict["component"]}</component>\n')
        xml_out += (f'\t\t\t<details type="formattedtext">{alchemy_dict["details"]}\n')
        xml_out += (f'\t\t\t\t<linklist>{alchemy_dict["linklist"]}</linklist>\n')
        xml_out += (f'\t\t\t</details>\n')
        if alchemy_dict["duration"] != '':
            xml_out += (f'\t\t\t<duration type="string">{alchemy_dict["duration"]}</duration>\n')
        if alchemy_dict["flavor"] != '':
            xml_out += (f'\t\t\t<flavor type="string">{alchemy_dict["flavor"]}</flavor>\n')
        xml_out += (f'\t\t\t<level type="string">Level {alchemy_dict["level"]}</level>\n')
        if alchemy_dict["prerequisite"] != '':
            xml_out += (f'\t\t\t<prerequisite type="string">{alchemy_dict["prerequisite"]}</prerequisite>\n')
        xml_out += (f'\t\t\t<price type="string">{alchemy_dict["price"]}</price>\n')
        if alchemy_dict["skill"] != '':
            xml_out += (f'\t\t\t<skill type="string">{alchemy_dict["skill"]}</skill>\n')
        xml_out += (f'\t\t\t<time type="string">{alchemy_dict["time"]}</time>\n')
        xml_out += (f'\t\t</alchemy{name_camel}>\n')

        mi_out += alchemy_dict["mi_desc"]
        power_out += alchemy_dict["power"]

    return xml_out, mi_out, power_out


def extract_alchemy_db(db_in, filter_in):
    alchemy_out = []

    print('\n\n\n=========== ALCHEMY ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')

        category_str = ''
        class_str = ''
        component_str = ''
        details_str = ''
        duration_str = ''
        flavor_str = ''
        item_str = ''
        level_str = ''
        linklist_str = ''
        mi_desc_str = ''
        mi_table_str = ''
        power_str = ''
        price_str = ''
        prerequisite_str = ''
        section_id = 100
        skill_str =  ''
        time_str = ''

        # Component
        if component_tag := parsed_html.find(string=re.compile('^Component')):
            component_str = re.sub(':\w*', '', component_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

        if re.search(r'(See Alchemical|See below|See the item\'s price)', component_str, re.IGNORECASE)\
           or name_str in ['Grayflower Perfume', 'Keen Oil', 'Panther Tears']:
            class_str = 'Formula'
            section_id = 1

        if section_id < 100:
##        if name_str == 'Walking Death':

            # Find all the Items appearing within this Formula
            item_list = []
            power_list = []
            if p_tags := parsed_html.find_all('p'):
                for p in p_tags:
                    # For each found item, generate a dictonary with details, plus Magic Item & Item Power structures
                    if p.find('h1', class_='magicitem'):
                        item_soup = p.extract()
                        tbl_str, ll_str, mi_str, pow_str = extract_mi_details(item_soup, name_str)
                        mi_table_str += tbl_str
                        linklist_str += ll_str
                        mi_desc_str += mi_str
                        power_str += pow_str

            linklist_str += '\n\t\t\t\t'

            # Category
            if category_tag := parsed_html.find(string=re.compile('^Category')):
                category_str = re.sub(':\s*', '', category_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Duration
            if duration_tag := parsed_html.find(string=re.compile('^Duration')):
                duration_str = re.sub(':\s*', '', duration_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Flavor
            if flavor_tag := parsed_html.select_one('#detail > i'):
                flavor_str = flavor_tag.text

            # Level
            if level_tag := parsed_html.find(string=re.compile('^Level')):
                level_str = re.sub(':\s*', '', level_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Prerequisite
            prerequisite_tag = parsed_html.find(string=re.compile('^Prerequisite'))
            if prerequisite_tag:
                prerequisite_str = re.sub(':\s*', '', prerequisite_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Price
            if price_tag := parsed_html.find(string=re.compile('^Market Price')):
                price_str = re.sub(':\s*', '', price_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Skill
            if skill_tag := parsed_html.find(string=re.compile('^Key Skill')):
                skill_str = re.sub(':\s*', '', skill_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Time
            if time_tag := parsed_html.find(string=re.compile('^Time')):
                time_str = re.sub(':\s*', '', time_tag.parent.next_sibling.get_text(separator = ', ', strip = True))

            # Details
            if detail_tag := parsed_html.find('div', id='detail'):
                for tag in detail_tag.find_all('p'):
                    # skip heading & flavor
                    if tag.name in ['h1', 'i']:
                        continue
                    # remove the stats tag
                    if stats_tag := tag.find(class_='ritualstats'):
                        continue
                    # remove the tag class
                    del tag['class']
                    # remove the a tag
                    if anchor_tag := tag.find('a'):
                        anchor_tag.replaceWithChildren()
                    # append details
                    details_str += str(tag)

            # turn <br/> into new <p> as line breaks inside <p> don't render in formattedtext
            details_str = re.sub(r'(^\s*<br/>|<br/>\s*$)', r'', details_str)
            details_str = re.sub(r'<br/>', r'</p><p>', details_str)

            # replace <th> with <td><b> as FG appear to not render <th> correctly
            details_str = re.sub(r'<th>', r'<td><b>', details_str)
            details_str = re.sub(r'</th>', r'</b></td>', details_str)

            if int(level_str) >= settings.min_lvl and int(level_str) <= settings.max_lvl:
                export_dict = {}
                export_dict["category"] = category_str
                export_dict["class"] = class_str
                export_dict["component"] = component_str
                export_dict["details"] = details_str
                export_dict["duration"] = duration_str
                export_dict["flavor"] = flavor_str
                export_dict["level"] = level_str
                export_dict["linklist"] = linklist_str
                export_dict["mi_desc"] = mi_desc_str
                export_dict["mi_table"] = mi_table_str
                export_dict["name"] = name_str
                export_dict["power"] = power_str
                export_dict["prerequisite"] = prerequisite_str
                export_dict["price"] = price_str
                export_dict["skill"] = skill_str
                export_dict["time"] = time_str

                # Append a copy of generated item dictionary
                alchemy_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(alchemy_out)) + ' entries exported.')

    return alchemy_out
