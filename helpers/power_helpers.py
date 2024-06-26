import settings

import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .create_db import create_db

from helpers.mi_helpers import mi_list_sorter
from helpers.mi_helpers import multi_level
from helpers.mi_helpers import power_construct
from helpers.mi_helpers import powers_format
from helpers.mi_helpers import props_format

def classes_list():
    # These classes only have subclasses listed, so we need a 'base' version for string matching
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


def card_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def create_power_library(list_in, suffix_in):
    lib_xml = ''

    if not list_in:
        return lib_xml

    # Create one levels of menu except for Race, Class, Paragon Path, Epic Destiny

    previous_class = ''
    for power_dict in sorted(list_in, key=library_list_sorter):
        # skip these until later
        if power_dict["prefix"] in ['Class Powers', 'Racial Powers', 'Paragon Path Powers', 'Epic Destiny Powers']:
            continue

        if power_dict["class"] != previous_class:
            previous_class = power_dict["class"]
            class_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"]).lower()

            settings.lib_id += 1

            lib_xml += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
            lib_xml += ('\t\t\t\t\t<librarylink type="windowreference">\n')
            lib_xml += ('\t\t\t\t\t\t<class>reference_classpowerlist</class>\n')
            lib_xml += (f'\t\t\t\t\t\t<recordname>lists.powers.{class_lower}@{settings.library}</recordname>\n')
            lib_xml += ('\t\t\t\t\t</librarylink>\n')
            lib_xml += (f'\t\t\t\t\t<name type="string">{power_dict["prefix"]} - {power_dict["class"]}{suffix_in}</name>\n')
            lib_xml += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    # Create two levels of menu for Race, Class, Paragon Path, Epic Destiny

    previous_prefix = ''
    previous_class = ''
    for power_dict in sorted(list_in, key=library_list_sorter):

        # do 2 levels of menu if not one of these Power classes
        if not(power_dict["prefix"] in ['Class Powers', 'Racial Powers', 'Paragon Path Powers', 'Epic Destiny Powers']):
            continue
        
        prefix_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["prefix"]).lower()
        # Required to handle that there is both a Warmaster and a War Master E.D.
        if power_dict["class"] == 'War Master':
            class_lower = 'war_master'
        else:
            class_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"]).lower()

        # we only care when something changes
        if power_dict["prefix"] == previous_prefix and power_dict["class"] == previous_class:
            continue

        # Check for new Library
        if power_dict["prefix"] != previous_prefix:

            # Close previous Library
            if previous_prefix != '':
                lib_xml += (f'\t\t\t\t\t</index>\n')
                lib_xml += (f'\t\t\t\t\t<name type="string">Powers - {previous_prefix}{suffix_in}</name>\n')
                lib_xml += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

            # Open new Library
            settings.lib_id += 1

            lib_xml += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
            lib_xml += ('\t\t\t\t\t<librarylink type="windowreference">\n')
            lib_xml += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
            lib_xml += (f'\t\t\t\t\t\t<recordname>..</recordname>\n')
            lib_xml += ('\t\t\t\t\t</librarylink>\n')
            lib_xml += (f'\t\t\t\t\t<index>\n')

        # Check for new Class
        if power_dict["class"] != previous_class:

            # Write new Class
            lib_xml += (f'\t\t\t\t\t\t<{class_lower}>\n')
            lib_xml += ('\t\t\t\t\t\t\t<listlink type="windowreference">\n')
            lib_xml += ('\t\t\t\t\t\t\t\t<class>reference_classpowerlist</class>\n')
            lib_xml += (f'\t\t\t\t\t\t\t\t<recordname>lists.powers.{class_lower}@{settings.library}</recordname>\n')
            lib_xml += ('\t\t\t\t\t\t\t</listlink>\n')
            lib_xml += (f'\t\t\t\t\t\t\t<name type="string">{power_dict["class"]}{suffix_in}</name>\n')
            lib_xml += (f'\t\t\t\t\t\t</{class_lower}>\n')

        previous_class = power_dict["class"]
        previous_prefix = power_dict["prefix"]

    # Close final Library if there were any nested menus
    if previous_prefix != '':
        lib_xml += ('\t\t\t\t\t</index>\n')
        lib_xml += (f'\t\t\t\t\t<name type="string">Powers - {previous_prefix}{suffix_in}</name>\n')
        lib_xml += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return lib_xml


