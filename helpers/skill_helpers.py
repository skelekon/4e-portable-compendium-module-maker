import copy
import re
from bs4 import BeautifulSoup, Tag, NavigableString

import settings
from helpers.mod_helpers import clean_formattedtext


ABILITY_MAP = {
    'STRENGTH': 'Str',
    'CONSTITUTION': 'Con',
    'DEXTERITY': 'Dex',
    'INTELLIGENCE': 'Int',
    'WISDOM': 'Wis',
    'CHARISMA': 'Cha',
}


def skill_list_sorter(entry_in):
    name = entry_in["name"]

    return (name)


def skill_xml_id(name_in):
    return re.sub('[^a-zA-Z0-9_]', '', name_in).lower()


def create_skill_library():
    xml_out = ''

    settings.lib_id += 1

    xml_out += (f'\t\t\t\t<id-{settings.lib_id:0>5}>\n')
    xml_out += ('\t\t\t\t\t<librarylink type="windowreference">\n')
    xml_out += ('\t\t\t\t\t\t<class>referenceindex</class>\n')
    xml_out += (f'\t\t\t\t\t\t<recordname>lists.skills@{settings.library}</recordname>\n')
    xml_out += ('\t\t\t\t\t</librarylink>\n')
    xml_out += ('\t\t\t\t\t<name type="string">Skills</name>\n')
    xml_out += (f'\t\t\t\t</id-{settings.lib_id:0>5}>\n')

    return xml_out


