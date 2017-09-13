# -*-coding:Utf-8 -*

from tkMessageBox import *
import Tkinter as tk
import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys
import os


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##############################################
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

#valeurs globals pour gérer le graphe 
valeurTop = 0
valeurSmokeP = 0
valeurConcentration = 0
xdata, ydata, concData = [], [], []
#valeurs globals pour gérer le tableau
arraySmokeP = []
arrayConcen = []
Tops = []
Bottoms = []
smkP = []
conc = []
# Les types de notifications
notif1 = ["Test de fumée Terminé!\n","Les résultats sont affichés dans le tableau suivant.\nVeuillez vider complètement la fumée avant\nde calibrer si nécessaire."]
notif2 = ["Données insuffisantes!\n","Pas assez d'acquisitions pour calculer\nconvenablement les valeurs moyennes.\nVeuillez remettre de la fumée"]		
notif3 = ["Données suffisantes!\n","Vous pouvez vider doucement la fumée"]

# Les flags
flag_terminal_log = 1
flag_calib = 0
flag_calib_log = 1
#####################################################
class TerminalLog(threading.Thread):
    def __init__(self,interface,terminal,leds,pots,backgrounds,top,bottom,smokeP,concen,widgets,Boutoncalib,Boutonclear,zoneNotifs,count):
        threading.Thread.__init__(self)
        self.interface = interface
	self.terminal = terminal
	self.leds = leds
	self.pots = pots
	self.bgcks = backgrounds
	self.top = top
	self.bottom = bottom
	self.smokeP = smokeP
	self.concen = concen
	self.widgets = widgets
	self.BoutonCalib = Boutoncalib
	self.BoutonClear = Boutonclear
	self.zoneNotifs = zoneNotifs
	self.EntryCount = count
	
	
	
    def run(self):
	global arraySmokeP, arrayConcen, smkP, conc, flag_terminal_log
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
	# apparence des notifs
	self.zoneNotifs.tag_configure("Error",font=('Helvetica', 12, 'bold'), foreground='red')
	self.zoneNotifs.tag_configure("Ready",font=('Helvetica', 12, 'bold'), foreground='blue')
	self.zoneNotifs.tag_configure("Finish",font=('Helvetica', 12, 'bold'), foreground='green')
	#self.flag = 1
        while flag_terminal_log:
            message = bus.recv()
            if message is None:
                break   
            else :		
                print(message)
                info = str(message)+"\n"
		if info[36:44] == "00400103":
		    try:
			self.clignotant(info[65:67])
			self.parametres(info)
			self.terminal.insert('0.0', info)
		    except:
			pass
		    
		elif info[36:44] == "0611e103":
		    print(message)
		    for i in range(4):
			self.pots[i].delete(0,tk.END)
		    self.pots[0].insert(0,info[68:70])
		    self.pots[1].insert(0,info[71:73])
		    self.pots[2].insert(0,info[74:76])
		    self.pots[3].insert(0,info[77:79])
		
		elif info[36:44] == "06121d03":
		   
		    for i in range(4):
			self.bgcks[i].delete(0,tk.END)
		    val1 = info[65:70].replace(" ","").lstrip("0")
		    val2 = info[71:76].replace(" ","").lstrip("0")
		    val3 = info[77:82].replace(" ","").lstrip("0")
		    val4 = info[83:88].replace(" ","").lstrip("0")
		    if val3 == '':
			val3 = '0'
		    if val4 == '':
			val4 = '0'
		    self.bgcks[0].insert(0,val1)
		    self.bgcks[1].insert(0,val2)
		    self.bgcks[2].insert(0,val3)
		    self.bgcks[3].insert(0,val4)
		    
		"""
		elif info[36:44] == "06125903":
		    self.SN = info[65:88].replace(" ","").decode("hex")
		    
		elif info[36:44] == "06107903":
		    self.PN = info[65:76].replace(" ","")
		
		"""
		
		
	
		
    def parametres(self,msg):
	global Tops, Bottoms, flag_calib
	top = float(int(msg[77:82].replace(" ",""),16))/float(204)
	bottom = float(int(msg[83:88].replace(" ",""),16))/float(204)
	smokeP = top/bottom
	self.top.delete(0,tk.END)
	self.bottom.delete(0,tk.END)
	self.smokeP.delete(0,tk.END)
	self.top.insert(0,round(top,3))
	self.bottom.insert(0,round(bottom,3))
	self.smokeP.insert(0,round(smokeP,3))
	if flag_calib == 1 and self.concen.get() == '1.2':
	    #if flag_calib == 1:
	    if len(Tops) < 20:
		Tops.append(round(top,3))
		Bottoms.append(round(bottom,3))
    
	print ("Tops: ", len(Tops))
	
    def clignotant(self, val):
	global arraySmokeP, arrayConcen, smkP, conc, concData, notif1,notif1,notif3
	val =  '{0:08b}'.format(int(val,16))[::-1]
	if val[0] == '0':
	    self.leds[0].create_oval(0,0,15,15, fill="grey")
	if val[0] == '1':
	    self.leds[0].create_oval(0,0,15,15, fill="green2")
	if val[1] == '0':
	    self.leds[1].create_oval(0,0,15,15, fill="grey")
	if val[1] == '1':
	    self.leds[1].create_oval(0,0,15,15, fill="green2")
	if val[2] == '0':
	    self.leds[2].create_oval(0,0,15,15, fill="grey")
	if val[2] == '1':
	    self.leds[2].create_oval(0,0,15,15, fill="green2")
	if val[3] == '0':
	    self.leds[3].create_oval(0,0,15,15, fill="grey")
	if val[3] == '1':
	    sel.leds[3].create_oval(0,0,15,15, fill="green2")
	if val[4] == '0':
	    self.leds[4].create_oval(0,0,15,15, fill="grey")
	if val[4] == '1':
	    self.leds[4].create_oval(0,0,15,15, fill="green2")
	    
	if val[5] == '0':
	    self.leds[5].create_oval(0,0,15,15, fill="grey")
	if val[5] == '1':
	    self.leds[5].create_oval(0,0,15,15, fill="green2")
	    
	if val[6] == '0':
	    self.leds[6].create_oval(0,0,15,15, fill="grey")
	    if len(arraySmokeP) == 1:
		# on récupere la concentration et la valeur du smoke P pour Alarm Lav OFF
		arraySmokeP.append(float(self.smokeP.get()))
		val = self.concen.get()
		if val == '':
		    val = concData[-1]
		arrayConcen.append(val)
		# On affiche les valeurs
		self.widgets[2][1].configure(text=str(arraySmokeP[1]))
		self.widgets[2][2].configure(text=str(arrayConcen[1]))
		
		if len(smkP) >= 30 :
		    #self.flag = 0
		    # On ajoute les valeurs moyennes
		    arraySmokeP.append(round(np.mean(smkP),3))
		    arrayConcen.append(round(np.mean(conc),3))
		    # On ajoute les valeurs Max
		    arraySmokeP.append(round(np.max(smkP),3))
		    arrayConcen.append(round(np.max(conc),3))
		    # On ajoute les valeurs min
		    arraySmokeP.append(round(np.min(smkP),3))
		    arrayConcen.append(round(np.min(conc),3))
		    
		    # On affiche les resultats dans le tableau
		   
		    self.widgets[3][1].configure(text=str(arraySmokeP[2]))
		    self.widgets[4][1].configure(text=str(arraySmokeP[3]))
		    self.widgets[5][1].configure(text=str(arraySmokeP[4]))
		    		    
		    self.widgets[3][2].configure(text=str(arrayConcen[2]))
		    self.widgets[4][2].configure(text=str(arrayConcen[3]))
		    self.widgets[5][2].configure(text=str(arrayConcen[4]))
		    # On active le bouton calibrer
		    self.BoutonCalib.configure(state='normal')
		    # On active le bouton clear
		    self.BoutonClear.configure(state='normal')
		    # on affiche une notification
		    self.zoneNotifs.delete(0.0,tk.END)
		    self.zoneNotifs.insert(tk.INSERT,notif1[0])
		    self.zoneNotifs.insert(tk.INSERT,notif1[1])
		    self.zoneNotifs.tag_add("Finish",0.0,tk.END)
		else:
		    # on affiche une notification
		    self.zoneNotifs.delete(0.0,tk.END)
		    self.zoneNotifs.insert(tk.INSERT,notif2[0])
		    self.zoneNotifs.insert(tk.INSERT,notif2[1])
		    self.zoneNotifs.tag_add("Error",0.0,tk.END)
		    # On enlève la derniere valeur de arraySmokeP pour n'avoir que len(arraySmokeP) = 1
		    del arraySmokeP[-1]
		    # On efface les valeurs du tableau
		    self.widgets[2][1].configure(text="")
		    self.widgets[2][2].configure(text="")
		    
	if val[6] == '1':
	    self.leds[6].create_oval(0,0,15,15, fill="green2")
	    #self.flag = 0
	    val1 = self.smokeP.get()
	    val2 = self.concen.get()
	    val_conc = concData[-1]
	    if len(arraySmokeP) == 0:
		# on récupere la concentration et la valeur du smoke P pour Alarm Lav ON
		arraySmokeP.append(float(val1))
		if val2 != '':
		    val_conc = val2
		arrayConcen.append(val_conc)
		# On affiche les resultats dans le tableau
		self.widgets[1][1].configure(text=str(arraySmokeP[0]))
		self.widgets[1][2].configure(text=str(arrayConcen[0]))
		# On active le bouton calibrer
		#self.BoutonCalib.configure(state='normal')
		#if val_conc < 1 or val_conc > 1.4:
		    
		
	    
	    if val2 != '' and  abs(float(val2)-float(arrayConcen[0])) <= 0.2:
		conc.append(float(val2))
		smkP.append(float(val1))
		if len(smkP) == 30 :
		    # on affiche une notification
		    self.zoneNotifs.delete(0.0,tk.END)
		    self.zoneNotifs.insert(tk.INSERT,notif3[0])
		    self.zoneNotifs.insert(tk.INSERT,notif3[1])
		    self.zoneNotifs.tag_add("Ready",0.0,tk.END)
		    
	    
	if val[7] == '0':
	    self.leds[7].create_oval(0,0,15,15, fill="grey")
	if val[7] == '1':
	    self.leds[7].create_oval(0,0,15,15, fill="green2")
	    
	self.EntryCount.delete(0,tk.END)
	self.EntryCount.insert(tk.INSERT,len(conc))
    
   
	
    def stop(self):
	flag_terminal_log = 0


