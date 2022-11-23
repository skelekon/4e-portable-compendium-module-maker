import settings

import optparse
import os
import re
import shutil
import sys
from zipfile import ZipFile, ZIP_DEFLATED

def title_format(text_in):
    text_out = ''
    text_out = re.sub(r'[A-Za-z]+(\'[A-Za-z]+)?', lambda word: word.group(0).capitalize(), text_in)
    return text_out


def clean_formattedtext(text_in):
    text_out = text_in
    # assume that colons at the start of a paragraph should be one continuous paragraph
    text_out = re.sub('</p>\s*<p>\s*:', ':', text_out)
    # assume that italics at the start or end of a paragraph should be one continuous paragraph
    text_out = re.sub('</p>\s*<p><i>', '<i>', text_out)
    text_out = re.sub('</i></p>\s*<p>', '</i>', text_out)
    # turn <br/> into new <p> as line breaks inside <p> don't render in formattedtext
    text_out = re.sub(r'(\s*<br/>\s*)', r'</p><p>', text_out)
    # get rid of empty paragraphs
    text_out = re.sub('<p>\s*</p>', '', text_out)
    # get rid of mutliple linebreaks
    text_out = re.sub('\n+', '\n', text_out)
    # replace <th> with <td><b> as FG appear to not render <th> correctly
    text_out = re.sub(r'<th>', r'<td><b>', text_out)
    text_out = re.sub(r'</th>', r'</b></td>', text_out)
    # escape &
    text_out = re.sub(r'&', r'&amp;', text_out)

    return text_out


def check_all_dbs():
    file_list = ['sql\ddiBackground.sql', 'sql\ddiClass.sql', 'sql\ddiCompanion.sql', 'sql\ddiDeity.sql', 'sql\ddiDisease.sql', 'sql\ddiEpicDestiny.sql', 'sql\ddiFeat.sql', 'sql\ddiItem.sql',\
                 'sql\ddiMonster.sql', 'sql\ddiParagonPath.sql', 'sql\ddiPoison.sql', 'sql\ddiPower.sql', 'sql\ddiRace.sql', 'sql\ddiRitual.sql', 'sql\ddiTerrain.sql', 'sql\ddiTheme.sql', 'sql\ddiTrap.sql']
    for f in file_list:
        if not os.path.isfile(f):
            print('Missing File: ' + f)
            sys.exit(0)

    return


def parse_argv(args_in):

    # Set up all the command line options and extract to 'options'
    parser = optparse.OptionParser()
    parser.set_defaults(filename='4E_Compendium', library='4E Compendium', min=0, max=99)
    parser.add_option('--filename', action='store', dest='filename', help='create library at FILE', metavar='FILE')
    parser.add_option('--library', action='store', dest='library', help='Fantasy Grounds\' internal name for the Library', metavar='LIBRARY')
    parser.add_option('--min', action='store', dest='min', help='export items of this level and above. Applies to NPCs, Alchemical Items, Rituals, Martial Practices and Powers.')
    parser.add_option('--max', action='store', dest='max', help='export items of this level and below. Applies to NPCs, Alchemical Items, Rituals, Martial Practices and Powers.')
    parser.add_option('-s', '--static', action='store_true', dest='static', help='adds "static=\"true\" clause to make objects locked')
    parser.add_option('-t', '--tiers', action='store_true', dest='tiers', help='divide Magic Armor, Implements and Weapons, NPCs into Tiers')
    parser.add_option('-n', '--npcs', action='store_true', dest='npcs', help='export NPCs (Monsters)')
    parser.add_option('-T', '--traps', action='store_true', dest='traps', help='export Traps and Hazards')
    parser.add_option('-e', '--terrain', action='store_true', dest='terrain', help='export Terrain information')
    parser.add_option('-d', '--diseases', action='store_true', dest='diseases', help='export Disease tracks')
    parser.add_option('-R', '--races', action='store_true', dest='races', help='export Races information')
    parser.add_option('-C', '--classes', action='store_true', dest='classes', help='export Classes information')
    parser.add_option('-B', '--backgrounds', action='store_true', dest='backgrounds', help='export PC Background information')
    parser.add_option('-H', '--heroic', action='store_true', dest='heroic', help='export Heroic Themes')
    parser.add_option('-P', '--paragon', action='store_true', dest='paragon', help='export Paragon Paths')
    parser.add_option('-E', '--epic', action='store_true', dest='epic', help='export Epic Destinies')
    parser.add_option('-F', '--familiars', action='store_true', dest='familiars', help='export Familiars information')
    parser.add_option('-D', '--deities', action='store_true', dest='deities', help='export Deity information')
    parser.add_option('-f', '--feats', action='store_true', dest='feats', help='export Feats')
    parser.add_option('-p', '--powers', action='store_true', dest='powers', help='export PC Powers')
    parser.add_option('-b', '--basic', action='store_true', dest='basic', help='include Basic Attacks in Power export')
    parser.add_option('-a', '--alchemy', action='store_true', dest='alchemy', help='export Alchemical Formulas and Items')
    parser.add_option('-r', '--rituals', action='store_true', dest='rituals', help='export Rituals')
    parser.add_option('-m', '--martial', action='store_true', dest='martial', help='export Martial Practices')
    parser.add_option('-o', '--poisons', action='store_true', dest='poisons', help='export Poisons')
    parser.add_option('-i', '--items', action='store_true', dest='items', help='export all item types (= --mundane & --magic)')
    parser.add_option('--mundane', action='store_true', dest='mundane', help='export all mundane items')
    parser.add_option('--magic', action='store_true', dest='magic', help='export all magic items')

