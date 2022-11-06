:: This will create four Fantasy Grounds modules
:: 4E Monsters contains all NPCs
:: 4E Traps and Diseases contains all Traps, Hazards and Diseases
:: 4E PC Options contains all Races, Classes, Backgrounds, Themes, Paragon Paths, Epic Destinies, Feats and Powers
:: 4E Items contains all mundane & magical items, all Rituals and all Alchemical Items

module_maker.exe --filename 4E_Monsters --library "4E Monsters" -n -t -s
module_maker.exe --filename 4E_Traps_Diseases --library "4E Traps and Diseases" -T -d -s
module_maker.exe --filename 4E_PC_Options --library "4E PC Options" -r -c -B -H -P -E -F -f -p -b -s
module_maker.exe --filename 4E_Items --library "4E Items" -a -u -m -i -t -s