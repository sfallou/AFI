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
            if message is not None:		
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
	    else:
		pass   
		
	
		
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
	"""if flag_calib == 1 and self.concen.get() == '1.2':
	    #if flag_calib == 1:
	    if len(Tops) < 20:
		Tops.append(round(top,3))
		Bottoms.append(round(bottom,3))
    
	print ("Tops: ", len(Tops))
	"""
    def clignotant(self, val):
	global arraySmokeP, arrayConcen, smkP, conc, concData, notif1,notif1,notif3
	val =  '{0:08b}'.format(int(val,16))[::-1]
	if val[0] == '1':
	    self.leds[0].itemconfig("light", fill="green2")
	else:
	    self.leds[0].itemconfig("light", fill="grey")
	if val[1] == '1':
	    self.leds[1].itemconfig("light", fill="green2")
	else:
	    self.leds[1].itemconfig("light", fill="grey")
	if val[2] == '1':
	    self.leds[2].itemconfig("light", fill="green2")
	else:
	    self.leds[2].itemconfig("light", fill="grey")
	if val[3] == '1':
	    self.leds[3].itemconfig("light", fill="green2")
	else:
	    self.leds[3].itemconfig("light", fill="grey")
	if val[4] == '1':
	    self.leds[4].itemconfig("light", fill="green2")
	else:
	    self.leds[4].itemconfig("light", fill="grey")
	if val[5] == '1':
	    self.leds[5].itemconfig("light", fill="green2")
	else:
	    self.leds[5].itemconfig("light", fill="grey")
	    
	if val[6] == '1':
	    self.leds[6].itemconfig("light", fill="green2")
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
		
	    if val2 != '' and  abs(float(val2)-float(arrayConcen[0])) <= 0.2 and len(smkP) < 10:
		conc.append(float(val2))
		smkP.append(float(val1))
	    else:
		if flag_calib != 1 :
		    # on affiche une notification
		    self.zoneNotifs.delete(0.0,tk.END)
		    self.zoneNotifs.insert(tk.INSERT,notif3[0])
		    self.zoneNotifs.insert(tk.INSERT,notif3[1])
		    self.zoneNotifs.tag_add("Ready",0.0,tk.END)
	    
	else:
	    self.leds[6].itemconfig("light", fill="grey")
	    if len(arraySmokeP) == 1 and flag_calib == 0:
		# on récupere la concentration et la valeur du smoke P pour Alarm Lav OFF
		arraySmokeP.append(float(self.smokeP.get()))
		val = self.concen.get()
		if val == '':
		    val = concData[-1]
		arrayConcen.append(val)
		# On affiche les valeurs
		self.widgets[2][1].configure(text=str(arraySmokeP[1]))
		self.widgets[2][2].configure(text=str(arrayConcen[1]))
		self.zoneNotifs.delete(0.0,tk.END)
		if len(smkP) == 10 :
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
		    
	if val[7] == '1':
	    self.leds[7].itemconfig("light", fill="green2")
	else:
	    self.leds[7].itemconfig("light", fill="grey")
	
	
	self.EntryCount.delete(0,tk.END)
	self.EntryCount.insert(tk.INSERT,len(conc))

	
    def stop(self):
	flag_terminal_log = 0