def create_power_list(list_in):
    list_xml = ''

    if not list_in:
        return list_xml

    previous_class = ''
    previous_group = ''
    class_lower = ''

    # Power List
    # This controls the table that appears when you click on a Library menu
    list_xml += ('\t\t<powers>\n')

    # Create individual item entries
    for power_dict in sorted(list_in, key=power_list_sorter):
        # Required to handle that there is both a Warmaster and a War Master E.D.
        if power_dict["class"] == 'War Master':
            class_lower = 'war_master'
        else:
            class_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"]).lower()
        group_lower = power_dict["group_id"].lower()
        name_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"]).lower()

        # Check for new Class
        if class_lower != previous_class:

            # Close previous Group
            if previous_group != '':
                list_xml += ('\t\t\t\t\t</powers>\n')
                list_xml += (f'\t\t\t\t\t</{previous_class}_{previous_group}>\n')

            # Close previous Class
            if previous_class != '':
                list_xml += ('\t\t\t\t</groups>\n')
                list_xml += (f'\t\t\t</{previous_class}>\n')

            # Open new Class
            previous_group = group_lower
            list_xml += (f'\t\t\t<{class_lower}>\n')
            list_xml += (f'\t\t\t\t<description type="string">{power_dict["class"]}</description>\n')
            list_xml += ('\t\t\t\t<groups>\n')
    
            # Open new Group
            list_xml += (f'\t\t\t\t\t<{class_lower}_{group_lower}>\n')
            list_xml += (f'\t\t\t\t\t<description type="string">{power_dict["group"]}</description>\n')
            list_xml += ('\t\t\t\t\t<powers>\n')

        # Check for new Group
        if group_lower != previous_group:

            # Close previous Group
            if previous_group != '':
                list_xml += ('\t\t\t\t\t\t</powers>\n')
                list_xml += (f'\t\t\t\t\t</{class_lower}_{previous_group}>\n')

            # Open new Group if not the first entry in the table
            if previous_class != '':
                list_xml += (f'\t\t\t\t\t<{class_lower}_{group_lower}>\n')
                list_xml += (f'\t\t\t\t\t<description type="string">{power_dict["group"]}</description>\n')
                list_xml += ('\t\t\t\t\t<powers>\n')

        # Powers list entry
        list_xml += (f'\t\t\t\t\t\t<{name_lower}>\n')
        list_xml += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        list_xml += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        list_xml += (f'\t\t\t\t\t\t\t\t<recordname>reference.powers.{name_lower}@{settings.library}</recordname>\n')
        list_xml += ('\t\t\t\t\t\t\t</link>\n')
        list_xml += (f'\t\t\t\t\t\t\t<name type="string">{power_dict["name"]}</name>\n')
        list_xml += (f'\t\t\t\t\t\t</{name_lower}>\n')

        previous_class = class_lower
        previous_group = group_lower

    # Close final Group
    list_xml += ('\t\t\t\t\t</powers>\n')
    list_xml += (f'\t\t\t\t\t</{class_lower}_{previous_group}>\n')

    # Close final Class
    list_xml += ('\t\t\t\t</groups>\n')
    list_xml += (f'\t\t\t</{class_lower}>\n')

    list_xml += ('\t\t</powers>\n')

    return list_xml


def create_linkedpowers(basename_in, name_in, list_in):
    xml_out = ''
    linked_list = []

    # Loop through the list of powers to find a related power
    for pwr_dict in list_in:
        if pwr_dict["basename"] == basename_in and pwr_dict["name"] != name_in:
            linked_list.append(pwr_dict["name"])

    # Create any linked power entries
    for pwr in linked_list:
        power_lower = re.sub('[^a-zA-Z0-9_]', '', pwr).lower()
        xml_out += (f'\t\t\t\t\t<{power_lower}>\n')
        xml_out += ('\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t<recordname>reference.powers.{power_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t</{power_lower}>\n')
    
    return xml_out


