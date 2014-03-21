#----------------------------------------------------------------------------#
# PyTextEdit                                                                 #
# Author: Jake Martinez (jrm98)                                              #
# Version: v0.1 (3/21/2014 @ 1:46PM)                                         #
#                                                                            #
# Description                                                                #
# -----------                                                                #
# A basic text editor created with python to run in a command line           #
# environment. Retains basic functionality of creating new files,            #
# saving current files, and loading from files. Text editing operations      #
# include inserting text at a the cursor and deleting text at the cursor     #
#                                                                            #
# Supported Commands: new <filename>, open <filename>, save,                 #
#                     saveas <filename>, insert <string>, erase,             #
#                     erase <integer>, move <integer>, status, close, quit,  # 
#                     help, history, info, devmode, sub, config              #
#----------------------------------------------------------------------------#

import os
import subprocess
import configparser

charArray = "" 		# represents the text of the current file
filename = "" 		# represents the name of the current file
cursorLocation = 0 	# represents the current location of the cursor
fileIsOpen = False 	# true if a file is open, false if not
f = None 			# the file that is currently in use
modified = False 	# if the current file has been modified since being opened
history = ""
devMode = False

def main():
	global charArray
	global filename
	global cursorLocation
	global fileIsOpen
	global f
	global modified
	global history
	global devMode

	loadconfig()
	prevCmdInvalid = False
	info()
	check = True
	while check:
		nextLine = readNextCommand(prevCmdInvalid)
		prevCmdInvalid = False
		history += str(nextLine) + "\n"
		subprocess.call("clear")

		#---HEADER----
		if fileIsOpen and not modified and devMode:
			print("~PyTextEdit[devMode]~  (%s)" % filename)
		elif fileIsOpen and devMode:
			print("~PyTextEdit[devMode]~ *(%s)" % filename)
		elif fileIsOpen and not modified:
			print("~PyTextEdit~  (%s)" % filename)
		elif fileIsOpen:
			print("~PyTextEdit~ *(%s)" % filename)
		elif devMode:
			print("~PyTextEdit[devMode]~")
		else:
			print("~PyTextEdit~")
		print("----------------------------------------------------------------------")
		#-------------


		if len(nextLine) < 1:
			display()

		elif nextLine[0] == "open" and len(nextLine) > 1:
			if fileIsOpen:
				close()
			f = loadFile(nextLine[1])
			if (f != None):
				display()

		elif nextLine[0] == "insert" and fileIsOpen and len(nextLine) > 1:
			if nextLine[1] == "\s":
				insert(" ")
			elif nextLine[1] == "\\n":
				insert("\n")
			elif nextLine[1] == "\\t":
				insert(" ")
			else:
				insert(nextLine[1])
			display()

		elif nextLine[0] == "erase" and fileIsOpen:
			if  len(nextLine) > 1:
				erase(nextLine[1])
			else:
				erase(0)
			display()

		elif nextLine[0] == "move" and fileIsOpen and len(nextLine) > 1:
			move(nextLine[1])
			display()

		elif nextLine[0] == "save" and fileIsOpen:
			saveFile()
			display()

		elif nextLine[0] == "saveas" and fileIsOpen and len(nextLine) > 1:
			saveFileAs(nextLine[1])
			display()

		elif nextLine[0] == "status" and fileIsOpen:
			status()
			display()

		elif nextLine[0] == "close" and fileIsOpen:
			close()
			print("File closed...")

		elif nextLine[0] == "quit":
			if fileIsOpen:
				quit()
			check = False

		elif nextLine[0] == "help":
			help()

		elif nextLine[0] == "info":
			info()

		elif nextLine[0] == "devmode":
			devMode = not devMode

		elif nextLine[0] == "sub":
			sub()

		elif nextLine[0] == "config":
			config()

		elif nextLine[0] == "history":
			print("COMMAND HISTORY:")
			print(history)

		elif nextLine[0] == "new" and len(nextLine) > 1:
			if fileIsOpen:
				close()
			f = newFile(nextLine[1])
			if (f != None):
				display()

		elif not fileIsOpen:
			print("Command not recognized or no file is currently open...")
			print("   (hint: to open a file, enter: open [filename] )")
			print("   (hint: to create a new file, enter: new [filename] )")

		else:
			prevCmdInvalid = True
			display()

	return