##    parser.add_option('--armor', action='store_true', dest='armor', help='include mundane Armor items in the Library')
##    parser.add_option('--equipment', action='store_true', dest='equipment', help='include mundane Equipment items in the Library')
##    parser.add_option('--weapons', action='store_true', dest='weapons', help='include mundane Weapon items in the Library')
##    parser.add_option('--mi_armor', action='store_true', dest='mi_armor', help='include Magic Armor items in the Library')
##    parser.add_option('--mi_implements', action='store_true', dest='mi_implements', help='include Magic Implements items in the Library')
##    parser.add_option('--mi_weapons', action='store_true', dest='mi_weapons', help='include Magic Weapon items in the Library')
##    parser.add_option('--mi_other', action='store_true', dest='mi_other', help='includes all Other Magic item (overrides the following)')
##    parser.add_option('--mi_alchemical', action='store_true', dest='mi_alchemical', help='includes Alchemical items in the Library')
##    parser.add_option('--mi_alternative', action='store_true', dest='mi_alternative', help='includes Alternative Rewards in the Library')
##    parser.add_option('--mi_ammunition', action='store_true', dest='mi_ammunition', help='includes Ammunition in the Library')
##    parser.add_option('--mi_arms', action='store_true', dest='mi_arms', help='includes Arms Slot items in the Library')
##    parser.add_option('--mi_companion', action='store_true', dest='mi_companion', help='includes Companions in the Library')
##    parser.add_option('--mi_consumable', action='store_true', dest='mi_consumable', help='includes Consumable items in the Library')
##    parser.add_option('--mi_familiar', action='store_true', dest='mi_familiar', help='includes Familiars in the Library')
##    parser.add_option('--mi_feet', action='store_true', dest='mi_feet', help='includes Feet Slot items in the Library')
##    parser.add_option('--mi_hands', action='store_true', dest='mi_hands', help='includes Hands Slot items in the Library')
##    parser.add_option('--mi_head', action='store_true', dest='mi_head', help='includes Head Slot in the Library')
##    parser.add_option('--mi_head_neck', action='store_true', dest='mi_head_neck', help='includes Nead and Neck Slot items in the Library')
##    parser.add_option('--mi_mount', action='store_true', dest='mi_mount', help='includes Mount items in the Library')
##    parser.add_option('--mi_neck', action='store_true', dest='mi_neck', help='includes Neck SLot items in the Library')
##    parser.add_option('--mi_ring', action='store_true', dest='mi_ring', help='includes Ring Slot items in the Library')
##    parser.add_option('--mi_waist', action='store_true', dest='mi_waist', help='includes Waist Slot items in the Library')
##    parser.add_option('--mi_wondrous', action='store_true', dest='mi_wondrous', help='includes Wondrous Items in the Library')
    (options, args) = parser.parse_args()

    # Copy all values from options except 'all' and 'mi_other'
    settings.filename = options.filename
    settings.library = options.library
    settings.min_lvl = int(options.min) if int(options.min) >= 0 else 0
    settings.max_lvl = int(options.max) if int(options.min) <= 99 else 99
    settings.static = options.static if options.static != None else False
    settings.tiers = options.tiers if options.tiers != None else False
    settings.npcs = options.npcs if options.npcs != None else False
    settings.traps = options.traps if options.traps != None else False
    settings.terrain = options.terrain if options.terrain != None else False
    settings.diseases = options.diseases if options.diseases != None else False
    settings.races = options.races if options.races != None else False
    settings.classes = options.classes if options.classes != None else False
    settings.backgrounds = options.backgrounds if options.backgrounds != None else False
    settings.heroic = options.heroic if options.heroic != None else False
    settings.paragon = options.paragon if options.paragon != None else False
    settings.epic = options.epic if options.epic != None else False
    settings.familiars = options.familiars if options.familiars != None else False
    settings.deities = options.deities if options.deities != None else False
    settings.feats = options.feats if options.feats != None else False
    settings.powers = options.powers if options.powers != None else False
    settings.basic = options.basic if options.basic != None else False
    settings.alchemy = options.alchemy if options.alchemy != None else False
    settings.rituals = options.rituals if options.rituals != None else False
    settings.practices = options.martial if options.martial != None else False
    settings.poisons = options.poisons if options.poisons != None else False
    settings.items = options.items if options.items != None else False
    settings.mundane = options.mundane if options.mundane != None else False
    settings.magic = options.magic if options.magic != None else False

    # Note these are currently internal/debug options that are more granular than is currently offered by the switches
    settings.armor = False
    settings.equipment = False
    settings.weapons = False
    settings.mi_armor = False
    settings.mi_implements = False
    settings.mi_weapons = False
    settings.mi_alchemical = False
    settings.mi_alternative = False
    settings.mi_ammunition = False
    settings.mi_arms = False
    settings.mi_companion = False
    settings.mi_consumable = False
    settings.mi_familiar = False
    settings.mi_feet = False
    settings.mi_hands = False
    settings.mi_head = False
    settings.mi_head_neck = False
    settings.mi_mount = False
    settings.mi_neck = False
    settings.mi_ring = False
    settings.mi_waist = False
    settings.mi_wondrous = False

    # If --items is specified then set all items to True
    if settings.items == True:
        settings.mundane = True
        settings.magic = True

    # If --mundane is specified then set mundane items to True
    if settings.mundane == True:
        settings.armor = True
        settings.equipment = True
        settings.weapons = True

    # If --magic  is specified then set magic items to True
    if settings.magic == True:
        settings.tiers = True
        settings.mi_armor = True
        settings.mi_implements = True
        settings.mi_weapons = True
        settings.mi_alchemical = True
        settings.mi_alternative = True
        settings.mi_ammunition = True
        settings.mi_arms = True
        settings.mi_companion = True
        settings.mi_consumable = True
        settings.mi_familiar = True
        settings.mi_feet = True
        settings.mi_hands = True
        settings.mi_head = True
        settings.mi_head_neck = True
        settings.mi_mount = True
        settings.mi_neck = True
        settings.mi_ring = True
        settings.mi_waist = True
        settings.mi_wondrous = True

    return


