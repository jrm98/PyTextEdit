##PyTextEdit v0.2
-----------------------------

####Description
A basic text editor created with python to run in a command line
environment. Retains basic functionality of creating new files,
saving current files, and loading from files. Text editing operations
include inserting text at a the cursor and deleting text at the cursor.

####Features
- Opens with a splash screen along with a ```>``` indicating the program
is awaiting user input
- After each command is entered, The command-line interface will clear
to provide a more consistent user interface
- If a file is open, the name of the file will be displayed in parenthesis
at the top of the UI
- If the file currently open has been modified, an asterisk will be
displayed next to the file name
- While in developer's mode, ```[devMode]``` will be displayed at the top
of the UI next to the program's name

To run the program, enter the following command:
```python3 ~/*pathname*/pytext.py```

*Note: the bash script "run.sh" will not work if it is not given
      execute permissions*

#####Supported Commands: 
- ```new <*filename*>```
- ```open <*filename*>```
- ```save```
- ```saveas <*filename*>```
- ```insert <*string*>```
- ```erase```
- ```erase <*integer*>```
- ```move <*integer*>```
- ```status```
- ```close```
- ```quit```
- ```help```
- ```info```
- ```history```
- ```devmode```
- ```sub```*
- ```config```*

#####Commands in development:
- ```config```
- ```sub```

#####Potential commands to be added:
- peek (or preview)
- compile
- run

#####Potential upgrades:
- cleaner, more user-friendly UI

**Commands may be mildly functional, but almost certainly contains bugs*
