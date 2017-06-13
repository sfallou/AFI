# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
#from classes import *

import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys
import os

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


class ReadConfig(threading.Thread):
    def __init__(
	self,
	interface,
	crc_Calib_MEP_Ref,
	crc_Flight_MEP_Ref,
	crc_BBP_Ref,
	terminal,
	bar,
	pn,
	sn,
	date,
	crc_bbp_ref,
	crc_bbp_calc,
	crc_bbp_actu,
	signal1,
	crc_mep_ref,
	crc_mep_calc,
	crc_mep_actu,
	signal2,prog,
	faults,
	btSave,
	btLoad,
	btDelete):
        threading.Thread.__init__(self)
        self.interface = interface
	self.CRC_Calib_MEP_Ref = crc_Calib_MEP_Ref
	self.CRC_Flight_MEP_Ref = crc_Flight_MEP_Ref
	self.CRC_BBP_Ref = crc_BBP_Ref
	self.terminal = terminal
	self.progressBar = bar
	self.pn,self.sn,self.date = pn,sn,date
	self.crc_bbp_ref,self.crc_bbp_calc,self.crc_bbp_actu = crc_bbp_ref,crc_bbp_calc,crc_bbp_actu
	self.signal1,self.signal2 = signal1,signal2
	self.crc_mep_ref,self.crc_mep_calc,self.crc_mep_actu = crc_mep_ref,crc_mep_calc,crc_mep_actu
	self.prog = prog
	self.faults = faults
	self.btSave = btSave
	self.btLoad = btLoad
	self.btDelete = btDelete

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
        file = open("resultat_nvm.txt","w")
	#progressBar
	self.progressBar["value"] = 0
	self.progressBar["maximum"] = 504
	i=0
	
        while 1:
            message = bus.recv(1)
            if message is None:
                break   
            else :
		i +=1
                print(message)
		info = str(message)+"\n"
		self.terminal.insert('0.0', info)
		if info[40:44]=="07ff":
		    file.write(info)
		self.progressBar["value"] = i
        file.close()
	file = open("resultat_nvm.txt","r")
	tab = file.readlines()
	for i in range (len(tab)):
	    if i==5:
		self.pn.delete(0,END)
		self.pn.insert(0,(tab[i][77:86]+"-"+tab[i][86:88]).replace(" ",""))
	    if i==4:
		    sn = (tab[i-1][77:88]).replace(" ","")+(tab[4][77:88]).replace(" ","")
		    sn = sn.decode("hex")
		    self.sn.delete(0,END)
		    self.sn.insert(0,sn)
	    if i==9:
		    date_fab = (tab[i][77:83]+"-"+tab[i][83:86]+"-"+tab[i][86:88]).replace(" ","")
		    self.date.delete(0,END)
		    self.date.insert(0,date_fab)
	    if i==1:
		    crc_mep_actu = (tab[i][77:88]).replace(" ","")
		    self.crc_mep_actu.delete(0,END)
		    self.crc_mep_actu.insert(0,crc_mep_actu)
	    if i==2:
		    crc_bbp_actu = (tab[i][77:88]).replace(" ","")
		    self.crc_bbp_actu.delete(0,END)
		    self.crc_bbp_actu.insert(0,crc_bbp_actu)
	    if i==122:
		    crc_bbp_calc = (tab[i][77:88]).replace(" ","")
		    self.crc_bbp_calc.delete(0,END)
		    self.crc_bbp_calc.insert(0,crc_bbp_calc)
		    crc_mep_calc = (tab[i-1][77:88]).replace(" ","")
		    self.crc_mep_calc.delete(0,END)
		    self.crc_mep_calc.insert(0,crc_mep_calc)
	# on affiche les crc de référence
	programme_running = "inconnu"
	mep_ref = "XXXXXXXXX"
	bbp_ref = "XXXXXXXXX"
	couleur1 = "red"
	couleur2 = "red"
	notice1 = "Problème avec le CRC BBP !" 
	notice2 = "Problème avec le CRC MEP" 
	    
	if crc_mep_actu == self.CRC_Calib_MEP_Ref:
	    mep_ref = self.CRC_Calib_MEP_Ref
	    programme_running = "Calibration"
	    if crc_mep_calc == crc_mep_actu:
		couleur2 = "green"
		notice2 = "Le CRC MEP est correct"
		
	    
	elif crc_mep_actu == self.CRC_Flight_MEP_Ref:
	    mep_ref = self.CRC_Flight_MEP_Ref
	    programme_running = "Flight"
	
	
	
	self.crc_mep_ref.delete(0,END)
	self.crc_mep_ref.insert(0,mep_ref)
	
	if crc_bbp_actu == self.CRC_BBP_Ref and crc_bbp_actu == crc_bbp_calc:
	    bbp_ref = self.CRC_BBP_Ref
	    couleur1 = "green"
	    notice1 = "Le CRC BBP est correct"
	self.crc_bbp_ref.delete(0,END)
	self.crc_bbp_ref.insert(0,bbp_ref)
	
	# On affiche le type de programme en mémoire
	self.prog.delete(0,END)
	self.prog.insert(0,programme_running)
	# On change la couleur des indicateurs
	self.signal2.create_oval(0,0,35,35, fill=couleur2)
	self.signal1.create_oval(0,0,35,35, fill=couleur1)
	
	
	
	# On affiche les fautes
	self.faults.delete(0.0,END)
	f="2"
	ligne1 = "Smoke Alarm : "+tab[237][80:82]+"\t\t T° Alarm: "+tab[245][80:82]+"\n"
	ligne2 = "Program Mem: "+tab[125][80:82]+"\t\t Config Mem: "+tab[133][80:82]+"\n"
	ligne3 = "Watch Dog: "+tab[141][80:82]+"\t\t CAN Bus: "+tab[149][80:82]+"\n"
	ligne4 = "IR LED: "+tab[157][80:82]+"\t\t Blue LED: "+tab[165][80:82]+"\n"
	ligne5 = "Photo Diode: "+tab[174][80:82]+"\t\t Gain Amp: "+tab[181][80:82]+"\n"
	ligne6 = "ADC: "+tab[189][80:82]+"\t\t Temp Dif: "+tab[197][80:82]+"\n"
	ligne7 = "Air Temp: "+tab[205][80:82]+"\t\t Lab Temp: "+tab[213][80:82]+"\n"
	ligne8 = "Address: "+tab[221][80:82]+"\t\t Reserved: "+tab[229][80:82]+"\n"
	
	self.faults.insert(INSERT,ligne1)
	self.faults.insert(INSERT,ligne2)
	self.faults.insert(INSERT,ligne3)
	self.faults.insert(INSERT,ligne4)
	self.faults.insert(INSERT,ligne5)
	self.faults.insert(INSERT,ligne6)
	self.faults.insert(INSERT,ligne7)
	self.faults.insert(INSERT,ligne8)
	
	# on affiche une message d'information
	showinfo("Test Terminé!",notice1+"\n"+notice2)
	
	# on réactive les boutons du fenetre 2
	self.btSave.configure(state=NORMAL)
	self.btLoad.configure(state=NORMAL)
	self.btDelete.configure(state=NORMAL)
