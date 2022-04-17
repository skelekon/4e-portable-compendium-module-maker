import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

from .create_db import create_db

from .mod_helpers import mi_list_sorter
from .mod_helpers import multi_level
from .mod_helpers import power_construct
from .mod_helpers import powers_format
from .mod_helpers import props_format


def races_list():
    race_out = []
    race_db = []
    race_db = create_db('ddiRace.sql', "','")
    for i, row in enumerate(race_db, start=1):
        race_out.append(row["Name"].replace('\\', ''))
    race_out.sort()
    return race_out

def classes_list():
    cc_out = []
    cc_db = []
    cc_db = create_db('ddiClass.sql', "','")
    for i, row in enumerate(cc_db, start=1):
        cc_out.append(row["Name"].replace('\\', ''))
    cc_out.sort()
    return cc_out

def heroic_themes_list():
    ht_out = []
    ht_db = []
    ht_db = create_db('ddiTheme.sql', "','")
    for i, row in enumerate(ht_db, start=1):
        ht_out.append(row["Name"].replace('\\', ''))
    ht_out.sort()
    return ht_out

def paragon_paths_list():
    pp_out = []
    pp_db = []
    pp_db = create_db('ddiParagonPath.sql', "','")
    for i, row in enumerate(pp_db, start=1):
        pp_out.append(row["Name"].replace('\\', ''))
    pp_out.sort()
    return pp_out

def epic_destinies_list():
    ed_out = []
    ed_db = []
    ed_db = create_db('ddiEpicDestiny.sql', "','")
    for i, row in enumerate(ed_db, start=1):
        ed_out.append(row["Name"].replace('\\', ''))
    ed_out.sort()
    return ed_out

def replace_line_breaks(soup):
    while soup.p.br:
        soup.p.br.replace_with('\n')

def construct_description(tags, tag_classes):
    description = []
    shortdescription = []
    for t in tags:
        child_tags = t.find_all(class_=tag_classes)
        if child_tags:
            desc, sdesc = construct_description(child_tags, tag_classes)
            description += desc
            shortdescription+= sdesc
        else:
            soup = BeautifulSoup(str(t), features="html.parser")
            if soup.p:
                soup.p.wrap(soup.new_tag('p'))
                soup.p.p.unwrap()
                # Replace any line breaks with new p tags or newline characters
                description += [str(soup).replace("<br/>", "</p>\n<p>")]
                replace_line_breaks(soup)
                shortdescription += [soup.text]
            elif soup.h1:
                soup.h1.wrap(soup.new_tag('h'))
                soup.h.h1.unwrap()
                description += [str(soup)]
                shortdescription += [soup.text]
    return description, shortdescription

def library_list_sorter(entry_in):
    prefix_id = entry_in["prefix_id"]
    clss = entry_in["class"]

    return (prefix_id, clss)

def power_list_sorter(entry_in):
    clss = entry_in["class"]
    group_id = entry_in["group_id"]
    name = entry_in["name"]

    return (clss, group_id, name)

def create_power_library(id_in, library_in, list_in, name_in):
    xml_out = ''

    if not list_in:
        return xml_out

    previous_class = ''
    for power_dict in sorted(list_in, key=library_list_sorter):
        if power_dict["class"] != previous_class:
            previous_class = power_dict["class"]
            class_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"].lower())

            id_in += 1
            entry_id = '000'[0:len('000')-len(str(id_in))] + str(id_in)

            xml_out += (f'\t\t\t\t<a{entry_id}class-{class_lower}>\n')
            xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
            xml_out += ('\t\t\t\t\t\t<class>reference_classpowerlist</class>\n')
            xml_out += (f'\t\t\t\t\t\t<recordname>powerlists.class-{class_lower}@{library_in}</recordname>\n')
            xml_out += ('\t\t\t\t\t</librarylink>\n')
            xml_out += (f'\t\t\t\t\t<name type="string">{power_dict["prefix"]} - {power_dict["class"]}</name>\n')
            xml_out += (f'\t\t\t\t</a{entry_id}class-{class_lower}>\n')
    return xml_out, id_in

