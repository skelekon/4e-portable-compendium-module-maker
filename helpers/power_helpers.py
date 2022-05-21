import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .create_db import create_db

from .mod_helpers import mi_list_sorter
from .mod_helpers import multi_level
from .mod_helpers import power_construct
from .mod_helpers import powers_format
from .mod_helpers import props_format

def classes_list():
    cc_out = ['Cleric','Fighter','Rogue','Warlord','Wizard']
    cc_db = []
    cc_db = create_db('sql\ddiClass.sql', "','")
    for i, row in enumerate(cc_db, start=1):
        cc_out.append(row["Name"].replace('\\', ''))
    return cc_out

def races_list():
    race_out = []
    race_db = []
    race_db = create_db('sql\ddiRace.sql', "','")
    for i, row in enumerate(race_db, start=1):
        race_out.append(row["Name"].replace('\\', ''))
    return race_out

def paragon_paths_list():
    pp_out = []
    pp_db = []
    pp_db = create_db('sql\ddiParagonPath.sql', "','")
    for i, row in enumerate(pp_db, start=1):
        pp_out.append(row["Name"].replace('\\', ''))
    return pp_out

def epic_destinies_list():
    ed_out = []
    ed_db = []
    ed_db = create_db('sql\ddiEpicDestiny.sql', "','")
    for i, row in enumerate(ed_db, start=1):
        ed_out.append(row["Name"].replace('\\', ''))
    return ed_out

def library_list_sorter(entry_in):
    prefix_id = entry_in["prefix_id"]
    clss = entry_in["class"]

    return (prefix_id, clss)

def power_list_sorter(entry_in):
    clss = entry_in["class"]
    group_id = entry_in["group_id"]
    name = entry_in["name"]

    return (clss, group_id, name)

def create_power_library(id_in, list_in, suffix_in):
    xml_out = ''

    if not list_in:
        return xml_out, id_in

    previous_class = ''
    for power_dict in sorted(list_in, key=library_list_sorter):
        if power_dict["class"] != previous_class:
            previous_class = power_dict["class"]
            class_camel = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"])

            id_in += 1
            lib_id = 'l' + str(id_in).rjust(3, '0')

            xml_out += (f'\t\t\t\t<{lib_id}-powers{class_camel}>\n')
            xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
            xml_out += ('\t\t\t\t\t\t<class>reference_classpowerlist</class>\n')
            xml_out += (f'\t\t\t\t\t\t<recordname>powerlists.powers{class_camel}@{settings.library}</recordname>\n')
            xml_out += ('\t\t\t\t\t</librarylink>\n')
            xml_out += (f'\t\t\t\t\t<name type="string">{power_dict["prefix"]} - {power_dict["class"]}{suffix_in}</name>\n')
            xml_out += (f'\t\t\t\t</{lib_id}-powers{class_camel}>\n')
    return xml_out, id_in

