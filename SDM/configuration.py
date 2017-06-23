# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import ttk
import tkFileDialog
import ics
from write_nvm import *
from subprocess import Popen, PIPE
import os
import time                    ## Time-related library
import datetime
import data


bgColor = 'light yellow' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Couleur des boutons
tailleBorder = 2 # borderwidth
    
# la classe Configuration
class Configuration(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.fenP = fenetre_principale
	self.fenP.protocol("WM_DELETE_WINDOW", self.quit)
	# center window
	#self.fenP.eval('tk::PlaceWindow %s center' % self.fenP.winfo_pathname(self.fenP.winfo_id()))
        #self.pack()
	self.configure(bg=bgColor)
	self.PN = ""
	self.CRC_MEP = ""
	self.CRC_BBP = ""
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
	
	Label(self.frame00,text="PN :", fg=fgColor, font=titreFont, bg=bgColor).grid(padx=2,row=0,column=0)
	choix_pn = ["474560-1x","474560-2x","474560-4x-5x","475571-x","474449-5"]
	self.choixPN = StringVar(self.fenetre1)
        self.choixPN.set("Choisir le type de PN")
        self.EntryChoixPN=OptionMenu(self.frame00, self.choixPN,*choix_pn)
	self.EntryChoixPN.config(width=18)
        self.EntryChoixPN.grid(padx=2,row=0,column=1)
	
	choix_prog = ["Calibration","Flight"]
	self.choixPROG = StringVar(self.fenetre1)
        self.choixPROG.set("Type de programme")
	self.EntryChoixPROG=OptionMenu(self.frame00, self.choixPROG,*choix_prog)
	self.EntryChoixPROG.config(width=15)
        self.EntryChoixPROG.grid(padx=2,row=0,column=2)
	
	self.boutonValider=Button(self.frame00,text="Valider",bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.valider_choix)
        self.boutonValider.grid(padx=2,row=0,column=3)
	
	# Zone des données récupérées et des read/write
	self.frame0 = Frame(self.fenetre1,bg=bgColor) # sert à bien arranger les widgets de cette zone
	self.frame0.pack(pady=5)
	
	Label(self.frame0,text="BBP CRC Réf", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=1,column=1)
	self.EntryBBPCRC=Entry(self.frame0, font=fontSimple, width=entryLength)
        self.EntryBBPCRC.grid(padx=2,pady=2, row=1 ,column=2)
	
	Label(self.frame0,text="MEP CRC Réf", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=2,column=1)
	self.EntryMEPCRC=Entry(self.frame0, font=fontSimple, width=entryLength)
        self.EntryMEPCRC.grid(padx=2,pady=2, row=2 ,column=2)
	
	self.labeMEP = Label(self.frame0,text="......", fg=fgColor, font=fontSimple, bg=bgColor)
	self.labeMEP.grid(padx=2,pady=2, row=3 ,column=0,columnspan=3)
	
	Label(self.frame0,text="CBDS CRC Réf", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=4,column=1)
	self.EntryCBDSCRC=Entry(self.frame0, font=fontSimple, width=entryLength)
        self.EntryCBDSCRC.grid(padx=2,pady=2, row=4 ,column=2)
	
	self.boutonConfigurer=Button(self.frame0,text="Configurer le MCU",bd=2, width=50, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonConfigurer.grid(padx=2,pady=15,row=5,column=0,columnspan=4)
	
	# Zone updates

        self.label_fWrite=LabelFrame(self.frame0,text="Updates", fg=fgColor, font=titreFont, bg=bgColor)
	self.label_fWrite.grid(padx=2,pady=5,row=6,column=0,columnspan=4)
	
	self.labelUpdatePN=Label(self.label_fWrite,text="Format BCD(8)", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelUpdatePN.grid(padx=2, pady=2, row=0 ,column=0)
	
	self.labelUpdateSN=Label(self.label_fWrite,text="Format ASCII(7)", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelUpdateSN.grid(padx=2, pady=2, row=0 ,column=1)
	
	self.labelUpdateDate=Label(self.label_fWrite,text="YYYYMMDD", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelUpdateDate.grid(padx=2, pady=2, row=0 ,column=2)
	
        self.EntryUpdatePN=Entry(self.label_fWrite, font=fontSimple, width=entryLength)
        self.EntryUpdatePN.grid(padx=2, pady=2, row=1 ,column=0)

        self.EntryUpdateSN=Entry(self.label_fWrite, font=fontSimple, width=entryLength)
        self.EntryUpdateSN.grid(padx=2, pady=2, row=1 ,column=1)

        self.EntryUpdateDate=Entry(self.label_fWrite, font=fontSimple, width=entryLength)
        self.EntryUpdateDate.grid(padx=2, pady=2, row=1 ,column=2)

        self.boutonUpdatePN=Button(self.label_fWrite,text='Modifier PN',bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonUpdatePN.grid(padx=2, pady=2, row=2 ,column=0)

        self.boutonUpdateSN=Button(self.label_fWrite,text='Modifier SN',bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonUpdateSN.grid(padx=2, pady=2, row=2 ,column=1)
        
        self.boutonUpdateDate=Button(self.label_fWrite,text='Modifier Date ',bd=2, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonUpdateDate.grid(padx=2, pady=2, row=2 ,column=2)

	# Zone read Case mémoire
	self.labelReadMemoire=LabelFrame(self.frame0,text="Read", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelReadMemoire.grid(padx=2,pady=5,row=7,column=0,columnspan=4)

        self.labelReadCaseMemoire=Label(self.labelReadMemoire,text="@ Mémoire", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelReadCaseMemoire.grid(padx=2, pady=2, row=0 ,column=1)

        self.labelTypeMemoire=Label(self.labelReadMemoire,text="Mémoire ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelTypeMemoire.grid(padx=2, pady=2, row=0 ,column=2)


        self.labelReadNbOctets=Label(self.labelReadMemoire,text="Octets ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelReadNbOctets.grid(padx=2, pady=2, row=0 ,column=3)

        Label(self.labelReadMemoire,text="0x", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=0, pady=2, row=1 ,column=0)
        self.EntryReadCaseMemoire=Entry(self.labelReadMemoire, font=fontSimple, width=entryLength)
        self.EntryReadCaseMemoire.grid(ipadx=0, row=1,column=1,sticky=W)

        self.typeMemoire = StringVar(self.labelReadMemoire)
        self.typeMemoire.set("NVM")
        self.EntryTypeMemoire=OptionMenu(self.labelReadMemoire, self.typeMemoire,"RAM","FLASH","NVM")
        self.EntryTypeMemoire.grid(padx=2, row=1 ,column=2)
        
        self.nbOctet = StringVar(self.labelReadMemoire)
        self.nbOctet.set("4")
        self.EntryReadNbOctets=OptionMenu(self.labelReadMemoire, self.nbOctet,"1","2","3","4")
        self.EntryReadNbOctets.grid(padx=2, row=1 ,column=3)

        self.boutonReadCaseMemoire=Button(self.labelReadMemoire,text="Read",bd=2, relief=RAISED,width=9, overrelief=RIDGE, bg=buttonColor)
        self.boutonReadCaseMemoire.grid(padx=2, pady=2, row=1 ,column=4)

	# Zone Write memory
	
	self.label_fWriteMemoire=LabelFrame(self.frame0,text="Write", fg=fgColor, font=titreFont, bg=bgColor)
        self.label_fWriteMemoire.grid(padx=2,pady=5,row=8,column=0,columnspan=4)
        

        self.labelWriteCaseMemoire=Label(self.label_fWriteMemoire,text="@ Mémoire", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelWriteCaseMemoire.grid(padx=2, pady=2, row=0 ,column=1)

        self.labelWriteDatas=Label(self.label_fWriteMemoire,text="Données ", fg=fgColor, font=fontSimple, bg=bgColor)
        self.labelWriteDatas.grid(padx=2, pady=2, row=0 ,column=2)
	
	Label(self.label_fWriteMemoire,text="0x", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=0, pady=2, row=1 ,column=0)
        self.EntryWriteCaseMemoire=Entry(self.label_fWriteMemoire, font=fontSimple, width=entryLength)
        self.EntryWriteCaseMemoire.grid(ipadx=0, row=1,column=1,sticky=W)

        self.EntryWriteDatas=Entry(self.label_fWriteMemoire, font=fontSimple, width=entryLength)
        self.EntryWriteDatas.grid(padx=2, row=1 ,column=2)

        self.boutonWriteCaseMemoire=Button(self.label_fWriteMemoire,text="Write",bd=2, width=14, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonWriteCaseMemoire.grid(padx=2, pady=2, row=1 ,column=3)
	
    
	###### Fêntre 2 #########
	# Zone de Text pour les consignes à appliqué
	
	self.labelConsigne = Label(self.fenetre2,text="Consignes", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelConsigne.grid(row=0,column=0)
	self.textConsigne = Text(self.fenetre2, height=20, width=80,font=("consolas",10))
	self.textConsigne.grid(row=1,column=0)
	# le scrollbar 
	self.scrollbar = Scrollbar(self.fenetre2, command=self.textConsigne.yview)
	self.scrollbar.grid(row=1,column=1,sticky="nsew")
	self.textConsigne['yscrollcommand'] = self.scrollbar.set
	# Zone de Text pour les logs
	self.labelLogs = Label(self.fenetre2,text="Logs", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelLogs.grid(row=2,column=0)
	self.textLogs = Text(self.fenetre2, height=10, width=80,font=("consolas",10))
	self.textLogs.grid(row=3,column=0)
	# le scrollbar
	self.scrollb = Scrollbar(self.fenetre2, command=self.textLogs.yview)
	self.scrollb.grid(row=3,column=1,sticky="nsew")
	self.textLogs['yscrollcommand'] = self.scrollb.set
	
	self.boutonClear=Button(self.fenetre2,text="Effacer",bd=2,width=15, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.effacer_logs)
        self.boutonClear.grid(padx=2, pady=2, row=4 ,column=0,columnspan=2)
	
	# On désactive certains bouttons au démarrage
	self.boutonConfigurer.configure(state=DISABLED)
	self.boutonUpdatePN.configure(state=DISABLED)
        self.boutonUpdateSN.configure(state=DISABLED)
	self.boutonUpdateDate.configure(state=DISABLED)
	self.boutonWriteCaseMemoire.configure(state=DISABLED)
	self.boutonReadCaseMemoire.configure(state=DISABLED)
    ####################################################
    def valider_choix(self):
	try:
	    choix_pn = self.choixPN.get()
	    choix_prog = self.choixPROG.get()
	    if choix_pn  != "Choisir le type de PN" and choix_prog  != "Type de programme" :
		self.PN = choix_pn
		# on établit la connexion avec la clé
		res = self.open_dongle()
		# Si res = 1, on lance le test et on affiche les trames CAN dans la zone logs ainsi que la progressBar
		if res:
		    self.boutonConfigurer.configure(state=NORMAL, command=self.configurer)
		    self.boutonUpdatePN.configure(state=NORMAL, command=self.changer_pn)
		    self.boutonUpdateSN.configure(state=NORMAL, command=self.changer_sn)
		    self.boutonUpdateDate.configure(state=NORMAL, command=self.changer_date)
		    self.boutonWriteCaseMemoire.configure(state=NORMAL, command=self.write_memory)
		    self.boutonReadCaseMemoire.configure(state=NORMAL, command=self.read_memory)
		    self.boutonValider.configure(state=DISABLED)
		    self.EntryChoixPROG.configure(state=DISABLED)
		    self.EntryChoixPN.configure(state=DISABLED)
		    try:
			# On affiche le message sur le MEP à charger
			self.labeMEP.configure(text="Le MEP de "+choix_prog+" aussi va à être chargé")
			self.labeMEP.grid(padx=2,pady=2, row=3 ,column=2)
			# On récupère les valeurs du CRC MEP, CRC BBP et CRC CBDS ainsi que le contenu du MEP
			chemin = "./docs/PNs/"+choix_pn
			self.valeur_adresse_2c = 0x00
			contenu_mep = ""
			#on ouvre consignes.txt et on l'affiche dans la zone de texte
			consigne = open(os.path.join(chemin+"/consignes.txt"),"r")
			for line in consigne:
			    self.textConsigne.insert(INSERT, line)
			self.CRC_BBP = open(os.path.join(chemin+"/BBP/crc.txt"),"r").readline()[:-1]
			if choix_prog == "Calibration":
			    self.CRC_MEP = open(os.path.join(chemin+"/MEP/crc_calib.txt"),"r").readline()[:-1]
			    self.contenu_mep = "mep_calibration_"+self.nom_fichier_pn(choix_pn)
			    #self.contenu_mep = getattr(data,self.contenu_mep)
			    #print (self.contenu_mep)
			    self.valeur_adresse_2c = 0x01
			elif choix_prog == "Flight":
			    self.CRC_MEP = open(os.path.join(chemin+"/MEP/crc_flight.txt"),"r").readline()[:-1]
			    self.contenu_mep = "mep_flight_"+self.nom_fichier_pn(choix_pn)
			    
			# On écrit valeur_adresse_2c dans l'eeprom sur 1 octet
			# Puis on charge le MEP dans la mémoire flash
			# Ensuite on charge le CRC_MEP dans le NVM
			# Et enfin on charge le CRC_CBDS
			
		    
		    except Exception as error:
			print(repr(error))
		    
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    
    #######################################################
    def configurer(self):
	#config = Configurer_carte(self.valeur_adresse_2c, self.contenu_mep, self.CRC_MEP)
	#config.start()
	pass
	
    #####################################################
    def open_dongle(self):
	#self.close_dongle() # au cas ou le processus etait toujours en vie
	# On execute le processus setup
	
	try:
	    self.device = ics.find_devices()
	    if self.device:
		self.process1 = Popen(["sudo","./icsscand/icsscand","-D"], stdout=PIPE)
		time.sleep(1)
		self.process2 = Popen(["sudo","ifconfig","ics0can0","up"], stdout=PIPE)
		return 1
	    else:
		showerror("No device Found","Veuillez brancher la clé VCAN !")
		return 0
	except:
	    print ("impossible de se connecter")
	    showerror("Erreur de communication","Impossible d'ouvrir la clé VCAN. Assurez vous qu'elle est bien branchée et relancer le logiciel")
	return O
    #######################################################
    def close_dongle(self):
	# On arrete le processus setup
	try:
	    os.system('sudo pkill icsscand')
	except:
	    print ("impossible de fermer")
    ######################################################
    def quit(self):
	self.close_dongle()
	self.fenP.destroy()
    ######################################################
    def read_memory(self):
        try:
	    memoire = int(self.EntryReadCaseMemoire.get(),16)
	    octet = self.nbOctet.get()
	    type_memoire = self.typeMemoire.get()
    
	    ask_adress_memory = AskAdressMemory(memoire,octet,type_memoire)
	    # On démarre l'écoute des logs
	    log1 = TerminalLog('ics0can0',self.textLogs)
	    log1.start()
	    ask_adress_memory.start()
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    ######################################################
    def write_memory(self):
        try:
	    memoire = int(self.EntryWriteCaseMemoire.get(),16)
	    data = int(self.EntryWriteDatas.get())
	    if len(str(data))<=8:
		write_adress_memory = WriteAdressMemory(memoire,data)
		# On démarre l'écoute des logs
		log2 = TerminalLog('ics0can0',self.textLogs)
		log2.start()
		write_adress_memory.start()
	    else:
		showwarning("Erreur de saisie","Impossible de depasser 8 caractères")
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    ######################################################
    def changer_pn(self):
        try:
	    newPN = int(self.EntryUpdatePN.get())
	    memoire = 0x14
	    if len(str(newPN))==8:
		write_adress_memory = WriteAdressMemory(memoire,newPN)
		# On démarre l'écoute des logs
		log2 = TerminalLog('ics0can0',self.textLogs)
		log2.start()
		write_adress_memory.start()
	    else:
		showwarning("Erreur de saisie","Il faut 8 caractères")
	    
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    ######################################################
    def changer_sn(self):
        try:
	    newSN = self.EntryUpdateSN.get()
	    if len(newSN) == 7:
		sn_1 = newSN[0:4].encode("hex")
		sn_2 = newSN[4:7].encode("hex")
		write_adress_memory_1 = WriteAdressMemory(0xc,sn_1)
		write_adress_memory_2 = WriteAdressMemory(0x10,sn_2)
		# On démarre l'écoute des logs
		log2 = TerminalLog('ics0can0',self.textLogs)
		log2.start()
		write_adress_memory_1.start()
		time.sleep(0.5)
		write_adress_memory_2.start()
	    else:
		showwarning("Erreur de saisie","Il faut 7 caractères")
	    
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    ######################################################
    def changer_date(self):
        try:
	    newDate = self.EntryUpdateDate.get()
	    print("date",newDate)
	    memoire = 0x24
	    if len(str(newDate))==8:
		write_adress_memory = WriteAdressMemory(memoire,newDate)
		# On démarre l'écoute des logs
		log2 = TerminalLog('ics0can0',self.textLogs)
		log2.start()
		write_adress_memory.start()
	    else:
		showwarning("Erreur de saisie","Il faut 8 caractères")
	    
	except Exception as error:
	    print('Erreur de saisie: ' + repr(error))
    ######################################################
    def effacer_logs(self):
	self.textLogs.delete(0.0,END)
    ######################################################
    def nom_fichier_pn(self,x):
	return{
	    "474560-1x":"474560_1x",
	    "474560-2x":"474560_2x",
	    "474560-4x-5x":"474560_4x_5x",
	    "475571-x":"475571_x",
	    "474449-5":"474449_5",
	}[x]

	    
    
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Configuration")
    root.configure(bg=bgColor)
    configuration = Configuration(fenetre_principale=root)
    configuration.mainloop()
    
    