#----------------------------------------------------------------------------
# Description: Reads in the next command from the standard input
# Returns: array of tokens
#----------------------------------------------------------------------------
def readNextCommand(prev):
	if not prev:
		inp = input(">")
	else:
		inp = input("!~ >")
	tokens = inp.split()
	return tokens

def loadconfig():
	global cursorLocation
	global devMode

	config = configparser.ConfigParser()
	try:
		config.read('pytext_config.ini')
	except:
		print("no config file found...")
		return

	if ('DEFAULT' not in config):
		print("pytext_config.ini exists but is incorrectly formatted")
		return
	if ('cursor' in config['DEFAULT']):
		cursorLocation = int(config['DEFAULT']['cursor'])
	if ('devMode' in config['DEFAULT']):
		devMode = bool(config['DEFAULT']['devMode'])

	print("pytext_config.ini loaded...")
	return

######################### BASIC TEXT EDIT CMDS ##############################

#----------------------------------------------------------------------------
# Description: Inserts a string into the charArray at the location
# 			   of the cursor
# Returns: nothing
#----------------------------------------------------------------------------
def insert(string):
	newString = ""
	string = str(string)
	global cursorLocation
	global charArray
	global modified

	i = 0
	while i < cursorLocation:
		newString += charArray[i]
		i += 1

	j = 0
	while j < len(string):
		newString += string[j]
		j += 1

	while i < len(charArray):
		newString += charArray[i]
		i += 1

	charArray = newString
	modified = True;
	return

#----------------------------------------------------------------------------
# Description: Erases one or more elements from the charArray at the
#			   location of the cursor
# Returns: nothing
#----------------------------------------------------------------------------
def erase(numSpaces):
	global charArray
	global cursorLocation
	numSpaces = int(numSpaces)
	pos = cursorLocation
	modified = True
	if pos == len(charArray):
		charArray = charArray[:pos]
		cursorLocation -= 1
		return
	charArray = charArray[:pos] + charArray[(pos+1):]
	i = numSpaces - 1
	while i > 0:
		if pos == len(charArray):
			charArray = charArray[:pos]
			cursorLocation -= 1
			return
		charArray = charArray[:pos] + charArray[(pos+1):]
		i -= 1;
	return

#----------------------------------------------------------------------------
# Description: Moves the cursor's location to the designated location
# Returns: true if the cursor was moved successfully, false otherwise
#----------------------------------------------------------------------------
def move(newLocation):
	global cursorLocation
	newLocation = int(newLocation)
	if newLocation > len(charArray):
		print("Invalid cursor.")
		return False
	cursorLocation = newLocation
	return True

#----------------------------------------------------------------------------
# Description: Loads from the given filename and reads and copys the data to
# 			   the charArray
# Returns: the file that was opened or nothing if no file was opened
#----------------------------------------------------------------------------
def loadFile(ofilename):
	global filename
	filename = ofilename
	try:
		new = open(filename, 'r+')
	except:
		print("Could not open file: %s. Please try a different file." % filename)
		return

	global charArray
	global fileIsOpen

	charArray = new.read()
	new.close()
	fileIsOpen = True
	return new

#----------------------------------------------------------------------------
# Description: Saves the current charArray to the filename it was loaded from
# Returns: nothing
#----------------------------------------------------------------------------
def saveFile():
	global f
	global filename
	save = filename
	f = open(save, 'w')
	global modified
	global charArray
	modified = False;
	f.write(charArray)
	f.close()
	return

