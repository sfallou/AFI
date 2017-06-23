# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
#from classes import *

import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys
import os
import data

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
	if len(tab) == 0:
	    # on affiche une message d'erreur
	    showinfo("Problème de communication!","La communication n'est pas établie! Vérifier vos branchements")
	    return
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
	
	if crc_mep_actu == self.CRC_Flight_MEP_Ref:
	    mep_ref = self.CRC_Flight_MEP_Ref
	    programme_running = "Flight"
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
	ligne1 = "Smoke Alarm:  "+tab[237][80:82]+"\t\t T° Alarm   :     "+tab[245][80:82]+"\n"
	ligne2 = "Program Mem: "+tab[125][80:82]+"\t\t Config Mem:    "+tab[133][80:82]+"\n"
	ligne3 = "Watch Dog  :    "+tab[141][80:82]+"\t\t CAN Bus    :     "+tab[149][80:82]+"\n"
	ligne4 = "IR LED     :        "+tab[157][80:82]+"\t\t Blue LED   :      "+tab[165][80:82]+"\n"
	ligne5 = "Photo Diode:     "+tab[174][80:82]+"\t\t Gain Amp   :    "+tab[181][80:82]+"\n"
	ligne6 = "ADC        :        "+tab[189][80:82]+"\t\t Temp Dif   :     "+tab[197][80:82]+"\n"
	ligne7 = "Air Temp   :      "+tab[205][80:82]+"\t\t Lab Temp   :    "+tab[213][80:82]+"\n"
	ligne8 = "Address    :      "+tab[221][80:82]+"\t\t Reserved   :     "+tab[229][80:82]+"\n"
	
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
        bus = can.interface.Bus()
        for d in data.read_config:
            messages.append(can.Message(arbitration_id=0x7bf,data=d,extended_id=False))
        
        for msg in messages:
            try:
                bus.send(msg)
                #print("Message sent on {}".format(bus.channel_info))
            except can.CanError:
                print("Message NOT sent")
		return
            time.sleep(0.3)
            
#############################################################################
class Logs(threading.Thread):
    def __init__(self,terminal,pbar,btClr):
	threading.Thread.__init__(self)
	self.terminal = terminal
	self.progressBar = pbar
	self.btCLR = btClr
    
    def run(self):
	# on affiche le message d'attente dans les logs
	self.terminal.delete('0.0',END)
	self.terminal.insert('0.0', "Clearing ...")
	#progressBar
	self.progressBar["value"] = 0
	self.progressBar["maximum"] = 128
	i=0
	messages = []
	bus = can.interface.Bus()
        for d in data.clear_nvm:
            messages.append(can.Message(arbitration_id=0x7bf,data=d,extended_id=False))
        
        for msg in messages:
	    i +=1
            try:
                bus.send(msg)
		info = str(msg)+"\n"
		self.terminal.insert('0.0', info)
            except can.CanError:
                print("Message NOT sent")
            time.sleep(0.3)
	    self.progressBar["value"] = i
	# on affiche une message d'information
	showinfo("Nettoyage Terminé!","Le NVM a été correctement nettoyé")
	
	self.btCLR.configure(state=NORMAL)
	    
    

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
	
	
	
	

