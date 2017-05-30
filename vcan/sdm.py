# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
from classes import *
from terminal import *
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import platform                ## Underlying platform’s info library


# la classe SDM (Smoke Detector Maintenance)
class SDM(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Smoke Detector Maintenance')
        self.geometry("1150x750")
        self.resizable(0, 0)
        self.configure(bg='white')
        self.taille_police = 12
        self.taille_entry = 10
        self.body = Frame(self)  # corps de l'interface graphique
        #self.__CAN=None # on crée une variable initialisé à None qui va etre l'objet CAN par la suite
        # On fait appel à la méthode menu() et config_page
        self.menu()
        self.config_page()
        self.style()
        self.initialiser_terminal()

        #self.initialiser_interface()

    def menu(self):
        # creation du menu principale
        menubar = Menu(self)
        self.config(menu=menubar)
        menuConfiguration = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.config_page)
        menubar.add_cascade(label="Configuration", menu=menuConfiguration)
        menuMonitoring = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "Monitoring", menu=menuMonitoring)
        menuPAB = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "PAB", menu=menuPAB)
        menuHelp = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "Help", menu=menuHelp)
        menuAbout = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "About", menu=menuAbout) 
        
        ################################
        #L'entete
        ################################
        self.entete = Frame(self, bd =1, relief =RAISED)
        self.entete.pack(side=TOP)
        self.textEntete=Label(self.entete,text='Air France Industrie ', width=900,bd=1, bg ='#03224C', relief=RAISED, fg="#ff0000", font=('Helvetica', 14))
        #self.textEntete.grid(row =0, column =0, columnspan =3, padx =1, pady =1)
        self.textEntete.pack(side=TOP)

    # La fonction qui permet d'afficher la page de configuration 
    def config_page(self):
        # on efface le contenu précédent
        for widget in self.body.winfo_children():
            widget.destroy()
        # on attache le body à l'interface graphique
        self.body.pack(side=TOP)
        #--------------------------------------------------------------------------
        #Section Connexion
        #---------------------------------------------------------------------------
        self.fConnexion = Frame(self.body, bg='white')
        self.fConnexion.pack(pady=2,expand="yes",fill="both")
        #self.fConnexion.pack_propagate(0)

        self.label_fConnexion=LabelFrame(self.fConnexion,text="Connexion", fg="#03224C", font=('Helvetica', 20), width=1000, height=200, bg='white')
        self.label_fConnexion.pack_propagate(0)
        self.label_fConnexion.pack()

        self.labelDongle=Label(self.label_fConnexion,text="Dongle ", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelDongle.grid(padx=2, row=0 ,column=0)
        
        self.labelBaudrate=Label(self.label_fConnexion,text="Baudrate", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelBaudrate.grid(padx=2, row=0 ,column=1)

        self.labelDongleType=Label(self.label_fConnexion,text="Dongle Type", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelDongleType.grid(padx=2, row=0 ,column=2)
        
        self.boutonConnexion=Button(self.label_fConnexion,text='Ouvrir',bd=1, width=5, relief=RAISED,  overrelief=RIDGE, bg='#C0C0C0')
        self.boutonConnexion.grid(padx=2, row=0 ,column=3)

        self.EntryDongle=Entry(self.label_fConnexion, fg="#03224C", font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryDongle.grid(padx=2, row=1 ,column=0)
        
        self.EntryBaudrate=Entry(self.label_fConnexion, fg="#03224C", font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryBaudrate.grid(padx=2, row=1 ,column=1)

        self.EntryDongleType=Entry(self.label_fConnexion, fg="#03224C", font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryDongleType.grid(padx=2, row=1 ,column=2)
        
        self.boutonDeconnexion=Button(self.label_fConnexion,text='Fermer',bd=1,width=5, relief=RAISED, overrelief=RIDGE, bg='#C0C0C0')
        self.boutonDeconnexion.grid(padx=2, row=1 ,column=3)

        #-------------------------------------------
        # Zone de lecture et écriture des infos    |
        #-------------------------------------------
        self.ZonePrincipale = Frame(self.body, bg='white')
        self.ZonePrincipale.pack(pady=2,expand="yes",fill="both")
        #--------------------------------------------------------------------------
        # Section Lecture des données du smoke
        #---------------------------------------------------------------------------
        self.fRead = Frame(self.ZonePrincipale, width=400, height=200, bg='white')
        self.fRead.grid_propagate(0)
        self.fRead.grid(padx=2, pady=2, row=0 ,column=0)

        self.label_fRead=LabelFrame(self.fRead,text="Lecture", fg="#03224C", font=('Helvetica', 20), bg='white')
        self.label_fRead.pack_propagate(0)
        self.label_fRead.pack(side=TOP)

        self.labelPN=Label(self.label_fRead,text="Part Number", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelPN.grid(padx=2, row=1 ,column=0)

        self.labelSN=Label(self.label_fRead,text="Serial Number", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelSN.grid(padx=2, row=1 ,column=1)

        self.labelDate=Label(self.label_fRead,text="Date Fabrication", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelDate.grid(padx=2, row=1 ,column=2)

        self.labelCRCMEP=Label(self.label_fRead,text="MEP CRC", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelCRCMEP.grid(padx=2, row=3 ,column=0)

        self.labelCRCBBP=Label(self.label_fRead,text="BBP CRC", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelCRCBBP.grid(padx=2, row=3 ,column=1)

        self.labelLRU=Label(self.label_fRead,text="LRU Run Time", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelLRU.grid(padx=2, row=3 ,column=2)

        self.EntryPN=Entry(self.label_fRead,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryPN.grid(padx=2, row=2 ,column=0)

        self.EntrySN=Entry(self.label_fRead,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntrySN.grid(padx=2, row=2 ,column=1)

        self.EntryDate=Entry(self.label_fRead,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryDate.grid(padx=2, row=2 ,column=2)

        self.EntryCRCMEP=Entry(self.label_fRead,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryCRCMEP.grid(padx=2, row=4 ,column=0)

        self.EntryCRCBBP=Entry(self.label_fRead, font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryCRCBBP.grid(padx=2, row=4 ,column=1)

        self.EntryLRU=Entry(self.label_fRead, font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryLRU.grid(padx=2, row=4 ,column=2)

        self.boutonReadConfig=Button(self.label_fRead,text="Lire la configuration des données NVM",bd=2, relief=RAISED, overrelief=RIDGE, bg='#C0C0C0', command=self.read_config)
        self.boutonReadConfig.grid(padx=2, pady=2, row=5 ,column=0, columnspan=3)

        self.fReadMemoire = Frame(self.label_fRead, bg='white')
        self.fReadMemoire.grid_propagate(0)
        self.fReadMemoire.grid(padx=2, pady=2, row=6 ,column=0, columnspan=3)

        self.label_fReadMemoire=LabelFrame(self.fReadMemoire,text="Lire une case mémoire", fg="#03224C", font=('Helvetica', 20), bg='white')
        self.label_fReadMemoire.pack_propagate(0)
        self.label_fReadMemoire.pack(side=TOP)

        self.labelReadCaseMemoire=Label(self.label_fReadMemoire,text="Adresse Mémoire", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelReadCaseMemoire.grid(padx=2, pady=2, row=0 ,column=0)

        self.labelReadNbOctets=Label(self.label_fReadMemoire,text="Nombre d'octets ", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelReadNbOctets.grid(padx=2, pady=2, row=0 ,column=1)

        self.EntryReadCaseMemoire=Entry(self.label_fReadMemoire,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryReadCaseMemoire.grid(padx=2, row=1,column=0)

        #self.EntryReadNbOctets=Entry(self.label_fReadMemoire, fg="#03224C", font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        #self.EntryReadNbOctets.grid(padx=2, row=1 ,column=1)
        
        self.nbOctet = StringVar(self.label_fReadMemoire)
        self.nbOctet.set("4")
        self.EntryReadNbOctets=OptionMenu(self.label_fReadMemoire, self.nbOctet,"1","2","3","4")
        self.EntryReadNbOctets.grid(padx=2, row=1 ,column=1)

        self.boutonReadCaseMemoire=Button(self.label_fReadMemoire,text="Lire",bd=2, relief=RAISED, overrelief=RIDGE, bg='#C0C0C0')
        self.boutonReadCaseMemoire.grid(padx=2, pady=2, row=1 ,column=2)



        #--------------------------------------------------------------------------
        # Section Ecriture vers le smoke
        #---------------------------------------------------------------------------
        self.fWrite = Frame(self.ZonePrincipale, width=400, height=200, bg='white')
        self.fWrite.grid_propagate(0)
        self.fWrite.grid(padx=2, pady=2, row=1 ,column=0)

        self.label_fWrite=LabelFrame(self.fWrite,text="Ecriture", fg="#03224C", font=('Helvetica', 20), bg='white')
        self.label_fWrite.pack_propagate(0)
        self.label_fWrite.pack(side=TOP)

        self.EntryUpdatePN=Entry(self.label_fWrite, font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryUpdatePN.grid(padx=2, pady=2, row=0 ,column=0)

        self.EntryUpdateSN=Entry(self.label_fWrite, font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryUpdateSN.grid(padx=2, pady=2, row=0 ,column=1)

        self.EntryUpdateDate=Entry(self.label_fWrite, font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryUpdateDate.grid(padx=2, pady=2, row=0 ,column=2)

        self.boutonWritePN=Button(self.label_fWrite,text='Modifier PN',bd=2, relief=RAISED,  overrelief=RIDGE, bg='#C0C0C0')
        self.boutonWritePN.grid(padx=2, pady=2, row=1 ,column=0)

        self.boutonWriteSN=Button(self.label_fWrite,text='Modifier SN',bd=2, relief=RAISED,  overrelief=RIDGE, bg='#C0C0C0')
        self.boutonWriteSN.grid(padx=2, pady=2, row=1 ,column=1)
        
        self.boutonWriteDate=Button(self.label_fWrite,text='Modifier Date ',bd=2, relief=RAISED,  overrelief=RIDGE, bg='#C0C0C0')
        self.boutonWriteDate.grid(padx=2, pady=2, row=1 ,column=2)

        self.boutonRecupCRCMEP=Button(self.label_fWrite,text='Charger MEP CRC',bd=2, relief=RAISED,  overrelief=RIDGE, bg='#C0C0C0')
        self.boutonRecupCRCMEP.grid(padx=2, pady=2, row=2 ,column=0)

        self.EntryRecupCRCMEP=Entry(self.label_fWrite,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryRecupCRCMEP.grid(padx=2, pady=2, row=2 ,column=1)

        self.boutonWriteCRCMEP=Button(self.label_fWrite,text='Écrire MEP CRC',bd=2, relief=RAISED,  overrelief=RIDGE, bg='#C0C0C0')
        self.boutonWriteCRCMEP.grid(padx=2,pady=2, row=2 ,column=2)

        self.fWriteMemoire = Frame(self.label_fWrite, bg='white')
        self.fWriteMemoire.grid_propagate(0)
        self.fWriteMemoire.grid(padx=2, pady=2, row=6 ,column=0, columnspan=3)

        self.label_fWriteMemoire=LabelFrame(self.fWriteMemoire,text="Écrire en case mémoire", fg="#03224C", font=('Helvetica', 20), bg='white')
        self.label_fWriteMemoire.pack_propagate(0)
        self.label_fWriteMemoire.pack(side=TOP)

        self.labelWriteCaseMemoire=Label(self.label_fWriteMemoire,text="Adresse Mémoire", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelWriteCaseMemoire.grid(padx=2, pady=2, row=0 ,column=0)

        self.labelWriteDatas=Label(self.label_fWriteMemoire,text="Données ", fg="#03224C", font=('Helvetica', self.taille_police), bg='white')
        self.labelWriteDatas.grid(padx=2, pady=2, row=0 ,column=1)

        self.EntryWriteCaseMemoire=Entry(self.label_fWriteMemoire,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryWriteCaseMemoire.grid(padx=2, row=1,column=0)

        self.EntryWriteDatas=Entry(self.label_fWriteMemoire,  font=('Helvetica', self.taille_police), bg='white', width=self.taille_entry)
        self.EntryWriteDatas.grid(padx=2, row=1 ,column=1)

        self.boutonWriteCaseMemoire=Button(self.label_fWriteMemoire,text="Lire",bd=2, relief=RAISED, overrelief=RIDGE, bg='#C0C0C0')
        self.boutonWriteCaseMemoire.grid(padx=2, pady=2, row=1 ,column=2)
        
        # on initialise le terminal
        self.initialiser_terminal()

        #--------------------------------------------------------------------------
        # Terminal pour afficher les trames
        #---------------------------------------------------------------------------
    def initialiser_terminal(self):
        self.fTerminal = Frame(self.ZonePrincipale, width=300, height=300, bg='white')
        self.fTerminal.grid_propagate(0)
        self.fTerminal.grid(padx=2, pady=2, row=0, column=1,rowspan=3)

        self.label_fTerminal=LabelFrame(self.fTerminal,text="Terminal", fg="#03224C", font=('Helvetica', 20), bg='white')
        #self.label_fTerminal.pack_propagate(0)
        self.label_fTerminal.pack(side=TOP)
       
        self.terminal=Canvas(self.label_fTerminal, width=450, height=300, bg='white', relief=SUNKEN)
        self.terminal.pack(fill=BOTH)
        
        

        #--------------------------------------------------------------------------
        # Zone des boutons optionnels
        #--------------------------------------------------------------------------
        
        self.boutonClear=Button(self.fTerminal,text="Effacer",bd=2, relief=RAISED, overrelief=RIDGE, bg='#C0C0C0', command=self.effacer_terminal)
        self.boutonClear.pack(padx=2, pady=2)

        #######################################################################

    def effacer_terminal(self):
        for widget in self.label_fTerminal.winfo_children():
            widget.destroy()

    def effacer_zone_lecture(self):
        self.EntryPN.delete(0,END)
        self.EntrySN.delete(0,END)
        self.EntryDate.delete(0,END)
        self.EntryCRCMEP.delete(0,END)
        self.EntryCRCBBP.delete(0,END)
        self.EntryLRU.delete(0,END)

    def read_config(self):
        self.effacer_terminal()
        self.effacer_zone_lecture()
        self.trame= Trame()
        # on affiche les logs
        self.log = Terminal(fenetre_principale=self.label_fTerminal)
        self.app =  DisplayLogs(self.log)

        # on récupère les valeurs du PN,SN...
        self.PN = self.trame.valeurs_config("trame.txt")[0]
        self.SN = self.trame.valeurs_config("trame.txt")[1]
        self.Date_Fab = self.trame.valeurs_config("trame.txt")[2]
        self.CRC_MEP = self.trame.valeurs_config("trame.txt")[3]
        self.CRC_BBP = self.trame.valeurs_config("trame.txt")[4]

        # On affiche ces valeurs dans les cases prévues
        self.EntryPN.delete(0,END)
        self.EntryPN.insert(0,self.PN)

        self.EntrySN.delete(0,END)
        self.EntrySN.insert(0,self.SN)

        self.EntryDate.delete(0,END)
        self.EntryDate.insert(0,self.Date_Fab)

        self.EntryCRCMEP.delete(0,END)
        self.EntryCRCMEP.insert(0,self.CRC_MEP)

        self.EntryCRCBBP.delete(0,END)
        self.EntryCRCBBP.insert(0,self.CRC_BBP)

    def effacer(self):
        for widget in self.winfo_children():
            widget.destroy()

    def style(self):
        for widget in self.winfo_children():
            widget.configure(bg='white')
        

##############################################################################

if __name__ == '__main__':
    Sdm = SDM()
    Sdm.mainloop()