####################################################################################
# Cette classe dénommée AjustementPotars est le thread qui va faire le calibrage 
# Il prend en arguments :
    # concen: le champs qui affiche la concentration de fumée
    # potars : une liste contenant les 4 champs qui affichent les potars
    # top: le champ qui affiche la valeur de Top
    # bottom : le champ qui affiche la valeur de bottom
    # progressBar : la barre de progression qui signale le déroulement du programme
    # zoneNotif : La zone de text oû l'on affiche les différentes notification
    # waitZone : le champ de text qui va afficher "Calibration en cours ..."
    # boutonCal : le bouton Calibrer ( c'est pour l'activer ou le desactiver aux moments opportuns)
# Cette classe tourne en boucle dès qu'elle est lancée
###################################################################################
class AjustementPotars(threading.Thread):
    def __init__(self,concen,potars,top,bottom,progressBar,zoneNotif, waitZone,boutonCal):
        threading.Thread.__init__(self)
        self.concentration = concen
	self.POTs = potars
	self.EntryTop = top
	self.EntryBottom = bottom
	self.progressBar = progressBar
	self.zoneNotifs = zoneNotif
	self.waitZone = waitZone
	self.boutonCalibrer = boutonCal
	self.flag = 1 # ce flag servira de condition de test lors des differentes phases de la calibration
	
    def run(self):
	global flag_calib_log, flag_calib, Tops, Bottoms # ce sont des variables globales qui sont partagées par toutes les classes
	self.ok = 0 # une sorte de flag qui permet de vérifier si la calibration est terminée ou pas
	self.objetAnnexe = Annexes() # un objet de la classe Annexe qui va nous servir réaliser des opérations répétitives
	# Tant que flag_calib_log vaut 1 (ce qui est toujours le cas lorsqu'on démarre le test de fumée), la boucle tourne 
	while flag_calib_log:
	    if flag_calib: # si on est en mode calibration
		self.progressBar.start() # On démarre la barre de progression
		self.waitZone.configure(text="Calibration en Cours....") #on affiche aussi l'indication que la calib est en ccours
		if len(Tops) < 20: # Si on a acquis moins de 20 valeurs de Top et bottom, on fait rien mais ces acquisitions continuent de se faire
		    pass
		else: # sinon, c-a-d qu'on a assez de valeurs pour choisir le bon Top et le bon Bottom
		    self.calibration() # on appelle la fonction calibration qui sert principalement à ajuster les potars
		    if self.ok:      # si l'ajustement est bonne, on arrête d'ajuster et on écrit les valeurs de potars obtenues
			#On fait set clear clear zero en s'assurant qu'il n'y ait plus de fumée
			valConf = self.concentration.get()
			if valConf != '':
			    if abs(float(valConf)) == 0.1 or abs(float(valConf)) == 0:
				print "OK"
				potars = []
				for p in self.POTs:
				    potars.append(int(p.get(),16))
				self.objetAnnexe.set_potars(potars)
				self.objetAnnexe.get_potars()
				self.stop()
				time.sleep(5)
				# On réactive le bouton
				self.boutonCalibrer.configure(state='normal')
				# on affiche une notification
				self.zoneNotifs.delete(0.0,tk.END)
				self.zoneNotifs.insert(tk.INSERT,"Calibration terminée !")
				self.zoneNotifs.tag_add("Error",0.0,tk.END)
				
			    else:
				#print("Videz complètement la fumée !")
				# on affiche une notification
				self.zoneNotifs.delete(0.0,tk.END)
				self.zoneNotifs.insert(tk.INSERT,"Videz complètement la fumée !")
				self.zoneNotifs.tag_add("Ready",0.0,tk.END)
		    
    ### la fonction qui calcul les tops et bottoms souhaités et ajuste les potars 
    
    def calibration(self,):
	global flag_calib, Tops, Bottoms
	# si alarm_Lav_on supérieur ou égale à 2, on est dans le cas des smokes peu sensibles
	#on fixe les paramètres qui vont permettre de calculer convenablement les valeurs de top et bottom voulus
	if float(arrayConcen[0]) >= 2:
	    k = 10
	    coef1 = 1.3
	    coef2 = 6.5
	# Sinon, on est dans le cas des smokes très sensibles et on changes les paramètres 
	else:
	    k = 5
	    coef1 =  (0.15)/(0.3)#(0.1)/(0.3)
	    coef2 = (0.25)/(0.03)
	# on récupère les valeurs de top et de bottom les plus récurrentes lorsque la concentration=1.2 et les potars 19-19-32-14
	top_prim = float(max(set(Tops),key=Tops.count))
	bottom_prim = float(max(set(Bottoms),key=Bottoms.count))
	# On calcule les valeurs de top et bottom voulues pendant la calibration
	bottom_second = round(bottom_prim + coef2 * (0.1 - bottom_prim),3)
	top_second = round(top_prim + coef1*(0.6 - top_prim),3)
	# On définit les messages qu'on va afficher pour informer l'opérateur
	msg0 = "\nTop prévu après la calibration : "+str(top_second)+" +/- 0.05"
	msg1 = "\nBottom prévu après la calibration : "+str(bottom_second)+" +/- 0.005"
	msg2 = "\n----------"
	msg3 = "\nTop avant calibration : "+str(top_prim)
	msg4 = "\nBottom  avant calibration : "+str(bottom_prim)
	###
	# on affiche une notification
	if not self.ok: 
	    self.zoneNotifs.delete(0.0,tk.END)
	    self.zoneNotifs.insert(tk.INSERT,"Maintenez la concentration de fumée à 1.2 jusqu'à la fin de la calib\n")
	    self.zoneNotifs.insert(tk.INSERT,msg0)
	    self.zoneNotifs.insert(tk.INSERT,msg1)
	    self.zoneNotifs.insert(tk.INSERT,msg2)
	    self.zoneNotifs.insert(tk.INSERT,msg3)
	    self.zoneNotifs.insert(tk.INSERT,msg4)
	    self.zoneNotifs.tag_add("Done",0.0,tk.END)
	    self.top_voulu = top_second
	    self.bottom_voulu = bottom_second
	try:
	    if self.flag: # si ce flag vaut 1 (vrai pour le premier tour de boucle), on définit les potars de départ et on fait "set"
		self.pot0 = 20 * float(arrayConcen[0]) + k
		self.pot0 = int(str(int(self.pot0)),16)
		self.pot1 = self.pot0
		potars = [self.pot0,self.pot1,0x32,0x14]
		self.set_potars(potars)
		self.flag = 0 # permet de ne plus revenir sur le if précédent
		time.sleep(5)
	    
	    # On récupère la valeur de top et de bottom
	    val1 = self.EntryTop.get() 
	    val2 = self.EntryBottom.get()
	    val3 = self.concentration.get()
	    
	    if val3 =='1.2' and val1 !='' and val2!='':
		# Potars durants la calibration
		potars = []
		for p in self.POTs:
		    potars.append(int(p.get(),16))
		print potars
		valTop = float(val1)
		valBottom = float(val2)
	
		# On règle l'ajustement des potars
		if valBottom < self.bottom_voulu and (self.bottom_voulu - valBottom) > 0.005:
		    if potars[2] < 0x96:
			potars[2] += 1
		    else:
			if potars[0] < 0xA0:
			    potars[0] += 1
			else:
			    potars[0] = self.pot0
			    potars[2] = 0x32
		
		elif valBottom > self.bottom_voulu and (valBottom - self.bottom_voulu) > 0.005:
		    if potars[2] > 0x32:
			potars[2] -= 1
		    else:
			if potars[0] > 0x19:
			    potars[0] -= 1
			else:
			    potars[0] = self.pot0
			    potars[2] = 0x32
			    
		elif valTop < self.top_voulu and (self.top_voulu - valTop) > 0.05:
		    if potars[3] < 0x5A:
			potars[3] += 1
			    
		    else:
			if potars[1] < 0xA0:
			    potars[1] += 1
			else:
			    potars[1] = self.pot1
			    potars[3] = 0x14
			    
		elif valTop > self.top_voulu and (valTop - self.top_voulu) > 0.05:
		    if potars[1] > 0x19:
			potars[1] -= 1
		    else:
			if potars[3] > 0x14:
			    potars[3] -= 1
			else:
			    potars[1] = self.pot1
			    potars[3] = 0x14
	    
		else:
		    self.ok = 1 # c'est à dire que l'ajustement est fini
		    
		#set potars
		self.set_potars(potars)
		
	except:
	    pass
	time.sleep(1)
    
    # la fonction qui permet d'écrire les potars (set uniquement)
    def set_potars(self,potars):
	bus = can.interface.Bus()
	msg1 = can.Message(arbitration_id=0x06103403,
		data=[0x17, 0x0e, potars[0], potars[1], potars[2], potars[3], 0x00, 0x00],
		extended_id=True)
	bus.send(msg1)
	time.sleep(0.5)
	# on demande la valeur des potars
	msg = can.Message(arbitration_id=0x06103403,
		data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
		extended_id=True)
	bus.send(msg)
	
    # La fonction qui donne le départ de la calibration. C'est elle qui est appelée par le bouton calibrer
    def set_flag(self):
	global flag_calib
	flag_calib = 1
	self.flag = 1
    # La fonction qui permet d'arrêter l'ajustement et le calibrage
    def stop(self):
	global flag_calib
	self.ok = 0
	flag_calib = 0
	#self.flag = 0
	self.progressBar.stop()
	self.waitZone.configure(text="")
	
