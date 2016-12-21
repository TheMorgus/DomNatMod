import SpecialWords

class DomNationMod:
	def __init__(self):
		self.modinfo = {} #Dictionary of --Command:Value-- pairs
		self.weapons = [] #List of Dictionarys of --Command:Value-- pairs. Each dict represents a seperate weapon modification
		self.armors = []
		self.units = []
		self.names = []
		self.nations = []
		self.spells = []
		self.magicitems = []
		self.general = []
		self.poptypes = []
		self.mercenaries = []
		self.events = []

class FileManipulator:
	def __init__(self, filepath):
		self.filepath = filepath
		self.thefile = self.getfile()

	def getfile(self):
		filestream = open(self.filepath)
		filelist = []
		for line in filestream:
			if line.strip() == "":
				pass
			elif line[0:2] == "--":
				pass
			else:
				filelist.append(line.strip())
		filestream.close()
		return(filelist)
	#finds and returns the command present at the start of the line
	def get_line_command(self, theline):
		command = ""
		for letter in theline:
			if letter != " ":
				command += letter
			else:
				break
		return(command)
		
	#Gets the value present in a line. Optional tostrip argument should be a line command (ex. #attk).
	def get_line_value(self, line, tostrip = ""):  
		if tostrip != "":
			value = line.strip(tostrip)
			if "--" in line: #Should work to remove comments, untested atm.
				indexremove = line.index("--")
				line = line[:indexremove]
			value = value.strip()
			value = value.strip('"')
			return(value)
		
	#searches for modinfo commands until the newweapon portion of load order is reached
	#returns a dictionary of modinfo commands and their respective values
	def get_mod_info(self):
		end = False
		value = ""
		command = ""
		modinfodictionary = {}
		while end == False:
			for line in self.thefile:
				if "#newweapon" in line or "#selectweapon" in line:
					end = True
					break
				if line[0] == "#":
					command = self.get_line_command(line)
					if command in SpecialWords.modinfocommands:
						value = self.get_line_value(line, tostrip = command)
						modinfodictionary[command] = value
		return(modinfodictionary)

	#get all the indexes for the start of weapon modifications
	def get_item_indexes(self, toindex1):     #!!!change to get indexes of whatver you're looking for!!!!
		itemindexes = []
		for i, theline in enumerate(self.thefile):
			if toindex1 in theline:
				itemindexes.append(i)
		return(itemindexes)
		
	#gets weapon info from an index up to #end command, returns dictionary of --Command:Value-- Pairs
	def get_weapon_info(self, index):
		weapondict = {}
		newfile = self.thefile[index:]
		for line in newfile:
			if "#end" in line:
				break
			command = self.get_line_command(line)
			value = self.get_line_value(line,command)
			weapondict[command] = value
		return(weapondict)	
		
	#Gets all weapon dictionarys, puts them in a list, and returns them
	def get_all_weapons(self):
		allweapons = []
		indexes = self.get_item_indexes("#newweapon")
		indexex = indexes + self.get_item_indexes("#selectweapon")
		for index in indexes:
			allweapons.append(self.get_weapon_info(index))
		return(allweapons)
