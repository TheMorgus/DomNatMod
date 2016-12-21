import SpecialWords

class DomNationMod:
	def __init__(self):
		self.modinfo = {} #Dictionary of --Command:Value-- pairs
		self.weapons = [] #List of Dictionaries of --Command:Value-- pairs. Each dict represents a seperate weapon modification
		self.armors = [] #List of Dictionaries of --Command:Value-- pairs. Each dict = an armor.
		self.units = [] #List of Dictionaries of --Command:Value-- pairs. Each dict = a unit.
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
		
	def get_line_string(self, line):
		returnvalue = '"'
		startindex = line.index('"')
		line = line[startindex+1:]
		for letter in line:
			if letter == '"':
				returnvalue += letter
				return(returnvalue)
			else:
				returnvalue += letter
				
	def get_line_value(self, line):
		returnvalue = ""
		for letter in line:
			if letter is " ":
				return(returnvalue)
			else:
				returnvalue += letter
		return(returnvalue)
		
	#Gets the value present in a line. Optional tostrip argument should be a line command (ex. #attk).
	def get_line_values(self, line, tostrip = ""):  ## !! MUST BE UPDATED TO 3 MAX VALUES!! 
		value1 = ""
		value2 = ""
		value = ""
		if tostrip != "":
			value = line.strip(tostrip)
			if "--" in value: 
				indexremove = value.index("--")
				value = value[:indexremove]
			value = value.strip()
			if '"' in value:
				value1 = self.get_line_string(value)
			else:
				value1 = self.get_line_value(value)
			index = value.index(value1)
			value2 = value[index + len(value1):]
			value1 = value1.strip()
			value1 = value1.strip('"')
			value2 = value2.strip()
			value2 = value2.strip('"')
			if value2 != "":
				return(value1,value2)
			else:
				return(value1)
		
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
						value = self.get_line_values(line, tostrip = command)
						modinfodictionary[command] = value
		return(modinfodictionary)

	#get all the indexes for a string, which should be a #command that starts a new item type
	def get_item_indexes(self, toindex):
		itemindexes = []
		for i, theline in enumerate(self.thefile):
			if toindex in theline:
				itemindexes.append(i)
		return(itemindexes)
		
	#gets info from an index up to #end command, returns dictionary of --Command:Value-- Pairs
	def get_item_info(self, index):
		itemdict = {}
		#these values may have more than one entry per unit, so their values are taken as a list of all values found
		commandswithlist = ["#weapon","#armor","#custommagic","#magicskill"]
		newfile = self.thefile[index:]
		for line in newfile:
			if "#end" in line:
				break
			command = self.get_line_command(line)
			if command in commandswithlist:
				value = self.get_line_values(line, command)
				if command not in itemdict:
					itemlist = []
					itemlist.append(value)
					itemdict[command] = itemlist
				else:
					itemlist = itemdict[command]
					itemlist.append(value)
					itemdict[command] = itemlist
			else:
				value = self.get_line_values(line,command)
				itemdict[command] = value
		return(itemdict)	
	
	#Gets all mod information of selected type
	def get_all(self, toget):
		listofitems = []
		startindexes = []
		indexstartkeys = []
		if toget == "weapons":
			indexstartkeys = ["#newweapon", "#selectweapon"]
		elif toget == "armors":
			indexstartkeys = ["#newarmor", "#selectarmor"]
		elif toget == "units":
			indexstartkeys = ["#newmonster", "#selectmonster"]
		for startkey in indexstartkeys:
			startindexes +=  self.get_item_indexes(startkey)
		for index in startindexes:
			listofitems.append(self.get_item_info(index))
		return(listofitems)