def create_power_table(list_in, library_in):
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
        class_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["class"].lower())
        group_lower = power_dict["group_id"]
        name_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"])

        #Check for new Class
        if class_lower != previous_class:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</{previous_class}-{previous_group}>\n')

            # Close previous Class
            if previous_class != '':
                xml_out += ('\t\t\t</groups>\n')
                xml_out += (f'\t\t</class-{previous_class}>\n')

            # Open new Class
            previous_group = group_lower
            xml_out += (f'\t\t<class-{class_lower}>\n')
            xml_out += (f'\t\t\t<description type="string">{power_dict["class"]}</description>\n')
            xml_out += ('\t\t\t<groups>\n')
    
            # Open new Group
            xml_out += (f'\t\t\t\t<{class_lower}-{group_lower}>\n')
            xml_out += (f'\t\t\t\t<description type="string">{power_dict["group"]}</description>\n')
            xml_out += ('\t\t\t\t\t<powers>\n')

        # Check for new Group
        if group_lower != previous_group:

            # Close previous Group
            if previous_group != '':
                xml_out += ('\t\t\t\t\t</powers>\n')
                xml_out += (f'\t\t\t\t</{class_lower}-{previous_group}>\n')

            # Open new Group if not the first entry in the table
            if previous_class != '':
                xml_out += (f'\t\t\t\t<{class_lower}-{group_lower}>\n')
                xml_out += (f'\t\t\t\t<description type="string">{power_dict["group"]}</description>\n')
                xml_out += ('\t\t\t\t\t<powers>\n')

        # Powers list entry
        xml_out += (f'\t\t\t\t\t\t<power{name_lower}>\n')
        xml_out += ('\t\t\t\t\t\t\t<link type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t\t\t<class>powerdesc</class>\n')
        xml_out += (f'\t\t\t\t\t\t\t\t<recordname>powerdesc.power{name_lower}@{library_in}</recordname>\n')
        xml_out += ('\t\t\t\t\t\t\t</link>\n')
        xml_out += (f'\t\t\t\t\t\t\t<source type="string">{power_dict["name"]}</source>\n')
        xml_out += (f'\t\t\t\t\t\t</power{name_lower}>\n')

        previous_class = class_lower
        previous_group = group_lower

    # Close final Group
    xml_out += ('\t\t\t\t\t</powers>\n')
    xml_out += (f'\t\t\t\t</{class_lower}-{previous_group}>\n')

    # Close final Class
    xml_out += ('\t\t\t</groups>\n')
    xml_out += (f'\t\t</class-{class_lower}>\n')

    return xml_out

