:: This will create three Fantasy Grounds modules
:: 4E Monsters contains all NPCs
:: 4E Powers contains all Feats and Powers
:: 4E Items contains all mundane & magical items, all Rituals and all Alchemical Items

module_maker.exe --filename 4E_Monsters --library "4E Monsters" -n -t
module_maker.exe --filename 4E_Powers --library "4E Powers" -f -p -b
module_maker.exe --filename 4E_Items --library "4E Items" -a -r -m -i -t