#----------------------------------------------------------------------------
# Description: Saves the current charArray to the given filename
# Returns: nothing
#----------------------------------------------------------------------------
def saveFileAs(newFilename):
	global f
	f = open(newFilename, 'w')
	global modified
	global charArray
	global filename
	filename = newFilename
	modified = False;
	f.write(charArray)
	f.close()
	return

#----------------------------------------------------------------------------
# Description: creates a new file, named as newFilename
# Returns: the file that was loaded (and usually created)
#----------------------------------------------------------------------------
def newFile(newFilename):
	global f
	global filename
	global charArray
	filename = newFilename
	try:
		new = open(filename, 'r')
		print("File already exists...")
		inp = input("Would you like to open anyways? (Y/N): ")
		while inp != "Y" and inp != "N":
			inp = input("Would you like to open anyways? (Y/N): ")
		if inp == "N":
			return
		charArray = new.read()
	except:
		new = open(filename, 'w')
		new.write("")
	new.close()
	return loadFile(filename)

#----------------------------------------------------------------------------
# Description: Outputs the current state of the charArray with the cursor's position
# 			   as well as line numbers
# Returns: nothing
#----------------------------------------------------------------------------
def display():
	global charArray
	global cursorLocation
	lines = charArray.split("\n")
	current = 0;
	for i in range(len(lines)):
		if len(lines[i]) == 0:
			continue
		print("{0:70} |{1:3d}:{2:3d}|".format( lines[i], current, current + len(lines[i]) ) )
		if cursorLocation >= current and cursorLocation <= current + len(lines[i]):
			spacing = ""
			for j in range(cursorLocation - current):
				spacing += " "
			spacing += "^"
			print(spacing)
		current += len(lines[i]) + 1
	return

#----------------------------------------------------------------------------
# Description: displays the current status of the file
# Returns: nothing
#----------------------------------------------------------------------------
def status():
	global modified
	global charArray

	print("File Status:")
	print("-------------------------------")
	if modified:
		print("Modified: Yes")
	else:
		print("Modified: No")
	print("Length: %d" % len(charArray))
	print("Contents:")
	return

#----------------------------------------------------------------------------
# Description: prompts user to save before termination of the program
# Returns: nothing
#----------------------------------------------------------------------------
def quit():
	inp = input("Would you like to save before you exit? (Y/N): ")
	while inp != "Y" and inp != "N":
		inp = input("Would you like to save before you exit? (Y/N): ")
	if inp == "N":
		return

	filename = input("Enter filename: ")
	saveFile(filename)
	return

#----------------------------------------------------------------------------
# Description: closes the file that is currently open
# Returns: nothing
#----------------------------------------------------------------------------
def close():
	global charArray
	global filename
	global cursorLocation
	global fileIsOpen
	global f
	global modified

	if modified:
		inp = input("Would you like to save before you close? (Y/N): ")
		while inp != "Y" and inp != "N":
			inp = input("Would you like to save before you close? (Y/N): ")
		if inp == "Y":
			saveFile()

	# closes file
	if not f.closed:
		f.close()

	# resets global variables
	charArray = ""
	filename = ""
	cursorLocation = 0
	fileIsOpen = False
	f = None
	modified = False
	return