##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,concen):
        threading.Thread.__init__(self)
        self.concentration = concen
	

    def run(self):
	global flag_calib_log
	# On calcule le Zero de reference reading en determinant la constante de l'équation
	os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 500 -t 1 -v | tee tmp.txt > tmp3.txt ')
	file = open("tmp.txt","rb")
	resultat = file.readlines()[6:]
	resultat = np.mean(map(self.formater,resultat))
	self.k = round(resultat,4)
	file.close()
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	
	# on demande la valeur des backgrounds
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	
	# On demande la valeur des PN et SN
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
		    data=[0x03, 0x00, 0x00, 0x00, 0xff, 0x7f, 0x00, 0x00],
		    extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	    
       
	while flag_calib_log:
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 500 -t 1 -v | tee tmp.txt > tmp2.txt')
	    file = open("tmp.txt","rb")
	    resultat = file.readlines()[6:]
	    resultat = np.mean(map(self.formater,resultat))
	    file.close()
	    self.concentration.delete(0,tk.END)
	    y = round(resultat,4)
	    self.x = round(-(y-self.k)/0.0257,1)
	    self.concentration.insert(0,self.x)
	    
    def stop(self):
	flag_calib_log = 0
    	
    def formater(self,a):
	return float(a.replace(",",""))
