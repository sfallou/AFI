# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
from classes import *
#from terminal import *
from communication import *
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import platform                ## Underlying platform’s info library

bgColor = 'white' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Taille des boutons

    
# la classe Terminal
class Terminal(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.pack()
        self.configure(bg=bgColor)
    
	# on lance la creation des widgets
	self.widget_terminal()
    
    def widget_terminal(self):
	
	### un petit terminal pour lire les trames
	self.terminal = Text(self,width=90)
	#self.terminal.pack(pady=5)
	self.terminal.grid(pady=5,row=2,column=0)
        
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Terminal")
    fenLecture = Terminal(fenetre_principale=root)
    fenLecture.mainloop()
    