def create_power_desc(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    section_str = ''
    entry_str = ''
    name_lower = ''

    # Create individual item entries
    for power_dict in sorted(list_in, key=power_list_sorter):
        name_lower = re.sub('[^a-zA-Z0-9_]', '', power_dict["name"])

        xml_out += (f'\t\t<power{name_lower}>\n')
        xml_out += (f'\t\t\t<name type="string">{power_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t<recharge type="string">{power_dict["recharge"]}</recharge>\n')
        xml_out += (f'\t\t\t<keywords type="string">{power_dict["keywords"]}</keywords>\n')
        xml_out += (f'\t\t\t<action type="string">{power_dict["action"]}</action>\n')
        xml_out += (f'\t\t\t<range type="string">{power_dict["range"]}</range>\n')
        xml_out += (f'\t\t\t<source type="string">{power_dict["source"]}</source>\n')
        xml_out += (f'\t\t\t<description type="formattedtext">{power_dict["description"]}\n\t\t\t\t</description>\n')
        xml_out += (f'\t\t\t<shortdescription type="string">{power_dict["shortdescription"]}\n\t\t\t\t</shortdescription>\n')
        xml_out += (f'\t\t\t<class type="string">{power_dict["class"]}</class>\n')
        xml_out += (f'\t\t\t<powertype type="string">{power_dict["name"]}</powertype>\n')
        xml_out += (f'\t\t\t<level type="string">{power_dict["level"]}</level>\n')
        xml_out += (f'\t\t\t<tier type="string">{power_dict["name"]}</tier>\n')
        xml_out += (f'\t\t\t<type type="string">{power_dict["name"]}</type>\n')
        xml_out += (f'\t\t\t<flavor type="formattedtext">{power_dict["flavor"]}</flavor>\n')
        xml_out += (f'\t\t\t<stringflavor type="string">{power_dict["name"]}</stringflavor>\n')
        xml_out += (f'\t\t\t<requirement type="string">{power_dict["name"]}</requirement>\n')
        xml_out += (f'\t\t\t<target type="string">{power_dict["name"]}</target>\n')
        xml_out += (f'\t\t\t<attack type="string">{power_dict["name"]}</attack>\n')
        xml_out += (f'\t\t\t<hit type="string">{power_dict["name"]}</hit>\n')
        xml_out += (f'\t\t</power{name_lower}>\n')

    return xml_out

def extract_power_list(db_in, library_in, min_lvl, max_lvl):
    power_out = []


    # Build regex expressions for checking Classes/Races/Themes/PPs/EDs
    try:
        cc_list = classes_list()
    except:
        cc_list = []
    cc_str = '|'.join(cc_list)
    cc_expr = re.compile('^(' + cc_str + '|Cleric|Fighter|Rogue|Warlord|Wizard)$')

    try:
        race_list = races_list()
    except:
        race_list = []
    race_str = '|'.join(race_list)
    race_expr = re.compile('^(' + race_str + '|Cleric|Fighter|Rogue|Warlord|Wizard)$')

    try:
        ht_list = heroic_themes_list()
    except:
        ht_list = []
    ht_str = '|'.join(ht_list)
    ht_expr = re.compile('^(' + ht_str + ')$')

    try:
        pp_list = paragon_paths_list()
    except:
        pp_list = []
    pp_str = '|'.join(pp_list)
    pp_expr = re.compile('^(' + pp_str + ')$')

    try:
        ed_list = epic_destinies_list()
    except:
        ed_list = []
    ed_str = '|'.join(ed_list)
    ed_expr = re.compile('^(' + ed_str + ')$')

    print('\n\n\n=========== POWERS ===========')
    for i, row in enumerate(db_in, start=1):

        # Parse the HTML text 
        html = row["Txt"]
        html = html.replace('\\r\\n','\r\n').replace('\\','')
        parsed_html = BeautifulSoup(html, features="html.parser")

        # Retrieve the data with dedicated columns
        name_str =  row["Name"].replace('\\', '')
        class_str =  row["Class"].replace('\\', '')
        level_str =  row["Level"].replace('\\', '')
        published_str =  row["Source"].replace('\\', '')
        recharge_str =  row["Usage"].replace('\\', '')

        action_str = ''
        description_str = ''
        flavor_str = ''
        group_str = ''
        keywords_str = ''
        prefix_str = ''
        published_str = ''
        range_str = ''
        shortdescription_str = ''
        group_id = ''
        source_str = ''

        # PP workaround
        if re.search(r'^Hammer of Vengeance', class_str):
            class_str = 'Hammer of Vengeance'

        prefix_id = 0
        if re.search(cc_expr, class_str):
            prefix_id = 1
            prefix_str = 'Powers'
        elif re.search(race_expr, class_str):
            prefix_id = 2
            prefix_str = 'Racial'
        elif re.search(ht_expr, class_str):
            prefix_id = 3
            prefix_str = 'Theme'
        elif re.search(pp_expr, class_str):
            prefix_id = 4
            prefix_str = 'Paragon Path'
        elif re.search(ed_expr, class_str):
            prefix_id = 5
            prefix_str = 'Epic Destiny'
        else:
            prefix_id = 1
            prefix_str = 'Powers'

        # Power source doesn't always match with "{Class} {Kind} {Level}".
        # Ergo, get it directly from the power's header.
        source_str = parsed_html.find('span', class_='level').text

        # Get the Power statline:  Recharge, Keywords, Action, and Range.
        # We already have Recharge & Action; get Keywords & Range.
        powerstat_lbl = parsed_html.find('p', class_='powerstat')

        # If a power has a bullet, check for keywords after the bullet but
        # before the line break.
        keywords = []
        power_bullet = powerstat_lbl.find('img', attrs={'src': 'images/bullet.gif'})
        if power_bullet:
            for tag in power_bullet.next_siblings:
                if tag.name == "br":
                    break
                elif tag.name == "b":
                    keywords.append(tag.text)
        
        keywords_str = ", ".join(keywords)

        # Find the Action, immediately after the stat line break.
        powerstat_br = powerstat_lbl.find('br')
        powerstat_action = powerstat_br.find_next_sibling('b')
        action_str = powerstat_action.text

        # Find the range, if present; it's always after the Action.
        powerstat_rg_type = powerstat_action.find_next_sibling('b')
        range_str = ''
        if powerstat_rg_type:
            powerstat_rg = powerstat_rg_type.next_sibling
            rg_text = powerstat_rg.text if powerstat_rg else ''
            range_str = f'{powerstat_rg_type.text}{rg_text}'

        # Acquire flavor text, if present. Flavor text is always in italics.
        flavor_str = ''
        if flavor_tag := parsed_html.select_one('.flavor > i'):
            flavor_str = flavor_tag.text

        # Everything in a tag after the stat line is mechanics text.
        # Mechanics text can be either p (normal mechanics) or h1 (embedded power header).
        # Description will include all mechanics text + Published line.
        sibling_classes = ['powerstat', 'flavor', 'atwillpower', 'encounterpower', 'dailypower']
        power_mechanics = powerstat_lbl.find_next_siblings(class_=sibling_classes)

        try:
            description, shortdescription = construct_description(power_mechanics, sibling_classes)

            # Grab the Published line without external links, in class-less p tag
            published_in = parsed_html.find('p', class_='publishedIn')
            pub_soup = BeautifulSoup(str(published_in), features="html.parser")
            pub_soup.p.wrap(pub_soup.new_tag('p'))
            pub_soup.p.p.replace_with(pub_soup.p.p.text)
            description.append(str(pub_soup))
            shortdescription.append(pub_soup.text)
        except:
            print(f'Problem with {row["Name"]}')
            raise

        description_str = '\n'.join(description)
        shortdescription_str = '\n'.join(shortdescription)

        # Group - this is the subheading on the Powers table
        if level_str == '0':
            group_str = recharge_str + ' Features'
        else:
            group_str = 'Level ' + level_str + ' ' + recharge_str 

        # Group ID - this is in the correct sort order according to the Group, by Level then Recharge
        if recharge_str == 'At-Will':
            group_id = 'aat'
        elif recharge_str == 'Encounter':
            group_id = 'ben'
        elif recharge_str == 'Daily':
            group_id = 'cda'
        elif recharge_str == 'Utility':
            group_id = 'dut'
        else:
            group_id = 'zzz'
        group_id = '000'[0:len('000')-len(level_str)] + level_str + group_id



        export_dict = {}
        export_dict["action"] = action_str
        export_dict["class"] = class_str
        export_dict["description"] = description_str
        export_dict["flavor"] = flavor_str
        export_dict["group"] = group_str
        export_dict["group_id"] = group_id
        export_dict["keywords"] = keywords_str
        export_dict["level"] = level_str
        export_dict["name"] = name_str
        export_dict["prefix"] = prefix_str
        export_dict["prefix_id"] = prefix_id
        export_dict["published"] = published_str
        export_dict["range"] = range_str
        export_dict["recharge"] = recharge_str
        export_dict["shortdescription"] = shortdescription_str
        export_dict["source"] = source_str

##        if re.search(class_expr, export_dict["class"]):

            # Append a copy of generated item dictionary
        power_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(power_out)) + ' entries exported.')

    return power_out
