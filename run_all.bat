:: This will create three Fantasy Grounds modules
:: 4E Monsters contains all NPCs
:: 4E Powers contains all Races, Classes, Feats and Powers
:: 4E Items contains all mundane & magical items, all Rituals and all Alchemical Items

module_maker.exe --filename 4E_Monsters --library "4E Monsters" -n -t
module_maker.exe --filename 4E_PCs --library "4E PCs" -r -c -f -p -b
module_maker.exe --filename 4E_Items --library "4E Items" -a -u -m -i -t