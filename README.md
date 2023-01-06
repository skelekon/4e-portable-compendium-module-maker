# 4e-portable-compendium-module-maker
An application for creating Fantasy Grounds Library Modules from the D&amp;D 4e Portable Compendium.

This builds on
"4E Module Generator - Portable Compendium" package by VegaFontana on the [Fantasy Grounds 4e Forums](https://www.fantasygrounds.com/forums/showthread.php?60524-4E-Module-Generator-Portable-compendium-gt-Fantasy-Grounds) under a GNU GPL-3.0 License.
and further work done by Valkyrion (msprijatelj on github), Braincain007 and myself on [4e-module-generator-portable-compendium](https://github.com/msprijatelj/4e-module-generator-portable-compendium)
/ [Fantasy Grounds 4e Forums](https://www.fantasygrounds.com/forums/showthread.php?60524-4E-Module-Generator-Portable-compendium-gt-Fantasy-Grounds&p=647134&viewfull=1#post647134)

This repository modifies and builds off of that package to create indexed Library Modules for easier browsing and improved drag and drop support for forging magic weapons and armor.


**\*\*THIS PACKAGE DOES _NOT_ INCLUDE D&D 4E COMPENDIUM DATA.\*\***

It is designed to work with `.sql` data files from the Beta 30 version of the 4e Portable Compendium.

## How to Use

```
Usage: module_maker.exe [options]

Options:
  -h, --help         show this help message and exit
  --filename=FILE    create library at FILE
  --library=LIBRARY  Fantasy Grounds' internal name for the Library
  --min=MIN          export items of this level and above. Applies to NPCs,
                     Alchemical Items, Rituals, Martial Practices and Powers.
  --max=MAX          export items of this level and below. Applies to NPCs,
                     Alchemical Items, Rituals, Martial Practices and Powers.
  -s, --static       adds "static="true" clause to make objects locked
  -t, --tiers        divide Magic Armor, Implements and Weapons, NPCs into
                     Tiers
  -n, --npcs         export NPCs (Monsters)
  -T, --traps        export Traps and Hazards
  -e, --terrain      export Terrain information
  -d, --diseases     export Disease tracks
  -R, --races        export Races information
  -C, --classes      export Classes information
  -B, --backgrounds  export PC Background information
  -H, --heroic       export Heroic Themes
  -P, --paragon      export Paragon Paths
  -E, --epic         export Epic Destinies
  -F, --familiars    export Familiars information
  -D, --deities      export Deity information
  -f, --feats        export Feats
  -p, --powers       export PC Powers
  -b, --basic        include Basic Attacks in Power export
  -a, --alchemy      export Alchemical Formulas and Items
  -r, --rituals      export Rituals
  -m, --martial      export Martial Practices
  -o, --poisons      export Poisons
  -i, --items        export all item types (= --mundane & --magic)
  --mundane          export all mundane items
  --magic            export all magic items
```

1. Download `module_maker.exe` and `run_all.bat` into the unzipped Portable Compendium directory (default will be `/Portable Compendium New`. It will use the data files in the `/sql` subdirectory to create modules.

2. \[Optional\] Paste an image named `thumbnail.png` in the same directory if you want it to automatically add a thumbnail image to any created modules.

3. Open a command prompt or PowerShell and navigate to the Portable Compendium directory.

4. Run `run_all.bat` to create the following four Libraries, which include everything currently available:

```
module_maker.exe --filename 4E_Monsters --library "4E Monsters" -n -t
module_maker.exe --filename 4E_Traps_Terrain_Diseases --library "4E Traps, Terrain and Diseases" -T -e -d
module_maker.exe --filename 4E_PC_Options --library "4E PC Options" -R -C -B -H -P -E -F -D -f -p -b -s
module_maker.exe --filename 4E_Items --library "4E Items" -a -r -m -o -i -t -s
```

5. Copy or Move the new `.mod` file to into your FG modules folder (default should be `.../Fantasy Gounds/modules`) and load them in your campaign!

6. Don't forget to grant your players access to any items / feats / powers modules to ease character creation.

If you want more control over what is in the modules, or their names, you can roll your own module_maker commands using the available switches instead of using the ones supplied in the run_all file.
