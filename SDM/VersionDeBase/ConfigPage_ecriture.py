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

    
# la classe Ecriture
class Ecriture(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.pack()
        self.configure(bg=bgColor)
    
	# on lance la creation des widgets
	self.widget_ecriture()
    def widget_ecriture(self):
	self.fWrite = Frame(self,bg=bgColor)
        self.fWrite.grid_propagate(0)
        self.fWrite.grid(padx=2, pady=2, row=0 ,column=1)

        self.label_fWrite=LabelFrame(self.fWrite,text="Ecriture", fg=fgColor, font=titreFont, bg=bgColor)
        self.label_fWrite.pack_propagate(0)
        self.label_fWrite.pack(side=TOP)

        self.EntryUpdatePN=Entry(self.label_fWrite, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryUpdatePN.grid(padx=2, pady=2, row=0 ,column=0)

        self.EntryUpdateSN=Entry(self.label_fWrite, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryUpdateSN.grid(padx=2, pady=2, row=0 ,column=1)

        self.EntryUpdateDate=Entry(self.label_fWrite, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryUpdateDate.grid(padx=2, pady=2, row=0 ,column=2)

        self.boutonWritePN=Button(self.label_fWrite,text='Modifier PN',bd=2, relief=RAISED,  overrelief=RIDGE, bg=buttonColor)
        self.boutonWritePN.grid(padx=2, pady=2, row=1 ,column=0)

        self.boutonWriteSN=Button(self.label_fWrite,text='Modifier SN',bd=2, relief=RAISED,  overrelief=RIDGE, bg=buttonColor)
        self.boutonWriteSN.grid(padx=2, pady=2, row=1 ,column=1)
        
        self.boutonWriteDate=Button(self.label_fWrite,text='Modifier Date ',bd=2, relief=RAISED,  overrelief=RIDGE, bg=buttonColor)
        self.boutonWriteDate.grid(padx=2, pady=2, row=1 ,column=2)

        self.boutonRecupCRCMEP=Button(self.label_fWrite,text='Charger MEP CRC',bd=2, relief=RAISED,  overrelief=RIDGE, bg=buttonColor)
        self.boutonRecupCRCMEP.grid(padx=2, pady=2, row=2 ,column=0)

        self.EntryRecupCRCMEP=Entry(self.label_fWrite,  font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryRecupCRCMEP.grid(padx=2, pady=2, row=2 ,column=1)

        self.boutonWriteCRCMEP=Button(self.label_fWrite,text='Écrire MEP CRC',bd=2, relief=RAISED,  overrelief=RIDGE, bg=buttonColor)
        self.boutonWriteCRCMEP.grid(padx=2,pady=2, row=2 ,column=2)
	
	###################
        self.fWriteMemoire = Frame(self, bg=bgColor)
        self.fWriteMemoire.grid_propagate(0)
        self.fWriteMemoire.grid(padx=2, pady=2, row=1 ,column=1, columnspan=3)

        self.label_fWriteMemoire=LabelFrame(self.fWriteMemoire,text="Écrire en case mémoire", fg=fgColor, font=titreFont, bg=bgColor)
        self.label_fWriteMemoire.pack_propagate(0)
        self.label_fWriteMemoire.pack(side=TOP)

        self.labelWriteCaseMemoire=Label(self.label_fWriteMemoire,text="Adresse Mémoire", font=fontSimple, bg=bgColor, width=entryLength)
        self.labelWriteCaseMemoire.grid(padx=2, pady=2, row=0 ,column=0)

        self.labelWriteDatas=Label(self.label_fWriteMemoire,text="Données ", font=fontSimple, bg=bgColor, width=entryLength)
        self.labelWriteDatas.grid(padx=2, pady=2, row=0 ,column=1)

        self.EntryWriteCaseMemoire=Entry(self.label_fWriteMemoire, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryWriteCaseMemoire.grid(padx=2, row=1,column=0)

        self.EntryWriteDatas=Entry(self.label_fWriteMemoire, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryWriteDatas.grid(padx=2, row=1 ,column=1)

        self.boutonWriteCaseMemoire=Button(self.label_fWriteMemoire,text="Lire",bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonWriteCaseMemoire.grid(padx=2, pady=2, row=1 ,column=2)
	
        
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Ecriture PageConfiguration")
    fenLecture = Ecriture(fenetre_principale=root)
    fenLecture.mainloop()
    
