# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import ttk

from read_nvm import *

from subprocess import Popen, PIPE
import os
import time                    ## Time-related library

bgColor = 'white' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Couleur des boutons
tailleBorder = 2 # borderwidth
    
# la classe TestReception
class TestReception(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.fenP = fenetre_principale
	self.fenP.protocol("WM_DELETE_WINDOW", self.quit)
	# center window
	#self.fenP.eval('tk::PlaceWindow %s center' % self.fenP.winfo_pathname(self.fenP.winfo_id()))
        self.pack()
	self.configure(bg=bgColor)
	self.couleurSignal1 = "grey"
	self.couleurSignal2 = "grey"
	self.PN = ""
	# Les différentes zone de l'interface initialisées au démarrage
	self.init_interface()
	
    def init_interface(self):
	#création des  fenêtres
	self.fenetre1 = Frame(self,bg=bgColor,borderwidth=tailleBorder,relief=GROOVE)
	self.fenetre1.grid(padx=2,pady=2,row=0,column=0)
	self.fenetre2 = Frame(self,bg=bgColor,borderwidth=tailleBorder,relief=GROOVE)
	self.fenetre2.grid(padx=2,pady=2,row=0,column=1)
	
	# création des widgets de chaque fenêtre
	
	###### Fêntre 1 #########
	
	# Type de PN (menu déroulant)
	self.frame00 = Frame(self.fenetre1,bg=bgColor) # sert à bien arranger les widgets de l'entête
	self.frame00.pack(pady=5)
	
	Label(self.frame00,text="Part Number :", fg=fgColor, font=titreFont, bg=bgColor).grid(padx=4,row=0,column=0)
	
	choix = ["474560-1x","474560-2x","474560-4x-5x","475571-x","474449-5"]
	self.choixPN = StringVar(self.fenetre1)
        self.choixPN.set("Choisir le type de PN")
	
        self.EntryChoixPN=OptionMenu(self.frame00, self.choixPN,*choix)
	self.EntryChoixPN.config(width=20)
        self.EntryChoixPN.grid(padx=2,row=0,column=1)
	
	self.boutonValider=Button(self.frame00,text="Valider",bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.valider_choix)
        self.boutonValider.grid(padx=2,row=0,column=3)
	
	# Zone de Text pour les consignes à appliqué
	self.frame0 = Frame(self.fenetre1,bg=bgColor) # sert à bien arranger les widgets de cette zone
	self.frame0.pack(pady=5)
	self.labelConsigne = Label(self.frame0,text="Consignes", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelConsigne.grid(row=0,column=0)
	self.textConsigne = Text(self.frame0, height=20, width=80,font=("consolas",10))
	self.textConsigne.grid(row=1,column=0)
	# le scrollbar 
	self.scrollbar = Scrollbar(self.frame0, command=self.textConsigne.yview)
	self.scrollbar.grid(row=1,column=1,sticky="nsew")
	self.textConsigne['yscrollcommand'] = self.scrollbar.set
	# Zone de Text pour les logs
	self.labelLogs = Label(self.frame0,text="Logs", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelLogs.grid(row=2,column=0)
	self.textLogs = Text(self.frame0, height=8, width=80,font=("consolas",10))
	self.textLogs.grid(row=3,column=0)
	# le scrollbar
	self.scrollb = Scrollbar(self.frame0, command=self.textLogs.yview)
	self.scrollb.grid(row=3,column=1,sticky="nsew")
	self.textLogs['yscrollcommand'] = self.scrollb.set
	# La barre de progression
	self.progressBar = ttk.Progressbar(self.frame0,orient="horizontal",length=500,mode="determinate")
	self.progressBar.grid(pady=2,row=4,column=0)
	###### Fêntre 2 #########
	
	# Bouton Charger qui permet d'ouvir la clé et de lire le contenu du smoke
	self.boutonLoad=Button(self.fenetre2,text="Lancer le test",bd=2, width=50, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.loading)
        self.boutonLoad.pack(pady=5, side=TOP)
	
	self.frame1 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les labels et les entry pn, sn ...
	self.frame1.pack(pady=5)
	
	self.labelPN = Label(self.frame1,text="Part Number", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelPN.grid(padx=2,pady=2,row=0,column=0)
	
	self.labelSN = Label(self.frame1,text="Serial Number", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelSN.grid(padx=2,pady=2,row=1,column=0)
	
	self.labelDate = Label(self.frame1,text="Date Fabrication", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelDate.grid(padx=2,pady=2,row=2,column=0)
	
	self.EntryPN=Entry(self.frame1, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryPN.grid(padx=2,pady=2, row=0 ,column=1)
	
	self.EntrySN=Entry(self.frame1, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntrySN.grid(padx=2,pady=2, row=1 ,column=1)
	
	self.EntryDate=Entry(self.frame1, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryDate.grid(padx=2,pady=2, row=2 ,column=1)
	
	###
	self.frame2 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les labels et les entry bbcrc ...
	self.frame2.pack(pady=5)
	
	self.labelBBPCRC_Ref = Label(self.frame2,text="CRC BBP Réf ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelBBPCRC_Ref.grid(padx=2,pady=2,row=0,column=0)
	
	self.labelBBPCRC_calc = Label(self.frame2,text="CRC BBP calculé", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelBBPCRC_calc.grid(padx=2,pady=2,row=0,column=1)
	
	self.labelBBPCRC_actu = Label(self.frame2,text="CRC BBP actuel", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelBBPCRC_actu.grid(padx=2,pady=2,row=0,column=2)
	
	self.EntryBBPCRC_ref=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryBBPCRC_ref.grid(padx=2,pady=2, row=1, column=0)
	
	self.EntryBBPCRC_calc=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryBBPCRC_calc.grid(padx=2,pady=2, row=1, column=1)
	
	self.EntryBBPCRC_actu=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryBBPCRC_actu.grid(padx=2,pady=2, row=1 ,column=2)
	
	# On crée un voyant qui joue un rôle de signalisation
	self.canvas = Canvas(self.frame2, width=40,heigh=38, bg=bgColor, bd=0, highlightthickness=0)
	self.canvas.grid(padx=2,pady=2,row=1,column=3)
	self.canvas.create_oval(0,0,35,35, fill=self.couleurSignal2)
	
	##
	self.labelMEPCRC_Ref = Label(self.frame2,text="CRC MEPP Réf ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelMEPCRC_Ref.grid(padx=2,pady=2,row=2,column=0)
	
	self.labelMEPCRC_calc = Label(self.frame2,text="CRC MEP calculé", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelMEPCRC_calc.grid(padx=2,pady=2,row=2,column=1)
	
	self.labelMEPCRC_actu = Label(self.frame2,text="CRC MEP actuel", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelMEPCRC_actu.grid(padx=2,pady=2,row=2,column=2)
	
	self.EntryMEPCRC_ref=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryMEPCRC_ref.grid(padx=2,pady=2, row=3, column=0)
	
	self.EntryMEPCRC_calc=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryMEPCRC_calc.grid(padx=2,pady=2, row=3, column=1)
	
	self.EntryMEPCRC_actu=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryMEPCRC_actu.grid(padx=2,pady=2, row=3 ,column=2)
	
	# On crée un voyant qui joue un rôle de signalisation
	self.canvas = Canvas(self.frame2, width=40,heigh=40, bg=bgColor, bd=0, highlightthickness=0)
	self.canvas.grid(padx=2,pady=2,row=3,column=3)
	self.canvas.create_oval(0,0,35,35, fill=self.couleurSignal1)
	
	##
	self.labelTypeProg = Label(self.frame2,text="Programme en mémoire", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelTypeProg.grid(padx=2,pady=5,row=5,column=1)
	
	self.EntryTypeProg=Entry(self.frame2, font=fontSimple, bg=bgColor, width=entryLength)
        self.EntryTypeProg.grid(padx=2,pady=2, row=6 ,column=1)
	
	##
	# Bouton sauvegarder
	self.boutonSave=Button(self.fenetre2,text="Sauvegarder",bd=2, width=50, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.valider_choix)
        self.boutonSave.pack(pady=5, side=TOP)
	
	self.frame3 = Frame(self.fenetre2,bg=bgColor) 
	self.frame3.pack(pady=5)
	
	# Zone de Text pour les "erreurs"
	self.labelFaults = Label(self.frame3,text="Faults", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelFaults.grid(row=0,column=0)
	self.textFaults = Text(self.frame3, height=8, width=50,font=("consolas",11))
	self.textFaults.grid(row=1,column=0)
	
	
	
	## on désactive les boutons du fenetre2 
	self.boutonLoad.configure(state=DISABLED)
	self.boutonSave.configure(state=DISABLED)
	
	
	
    def valider_choix(self):
	try:
	    choix_pn = self.choixPN.get()
	    if choix_pn  != "Choisir le type de PN":
		self.PN = choix_pn
		self.boutonLoad.configure(state=NORMAL)
		self.boutonValider.configure(state=DISABLED)
		try:
		    #on ouvre consignes.txt et on l'affiche dans la zone de texte
		    chemin = "./docs/PNs/"+choix_pn
		    consigne = open(os.path.join(chemin+"/consignes.txt"),"r")
		    for line in consigne:
			self.textConsigne.insert(INSERT, line)
		except Exception as error:
		    print(repr(error))
		    
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    
    
    def loading(self):
	# on établit la connexion avec la clé
	self.open_dongle()
	# on lance le test et on affiche les trames CAN dans la zone logs ainsi que la progressBar
	interface = 'ics0can0'
	ask_config = AskConfig()
	read_config = ReadConfig(interface,self.textLogs,self.progressBar)
	read_config.start()
	ask_config.start()
	self.boutonSave.configure(state=NORMAL)
	
    def disable_fenetre(self,widget,state='disabled'):
	try:
	    widget.configure(state=state)
	except TclError:
	    pass
	for child in widget.winfo_children():
	    self.disable_fenetre(child,state=state)
    
    def open_dongle(self):
	# On execute le processus setup
	try:
	    self.process1 = Popen(["./icsscand/icsscand","-D"], stdout=PIPE)
	    time.sleep(1)
	    self.process2 = Popen(["ifconfig","ics0can0","up"], stdout=PIPE)
	except:
	    print ("impossible de se connecter")
	    
    
    def close_dongle(self):
	# On arrete le processus setup
	try:
	    os.system('pkill icsscand')
	except:
	    print ("impossible de fermer")
    
    def quit(self):
	self.close_dongle()
	self.fenP.destroy()
    
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Test de Reception")
    root.configure(bg=bgColor)
    testDeReception = TestReception(fenetre_principale=root)
    testDeReception.mainloop()
    
    
