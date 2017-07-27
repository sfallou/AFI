# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import ttk
import tkFileDialog
import ics
import can
from read_nvm import *
from subprocess import Popen, PIPE
import os
import time                    ## Time-related library
import datetime
import data
import classes
#---------Imports for graphe
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports

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
    
# la classe Calibration
class Calibration(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.fenP = fenetre_principale
	self.fenP.protocol("WM_DELETE_WINDOW", self.quit)
	# center window
	#self.fenP.eval('tk::PlaceWindow %s center' % self.fenP.winfo_pathname(self.fenP.winfo_id()))
        #self.pack()
	self.configure(bg=bgColor)
	
	# Les autres attributs
	self.fig1 = plt.Figure()
	self.fig2 = plt.Figure()
	self.xdata_1, self.ydata_1 = [], []
	

	# Les différentes zone de l'interface initialisées au démarrage
	self.init_interface()
	
    def init_interface(self):
	#création des  fenêtres
	self.fenetre1 = Frame(self,bg=bgColor,borderwidth=tailleBorder,relief=GROOVE)
	self.fenetre1.grid(padx=2,pady=2,row=0,column=0)
	self.fenetre1_ = Frame(self,bg=bgColor,borderwidth=tailleBorder,relief=GROOVE)
	self.fenetre1_.grid(padx=2,pady=2,row=1,column=0,sticky="n",)
	self.fenetre2 = Frame(self,bg=bgColor,borderwidth=tailleBorder,relief=GROOVE)
	self.fenetre2.grid(padx=2,pady=2,row=0,column=1,rowspan=2)
	
	# création des widgets de chaque fenêtre
	
	###### Fêntre 1 #########
	
	# 
	self.boutonStartCalib=Button(self.fenetre1,text="Démarrer la calibration",bd=2, width=50, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.start_calib)
        self.boutonStartCalib.pack(pady=2)
	
	# Zone de Text pour les consignes à appliqué
	self.frame0 = Frame(self.fenetre1,bg=bgColor) # sert à bien arranger les widgets de cette zone
	self.frame0.pack(pady=5)
	self.labelConsigne = Label(self.frame0,text="Consignes", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelConsigne.grid(row=0,column=0)
	self.textConsigne = Text(self.frame0, height=25, width=60,font=("consolas",10))
	self.textConsigne.grid(row=1,column=0)
	# le scrollbar 
	self.scrollbar = Scrollbar(self.frame0, command=self.textConsigne.yview)
	self.scrollbar.grid(row=1,column=1,sticky="nsew")
	self.textConsigne['yscrollcommand'] = self.scrollbar.set
	
	# 
	self.boutonContinuer=Button(self.fenetre1,text="Continuer",bd=2, width=30, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonContinuer.pack(pady=5)
	
	###### Fêntre 1_ #########
	self._widgets = []
	for row in range(5):
            current_row = []
            for column in range(3):
                label = Label(self.fenetre1_, borderwidth=0, width=15)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(3):
            self.grid_columnconfigure(column, weight=3)
	
	self._widgets[0][1].configure(text="Smoke P")
	self._widgets[0][2].configure(text="Concentration")
	self._widgets[1][0].configure(text="Pre-Alarm")
	self._widgets[2][0].configure(text="Alarm Low")
	self._widgets[3][0].configure(text="Alarm Lav")
	self._widgets[4][0].configure(text="Alarm Mid/High")
	
	###### Fêntre 2 #########
	self.frame1 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les widgets de cette zone
	self.frame1.pack(pady=5)
	self.frame1_1 = Frame(self.frame1,bg=bgColor,bd=1,relief=GROOVE) # sert à bien arranger les widgets de cette zone
	self.frame1_1.grid(row=0,column=0)
	self.frame1_2 = Frame(self.frame1,bg=bgColor,bd=1,relief=GROOVE) # sert à bien arranger les widgets de cette zone
	self.frame1_2.grid(row=0,column=1)
	self.frame1_3 = Frame(self.frame1,bg=bgColor,bd=1,relief=GROOVE) # sert à bien arranger les widgets de cette zone
	self.frame1_3.grid(row=0,column=2)
	#On affiche les valeurs principales
	Label(self.frame1_1,text="Top", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=0)
	self.Top=Entry(self.frame1_1, font=fontSimple, width=entryLength)
        self.Top.grid(padx=2,pady=2, row=1 ,column=0)
	Label(self.frame1_1,text="Bottom", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=1)
	self.Bottom=Entry(self.frame1_1, font=fontSimple, width=entryLength)
        self.Bottom.grid(padx=2,pady=2, row=1 ,column=1)
	Label(self.frame1_1,text="Smoke P", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=2,column=0)
	self.SmokeP=Entry(self.frame1_1, font=fontSimple, width=entryLength)
        self.SmokeP.grid(padx=2,pady=2, row=3 ,column=0)
	Label(self.frame1_1,text="Concentration", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=2,column=1)
	self.Concentration=Entry(self.frame1_1, font=fontSimple, width=entryLength)
        self.Concentration.grid(padx=2,pady=2, row=3 ,column=1)
	#On affiche les LEDs (Alarm Status)
	self.Led7 = Canvas(self.frame1_2, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led7.create_oval(0,0,15,15, fill="grey")
        self.Led7.grid(padx=2,pady=2, row=0 ,column=0)
	Label(self.frame1_2,text="Alarm Mid/High", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=1,sticky="nsew")
	
	self.Led6 = Canvas(self.frame1_2, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led6.create_oval(0,0,15,15, fill="grey")
        self.Led6.grid(padx=2,pady=2, row=1 ,column=0)
	Label(self.frame1_2,text="Lavatory Alarm", fg="red", font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=1,column=1,sticky="nsew")
	
	self.Led5 = Canvas(self.frame1_2, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led5.create_oval(0,0,15,15, fill="grey")
        self.Led5.grid(padx=2,pady=2, row=2 ,column=0)
	Label(self.frame1_2,text="Alarm Low", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=2,column=1,sticky="nsew")
	
	self.Led4 = Canvas(self.frame1_2, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led4.create_oval(0,0,15,15, fill="grey")
        self.Led4.grid(padx=2,pady=2, row=3 ,column=0)
	Label(self.frame1_2,text="Pre Alarm", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=3,column=1,sticky="nsew")
	
	self.Led3 = Canvas(self.frame1_3, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led3.create_oval(0,0,15,15, fill="grey")
        self.Led3.grid(padx=2,pady=2, row=0 ,column=0)
	Label(self.frame1_3,text="Temperature Alarm", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=1,sticky="nsew")
	
	self.Led2 = Canvas(self.frame1_3, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led2.create_oval(0,0,15,15, fill="grey")
        self.Led2.grid(padx=2,pady=2, row=1 ,column=0)
	Label(self.frame1_3,text="Event 1", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=1,column=1,sticky="nsew")
	
	self.Led1 = Canvas(self.frame1_3, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led1.create_oval(0,0,15,15, fill="grey")
        self.Led1.grid(padx=2,pady=2, row=2 ,column=0)
	Label(self.frame1_3,text="Event 2", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=2,column=1,sticky="nsew")
	
	self.Led0 = Canvas(self.frame1_3, width=20,heigh=18, bg=bgColor, bd=0, highlightthickness=0)
	self.Led0.create_oval(0,0,15,15, fill="grey")
        self.Led0.grid(padx=2,pady=2, row=3 ,column=0)
	Label(self.frame1_3,text="Babble", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=3,column=1,sticky="nsew")
	
	# Je mets les LEDs dans une liste ordonnées pour les controler ensemble
	self.Leds = [self.Led0,self.Led1,self.Led2,self.Led3,self.Led4,self.Led5,self.Led6,self.Led7]
	
	# Le bouton "reference Reading"
	self.boutonRefReading=Button(self.fenetre2,text="Reference Reading",bd=2, width=20, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.reference_reading)
        self.boutonRefReading.pack(pady=5)
	
	
	self.frame5 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les labels et les entry pn, sn ...
	self.frame5.pack(pady=5)
	
	#On affiche les potars
	Label(self.frame5,text="POT1", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=0)
	self.POT1=Entry(self.frame5, font=fontSimple, width=entryLength)
        self.POT1.grid(padx=2,pady=2, row=1 ,column=0)
	Label(self.frame5,text="POT2", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=1)
	self.POT2=Entry(self.frame5, font=fontSimple, width=entryLength)
        self.POT2.grid(padx=2,pady=2, row=1 ,column=1)
	Label(self.frame5,text="POT3", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=2)
	self.POT3=Entry(self.frame5, font=fontSimple, width=entryLength)
        self.POT3.grid(padx=2,pady=2, row=1 ,column=2)
	Label(self.frame5,text="POT4", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=0,column=3)
	self.POT4=Entry(self.frame5, font=fontSimple, width=entryLength)
        self.POT4.grid(padx=2,pady=2, row=1 ,column=3)
	# Je mets les POTs dans une liste ordonnées pour les controler ensemble
	self.POTs = [self.POT1,self.POT2,self.POT3,self.POT4]
	
	#####
	self.frame10 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les labels et les entry pn, sn ...
	self.frame10.pack(pady=5)
	# Zone de Text pour les logs
	self.labelLogs = Label(self.frame10,text="Logs", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelLogs.grid(row=0,column=0)
	self.textLogs = Text(self.frame10, height=5, width=80,font=("consolas",10))
	self.textLogs.grid(row=1,column=0)
	# le scrollbar
	self.scrollb = Scrollbar(self.frame10, command=self.textLogs.yview)
	self.scrollb.grid(row=1,column=1,sticky="nsew")
	self.textLogs['yscrollcommand'] = self.scrollb.set
	# Le bouton "horn cancel"
	self.boutonHorn=Button(self.frame10,text="Horn Cancel",bd=2, width=20, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.horn_cancel)
        self.boutonHorn.grid(pady=2,row=3,column=0)
	
	
	self.frame20 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les labels et les entry pn, sn ...
	self.frame20.pack(pady=5)
	# On crée les 2 canvas qui vont contenir les graphes
	self.canvas1 = Frame(self.frame20, width=630,heigh=250, bg="white",  bd=0, highlightthickness=2)
	self.canvas1.pack()
	#self.canvas1.grid(padx=2,pady=2,row=0,column=0)
	#self.canvas2 = Frame(self.frame20, width=370,heigh=250, bg="white",  bd=0, highlightthickness=2)
	#self.canvas2.grid(padx=2,pady=2,row=0,column=1)
	
	# Bouton calibrer
	self.boutonCalibrer=Button(self.fenetre2,text="CALIBRER",bd=2, width=60, relief=RAISED, overrelief=RIDGE, bg=buttonColor)
        self.boutonCalibrer.pack(pady=5, side=TOP)
	
    ########## On désactive les widgets avant le démarrage
	self.disable_fenetre(self.fenetre2)
	self.boutonContinuer.configure(state='disabled')
	
    #####################
    def start_calib(self):
	# On efface tout le contenu des fenêtres 
	self.clean_interface()
	# On affiche les consignes
	try:
	    #on ouvre consignes.txt et on l'affiche dans la zone de texte
	    chemin = "./docs/Calibration/"
	    consigne = open(os.path.join(chemin+"/consignes.txt"),"r")
	    for line in consigne:
		self.textConsigne.insert(INSERT, line)
	except Exception as error:
	    print(repr(error))
	
	# On réactive les widgets
	self.boutonContinuer.configure(state='normal', command=self.continuer_calib)
	self.enable_fenetre(self.fenetre2)
	# On desactive le bout
     #####################
    def continuer_calib(self):
	# on établit la connexion avec la clé
	res = self.open_dongle()
	# Si res = 1, on lance le test et on affiche les trames CAN dans la zone logs ainsi que la progressBar
	if res:
	    self.log0 = classes.TerminalLog('ics0can0',
			self.textLogs,
			self.Leds,
			self.POTs,
			self.Top,
			self.Bottom,
			self.SmokeP,
			self.Concentration,
			self._widgets)
	    self.log0.start()
	   
	    #self.graphe1 = classes.MonGraphe(self.Top,fenetre_principale=self.canvas1)
	    self.graphe2 = classes.MonGraphe2(self.SmokeP,self.Concentration,fenetre_principale=self.canvas1)
	    #self.graphe = classes.MonGraphe3(self.SmokeP,self.Top,fenetre_principale=self.canvas2)
	### On désactive le bouton
	self.boutonContinuer.configure(state='disabled')
	# On désactive le boutonCalibrer
	self.boutonCalibrer.configure(state='disabled')
	# On insert "INF" dans l'EntryConcentration
	self.Concentration.insert(0,"INF")
    #################
    def horn_cancel(self):
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x16, 0x00, 0x00, 0x00, 0xff, 0x7f, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
     #################
    def reference_reading(self):
	self.Concentration.delete(0,END)
	self.thread_conc = classes.CalibrationLog(self.Concentration)
	self.thread_conc.start()
	
	self.boutonRefReading.configure(state='disabled')
    #######################################################
    
    
    def disable_fenetre(self,widget,state='disabled'):
	try:
	    widget.configure(state=state)
	except TclError:
	    pass
	for child in widget.winfo_children():
	    self.disable_fenetre(child,state=state)
     #######################################################
    
    def enable_fenetre(self,widget,state='normal'):
	try:
	    widget.configure(state=state)
	except TclError:
	    pass
	for child in widget.winfo_children():
	    self.disable_fenetre(child,state=state)
    #######################################################
    def clean_interface(self):
	self.textLogs.delete('0.0',END)
	self.textConsigne.delete('0.0',END)
	"""self.canvas.create_oval(0,0,35,35, fill=self.couleurSignal2)
	self.canvas2.create_oval(0,0,35,35, fill=self.couleurSignal2)
	for child in self.entries:
	    child.delete(0,END)
	"""
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
	self.log0.stop()
	self.thread_conc.stop()
	# On arrete le processus setup
	try:
	    os.system('sudo pkill icsscand')
	except:
	    print ("impossible de fermer")
    ######################################################
    def quit(self):
	self.close_dongle()
	self.fenP.destroy()
	# On arrete le processus python
	try:
	    os.system('sudo pkill python')
	except:
	    print ("impossible d'arrêter python")
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    calibration = Calibration(fenetre_principale=root)
    #calibration.mainloop()
    
    