#############################################
class AjustementPotars(threading.Thread):
    def __init__(self,concen,potars,top,bottom,progressBar,zoneNotif, waitZone,boutonCal,tableau):
        threading.Thread.__init__(self)
        self.concentration = concen
	self.POTs = potars
	self.EntryTop = top
	self.EntryBottom = bottom
	self.progressBar = progressBar
	self.zoneNotifs = zoneNotif
	self.waitZone = waitZone
	self.boutonCalibrer = boutonCal
	self.tableau = tableau
	self.flag = 0
	self.bottoms_temp = []
	self.tops_temp = []
	self.tops = []
    def run(self):
	global flag_calib_log, flag_calib, arrayConcen
	
	self.ok = 0
	pot0 = 0
	self.objetAnnexe = Annexes()
	
	#while self.flag:
	while flag_calib_log:
	    if flag_calib:
		print("tops:", len(self.tops))
		print("bottoms_tmp:", len(self.bottoms_temp))
		print("tops_tmp:", len(self.tops_temp))
		self.progressBar.start()
		# on demande de mettre de la fumée	
		if self.flag == 1:
		    if len(arrayConcen) >= 1:
			self.flag = 2
		    else:
			self.notification(3) 
			
			
		elif self.flag == 2:
		    self.notification(1) # on demande de fixer la concentration à 1.2
		    try:
			# On récupère la valeur de top et de bottom
			val1 = self.EntryTop.get()
			val2 = self.EntryBottom.get()
			val3 = self.concentration.get()
			if len(self.bottoms_temp) < 10:
			    try:
				if float(val3) == 1.2 and float(val2)!=0 and float(val1)!=0:
				    self.bottoms_temp.append(float(val2))
				    self.tops.append(float(val1))
			    except:
				pass
			else:
			    self.pot0 = self.POTs[0].get() 
			    self.pot1 = self.POTs[1].get() 
			    # on récupère bottom_prim
			    #bottom_prim = float(max(set(self.bottoms_temp),key=self.bottoms_temp.count))
			    #print("bottom_prim: ",bottom_prim)
			    # on set pot0 et pot1
			    if self.pot0 !='' and self.pot1 !='':
				if float(arrayConcen[0]) > 1.4:
				    #pot0 = 20 * float(arrayConcen[0])
				    #pot0 = int(str(int(pot0)),16)
				    #pot1 = pot0
				    self.algo = 2
				
				else:
				    #pot0 = int(pot0,16)
				    #pot1 = int(pot1,16)
				    self.algo = 1
				self.flag = 3
		    except:
			print("error recup bottom_prim")
			
		elif self.flag == 3:
		    if self.algo == 1:
			if self.ok == 0:
			    self.calibration_1()
			else:
			    #On fait set clear clear zero en s'assurant qu'il n'y a plus de fumée
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
			
		    elif self.algo == 2:
			self.flag = 4
		
		elif self.flag == 4:
		    self.pot0 = 20 * float(arrayConcen[0]) + 5
		    self.pot0 = int(str(int(self.pot0)),16)
		    self.pot1 = self.pot0
		    potars = [self.pot0,self.pot1,0x32,0x14]
		    self.objetAnnexe.set_potars(potars)
		    self.objetAnnexe.get_potars()
		    self.flag = 5
		
		elif sefl.flag == 5:
		    # On récupère la valeur de top et de bottom
		    val1 = self.EntryTop.get() 
		    val3 = self.concentration.get()
		    val_pot0 = self.POTs[0].get()
		    val_pot1 = self.POTs[1].get()
		    if len(self.tops_temp) < 10:
			try:
			    if float(val3) == 1.2 and float(val1) != 0 and int(val_pot0,16) == self.pot0 and int(val_pot1,16) == self.pot1:
				self.tops_temp.append(float(val1))
				self.objetAnnexe.silence()
			except:
			    pass
				    
		    elif len(self.tops_temp) == 10:
			self.flag = 6
		
		elif self.flag == 6:
		    # on récupère top_second
		    top_second = float(max(set(self.tops_temp),key=self.tops_temp.count))
		    bottom_second = round(6.5 * (top_second/6 - bottom_prim) + bottom_prim,3)
		    msg0 = "\nTop prévu après la calibration : "+str(top_second)+" +/- 0.01"
		    msg1 = "\nBottom prévu après la calibration : "+str(bottom_second)+" +/- 0.005"
		    msg2 = "\n----------"
		    # on affiche une notification
		    if not self.ok:
			self.zoneNotifs.delete(0.0,tk.END)
			self.zoneNotifs.insert(tk.INSERT,"Maintenez la concentration de fumée à 1.2 jusqu'à la fin de la calib\n")
			self.zoneNotifs.insert(tk.INSERT,msg2)
			self.zoneNotifs.insert(tk.INSERT,msg0)
			self.zoneNotifs.insert(tk.INSERT,msg1)
			self.zoneNotifs.tag_add("Done",0.0,tk.END)
			self.top_voulu = top_second
			self.bottom_voulu = bottom_second
		    self.flag = 7
		    
		# On commence à ajuster les potars
		elif self.flag ==  7:
		    if not self.ok:
			self.calibration_2()
		    else:
			#On fait set clear clear zero en s'assurant qu'il n'y a plus de fumée
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
				self.zoneNotifs.delete(0.0,tk.END)
				self.zoneNotifs.insert(tk.INSERT,"Videz complètement la fumée !")
				self.zoneNotifs.tag_add("Ready",0.0,tk.END)
		time.sleep(1)
    	
    def calibration_1(self):
	global flag_calib
	k1 = (0.2)/(0.03) #10.7 #0.1/0.03 #(0.2)/(0.03)
	k2 = (0.1)/(0.3)
	bus = can.interface.Bus()
	top_prim = float(max(set(self.tops),key=self.tops.count))
	bottom_prim = float(max(set(self.bottoms_temp),key=self.bottoms_temp.count))
	#print("top = ",top_prim)
	#print("bottom = ",bottom_prim)
	
	bottom_second = round(bottom_prim + k1*(0.1 - bottom_prim),3)
	top_second = round(top_prim + k2*(0.6 - top_prim),3)
	msg0 = "\nTop prévu après la calibration : "+str(top_second)+" +/- 0.01"
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
	    # On récupère la valeur de top et de bottom
	    val1 = self.EntryTop.get() 
	    val2 = self.EntryBottom.get()
	    val3 = self.concentration.get()
	    if float(val3) == 1.2 and val1 !='' and val2!='':
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
			    potars[0] = 0x19
			    potars[2] = 0x32
		
		elif valBottom > self.bottom_voulu and (valBottom - self.bottom_voulu) > 0.005:
		    if potars[2] > 0x32:
			potars[2] -= 1
		    else:
			if potars[0] > 0x19:
			    potars[0] -= 1
			else:
			    potars[0] = 0x19
			    potars[2] = 0x32
			    
		elif valTop < self.top_voulu and (self.top_voulu - valTop) > 0.01:
		    if potars[3] < 0x5A:
			potars[3] += 1
			    
		    else:
			if potars[1] < 0xA0:
			    potars[1] += 1
			else:
			    potars[1] = 0x19
			    potars[3] = 0x14
			    
		elif valTop > self.top_voulu and (valTop - self.top_voulu) > 0.01:
		    if potars[1] > 0x19:
			potars[1] -= 1
		    else:
			if potars[3] > 0x14:
			    potars[3] -= 1
			else:
			    potars[1] = 0x19
			    potars[3] = 0x14
	    
		else:
		    #flag_calib = 0
		    self.ok = 1
		    #self.progressBar.stop()
		
		#print("Potars ajustés: ", potars)
		
		#set potars
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
		
	except:
	    #print("Error")
	    pass
	time.sleep(1)
    
    def calibration_2(self):
	global flag_calib
	bus = can.interface.Bus()
	try:
	    # On récupère la valeur de top et de bottom
	    val1 = self.EntryTop.get() 
	    val2 = self.EntryBottom.get()
	    val3 = self.concentration.get()
	    if float(val3) == 1.2 and val1 !='' and val2!='':
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
			    potars[0] = pot0
			    potars[2] = 0x32
		
		elif valBottom > self.bottom_voulu and (valBottom - self.bottom_voulu) > 0.005:
		    if potars[2] > 0x32:
			potars[2] -= 1
		    else:
			if potars[0] > 0x19:
			    potars[0] -= 1
			else:
			    potars[0] = pot0
			    potars[2] = 0x32
			    
		elif valTop < self.top_voulu and (self.top_voulu - valTop) > 0.01:
		    if potars[3] < 0x5A:
			potars[3] += 1
			    
		    else:
			if potars[1] < 0xA0:
			    potars[1] += 1
			else:
			    potars[1] = pot0
			    potars[3] = 0x14
			    
		elif valTop > self.top_voulu and (valTop - self.top_voulu) > 0.01:
		    if potars[1] > 0x19:
			potars[1] -= 1
		    else:
			if potars[3] > 0x14:
			    potars[3] -= 1
			else:
			    potars[1] = pot0
			    potars[3] = 0x14
	    
		else:
		    #flag_calib = 0
		    self.ok = 1
		    #self.progressBar.stop()
		
		#print("Potars ajustés: ", potars)
		
		#set potars
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
		
	except:
	    #print("Error")
	    pass
	#time.sleep(1)
	
    
    def notification(self,arg):
	self.zoneNotifs.delete(0.0,tk.END)
	if arg == 1:
	    msg = "Maintenez la concentration de fumée à 1.2 jusqu'à la fin de la calib\n"
	else:
	    if arg == 2:
		msg = "Videz complètement la fumée"
	    elif arg == 3:
		msg = "Mettez de la fumée jusqu'au déclenchement et allumage de Alarm Lav\n"
	self.zoneNotifs.insert(tk.INSERT,msg)
	self.zoneNotifs.tag_add("Ready",0.0,tk.END)
	
    def set_flag(self):
	global flag_calib
	flag_calib = 1
	self.flag = 1
	
    def stop(self):
	global flag_calib
	self.ok = 0
	flag_calib = 0
	self.flag = 0
	self.progressBar.stop()
	
##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,concen):
        threading.Thread.__init__(self)
        self.concentration = concen
	

    def run(self):
	global flag_calib_log
	# On calcule le Zero de reference reading en determinant la constante de l'équation
	os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp3.txt ')
	file = open("tmp.txt","rb")
	self.k = round(float(file.readlines()[-1].replace(",","")),4)
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
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp2.txt')
	    file = open("tmp.txt","rb")
	    resultat = float(file.readlines()[-1].replace(",",""))
	    file.close()
	    self.concentration.delete(0,tk.END)
	    y = round(resultat,4)
	    #self.x = round(-(y-self.k)/0.0257,1)
	    self.x = round(-(y-self.k)/0.024,1)
	    self.concentration.insert(0,self.x)
	    
    def stop(self):
	flag_calib_log = 0
    	
  
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
     
    def silence(self):
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x16, 0x00, 0x00, 0x00, 0xff, 0x7f, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
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
 
