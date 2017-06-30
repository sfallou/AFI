# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *

import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys
import data

class TerminalLog(threading.Thread):
    def __init__(self,interface,terminal):
        threading.Thread.__init__(self)
        self.interface = interface
	self.terminal = terminal

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
        #file = open("contentMemory.txt","w")
        while 1:
            message = bus.recv(1)
            if message is None:
                break   
            else :
                print(message)
                info = str(message)+"\n" 
		if info[40:44] == "07ff":
		    self.terminal.insert('0.0', "Trame reçue:\n")
		if info[40:44] == "07bf":
		    self.terminal.insert('0.0', "Trame émise:\n")
		self.terminal.insert('0.0', info)
                #file.write(info)
        #file.close() 
        

class AskAdressMemory(threading.Thread):
    def __init__(self,adr,taille,type_m):
        threading.Thread.__init__(self)
        self.adresse = adr
        self.taille = taille
        self.type_memoire = type_m
        self.commande = ''
    
    def run(self):
		if self.taille == '4' and self.type_memoire == "NVM":
			self.commande = 0x31
		if self.taille == '4' and self.type_memoire == "RAM":
			self.commande = 0x30
		if self.taille == '4' and self.type_memoire == "FLASH":
			self.commande = 0x32
		if self.taille == '3' and self.type_memoire == "NVM":
			self.commande = 0x21
		if self.taille == '3' and self.type_memoire == "RAM":
			self.commande = 0x20
		if self.taille == '3' and self.type_memoire == "FLASH":
			self.commande = 0x22
		if self.taille == '2' and self.type_memoire == "NVM":
			self.commande = 0x11
		if self.taille == '2' and self.type_memoire == "RAM":
			self.commande = 0x10
		if self.taille == '2' and self.type_memoire == "FLASH":
			self.commande = 0x12
		if self.taille == '1' and self.type_memoire == "NVM":
			self.commande = 0x01
		if self.taille == '1' and self.type_memoire == "RAM":
			self.commande = 0x00
		if self.taille == '1' and self.type_memoire == "FLASH":
			self.commande = 0x02
		
		d = [self.commande, 0x00, 0x00, self.adresse, 0x00, 0x00, 0x00, 0x00]
		#print (d)
		bus = can.interface.Bus()
		msg = can.Message(arbitration_id=0x7bf,data=d,extended_id=False)
		try:
		    bus.send(msg)
		except can.CanError:
		    print("Message NOT sent")
		    return
		

###################################################
class WriteAdressMemory(threading.Thread):
    def __init__(self,adr,donnee):
        threading.Thread.__init__(self)
        self.adresse = adr
        self.donnee = str(donnee)
        
    def run(self):
	if len(self.donnee) < 8:
	    while len(self.donnee) <8:
		self.donnee += '0'
	data = [self.adresse]+[int(self.donnee[i:i+2],16) for i in range(0,len(self.donnee),2)]
	d = [0xb1]+[0x00]+[0x00]+data
	#print (d)
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x7bf,data=d,extended_id=False)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	    return

##################################################################

class Configurer_carte(threading.Thread):
    def __init__(self, val2c, mep, crc_mep, crc_cbds,btC, prgBar):
        threading.Thread.__init__(self)
	self.valeur_adresse_2c = val2c
	self.mep = getattr(data,mep)
	self.crc_mep = crc_mep
	self.crc_cbds = getattr(data,crc_cbds)
	self.btConfig = btC
	self.progressBar = prgBar

    def run(self):
        trames_mep = []
        bus = can.interface.Bus()
        for d in self.mep:
            trames_mep.append(can.Message(arbitration_id=0x7bf,data=d,extended_id=False))
	#progressBar
	self.progressBar["value"] = 0
	self.progressBar["maximum"] = 7492
	i=0
	try:
	    # on change la valeur de l'adresse 2c
	    d0 = [0x81, 0x00, 0x00, 0x2c, self.valeur_adresse_2c, 0x00, 0x00, 0x00]
	    msg0 = can.Message(arbitration_id=0x7bf,data=d0,extended_id=False)
	    #bus.send(msg0)
	    # On charge le crc_mep
	    data = [0x04]+[int(self.crc_mep[i:i+2],16) for i in range(0,len(self.crc_mep),2)]
	    d2 = [0xb1]+[0x00]+[0x00]+data
	    msg2 = can.Message(arbitration_id=0x7bf,data=d2,extended_id=False)
	    #bus.send(msg2)
	    # On charge le crc_cbds
	    msg3 = can.Message(arbitration_id=0x7bf,data=self.crc_cbds,extended_id=False)
	    #bus.send(msg3)
	    bus.send(msg0)
	    time.sleep(0.3)
	    i += 1
	    bus.send(msg2)
	    time.sleep(0.3)
	    i += 1
	    bus.send(msg3)
	    time.sleep(0.3)
	    i += 1
	    # on charge le mep
	    for msg in trames_mep:
		i += 1
		try:
		    if str(msg)[63:68] == "d2 00":
			bus.send(msg)
			time.sleep(0.05)
		    else:
			bus.send(msg)
			time.sleep(0.02)
		except can.CanError:
		    print("Message NOT sent")
		    return
		self.progressBar["value"] = i
	except can.CanError:
	    print("Message NOT sent")
	    return
	# on affiche une message d'information
	showinfo("Configuration Terminée!","L'équipement  a été correctement configuré")
	
	self.btConfig.configure(state=NORMAL)
	
##############################################################################

if __name__ == '__main__':
	interface = 'ics0can0'
	ask_config = AskConfig()
	read_config = ReadConfig(interface)
	read_config.start()
	ask_config.start()
	
	#ask_adress_memory = AskAdressMemory(0x14,'4',"NVM")
	#read_adress_memory = ReadAdressMemory(interface)
	#read_adress_memory.start()
	#ask_adress_memory.start()