################################################
class MonGraphe2(tk.Frame):
    def __init__(self,smkP,conc,fenetre_principale=None):
        tk.Frame.__init__(self)
	self.fenP = fenetre_principale
	self.fenSmokeP = smkP
	self.fenConc = conc
	self.configure(bg=bgColor)
	
	self.fig = plt.Figure(figsize=(7, 3)) 
	self.ax = self.fig.add_subplot(111)
    
	self.canvas = FigureCanvasTkAgg(self.fig, master=self.fenP)
	self.canvas.get_tk_widget().pack()
	
	self.lineSmoke, = self.ax.plot([], [], 'r', lw=1)
	self.lineConc, = self.ax.plot([], [], 'b', lw=1)
	self.ax.grid()
	self.ax.legend(["SmokeP","Concen"], loc="best", frameon=False, labelspacing=0)
	#self.xdata, self.ydata, self.concData = [], [], []
	self.ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, blit=False, interval=10,
                              repeat=False, init_func=self.init)

    def data_gen(self,t=0):
	global valeurSmokeP, valeurConcentration
	while 1:
	    t += 0.1
	    try:
		if self.fenSmokeP.get():
		    valeurSmokeP = float(self.fenSmokeP.get())
		if self.fenConc.get() and self.fenConc.get() != "INF":
		    valeurConcentration = float(self.fenConc.get())
		yield t, valeurSmokeP, valeurConcentration
	    except:
		pass
	    
	    
	   


    def init(self):
	global xdata, ydata, concData
	self.ax.set_ylim(-1, 15)
	self.ax.set_xlim(0, 10)
	del xdata[:]
	del ydata[:]
	del concData[:]
	self.lineSmoke.set_data(xdata, ydata)
	self.lineConc.set_data(xdata, concData)
	return self.lineSmoke,self.lineConc,


    def run(self,data):
	global xdata, ydata, concData
	# update the data
	t, y, conc = data
	xdata.append(t)
	ydata.append(y)
	concData.append(conc)
	self.xmin, self.xmax = self.ax.get_xlim()
	self.ymin, self.ymax = self.ax.get_ylim()

	if t >= self.xmax:
	    self.ax.set_xlim(self.xmin, 2*self.xmax)
	    self.ax.figure.canvas.draw()
	if y >= self.ymax:
	    self.ax.set_ylim(self.ymin, 2*self.ymax)
	    self.ax.figure.canvas.draw()
	if self.ymax >= 20 and y <= 15:
	    self.ax.set_ylim(self.ymin, 15)
	    self.ax.figure.canvas.draw()
	self.lineSmoke.set_data(xdata, ydata)
	self.lineConc.set_data(xdata, concData)
	

	#print ("Concen:",concData)
	return self.lineSmoke,self.lineConc,

###################################################
class Annexes:
    def __init__(self):
	self.var = "OK"
	
    def clear(self):
	global arraySmokeP, arrayConcen, smkP, conc
	
	# On reinitialise les listes à 0
	smkP = []
	conc = []
	arraySmokeP = []
	arrayConcen = []
	xdata = []
	ydata = []
	concData = []
	
    def get_potars(self):
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	
	# on demande la valeur des backgrounds
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
    
    def set_potars(self,pots):
	bus = can.interface.Bus()
	#set
	msg1 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x00, 0x00],
                      extended_id=True)
	#clear
	msg2 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x01, 0x01],
                      extended_id=True)
	
	#Zero
	msg4 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x00, 0x01],
                      extended_id=True)
	try:
	    bus.send(msg1)
	    time.sleep(0.5)
	    bus.send(msg2)
	    time.sleep(0.5)
	    bus.send(msg2)
	    time.sleep(0.5)
	    bus.send(msg4)
	except can.CanError:
	    print("Message NOT sent")
#########################################################
if __name__ == "__main__":
    #app = ExampleApp()
    #app.mainloop()
    root = tk.Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    #graphe = MonGraphe(fenetre_principale=root)
    #graphe.mainloop()
 