def create_module(xml_in):

    # Use db.xml for DM only modules so they are not player readable
    if settings.npcs or settings.traps or settings.terrain or settings.diseases:
        db_filename = 'db.xml'
    else:
        db_filename = 'client.xml'

    # Write FG XML client file
    with open(db_filename, mode='w', encoding='iso-8859-1', errors='strict', buffering=1) as file:
        file.write(xml_in)
    print(f'\n{db_filename} written')

    # Write FG XML definition file
    definition_str = (f'<?xml version="1.0" encoding="iso-8859-1"?>\n<root version="2.2">\n\t<name>{settings.library}</name>\n\t<author>skelekon</author>\n\t<ruleset>4E</ruleset>\n</root>')
    with open('definition.xml', mode='w', encoding='iso-8859-1', errors='strict', buffering=1) as file:
        file.write(definition_str)
    print('\ndefinition.xml written.')

    try:
        with ZipFile(f'{settings.filename}.mod', 'w', compression=ZIP_DEFLATED) as modzip:
            modzip.write(db_filename)
            modzip.write('definition.xml')
            if os.path.isfile('thumbnail.png'):
                modzip.write('thumbnail.png')

        print(f'\n{settings.filename}.mod generated!')
        print('\nMove it to your Fantasy Grounds\modules directory')
    except Exception as e:
        print(f'\nError creating zipped .mod file:\n{e}')

    return