def create_power_table(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    previous_class = ''
    previous_group = ''
    class_lower = ''
    level_lower = ''

    # Power List
    # This controls the table that appears when you click on a Library menu

    # Create individual item entries
    for power_dict in sorted(list_in, key=power_list_sorter):
        class_camel = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"])
        group_camel = power_dict["group_id"]
        name_camel = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"])

        #Check for new Class
        if class_camel != previous_class:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</{previous_class}-{previous_group}>\n')

            # Close previous Class
            if previous_class != '':
                xml_out += ('\t\t\t</groups>\n')
                xml_out += (f'\t\t</powers{previous_class}>\n')

            # Open new Class
            previous_group = group_camel
            xml_out += (f'\t\t<powers{class_camel}>\n')
            xml_out += (f'\t\t\t<description type="string">{power_dict["class"]}</description>\n')
            xml_out += ('\t\t\t<groups>\n')
    
            # Open new Group
            xml_out += (f'\t\t\t\t<{class_camel}-{group_camel}>\n')
            xml_out += (f'\t\t\t\t<description type="string">{power_dict["group"]}</description>\n')
            xml_out += ('\t\t\t\t\t<powers>\n')

        # Check for new Group
        if group_camel != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</{class_camel}-{previous_group}>\n')

            # Open new Group if not the first entry in the table
            if previous_class != '':
                xml_out += (f'\t\t\t\t<{class_camel}-{group_camel}>\n')
                xml_out += (f'\t\t\t\t<description type="string">{power_dict["group"]}</description>\n')
                xml_out += ('\t\t\t\t\t<powers>\n')

        # Powers list entry
        xml_out += (f'\t\t\t\t\t\t<power{name_camel}>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>powerdesc.power{name_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t\t\t<source type="string">{power_dict["name"]}</source>\n')
        xml_out += (f'\t\t\t\t\t\t</power{name_camel}>\n')

        previous_class = class_camel
        previous_group = group_camel

    # Close final Group
    xml_out += ('\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t</{class_camel}-{previous_group}>\n')

    # Close final Class
    xml_out += ('\t\t\t</groups>\n')
    xml_out += (f'\t\t</powers{class_camel}>\n')

    return xml_out

def create_linkedpowers(basename_in, name_in, list_in):
    xml_out = ''
    linked_list = []

    # Loop through the list of powers to find a related power
    for pwr_dict in list_in:
        if pwr_dict["basename"] == basename_in and pwr_dict["name"] != name_in:
            linked_list.append(pwr_dict["name"])

    # Create any linked power entries
    for pwr in linked_list:
        power_camel = re.sub('[^a-zA-Z0-9_]', '', pwr)
        xml_out += (f'\t\t\t\t<power{power_camel}>\n')
        xml_out += ('\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>powerdesc.power{power_camel}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t</power{power_camel}>\n')
    
    return xml_out

def create_power_desc(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    entry_str = ''
    linked_powers = ''
    section_str = ''
    name_lower = ''

    # Create individual item entries
    for power_dict in sorted(list_in, key=power_list_sorter):
        linked_powers = create_linkedpowers(power_dict["basename"], power_dict["name"], list_in)

        name_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"])

        xml_out += (f'\t\t<power{name_lower}>\n')
        xml_out += (f'\t\t\t<name type="string">{power_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t<action type="string">{power_dict["action"]}</action>\n')
        xml_out += (f'\t\t\t<description type="formattedtext">{power_dict["description"]}</description>\n')
        xml_out += (f'\t\t\t<flavor type="string">{power_dict["flavor"]}</flavor>\n')
        xml_out += (f'\t\t\t<keywords type="string">{power_dict["keywords"]}</keywords>\n')
        xml_out += (f'\t\t\t<range type="string">{power_dict["range"]}</range>\n')
        xml_out += (f'\t\t\t<recharge type="string">{power_dict["recharge"]}</recharge>\n')
        xml_out += (f'\t\t\t<shortdescription type="string">{power_dict["shortdescription"]}</shortdescription>\n')
        xml_out += (f'\t\t\t<source type="string">{power_dict["source"]}</source>\n')
        if linked_powers != '':
            xml_out += (f'\t\t\t<linkedpowers>\n{linked_powers}\t\t\t</linkedpowers>\n')
        xml_out += (f'\t\t</power{name_lower}>\n')

    return xml_out

def extract_power_list(db_in, basic_flag):
    power_out = []

    # Add MBA/RBA/Bull Rush/Grab
    basic_dict = {}
    if basic_flag:

        basic_dict["Name"] = 'Melee Basic Attack'
        basic_dict["Class"] = 'Basic Attack'
        basic_dict["Level"] = '0'
        basic_dict["Txt"] = '<div id=\"detail\">'
        basic_dict["Txt"] += '<h1 class=\"atwillpower\"><span class=\"level\">Basic Attack</span>Melee Basic Attack</h1>'
        basic_dict["Txt"] += '<p class=\"flavor\"><i>You resort to the simple attack you learned when you first picked up a melee weapon.</i></p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>At-Will</b><img src=\"images/bullet.gif\" alt=\"\"/><b>Weapon</b><br/><b>Standard Action</b><b>Melee</b> weapon</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Target</b>: One creature</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Attack</b>: Strength vs. AC</p>'
        basic_dict["Txt"] += '<p class=\"flavor\"><b>Hit</b>: 1[W] + Strength modifier damage.<br/>Level 21: 2[W] + Strength modifier damage.</p>'
        basic_dict["Txt"] += '<br/>'
        basic_dict["Txt"] += '<p class=\"publishedIn\">Published in <a href=\"http://anonym.to/?http://www.wizards.com/default.asp?x=products/dndacc/9780786950164\" target=\"_new\">Rules Compendium</a>, page(s) 239.</p>'
        basic_dict["Txt"] += '</div>'
        db_in.append(copy.deepcopy(basic_dict))

        basic_dict["Name"] = 'Ranged Basic Attack'
        basic_dict["Class"] = 'Basic Attack'
        basic_dict["Level"] = '0'
        basic_dict["Txt"] = '<div id=\"detail\">'
        basic_dict["Txt"] += '<h1 class=\"atwillpower\"><span class=\"level\">Basic Attack</span>Ranged Basic Attack</h1>'
        basic_dict["Txt"] += '<p class=\"flavor\"><i>You resort to the simple attack you learned when you first picked up a ranged weapon.</i></p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>At-Will</b><img src=\"images/bullet.gif\" alt=\"\"/><b>Weapon</b><br/><b>Standard Action</b><b>Ranged</b> weapon</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Target</b>: One creature</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Attack</b>: Dexterity vs. AC</p>'
        basic_dict["Txt"] += '<p class=\"flavor\"><b>Hit</b>: 1[W] + Dexterity modifier damage.<br/>Level 21: 2[W] + Dexterity modifier damage.</p>'
        basic_dict["Txt"] += '<br/>'
        basic_dict["Txt"] += '<p class=\"publishedIn\">Published in <a href=\"http://anonym.to/?http://www.wizards.com/default.asp?x=products/dndacc/9780786950164\" target=\"_new\">Rules Compendium</a>, page(s) 239.</p>'
        basic_dict["Txt"] += '</div>'
        db_in.append(copy.deepcopy(basic_dict))

        basic_dict["Name"] = 'Bull Rush'
        basic_dict["Class"] = 'Basic Attack'
        basic_dict["Level"] = '0'
        basic_dict["Txt"] = '<div id=\"detail\">'
        basic_dict["Txt"] += '<h1 class=\"atwillpower\"><span class=\"level\">Attack</span>Bull Rush</h1>'
        basic_dict["Txt"] += '<p class=\"flavor\"><i>You hurl yourself at your foe and push it back.</i></p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>At-Will</b><br/><b>Standard Action</b><b>Melee</b> 1</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Target</b>: One creature</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Attack</b>: Strength vs. Fortitude</p>'
        basic_dict["Txt"] += '<p class=\"flavor\"><b>Hit</b>: You push the target 1 square and then shift 1 square into the space it left.</p>'
        basic_dict["Txt"] += '<br/>'
        basic_dict["Txt"] += '<p class=\"publishedIn\">Published in <a href=\"http://anonym.to/?http://www.wizards.com/default.asp?x=products/dndacc/9780786950164\" target=\"_new\">Rules Compendium</a>, page(s) 239.</p>'
        basic_dict["Txt"] += '</div>'
        db_in.append(copy.deepcopy(basic_dict))

        basic_dict["Name"] = 'Grab'
        basic_dict["Class"] = 'Basic Attack'
        basic_dict["Level"] = '0'
        basic_dict["Txt"] = '<div id=\"detail\">'
        basic_dict["Txt"] += '<h1 class=\"atwillpower\"><span class=\"level\">Attack</span>Grab</h1>'
        basic_dict["Txt"] += '<p class=\"flavor\"><i>You reach out and grasp your foe, preventing it from moving.</i></p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>At-Will</b><br/><b>Standard Action</b><b>Melee</b> touch</p>'
        basic_dict["Txt"] += '<p class=\"flavor\"><b>Requirement</b>: You must have a hand free.</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Target</b>: One creature that is no more than one size category larger than youe</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Attack</b>: Strength vs. Reflex</p>'
        basic_dict["Txt"] += '<p class=\"flavor\"><b>Hit</b>: You grab the target until the end of your next turn. You can end the grab as a free action.</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Sustain Minor</b>: The grab persists until the end of your next turn.</p>'
        basic_dict["Txt"] += '<br/>'
        basic_dict["Txt"] += '<p class=\"publishedIn\">Published in <a href=\"http://anonym.to/?http://www.wizards.com/default.asp?x=products/dndacc/9780786950164\" target=\"_new\">Rules Compendium</a>, page(s) 243.</p>'
        basic_dict["Txt"] += '</div>'
        db_in.append(copy.deepcopy(basic_dict))

    # Lists for checking what type of power it is
    try:
        cc_list = classes_list()
    except:
        cc_list = []

    try:
        race_list = races_list()
    except:
        race_list = []

    try:
        pp_list = paragon_paths_list()
    except:
        pp_list = []

    try:
        ed_list = epic_destinies_list()
    except:
        ed_list = []

    print('\n\n\n=========== POWERS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features='html.parser')

        # Retrieve the data with dedicated columns
        basename_str =  row["Name"].replace('\\', '')
        class_str =  row["Class"].replace('\\', '')
        level_str =  row["Level"].replace('\\', '')

##        if basename_str not in ['Demoralizing Strike', 'Cloud of Daggers', 'Spell Magnet', 'Open the Gate of Battle [Attack Technique]', 'Turn Undead', 'Healing Word', 'Holy Cleansing', 'Grease']:
##        if basename_str not in ['Aggressive Lunge']:
##            continue
##        print(basename_str)        

        # sort order for the Library list based on the broad class of the power
        prefix_id = 0
        prefix_str = ''

        if class_str in cc_list:
            prefix_id = 2
            prefix_str = 'Class'
        elif class_str in race_list:
            prefix_id = 3
            prefix_str = 'Racial'
        elif class_str in pp_list:
            prefix_id = 4
            prefix_str = 'Paragon Path'
        elif class_str in ed_list:
            prefix_id = 5
            prefix_str = 'Epic Destiny'
        else:
            prefix_id = 1
            prefix_str = 'Powers'

        # Published In - only one of these required per base power entry
        published_tag = parsed_html.find(class_='publishedIn').extract()
        if published_tag:
            # remove p classnames
            del published_tag['class']
            # remove the a tags
            anchor_tag = published_tag.find('a')
            while anchor_tag:
                anchor_tag.replaceWithChildren()
                anchor_tag = published_tag.find('a')
            published_str = '\\n' + str(published_tag)

        # set up variables used for looping mutiple power entries
        power_id = 0
        previous_name = ''
        in_power = False
        power_complete = False
        power_html = BeautifulSoup('', features='html.parser')

        # Get all the Power tags
        detail_div = parsed_html.find('div', id='detail')

        # Append a dummy tag to the end to ensure that it loops around one extra time to process the last power 
        dummy_tag = BeautifulSoup('<h1 class="atwillpower"></h1>', features='html.parser')
        detail_div.append(dummy_tag)

        # Loop through all the tags
        for pwr_tag in detail_div.find_all(recursive=False):
            # Found the start of a power
            if pwr_tag.has_attr('class'):
                if pwr_tag.get('class')[0] in ['atwillpower', 'encounterpower', 'dailypower']:
                    # trigger on the start of the first power so we can know when a power has ended
                    if in_power == False:
                        in_power = True
                    # on second or later encounters with a power start signify is it ready to process
                    else:
                        power_complete = True

            # Process all the power details and add it to the output list
            if power_complete == True:

                # Initialize variables that are per-power entry
                action_str = ''
                description_str = ''
                flavor_str = ''
                group_id = ''
                group_str = ''
                keywords_str = ''
                name_str = ''
                published_str = ''
                range_str = ''
                recharge_id = ''
                recharge_str = ''
                shortdescription_str = ''
                source_str = ''

                # Counter that can be used to distinguish between additional powers from the same base power
                power_id += 1

                # Source / Name
                if source_tag := power_html.select_one('span', class_='level'):
                    source_str = source_tag.text
                    name_str = source_tag.next_sibling.strip()
                if name_str == '':
                    name_str = basename_str

                # Flavor
                if flavor_tag := power_html.select_one('.flavor > i'):
                    flavor_str = flavor_tag.text

                # Recharge
                if recharge_tag := power_html.select_one('.powerstat > b'):
                    recharge_str = recharge_tag.text
                # small number of powers have alternate capitlaization
                if recharge_str == 'At-will':
                    recharge_str = 'At-Will'

                # Powerstat class - this is used to find Action, Range, Keywords
                powerstat_lbl = power_html.find('p', class_='powerstat')

                # Action
                powerstat_br = powerstat_lbl.find('br')
                action_tag = powerstat_br.find_next_sibling('b')
                action_str = action_tag.text

                # Range
                range_tag = action_tag.find_next_sibling('b')
                if range_tag:
                    range_next = range_tag.next_sibling
                    range_str = range_tag.text + range_next.text if range_next else range_tag.text

                # Keywords
                keywords = []
                power_bullet = powerstat_lbl.find('img', attrs={'src': 'images/bullet.gif'})
                if power_bullet:
                    for tag in power_bullet.next_siblings:
                        if tag.name == "br":
                            break
                        elif tag.name == "b":
                            keywords.append(tag.text)
                keywords_str = ", ".join(keywords)

                # Description
                if description_tags := powerstat_lbl.find_all_next(class_=['powerstat', 'flavor', 'atwillpower', 'encounterpower', 'dailypower']):
                    for tag in description_tags:
                        # remove p classnames
                        del tag['class']
                    description_str = ''.join(map(str, description_tags))
                    # power description doesn't honor <br/> tags, so replace with new paragraphs
                    description_str = re.sub('<br/>', '</p><p>', description_str)

                # Short Description
                # remove tags
                shortdescription_str = re.sub('<.*?>', '', description_str.replace('</p><p>', '\n'))

                # Group - this is the subheading on the Powers table
                if level_str == '0':
                    group_str = recharge_str + ' Features'
                    if recharge_str == 'At-Will':
                        recharge_id = '1at'
                    elif recharge_str == 'At-Will (Special)':
                        recharge_id = '1sp'
                    elif recharge_str == 'Encounter':
                        recharge_id = '2en'
                    elif recharge_str == 'Encounter (Special)':
                        recharge_id = '2sp'
                    elif recharge_str == 'Daily':
                        recharge_id = '3da'
                    elif recharge_str == 'Daily (Special)':
                        recharge_id = '3sp'
                    else:
                        recharge_id = '5zz'
                elif re.search(r'Utility', source_str):
                    group_str = 'Level ' + level_str + ' Utility'
                else:
                    group_str = 'Level ' + level_str + ' ' + recharge_str 

                # Group ID - this is in the correct sort order according to the Group, by Level then Recharge
                if recharge_id == '':
                    # Utility takes priority over A/E/D
                    if re.search(r'Utility', source_str):
                        recharge_id = '4ut'
                    elif recharge_str == 'At-Will':
                        recharge_id = '1at'
                    elif recharge_str == 'Encounter':
                        recharge_id = '2en'
                    elif recharge_str == 'Daily':
                        recharge_id = '3da'
                    else:
                        recharge_id = '5zz'
                # concatenate padded level and recharge id
                group_id = level_str.rjust(3, '0') + '-' + recharge_id

                if int(level_str) >= settings.min_lvl and int(level_str) <= settings.max_lvl:
                    export_dict = {}
                    export_dict["action"] = action_str
                    export_dict["basename"] = basename_str
                    export_dict["class"] = class_str
                    export_dict["description"] = description_str + published_str
                    export_dict["flavor"] = flavor_str
                    export_dict["group"] = group_str
                    export_dict["group_id"] = group_id
                    export_dict["keywords"] = keywords_str
                    ## add a suffix if a secondary power has the same name as the primary - I don't think this ever occurs
                    export_dict["name"] = name_str if name_str != previous_name else name_str + str(power_id)
                    export_dict["prefix"] = prefix_str
                    export_dict["prefix_id"] = prefix_id
                    export_dict["published"] = published_str
                    export_dict["range"] = range_str
                    export_dict["recharge"] = recharge_str
                    export_dict["shortdescription"] = shortdescription_str.replace('\n', '\\n')
                    export_dict["source"] = source_str

                    # Append a copy of generated item dictionary
                    power_out.append(copy.deepcopy(export_dict))

                # Start next power with the tag that triggered this power creation
                copy_tag = copy.copy(pwr_tag)
                power_html = copy_tag
                power_complete = False
                previous_name = name_str
            # keep adding to the power html until it gets processed
            else:
                copy_tag = copy.copy(pwr_tag)
                power_html.append(copy_tag)

    print(str(len(db_in)) + ' entries checked.')
    print(str(len(power_out)) + ' entries exported.')

    return power_out