def create_power_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    # Create individual item entries
    for power_dict in sorted(list_in, key=card_list_sorter):

        # Only the first power from an entry gets the linked powers, otherwise it causes an infinite loop when adding to a PC sheet
        if power_dict["power_id"] == 1:
            linked_powers = create_linkedpowers(power_dict["basename"], power_dict["name"], list_in)
        else:
            linked_powers = ''

        name_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"]).lower()

        xml_out += (f'\t\t\t<{name_lower}>\n')
        xml_out += (f'\t\t\t\t<action type="string">{power_dict["action"]}</action>\n')
        xml_out += (f'\t\t\t\t<description type="formattedtext">{power_dict["description"]}</description>\n')
        xml_out += (f'\t\t\t\t<flavor type="string">{power_dict["flavor"]}</flavor>\n')
        xml_out += (f'\t\t\t\t<keywords type="string">{power_dict["keywords"]}</keywords>\n')
        if linked_powers != '':
            xml_out += (f'\t\t\t\t<linkedpowers>\n{linked_powers}\t\t\t\t</linkedpowers>\n')
        else:
            xml_out += ('\t\t\t\t<linkedpowers />\n')
        xml_out += (f'\t\t\t\t<name type="string">{power_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t<range type="string">{power_dict["range"]}</range>\n')
        xml_out += (f'\t\t\t\t<recharge type="string">{power_dict["recharge"]}</recharge>\n')
## the description is required twice as this unformatted one is copied to the character sheet when a power is added
        xml_out += (f'\t\t\t\t<shortdescription type="string">{power_dict["shortdescription"]}</shortdescription>\n')
        xml_out += (f'\t\t\t\t<source type="string">{power_dict["source"]}</source>\n')
        xml_out += (f'\t\t\t</{name_lower}>\n')

    return xml_out


def extract_power_db(db_in):
    power_out = []

    # Add MBA/RBA/Bull Rush/Grab
    basic_dict = {}
    if settings.basic:

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
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Target</b>: One creature that is no more than one size category larger than you</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Attack</b>: Strength vs. Reflex</p>'
        basic_dict["Txt"] += '<p class=\"flavor\"><b>Hit</b>: You grab the target until the end of your next turn. You can end the grab as a free action.</p>'
        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Sustain Minor</b>: The grab persists until the end of your next turn.</p>'
        basic_dict["Txt"] += '<br/>'
        basic_dict["Txt"] += '<p class=\"publishedIn\">Published in <a href=\"http://anonym.to/?http://www.wizards.com/default.asp?x=products/dndacc/9780786950164\" target=\"_new\">Rules Compendium</a>, page(s) 243.</p>'
        basic_dict["Txt"] += '</div>'
        db_in.append(copy.deepcopy(basic_dict))

    # Add class 'powers' that are not in the Powers database
##    if settings.powers or settings.classes:
##        basic_dict["Name"] = 'Hunter\'s Quarry'
##        basic_dict["Class"] = 'Ranger'
##        basic_dict["Level"] = '0'
##        basic_dict["Txt"] = '<div id=\"detail\">'
##        basic_dict["Txt"] += '<h1 class=\"atwillpower\"><span class=\"level\">Hunter\'s Quarry</span>Hunter\'s Quarry</h1>'
##        basic_dict["Txt"] += '<p class=\"powerstat\"><b>At-Will</b><br/><b>Minor Action</b></p>'
##        basic_dict["Txt"] += '<p class=\"powerstat\"><b>Effect</b>: You can designate the nearest enemy to you that you can see as your quarry.</p>'
##        basic_dict["Txt"] += '<br/>'
##        basic_dict["Txt"] += '<p class=\"publishedIn\">Published in <a href=\"http://anonym.to/?http://www.wizards.com/default.asp?x=products/dndacc/217367200\" target=\"_new\">Player\'s Handbook</a>, page(s) 103.</p>'
##        basic_dict["Txt"] += '</div>'
##        db_in.append(copy.deepcopy(basic_dict))


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
        paragon_list = paragon_paths_list()
    except:
        paragon_list = []

    try:
        epic_list = epic_destinies_list()
    except:
        epic_list = []

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