def create_skill_list(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    xml_out += ('\t\t<skills>\n')
    xml_out += ('\t\t\t<name type="string">Skills</name>\n')
    xml_out += ('\t\t\t<index>\n')

    for skill_dict in sorted(list_in, key=skill_list_sorter):
        name_lower = skill_xml_id(skill_dict["name"])

        xml_out += (f'\t\t\t\t<{name_lower}>\n')
        xml_out += ('\t\t\t\t\t<listlink type="windowreference">\n')
        xml_out += ('\t\t\t\t\t\t<class>referenceskill</class>\n')
        xml_out += (f'\t\t\t\t\t\t<recordname>reference.skills.{name_lower}@{settings.library}</recordname>\n')
        xml_out += ('\t\t\t\t\t</listlink>\n')
        xml_out += (f'\t\t\t\t\t<name type="string">{skill_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t</{name_lower}>\n')

    xml_out += ('\t\t\t</index>\n')
    xml_out += ('\t\t</skills>\n')

    return xml_out


def create_skill_cards(list_in):
    xml_out = ''

    if not list_in:
        return xml_out

    xml_out += ('\t\t<skills>\n')
    for skill_dict in sorted(list_in, key=skill_list_sorter):
        name_lower = skill_xml_id(skill_dict["name"])

        xml_out += (f'\t\t\t<{name_lower}>\n')
        xml_out += (f'\t\t\t\t<name type="string">{skill_dict["name"]}</name>\n')
        xml_out += (f'\t\t\t\t<ability type="string">{skill_dict["ability"]}</ability>\n')
        xml_out += (f'\t\t\t\t<text type="formattedtext">{skill_dict["description"]}</text>\n')
        xml_out += (f'\t\t\t\t<armorcheckpenalty type="number">{skill_dict["armorcheckpenalty"]}</armorcheckpenalty>\n')
        xml_out += (f'\t\t\t</{name_lower}>\n')
    xml_out += ('\t\t</skills>\n')

    return xml_out


def clean_skill_tag(tag_in):
    for img_tag in tag_in.find_all('img'):
        img_tag.decompose()
    for anchor_tag in tag_in.find_all('a'):
        anchor_tag.replaceWithChildren()
    for clean_tag in tag_in.find_all(True):
        clean_tag.attrs = {}

    tag_in.attrs = {}

    return tag_in


def clean_table_tag(tag_in):
    clean_tag = clean_skill_tag(tag_in)
    for row in clean_tag.find_all('tr'):
        if row.get_text(strip=True) == '':
            row.decompose()

    return clean_tag


def normalize_skill_text(text_in):
    text_out = text_in.replace('\xa0', ' ')
    text_out = re.sub(r'\s+', ' ', text_out)
    text_out = re.sub(r'\s+([,.;:])', r'\1', text_out)

    return text_out.strip()


def create_list(items_in):
    list_items = [item for item in items_in if item != '']

    if not list_items:
        return ''

    xml_out = '<list>'
    for item in list_items:
        xml_out += f'<li>{item}</li>'
    xml_out += '</list>'

    return xml_out


def looks_like_list_item(text_in):
    text_clean = re.sub(r'</?[^>]+>', '', text_in).strip()

    return re.search(r'^(Action|DC|Distance Cleared Vertically|Failure|Failure by [0-9]+ or (Less|More)|Keep out of Sight|Keep Quiet|Keep Still|Don[\'’]t Attack|Not Remaining Hidden|Opposed Check|Reaching Something|Remaining Hidden|Result|Running Start|Success):', text_clean) != None


def format_text_block(text_in):
    text_str = normalize_skill_text(text_in)

    if text_str == '':
        return ''
    if update_match := re.search(r'^Update \(([^)]*)\)$', text_str):
        return f'<p><b>Update ({update_match.group(1)})</b></p>'
    if (text_str.isupper() and len(text_str) <= 80) or text_str in ['High Jump', 'Long Jump', 'Swim']:
        return f'<p><b>{text_str}</b></p>'

    return f'<p>{text_str}</p>'


def create_flavor_content(tag_in):
    parsed_tag = BeautifulSoup(str(tag_in), features="html.parser").find(tag_in.name)
    has_bullets = parsed_tag.find('img') != None or '[[BULLET]]' in parsed_tag.get_text()

    for img_tag in parsed_tag.find_all('img', recursive=False):
        img_tag.replace_with(NavigableString('[[BULLET]]'))
    for anchor_tag in parsed_tag.find_all('a'):
        anchor_tag.replaceWithChildren()

    description_parts = []
    list_items = []
    line_fragments = []
    line_is_bullet = False
    emitted_line = False

    def flush_list():
        nonlocal list_items
        if list_items:
            description_parts.append(create_list(list_items))
            list_items = []

    def flush_line():
        nonlocal emitted_line, line_fragments, line_is_bullet
        line_text = normalize_skill_text(''.join(line_fragments))
        if line_text != '':
            if line_is_bullet or (has_bullets and looks_like_list_item(line_text)):
                list_items.append(line_text)
            else:
                flush_list()
                description_parts.append(format_text_block(line_text))
            emitted_line = True
        line_fragments = []
        line_is_bullet = False

    for tag in parsed_tag.children:
        if isinstance(tag, NavigableString):
            tag_text = str(tag)
            while '[[BULLET]]' in tag_text:
                before_marker, tag_text = tag_text.split('[[BULLET]]', 1)
                if before_marker != '':
                    line_fragments.append(before_marker)
                    flush_line()
                else:
                    flush_line()
                line_is_bullet = True
            if tag_text != '':
                line_fragments.append(tag_text)
        elif isinstance(tag, Tag):
            if tag.name == 'br':
                flush_line()
            elif tag.name == 'table':
                flush_line()
                flush_list()
                description_parts.append(str(clean_table_tag(tag)))
            elif tag.name in ['h2', 'h3', 'h4']:
                flush_line()
                flush_list()
                description_parts.append(format_text_block(tag.get_text(' ', strip=True)))
            elif tag.name == 'p' and 'flavor' in tag.get('class', []):
                flush_line()
                flush_list()
                description_parts.append(create_flavor_content(tag))
            elif tag.name in ['p', 'ol', 'ul', 'list']:
                flush_line()
                flush_list()
                description_parts.append(str(clean_skill_tag(tag)))
            else:
                line_fragments.append(create_inline_fragment(tag))

    flush_line()
    flush_list()

    return ''.join(description_parts)


def create_inline_fragment(tag_in):
    if isinstance(tag_in, NavigableString):
        return str(tag_in)
    if isinstance(tag_in, Tag):
        if tag_in.name in ['br', 'img']:
            return ''
        return str(clean_skill_tag(tag_in))

    return ''


def collect_top_level_bullet(children_in, index_in):
    item_fragments = []
    idx = index_in + 1

    while idx < len(children_in):
        next_tag = children_in[idx]
        if isinstance(next_tag, Tag) and next_tag.name == 'img':
            break
        if isinstance(next_tag, Tag) and next_tag.name == 'br':
            idx += 1
            break
        if isinstance(next_tag, Tag) and next_tag.name in ['h1', 'h2', 'h3', 'h4', 'p', 'table']:
            break

        item_fragments.append(create_inline_fragment(next_tag))
        idx += 1

    return normalize_skill_text(''.join(item_fragments)), idx


def format_skill_description(detail_div):
    description_parts = []
    top_level_list = []
    children = list(detail_div.children)
    idx = 0

    def flush_top_level_list():
        nonlocal top_level_list
        if top_level_list:
            description_parts.append(create_list(top_level_list))
            top_level_list = []

    while idx < len(children):
        tag = children[idx]

        if isinstance(tag, NavigableString):
            tag_text = normalize_skill_text(str(tag).replace('\n', ''))
            if tag_text != '':
                flush_top_level_list()
                description_parts.append(f'<p>{tag_text}</p>')
            idx += 1
            continue

        if not isinstance(tag, Tag):
            idx += 1
            continue

        if tag.name == 'img':
            item_str, idx = collect_top_level_bullet(children, idx)
            if item_str != '':
                top_level_list.append(item_str)
            continue

        if tag.name == 'br':
            idx += 1
            continue

        flush_top_level_list()

        if tag.name == 'h1':
            pass
        elif tag.name in ['h2', 'h3', 'h4']:
            description_parts.append(f'<p><b>{normalize_skill_text(tag.get_text(" ", strip=True))}</b></p>')
        elif tag.name == 'p' and 'flavor' in tag.get('class', []):
            description_parts.append(create_flavor_content(tag))
        elif tag.name == 'table':
            description_parts.append(str(clean_table_tag(tag)))
        elif tag.name in ['p', 'ol', 'ul', 'list']:
            description_parts.append(str(clean_skill_tag(tag)))
        else:
            description_parts.append(f'<p>{str(clean_skill_tag(tag))}</p>')

        idx += 1

    flush_top_level_list()

    description_str = ''.join(description_parts)
    description_str = re.sub(r'<ul>', '<list>', description_str)
    description_str = re.sub(r'</ul>', '</list>', description_str)
    description_str = re.sub(r'<ol>', '<list>', description_str)
    description_str = re.sub(r'</ol>', '</list>', description_str)
    description_str = clean_formattedtext(description_str)
    description_str = re.sub(r'<p>\s*Update \(([^)]*)\)\s*</p>', r'<p><b>Update (\1)</b></p>', description_str)
    description_str = re.sub(r'<p>\s*<br/>\s*', '<p>', description_str)
    description_str = re.sub(r'<p>\s*</p>', '', description_str)

    return description_str


def extract_skill_db(db_in):
    skills_out = []

    print('\n\n\n=========== SKILLS ===========')
    for row in db_in:
        html_text = row["Txt"]
        html_text = html_text.replace('\\r\\n', '\r\n').replace('\\', '')
        parsed_html = BeautifulSoup(html_text, features="html.parser")

        name_str = row["Name"].replace('\\', '')
        ability_str = ''
        armorcheckpenalty_str = '0'

        if detail_div := parsed_html.find('div', id='detail'):
            if name_tag := detail_div.find('h1', class_='player'):
                if name_match := re.search(r'^\s*(.*?)\s*\((.*?)\)\s*$', name_tag.get_text(strip=True)):
                    name_str = name_match.group(1).title()
                    ability_str = ABILITY_MAP.get(name_match.group(2).upper(), name_match.group(2).title())

            if re.search(r'Armor Check Penalty', detail_div.get_text(' ', strip=True), re.IGNORECASE):
                armorcheckpenalty_str = '1'

            description_str = format_skill_description(detail_div)
        else:
            description_str = ''

        export_dict = {}
        export_dict["ability"] = ability_str
        export_dict["armorcheckpenalty"] = armorcheckpenalty_str
        export_dict["description"] = description_str
        export_dict["name"] = name_str

        skills_out.append(copy.deepcopy(export_dict))

    print(str(len(db_in)) + ' entries parsed.')
    print(str(len(skills_out)) + ' entries exported.')

    return skills_out
