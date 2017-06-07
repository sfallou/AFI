# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
from classes import *

from communication import *
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import platform                ## Underlying platform’s info library
import ics
from subprocess import Popen, PIPE
import os


bgColor = 'white' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Taille des boutons

    
# la classe Connexion
class Connexion(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.pack()
        self.configure(bg=bgColor)
	self.device = ics.find_devices()
	#print(device[0].Name, device[0].SerialNumber)
    
	# on lance la creation des widgets
	self.widget_connexion()
    
    def widget_connexion(self):
	self.label_fConnexion=LabelFrame(self,text="Connexion", fg=fgColor, font=titreFont, width=WinWidth, height=WinHigh, bg=bgColor)
        self.label_fConnexion.pack_propagate(0)
        self.label_fConnexion.pack(side=TOP)

        self.labelDongle=Label(self.label_fConnexion,text="Dongle ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelDongle.grid(padx=2, row=0 ,column=0)
        
        self.labelBaudrate=Label(self.label_fConnexion,text="Baudrate", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelBaudrate.grid(padx=2, row=0 ,column=1)
	

        self.labelDongleType=Label(self.label_fConnexion,text="Serial N°", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelDongleType.grid(padx=2, row=0 ,column=2)
        
        self.boutonConnexion=Button(self.label_fConnexion,text='Ouvrir',bd=1, width=buttonLength, relief=RAISED,  overrelief=RIDGE, bg=buttonColor, command=self.open)
        self.boutonConnexion.grid(padx=2, row=0 ,column=3)
	
	self.dongle = StringVar(self.label_fConnexion)
	if not self.device:
	    self.dongle.set("No device found")
	    cle = "No device found"
	    self.boutonConnexion.configure(state = DISABLED)
	else:
	    self.dongle.set("Select device")
	    cle = self.device[0].Name
        self.EntryDongle=OptionMenu(self.label_fConnexion, self.dongle, cle)
	self.EntryDongle.grid(padx=2, row=1 ,column=0)
        
        self.EntryBaudrate=Entry(self.label_fConnexion, fg=fgColor, font=fontSimple, bg='white', width=entryLength)
        self.EntryBaudrate.grid(padx=2, row=1 ,column=1)
	self.EntryBaudrate.configure(state=DISABLED)

        self.EntryDongleType=Entry(self.label_fConnexion,  fg=fgColor, font=fontSimple, bg='white', width=entryLength)
        self.EntryDongleType.grid(padx=2, row=1 ,column=2)
	self.EntryDongleType.configure(state=DISABLED)
        
        self.boutonDeconnexion=Button(self.label_fConnexion,text='Fermer',bd=1,width=buttonLength, relief=RAISED, overrelief=RIDGE, bg=bgColor, command=self.close)
        self.boutonDeconnexion.grid(padx=2, row=1 ,column=3)
	self.boutonDeconnexion.configure(state=DISABLED)
    
    def open(self):
	if self.dongle.get() != "Select device":
	    # On execute le processus setup
	    try:
		self.process1 = Popen(["./icsscand/icsscand","-D"], stdout=PIPE)
		time.sleep(1)
		self.process2 = Popen(["ifconfig","ics0can0","up"], stdout=PIPE)
		# On renseigne le serial number et le bitrate
		self.EntryDongleType.configure(state = NORMAL)
		self.EntryBaudrate.configure(state = NORMAL)
	    
		self.EntryDongleType.delete(0,END)
		self.EntryDongleType.insert(0,self.device[0].SerialNumber)
		self.EntryDongleType.configure(state = "readonly")
	    
		self.EntryBaudrate.delete(0,END)
		self.EntryBaudrate.insert(0,"125kbit/s")
		self.EntryBaudrate.configure(state = "readonly")
	    
		# On désactive le bouton ouvrir et on réactive fermer
		self.boutonConnexion.configure(state = DISABLED)
		self.boutonDeconnexion.configure(state = NORMAL)
	    
	    except:
		print ("impossible de se connecter")
	    
    
    def close(self):
	# On arrete le processus setup
	try:
	    os.system('pkill icsscand')
	    self.EntryDongleType.configure(state = NORMAL)
	    self.EntryBaudrate.configure(state = NORMAL)
	    self.EntryDongleType.delete(0,END)
	    self.EntryBaudrate.delete(0,END)
	    self.EntryDongleType.configure(state = DISABLED)
	    self.EntryBaudrate.configure(state = DISABLED)
	    # On désactive le bouton fermer et on réactive ouvrir
	    self.boutonConnexion.configure(state = NORMAL)
	    self.boutonDeconnexion.configure(state = DISABLED)
	    
	except:
	    print ("impossible de fermer")
    
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Connexion PageConfiguration")
    fenConnexion = Connexion(fenetre_principale=root)
    fenConnexion.mainloop()
    
