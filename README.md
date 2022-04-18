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
  -h, --help            show this help message and exit
  --filename=FILE       create library at FILE
  -l LIBRARY, --library=LIBRARY
                        Fantasy Grounds' internal name for the Library
  --min=MIN             only include magic items of this level and above
  --max=MAX             only include magic items of this level and below
  -p, --powers          outputs Power information
  -f, --feats           outputs Feat information
  -t, --tiers           divide Magic Armor, Implements and Weapons into Tiers
  -i, --items           include all item types (= --mundane & --magic)
  --mundane             include all mundane items in the Library
  --magic               include all magic items in the Library
  -a, --all             includes everything (WARNING very large library)
```

1. Copy `module_maker.exe` into the unzipped Portable Compendium directory (default will be `/Portable Compendium New`. It will use the data files in the `/sql` subdirectory to create modules.

2. \[Optional\] Paste an image named `thumbnail.png` in the same directory if you want it to automatically add a thumbnail image to any created modules.

3. Open a command prompt or PowerShell and navigate to the Portable Compendium directory.

4. Run `module_maker.exe` with the switches to create the modules you want. e.g.
```
module_maker.exe --filename 4E_Powers --library "4E Powers" -p
module_maker.exe --filename 4E_Feats --library "4E Feats" -f
module_maker.exe --filename 4E_Items --library "4E Items" -i -t
```
Default filename/library will be `4E_Compendium` / `4E Compendium` if not supplied.

5. Copy or Move the `.mod` file to into your FG modules folder (default should be `.../Fantasy Gounds/modules`) and load them in your campaign!

6. Don't forget to grant your players access to any items / feats / powers modules to ease character creation.