#----------------------------------------------------------------------------
# Description: displays all supported commands
# Returns: nothing
#----------------------------------------------------------------------------
def help():
	print("Supported Commands:")
	print("  new [filename]")
	print("    ---Creates a new file with specified")
	print("       filename")
	print("  open [filename]")
	print("    ---Loads data from the specified filename")
	print("  save")
	print("    ---Saves the text to the current filename")
	print("  saveas [filename]")
	print("    ---Saves the text to the specified filename")
	print("  insert [string]")
	print("    ---Inserts a string at the location of the")
	print("       cursor (special char.: \s for space")
	print("                              \\n for line break)")
	print("  erase")
	print("    ---Erases the value at the location of the")
	print("       cursor")
	print("  erase [integer]")
	print("    ---Erases the specified number of values")
	print("       from the location of the cursor")
	print("  move [integer]")
	print("    ---Moves the cursors location to the specified")
	print("       index")
	print("  status")
	print("    ---Displays the current status of the data")
	print("  close")
	print("    ---Closes the current file")
	print("  quit")
	print("    ---Exits the program")
	print("  help")
	print("    ---Displays this help message")
	print("  info")
	print("    ---Displays information about this software")
	print("  history")
	print("    ---Displays the command history")
	print("  devmode")
	print("    ---Developer's mode; includes extra commands")
	print("             (config,sub) as well as commands")
	print("             that are in development")
	return

#----------------------------------------------------------------------------
# Description: displays information about this software
# Returns: nothing
#----------------------------------------------------------------------------
def info():
	print("")
	print("             ___     _____        _   ___    _ _ _   ")
	print("            | _ \_  |_   _|____ _| |_| __|__| (_) |_ ")
	print("            |  _/ || || |/ -_) \ /  _| _|/ _` | |  _|")
	print("~Welcome to |_|  \_, ||_|\___/_\_\\\__|___\__,_|_|\__| ~")
	print("                 |__/                                ")
	print("                            v0.1 (3.21.2014)")
	print("                            created by: Jake Martinez")
	print("                            github.com/jrm98/PyTextEdit")
	print("\n Begin by entering a valid command")
	print(" (hint: for help, enter: help)\n")
	return

############################### DEV CMDS ####################################

#----------------------------------------------------------------------------
# Description: creates and edits config files
# Returns: nothing
#----------------------------------------------------------------------------
def config():
	global filename
	global fileIsOpen

	configFile = os.path.splitext(filename)[0] + "_config.ini"
	configText = ""
	new = None

	if fileIsOpen:
		inp = input("Would you like to configure the editor or the current file? (E/F): ")
		while inp != "E" and inp != "F":
			inp = input("Would you like to configure the editor or the current file? (E/F): ")
		if inp == "F":
			try:
				new = open(configFile, 'r')
				configText = new.read()
			except:
				new = open(configFile, 'w')
				new.write("")

			inp = input("Would you like to set the editor mode? (Y/N): ")
			while inp != "Y" and inp != "N":
				inp = input("Would you like to set the editor mode? (Y/N): ")
			if inp == "Y":
				configText += "[" + input("mode=") + "]"

			inp = input("Would you like to set the compile script for this file? (Y/N): ")
			while inp != "Y" and inp != "N":
				inp = input("Would you like to set the compile script for this file? (Y/N): ")
			if inp == "Y":
				configText += "compile=" + input("compile=")
		
			inp = input("Would you like to set the run script for this file? (Y/N): ")
			while inp != "Y" and inp != "N":
				inp = input("Would you like to set the run script for this file? (Y/N): ")
			if inp == "Y":
				configText += "run=" + input("run=")
			new.write(configText)
			new.close()
			return

	try:
		new = open("pytext_config.ini", 'r')
		configText = new.read()
	except:
		new = open("pytext_config.ini", 'w')
		new.write("")

	inp = input("Would you like to set the default editor to devMode? (Y/N): ")
	while inp != "Y" and inp != "N":
		inp = input("Would you like to set the default editor devMode? (Y/N): ")
	if inp == "Y":
		configText += "devMode=True"
		devMode = True

	new.write(configText)
	new.close()
	return

#----------------------------------------------------------------------------
# Description: command to bring up an input line for a bash subroutine
# Returns: nothing
#----------------------------------------------------------------------------
def sub():
	global devMode

	if not devMode:
		return

	inp = input("$bash >")
	inp = inp.split()
	subprocess.call(inp)

	return


if __name__ == "__main__":
	main()
