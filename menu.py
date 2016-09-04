#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pickle
from time import sleep
import curses, os #curses is the interface for capturing key presses on the menu, os launches the files
screen = curses.initscr() #initializes a new window for capturing key presses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() # Lets you use colors when highlighting selected menu option
screen.keypad(1) # Capture input from keypad

# Change this to use different colors when highlighting
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"

def lectureConfig():
    with open('donnees', 'rb') as fichier:
        mon_depickler = pickle.Unpickler(fichier)
        config_recupere = mon_depickler.load()

    global USER, WIT_AI_KEY, RECORD_DURATION, SENSIBILITE_SNOWBOY, NIVEAU_CONFIDENCE, ECHANTILLON_SILENCE
    
    USER = config_recupere.get("USER")
    WIT_AI_KEY = config_recupere.get("WIT_AI_KEY")
    RECORD_DURATION = str(config_recupere.get("RECORD_DURATION"))
    SENSIBILITE_SNOWBOY = str(config_recupere.get("SENSIBILITE_SNOWBOY"))
    NIVEAU_CONFIDENCE = str(config_recupere.get("NIVEAU_CONFIDENCE"))
    ECHANTILLON_SILENCE =  str(config_recupere.get("ECHANTILLON_SILENCE"))
    
def chargementConfig():
    lectureConfig()
    
    menu_data = {
    'title': "Menu principal", 'type': MENU, 'subtitle': "Choisir une option...",
    'options':[
    { 'title': "Lancer Optimus", 'type': COMMAND, 'command': './main.py' },
    { 'title': "Configuration Optimus", 'type': MENU, 'subtitle': "Choisir une option...",
        'options': [
            { 'title': "Nom Utilisateur : " + USER, 'type': COMMAND, 'command': "./commandemenu.py user" },
            { 'title': "Cle wit : " + WIT_AI_KEY, 'type': COMMAND, 'command': "./commandemenu.py wit" },
            { 'title': "Duree enregistrement : " + RECORD_DURATION, 'type': COMMAND, 'command': "./commandemenu.py record" },
            { 'title': "Sensibilite Snowboy : " + SENSIBILITE_SNOWBOY, 'type': COMMAND, 'command': "./commandemenu.py snowboy" },
            { 'title': "Niveau de confidence : " + NIVEAU_CONFIDENCE, 'type': COMMAND, 'command': "./commandemenu.py confidence" },
            { 'title': "Duree echantillon silence : " + ECHANTILLON_SILENCE, 'type': COMMAND, 'command': "./commandemenu.py silence" },
        ]}
    ]
    }
    return menu_data

def initMenu(getin):
    lectureConfig()
    listeConfig = [USER, WIT_AI_KEY, RECORD_DURATION, SENSIBILITE_SNOWBOY, NIVEAU_CONFIDENCE, ECHANTILLON_SILENCE]
    listeTitle = ["Nom Utilisateur : ", "Cle wit : ", "Duree enregistrement : ", "Sensibilite Snowboy : ", "Niveau de confidence : ", "Duree echantillon silence : "]
    menu = listeTitle[getin] + listeConfig[getin]
    return menu 
    
# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):
  # work out what text to display as the last menu option
  if parent is None:
    lastoption = "Sortie"
  else:
    lastoption = "Retour au %s " % parent['title']

  optioncount = len(menu['options']) # how many options in this menu

  pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
  oldpos=None # used to prevent the screen being redrawn every time
  x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

  # Loop until return key is pressed
  while x !=ord('\n'):
    if pos != oldpos:
      oldpos = pos
      screen.border(0)
      screen.addstr(2,2, menu['title'], curses.A_STANDOUT) # Title for this menu
      screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu

      # Display all the menu items, showing the 'pos' item highlighted
      for index in range(optioncount):
        textstyle = n
        if pos==index:
          textstyle = h
        screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
      # Now display Exit/Return at bottom of menu
      textstyle = n
      if pos==optioncount:
        textstyle = h
      screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
      screen.refresh()
      # finished updating screen

    x = screen.getch() # Gets user input

    # What is user input?
    if x >= ord('1') and x <= ord(str(optioncount+1)):
      pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
    elif x == 258: # down arrow
      if pos < optioncount:
        pos += 1
      else: pos = 0
    elif x == 259: # up arrow
      if pos > 0:
        pos += -1
      else: pos = optioncount
  
  # return index of the selected item
  return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu,parent=None):
  
  optioncount = len(menu['options'])
  exitmenu = False
  while not exitmenu: #Loop until the user exits the menu
   
    getin = runmenu(menu, parent)
    if getin == optioncount:
        exitmenu = True
    elif menu['options'][getin]['type'] == COMMAND:
      curses.def_prog_mode()    # save curent curses environment
      os.system('reset')
      screen.clear() #clears previous screen   
      os.system(menu['options'][getin]['command']) # run the command
      menu['options'][getin]['title'] = initMenu(getin)
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)
    elif menu['options'][getin]['type'] == MENU:
          screen.clear() #clears previous screen on key press and updates display based on pos
          processmenu(menu['options'][getin], menu) # display the submenu
          screen.clear() #clears previous screen on key press and updates display based on pos
    elif menu['options'][getin]['type'] == EXITMENU:
          exitmenu = True
    
          
# Main program
menu = chargementConfig()
processmenu(menu)
curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('clear')
