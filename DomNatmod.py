import SpecialWords

class DomNationMod:
	def __init__(self):
		self.modinfo = {} #Dictionary of --Command:Value-- pairs
		self.weapons = []
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
		self.thefile = open(filepath)
		
	
	#def search_line_for_string(thestring, theline):
		#if thestring in theline == True:
			#return True
		#else:
			#return False
			
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
	def get_line_value(self, line, tostrip = ""):  #!!In future, make code to remove any comments in file from value!!
		if tostrip != "":
			value = line.strip(tostrip)
			value = value.strip()
			value = value.strip('"')
			return(value)
		
	#searches for modinfo commands until the newweapon portion of load order is reached
	#returns a dictionary of modinfo commands and their respective values
	def get_mod_info(self):
		self.thefile.seek(0)
		end = False
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

path = "/home/morg/Desktop/Agholt.dm"

agholtmanip = FileManipulator(path)

Agholt = DomNationMod
Agholt.modinfo = agholtmanip.get_mod_info()
print(Agholt.modinfo)
