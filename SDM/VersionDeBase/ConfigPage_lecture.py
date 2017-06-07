# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
from classes import *
#from terminal import *
from communication import *
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import platform                ## Underlying platform’s info library
import ConfigPage_terminal as Terminal

bgColor = 'white' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Taille des boutons

    
# la classe Lecture
class Lecture(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.pack()
        self.configure(bg=bgColor)
    
	# on lance la creation des widgets
	self.widget_lecture()
    
    def widget_lecture(self):
	self.fReadConfig = Frame(self, bg=bgColor)
	self.fReadConfig.grid(row=0,column=0)
	
        self.label_fRead=LabelFrame(self.fReadConfig,text="Configuration", fg=fgColor, font=titreFont, bg=bgColor)
        #self.label_fRead.grid_propagate(0)
        self.label_fRead.pack(side=TOP)
	#self.label_fRead.grid(row=0,column=0)

        self.labelPN=Label(self.label_fRead,text="Part Number", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelPN.grid(padx=2, row=1 ,column=0)

        self.labelSN=Label(self.label_fRead,text="Serial Number", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelSN.grid(padx=2, row=1 ,column=1)

        self.labelDate=Label(self.label_fRead,text="Date Fabrication", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelDate.grid(padx=2, row=1 ,column=2)

        self.labelCRCMEP=Label(self.label_fRead,text="MEP CRC",  fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelCRCMEP.grid(padx=2, row=3 ,column=0)

        self.labelCRCBBP=Label(self.label_fRead,text="BBP CRC", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelCRCBBP.grid(padx=2, row=3 ,column=1)

        self.labelLRU=Label(self.label_fRead,text="LRU Run Time", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelLRU.grid(padx=2, row=3 ,column=2)

        self.EntryPN=Entry(self.label_fRead,  font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryPN.grid(padx=2, row=2 ,column=0)

        self.EntrySN=Entry(self.label_fRead, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntrySN.grid(padx=2, row=2 ,column=1)

        self.EntryDate=Entry(self.label_fRead, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryDate.grid(padx=2, row=2 ,column=2)

        self.EntryCRCMEP=Entry(self.label_fRead, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryCRCMEP.grid(padx=2, row=4 ,column=0)

        self.EntryCRCBBP=Entry(self.label_fRead, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryCRCBBP.grid(padx=2, row=4 ,column=1)

        self.EntryLRU=Entry(self.label_fRead, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryLRU.grid(padx=2, row=4 ,column=2)

        self.boutonReadConfig=Button(self.label_fRead,text="Lire la configuration des données NVM",bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.read_config)
        self.boutonReadConfig.grid(padx=2, pady=2, row=5 ,column=0, columnspan=3)
	
	############################################
        self.fReadMemoire = Frame(self, bg=bgColor)
        #self.fReadMemoire.pack(pady=2)
	self.fReadMemoire.grid(row=1,column=0)

        self.label_fReadMemoire=LabelFrame(self.fReadMemoire,text="Lire une case mémoire", fg=fgColor, font=titreFont, bg=bgColor)
        self.label_fReadMemoire.pack_propagate(0)
        self.label_fReadMemoire.pack(side=TOP)

        self.labelReadCaseMemoire=Label(self.label_fReadMemoire,text="Adresse Mémoire", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelReadCaseMemoire.grid(padx=2, pady=2, row=0 ,column=1)

        self.labelTypeMemoire=Label(self.label_fReadMemoire,text="Mémoire ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelTypeMemoire.grid(padx=2, pady=2, row=0 ,column=2)


        self.labelReadNbOctets=Label(self.label_fReadMemoire,text="Nombre d'octets ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelReadNbOctets.grid(padx=2, pady=2, row=0 ,column=3)

        Label(self.label_fReadMemoire,text="0x", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=0, pady=2, row=1 ,column=0)
        self.EntryReadCaseMemoire=Entry(self.label_fReadMemoire,  font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryReadCaseMemoire.grid(ipadx=0, row=1,column=1,sticky=W)

        self.typeMemoire = StringVar(self.label_fReadMemoire)
        self.typeMemoire.set("NVM")
        self.EntryTypeMemoire=OptionMenu(self.label_fReadMemoire, self.typeMemoire,"RAM","FLASH","NVM")
        self.EntryTypeMemoire.grid(padx=2, row=1 ,column=2)
        
        self.nbOctet = StringVar(self.label_fReadMemoire)
        self.nbOctet.set("4")
        self.EntryReadNbOctets=OptionMenu(self.label_fReadMemoire, self.nbOctet,"1","2","3","4")
        self.EntryReadNbOctets.grid(padx=2, row=1 ,column=3)

        self.boutonReadCaseMemoire=Button(self.label_fReadMemoire,text="Lire",bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.read_memory)
        self.boutonReadCaseMemoire.grid(padx=2, pady=4, row=2 ,column=0, columnspan=4)
	
	#######################################################
	### un petit terminal pour lire les trames
	self.terminal = Text(self,width=90)
	#self.terminal.pack(pady=5)
	self.terminal.grid(pady=5,row=2,column=0)


        
    def effacer_zone_lecture(self):
        self.EntryPN.delete(0,END)
        self.EntrySN.delete(0,END)
        self.EntryDate.delete(0,END)
        self.EntryCRCMEP.delete(0,END)
        self.EntryCRCBBP.delete(0,END)
        self.EntryLRU.delete(0,END)

    def read_config(self):
        self.effacer_zone_lecture()
	# On fait aux threads AskConfig et ReadConfig
	interface = 'ics0can0'
	ask_config = AskConfig()
	read_config = ReadConfig(interface,self.terminal,self.EntryPN,self.EntrySN,self.EntryDate,self.EntryCRCMEP,self.EntryCRCBBP,self.EntryLRU)
	read_config.start()
	ask_config.start()

    def read_memory(self):
	if type(int(self.EntryReadCaseMemoire.get(),16)) == type(1):
	    memoire = int(self.EntryReadCaseMemoire.get(),16)
	    octet = self.nbOctet.get()
	    type_memoire = self.typeMemoire.get()
    
	    ask_adress_memory = AskAdressMemory(memoire,octet,type_memoire)
	    read_adress_memory = ReadAdressMemory('ics0can0',self.terminal)
	    read_adress_memory.start()
	    ask_adress_memory.start()
    
        
        

    def effacer(self):
        for widget in self.winfo_children():
            widget.destroy()

    def style(self):
        for widget in self.winfo_children():
            widget.configure(bg='white')
        
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Lecture PageConfiguration")
    fenLecture = Lecture(fenetre_principale=root)
    fenLecture.mainloop()
    