##################################################################

class AskConfig(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        messages = []
	datas = [
	[49, 0, 0, 0, 0, 0, 0, 0], 
	[49, 0, 0, 4, 0, 0, 0, 0], 
	[49, 0, 0, 8, 0, 0, 0, 0], 
	[49, 0, 0, 12, 0, 0, 0, 0], 
	[49, 0, 0, 16, 0, 0, 0, 0], 
	[49, 0, 0, 20, 0, 0, 0, 0], 
	[49, 0, 0, 24, 0, 0, 0, 0], 
	[49, 0, 0, 28, 0, 0, 0, 0], 
	[49, 0, 0, 32, 0, 0, 0, 0], 
	[49, 0, 0, 36, 0, 0, 0, 0], 
	[49, 0, 0, 40, 0, 0, 0, 0], 
	[49, 0, 0, 44, 0, 0, 0, 0], 
	[49, 0, 0, 48, 0, 0, 0, 0], 
	[49, 0, 0, 52, 0, 0, 0, 0], 
	[49, 0, 0, 56, 0, 0, 0, 0], 
	[49, 0, 0, 60, 0, 0, 0, 0], 
	[49, 0, 0, 80, 0, 0, 0, 0], 
	[49, 0, 0, 84, 0, 0, 0, 0], 
	[49, 0, 0, 88, 0, 0, 0, 0], 
	[49, 0, 0, 92, 0, 0, 0, 0], 
	[49, 0, 0, 96, 0, 0, 0, 0], 
	[49, 0, 0, 100, 0, 0, 0, 0], 
	[49, 0, 0, 104, 0, 0, 0, 0], 
	[49, 0, 0, 108, 0, 0, 0, 0], 
	[49, 0, 0, 112, 0, 0, 0, 0], 
	[49, 0, 0, 116, 0, 0, 0, 0], 
	[49, 0, 0, 120, 0, 0, 0, 0], 
	[49, 0, 0, 124, 0, 0, 0, 0], 
	[49, 0, 0, 128, 0, 0, 0, 0], 
	[49, 0, 0, 132, 0, 0, 0, 0], 
	[49, 0, 0, 136, 0, 0, 0, 0], 
	[49, 0, 0, 140, 0, 0, 0, 0], 
	[49, 0, 0, 144, 0, 0, 0, 0], 
	[49, 0, 0, 148, 0, 0, 0, 0], 
	[49, 0, 0, 152, 0, 0, 0, 0], 
	[49, 0, 0, 156, 0, 0, 0, 0], 
	[49, 0, 0, 160, 0, 0, 0, 0], 
	[49, 0, 0, 164, 0, 0, 0, 0], 
	[49, 0, 0, 168, 0, 0, 0, 0], 
	[49, 0, 0, 172, 0, 0, 0, 0], 
	[49, 0, 0, 176, 0, 0, 0, 0], 
	[49, 0, 0, 180, 0, 0, 0, 0], 
	[49, 0, 0, 184, 0, 0, 0, 0], 
	[49, 0, 0, 188, 0, 0, 0, 0], 
	[49, 0, 0, 192, 0, 0, 0, 0], 
	[49, 0, 0, 196, 0, 0, 0, 0], 
	[49, 0, 0, 200, 0, 0, 0, 0], 
	[49, 0, 0, 204, 0, 0, 0, 0], 
	[49, 0, 0, 208, 0, 0, 0, 0], 
	[49, 0, 0, 212, 0, 0, 0, 0], 
	[49, 0, 0, 216, 0, 0, 0, 0], 
	[49, 0, 0, 220, 0, 0, 0, 0], 
	[49, 0, 0, 224, 0, 0, 0, 0], 
	[49, 0, 0, 228, 0, 0, 0, 0], 
	[49, 0, 0, 232, 0, 0, 0, 0], 
	[49, 0, 0, 236, 0, 0, 0, 0], 
	[49, 0, 0, 240, 0, 0, 0, 0], 
	[49, 0, 0, 244, 0, 0, 0, 0], 
	[49, 0, 0, 248, 0, 0, 0, 0], 
	[49, 0, 0, 252, 0, 0, 0, 0], 
	[49, 0, 1, 0, 0, 0, 0, 0], 
	[49, 0, 1, 4, 0, 0, 0, 0], 
	[49, 0, 1, 8, 0, 0, 0, 0], 
	[49, 0, 1, 12, 0, 0, 0, 0], 
	[49, 0, 1, 16, 0, 0, 0, 0], 
	[49, 0, 1, 20, 0, 0, 0, 0], 
	[49, 0, 1, 24, 0, 0, 0, 0], 
	[49, 0, 1, 28, 0, 0, 0, 0], 
	[49, 0, 1, 32, 0, 0, 0, 0], 
	[49, 0, 1, 36, 0, 0, 0, 0], 
	[49, 0, 1, 40, 0, 0, 0, 0], 
	[49, 0, 1, 44, 0, 0, 0, 0], 
	[49, 0, 1, 48, 0, 0, 0, 0], 
	[49, 0, 1, 52, 0, 0, 0, 0], 
	[49, 0, 1, 56, 0, 0, 0, 0], 
	[49, 0, 1, 60, 0, 0, 0, 0], 
	[49, 0, 1, 64, 0, 0, 0, 0], 
	[49, 0, 1, 68, 0, 0, 0, 0], 
	[49, 0, 1, 72, 0, 0, 0, 0], 
	[49, 0, 1, 76, 0, 0, 0, 0], 
	[49, 0, 1, 80, 0, 0, 0, 0], 
	[49, 0, 1, 84, 0, 0, 0, 0], 
	[49, 0, 1, 88, 0, 0, 0, 0], 
	[49, 0, 1, 92, 0, 0, 0, 0], 
	[49, 0, 1, 96, 0, 0, 0, 0], 
	[49, 0, 1, 100, 0, 0, 0, 0], 
	[49, 0, 1, 104, 0, 0, 0, 0], 
	[49, 0, 1, 108, 0, 0, 0, 0], 
	[49, 0, 1, 112, 0, 0, 0, 0], 
	[49, 0, 1, 116, 0, 0, 0, 0], 
	[49, 0, 1, 120, 0, 0, 0, 0], 
	[49, 0, 1, 124, 0, 0, 0, 0], 
	[49, 0, 1, 128, 0, 0, 0, 0], 
	[49, 0, 1, 132, 0, 0, 0, 0], 
	[49, 0, 1, 136, 0, 0, 0, 0], 
	[49, 0, 1, 140, 0, 0, 0, 0], 
	[49, 0, 1, 144, 0, 0, 0, 0], 
	[49, 0, 1, 148, 0, 0, 0, 0], 
	[49, 0, 1, 152, 0, 0, 0, 0], 
	[49, 0, 1, 156, 0, 0, 0, 0], 
	[49, 0, 1, 160, 0, 0, 0, 0], 
	[49, 0, 1, 164, 0, 0, 0, 0], 
	[49, 0, 1, 168, 0, 0, 0, 0], 
	[49, 0, 1, 172, 0, 0, 0, 0], 
	[49, 0, 1, 176, 0, 0, 0, 0], 
	[49, 0, 1, 180, 0, 0, 0, 0], 
	[49, 0, 1, 184, 0, 0, 0, 0], 
	[49, 0, 1, 188, 0, 0, 0, 0], 
	[49, 0, 1, 192, 0, 0, 0, 0], 
	[49, 0, 1, 196, 0, 0, 0, 0], 
	[49, 0, 1, 200, 0, 0, 0, 0], 
	[49, 0, 1, 204, 0, 0, 0, 0], 
	[49, 0, 1, 208, 0, 0, 0, 0], 
	[49, 0, 1, 212, 0, 0, 0, 0], 
	[49, 0, 1, 216, 0, 0, 0, 0], 
	[49, 0, 1, 220, 0, 0, 0, 0], 
	[49, 0, 1, 224, 0, 0, 0, 0], 
	[49, 0, 1, 228, 0, 0, 0, 0], 
	[49, 0, 1, 232, 0, 0, 0, 0], 
	[49, 0, 1, 236, 0, 0, 0, 0], 
	[49, 0, 1, 240, 0, 0, 0, 0], 
	[49, 0, 1, 244, 0, 0, 0, 0], 
	[49, 0, 1, 248, 0, 0, 0, 0], 
	[49, 0, 1, 252, 0, 0, 0, 0], 
	[49, 0, 2, 0, 0, 0, 0, 0], 
	[49, 0, 2, 4, 0, 0, 0, 0], 
	[49, 0, 2, 8, 0, 0, 0, 0], 
	[49, 0, 2, 12, 0, 0, 0, 0], 
	[49, 0, 2, 16, 0, 0, 0, 0], 
	[49, 0, 2, 20, 0, 0, 0, 0], 
	[49, 0, 2, 24, 0, 0, 0, 0], 
	[49, 0, 2, 28, 0, 0, 0, 0],
	[49, 0, 2, 32, 0, 0, 0, 0], 
	[49, 0, 2, 36, 0, 0, 0, 0], 
	[49, 0, 2, 40, 0, 0, 0, 0], 
	[49, 0, 2, 44, 0, 0, 0, 0], 
	[49, 0, 2, 48, 0, 0, 0, 0], 
	[49, 0, 2, 52, 0, 0, 0, 0], 
	[49, 0, 2, 56, 0, 0, 0, 0], 
	[49, 0, 2, 60, 0, 0, 0, 0], 
	[49, 0, 2, 64, 0, 0, 0, 0], 
	[49, 0, 2, 68, 0, 0, 0, 0], 
	[49, 0, 2, 72, 0, 0, 0, 0], 
	[49, 0, 2, 76, 0, 0, 0, 0], 
	[49, 0, 2, 80, 0, 0, 0, 0], 
	[49, 0, 2, 84, 0, 0, 0, 0], 
	[49, 0, 2, 88, 0, 0, 0, 0], 
	[49, 0, 2, 92, 0, 0, 0, 0], 
	[49, 0, 2, 96, 0, 0, 0, 0], 
	[49, 0, 2, 100, 0, 0, 0, 0], 
	[49, 0, 2, 104, 0, 0, 0, 0], 
	[49, 0, 2, 108, 0, 0, 0, 0], 
	[49, 0, 2, 112, 0, 0, 0, 0], 
	[49, 0, 2, 116, 0, 0, 0, 0], 
	[49, 0, 2, 120, 0, 0, 0, 0], 
	[49, 0, 2, 124, 0, 0, 0, 0], 
	[49, 0, 2, 128, 0, 0, 0, 0], 
	[49, 0, 2, 132, 0, 0, 0, 0], 
	[49, 0, 2, 136, 0, 0, 0, 0], 
	[49, 0, 2, 140, 0, 0, 0, 0], 
	[49, 0, 2, 144, 0, 0, 0, 0], 
	[49, 0, 2, 148, 0, 0, 0, 0], 
	[49, 0, 2, 152, 0, 0, 0, 0], 
	[49, 0, 2, 156, 0, 0, 0, 0], 
	[49, 0, 2, 160, 0, 0, 0, 0], 
	[49, 0, 2, 164, 0, 0, 0, 0], 
	[49, 0, 2, 168, 0, 0, 0, 0], 
	[49, 0, 2, 172, 0, 0, 0, 0], 
	[49, 0, 2, 176, 0, 0, 0, 0], 
	[49, 0, 2, 180, 0, 0, 0, 0], 
	[49, 0, 2, 184, 0, 0, 0, 0], 
	[49, 0, 2, 188, 0, 0, 0, 0], 
	[49, 0, 2, 192, 0, 0, 0, 0], 
	[49, 0, 2, 196, 0, 0, 0, 0], 
	[49, 0, 2, 200, 0, 0, 0, 0], 
	[49, 0, 2, 204, 0, 0, 0, 0], 
	[49, 0, 2, 208, 0, 0, 0, 0], 
	[49, 0, 2, 212, 0, 0, 0, 0], 
	[49, 0, 2, 216, 0, 0, 0, 0], 
	[49, 0, 2, 220, 0, 0, 0, 0], 
	[49, 0, 2, 224, 0, 0, 0, 0], 
	[49, 0, 2, 228, 0, 0, 0, 0], 
	[49, 0, 2, 232, 0, 0, 0, 0], 
	[49, 0, 2, 236, 0, 0, 0, 0], 
	[49, 0, 2, 240, 0, 0, 0, 0], 
	[49, 0, 2, 244, 0, 0, 0, 0], 
	[49, 0, 2, 248, 0, 0, 0, 0], 
	[49, 0, 2, 252, 0, 0, 0, 0], 
	[49, 0, 3, 0, 0, 0, 0, 0], 
	[49, 0, 3, 4, 0, 0, 0, 0], 
	[49, 0, 3, 8, 0, 0, 0, 0], 
	[49, 0, 3, 12, 0, 0, 0, 0], 
	[49, 0, 3, 16, 0, 0, 0, 0], 
	[49, 0, 3, 20, 0, 0, 0, 0], 
	[49, 0, 3, 24, 0, 0, 0, 0], 
	[49, 0, 3, 28, 0, 0, 0, 0], 
	[49, 0, 3, 32, 0, 0, 0, 0], 
	[49, 0, 3, 36, 0, 0, 0, 0], 
	[49, 0, 3, 40, 0, 0, 0, 0], 
	[49, 0, 3, 44, 0, 0, 0, 0], 
	[49, 0, 3, 48, 0, 0, 0, 0], 
	[49, 0, 3, 52, 0, 0, 0, 0], 
	[49, 0, 3, 56, 0, 0, 0, 0], 
	[49, 0, 3, 60, 0, 0, 0, 0], 
	[49, 0, 3, 64, 0, 0, 0, 0], 
	[49, 0, 3, 68, 0, 0, 0, 0], 
	[49, 0, 3, 72, 0, 0, 0, 0], 
	[49, 0, 3, 76, 0, 0, 0, 0], 
	[49, 0, 3, 80, 0, 0, 0, 0], 
	[49, 0, 3, 84, 0, 0, 0, 0], 
	[49, 0, 3, 88, 0, 0, 0, 0], 
	[49, 0, 3, 92, 0, 0, 0, 0], 
	[49, 0, 3, 96, 0, 0, 0, 0], 
	[49, 0, 3, 100, 0, 0, 0, 0], 
	[49, 0, 3, 104, 0, 0, 0, 0], 
	[49, 0, 3, 108, 0, 0, 0, 0], 
	[49, 0, 3, 112, 0, 0, 0, 0], 
	[49, 0, 3, 116, 0, 0, 0, 0], 
	[49, 0, 3, 120, 0, 0, 0, 0], 
	[49, 0, 3, 124, 0, 0, 0, 0], 
	[49, 0, 3, 128, 0, 0, 0, 0], 
	[49, 0, 3, 132, 0, 0, 0, 0], 
	[49, 0, 3, 136, 0, 0, 0, 0], 
	[49, 0, 3, 140, 0, 0, 0, 0], 
	[49, 0, 3, 144, 0, 0, 0, 0], 
	[49, 0, 3, 148, 0, 0, 0, 0], 
	[49, 0, 3, 152, 0, 0, 0, 0], 
	[49, 0, 3, 156, 0, 0, 0, 0], 
	[49, 0, 3, 160, 0, 0, 0, 0], 
	[49, 0, 3, 164, 0, 0, 0, 0], 
	[49, 0, 3, 168, 0, 0, 0, 0], 
	[49, 0, 3, 172, 0, 0, 0, 0], 
	[49, 0, 3, 176, 0, 0, 0, 0], 
	[49, 0, 3, 180, 0, 0, 0, 0], 
	[49, 0, 3, 184, 0, 0, 0, 0], 
	[49, 0, 3, 188, 0, 0, 0, 0], 
	[49, 0, 3, 192, 0, 0, 0, 0], 
	[49, 0, 3, 196, 0, 0, 0, 0], 
	[49, 0, 3, 200, 0, 0, 0, 0], 
	[49, 0, 3, 204, 0, 0, 0, 0], 
	[49, 0, 3, 208, 0, 0, 0, 0], 
	[49, 0, 3, 212, 0, 0, 0, 0], 
	[49, 0, 3, 216, 0, 0, 0, 0], 
	[49, 0, 3, 220, 0, 0, 0, 0], 
	[49, 0, 3, 224, 0, 0, 0, 0], 
	[49, 0, 3, 228, 0, 0, 0, 0], 
	[49, 0, 3, 232, 0, 0, 0, 0], 
	[49, 0, 3, 236, 0, 0, 0, 0], 
	[49, 0, 3, 240, 0, 0, 0, 0], 
	[49, 0, 3, 244, 0, 0, 0, 0], 
	[49, 0, 3, 248, 0, 0, 0, 0], 
	[49, 0, 3, 252, 0, 0, 0, 0]
	]

        bus = can.interface.Bus()
        for d in datas:
            messages.append(can.Message(arbitration_id=0x7bf,data=d,extended_id=False))
        
        for msg in messages:
            try:
                bus.send(msg)
                #print("Message sent on {}".format(bus.channel_info))
            except can.CanError:
                print("Message NOT sent")
            time.sleep(0.3)
            


##############################################################################

if __name__ == '__main__':
	"""fenetre3 = Tk()
	fenetre3.title("Test de Reception")
	fenetre3.configure(bg=bgColor)
	# Zone de Text pour les logs
	labelLogs = Label(fenetre3,text="Logs", fg=fgColor, font=titreFont, bg=bgColor)
        labelLogs.grid(row=2,column=0)
	textLogs = Text(fenetre3, height=6, width=40,font=("consolas",11))
	textLogs.grid(row=3,column=0)
	# le scrollbar
	scrollb = Scrollbar(fenetre3, command=textLogs.yview)
	scrollb.grid(row=3,column=1,sticky="nsew")
	textLogs['yscrollcommand'] = scrollb.set
	
	interface = 'ics0can0'
	ask_config = AskConfig()
	read_config = ReadConfig(interface,textLogs)
	read_config.start()
	ask_config.start()
	"""
	
	
	
	
