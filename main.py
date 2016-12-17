import DomNatmod as Fm

path = "/home/morg/Desktop/Agholt.dm"
agholtmanip = Fm.FileManipulator(path)
Agholt = Fm.DomNationMod



Agholt.modinfo = agholtmanip.get_mod_info()
Agholt.weapons = agholtmanip.get_all_weapons()

for weapon in Agholt.weapons:
	print(weapon)
	print("\n" * 5)
