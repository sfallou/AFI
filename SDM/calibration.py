# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import ttk
import tkFileDialog
import ics
from read_nvm import *
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
    
# la classe Calibration
class Calibration(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
	self.fenP = fenetre_principale
	self.fenP.protocol("WM_DELETE_WINDOW", self.quit)
	# center window
	#self.fenP.eval('tk::PlaceWindow %s center' % self.fenP.winfo_pathname(self.fenP.winfo_id()))
        self.pack()
	self.configure(bg=bgColor)
	
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
        self.boutonStartCalib.pack(pady=5)
	
	# Zone de Text pour les consignes à appliqué
	self.frame0 = Frame(self.fenetre1,bg=bgColor) # sert à bien arranger les widgets de cette zone
	self.frame0.pack(pady=5)
	self.labelConsigne = Label(self.frame0,text="Consignes", fg=fgColor, font=titreFont, bg=bgColor)
        self.labelConsigne.grid(row=0,column=0)
	self.textConsigne = Text(self.frame0, height=20, width=50,font=("consolas",10))
	self.textConsigne.grid(row=1,column=0)
	# le scrollbar 
	self.scrollbar = Scrollbar(self.frame0, command=self.textConsigne.yview)
	self.scrollbar.grid(row=1,column=1,sticky="nsew")
	self.textConsigne['yscrollcommand'] = self.scrollbar.set
	
	# 
	self.boutonContinuer=Button(self.fenetre1,text="Continuer",bd=2, width=30, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.start_calib)
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
        self.Top.grid(padx=2,pady=2, row=0 ,column=1)
	Label(self.frame1_1,text="Bottom", fg=fgColor, font=fontSimple, bg=bgColor).grid(padx=2,pady=2,row=1,column=0)
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
	
	# Bouton Charger qui permet d'ouvir la clé et de lire le contenu du smoke
	self.boutonLoad=Button(self.fenetre2,text="CALIBRER",bd=2, width=50, relief=RAISED, overrelief=RIDGE, bg=buttonColor, command=self.start_calib)
        self.boutonLoad.pack(pady=5, side=TOP)
	
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
	# La barre de progression
	self.progressBar = ttk.Progressbar(self.frame10,orient="horizontal",length=500,mode="determinate")
	self.progressBar.grid(pady=2,row=3,column=0)
	
	self.frame20 = Frame(self.fenetre2,bg=bgColor) # sert à bien arranger les labels et les entry pn, sn ...
	self.frame20.pack(pady=5)
	# On crée les 2 canvas qui vont contenir les graphes
	self.canvas1 = Canvas(self.frame20, width=320,heigh=200, bg="white", bd=0, highlightthickness=2)
	self.canvas1.grid(padx=2,pady=2,row=0,column=0)
	self.canvas2 = Canvas(self.frame20, width=320,heigh=200, bg="white",  bd=0, highlightthickness=2)
	self.canvas2.grid(padx=2,pady=2,row=0,column=1)

    def start_calib(self):
	pass
    
##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    calibration = Calibration(fenetre_principale=root)
    calibration.mainloop()
    
    