#        if basename_str not in ['Preserver\'s Rebuke', 'Armor of Wrath']:#'Brilliant Strategy', 'Your Doom Awaits', 'Iron Fist', 'Psychic Anomaly', 'Eyes of the Vestige']: #, 'Aggressive Lunge', 'Demoralizing Strike', 'Cloud of Daggers', 'Spell Magnet', 'Open the Gate of Battle [Attack Technique]', 'Turn Undead', 'Healing Word', 'Holy Cleansing', 'Grease']:
#            continue
#        print(basename_str)        

        # sort order for the Library list based on the broad class of the power
        prefix_id = 0
        prefix_str = ''

        if class_str in cc_list:
            prefix_id = 2
            prefix_str = 'Class Powers'
        elif class_str in race_list:
            prefix_id = 3
            prefix_str = 'Racial Powers'
        elif class_str in paragon_list:
            prefix_id = 5
            prefix_str = 'Paragon Path Powers'
        elif class_str in epic_list:
            prefix_id = 6
            prefix_str = 'Epic Destiny Powers'
        else:
            prefix_id = 1
            prefix_str = 'Powers'

        # Work out whether to process this Power
        process_flag = False
        # all Powers
        if settings.powers == True:
            process_flag = True

        # also export Racial powers if this run has Races
        if settings.races and prefix_str == 'Racial Powers' and basename_str in settings.races_power_list:
            process_flag = True

        # also export Classes powers if this run has Classes
        if settings.classes and prefix_str == 'Class Powers' and basename_str in settings.classes_power_list:
            process_flag = True

        # also export Heroic Theme powers if this run has Heroic Themes
        if settings.heroic and prefix_str == 'Powers' and basename_str in settings.heroic_power_list:
            process_flag = True

        # also export Paragon Path powers if this run has Paragon Paths
        if settings.paragon and prefix_str == 'Paragon Path Powers' and basename_str in settings.paragon_power_list:
            process_flag = True

        # also export Epic Destiny powers if this run has Epic Destinies
        if settings.epic and prefix_str == 'Epic Destiny Powers' and basename_str in settings.epic_power_list:
            process_flag = True

        # also export Feat powers if this run has Feats
        if settings.feats and prefix_str == 'Powers' and basename_str in settings.feat_power_list:
            process_flag = True

        if not process_flag:
            continue

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
            published_str = str(published_tag)

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
                # small number of powers have alternate capitalization
                if recharge_str == 'At-will':
                    recharge_str = 'At-Will'

                # Powerstat class - this is used to find Action, Range, Keywords
                powerstat_p = power_html.find('p', class_='powerstat')

                # Action
                powerstat_br = powerstat_p.find('br')
                action_tag = powerstat_br.find_next_sibling('b')
                action_str = action_tag.text

                # Range
                range_tag = action_tag.find_next_sibling('b')
                if range_tag:
                    range_next = range_tag.next_sibling
                    range_str = range_tag.text + range_next.text if range_next else range_tag.text

                # Keywords
                keywords = []
                power_bullet = powerstat_p.find('img', attrs={'src': 'images/bullet.gif'})
                if power_bullet:
                    for tag in power_bullet.next_siblings:
                        if tag.name == 'br':
                            break
                        elif tag.name == 'b':
                            keywords.append(tag.text)
                keywords_str = ', '.join(keywords)

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

                # Short Description
                # remove tags after replacing new paragraphs with newlines
                shortdescription_str = re.sub('<.*?>', '', description_str.replace('</p><p>', '\n'))
                shortdescription_str = shortdescription_str.replace('\n', '\\n')

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
                group_id = f'{level_str:0>2}_{recharge_id}'

                if int(level_str) >= settings.min_lvl and int(level_str) <= settings.max_lvl:
                    export_dict = {}
                    export_dict["action"] = action_str
                    export_dict["basename"] = basename_str
                    export_dict["class"] = class_str
                    export_dict["description"] = description_str
                    export_dict["flavor"] = flavor_str
                    export_dict["group"] = group_str
                    export_dict["group_id"] = group_id
                    export_dict["keywords"] = keywords_str
                    ## add a suffix if a secondary power has the same name as the primary - I don't think this ever occurs
                    export_dict["name"] = name_str if name_str != previous_name else name_str + str(power_id)
                    export_dict["power_id"] = power_id
                    export_dict["prefix"] = prefix_str
                    export_dict["prefix_id"] = prefix_id
                    export_dict["published"] = published_str
                    export_dict["range"] = range_str
                    export_dict["recharge"] = recharge_str
                    export_dict["shortdescription"] = shortdescription_str
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
