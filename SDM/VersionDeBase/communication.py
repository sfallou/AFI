# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
#from classes import *

import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys



class ReadConfig(threading.Thread):
    def __init__(self,interface,terminal,entry_pn,entry_sn,entry_date_fab,entry_crc_mep,entry_crc_bbp,entry_lru):
        threading.Thread.__init__(self)
        self.interface = interface
	self.terminal = terminal
	self.entry_pn =entry_pn
	self.entry_sn =entry_sn
	self.entry_date_fab =entry_date_fab
	self.entry_crc_mep =entry_crc_mep
	self.entry_crc_bbp =entry_crc_bbp
	self.entry_lru =entry_lru

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
        #file = open("configuration.txt","w")
	tab =[]
        while 1:
            message = bus.recv(1)
            if message is None:
                break   
            else :
                print(message)
                info = str(message)+"\n"
		self.terminal.insert(INSERT, info) 
		tab.append(info)
		if len(tab)==2 and tab[1][40:44]=='07ff':
		    pn = (tab[1][77:86]+"-"+tab[1][86:88]).replace(" ","")
		    print("pn: ",pn)
		    self.entry_pn.delete(0,END)
		    self.entry_pn.insert(0,pn)
		if len(tab)==6 and tab[3][40:44]=='07ff':
		    sn = (tab[3][77:88]).replace(" ","")+(tab[5][77:88]).replace(" ","")
		    sn = sn.decode("hex")
		    print("sn: ", sn)
		    self.entry_sn.delete(0,END)
		    self.entry_sn.insert(0,sn)
		if len(tab)==14 and tab[13][40:44]=='07ff':
		    date_fab = (tab[13][77:83]+"-"+tab[13][83:86]+"-"+tab[13][86:88]).replace(" ","")
		    print("date fabrication: ", date_fab)
		    self.entry_date_fab.delete(0,END)
		    self.entry_date_fab.insert(0,date_fab)
		if len(tab)==26 and tab[25][40:44]=='07ff':
		    crc_mep = (tab[25][77:88]).replace(" ","")
		    print("crc mep: ", crc_mep)
		    self.entry_crc_mep.delete(0,END)
		    self.entry_crc_mep.insert(0,crc_mep)
		if len(tab)==28 and tab[27][40:44]=='07ff':
		    crc_bbp = (tab[27][77:88]).replace(" ","")
		    print("crc bbp: ", crc_bbp)
		    self.entry_crc_bbp.delete(0,END)
		    self.entry_crc_bbp.insert(0,crc_bbp)
		   
                #file.write(info)
        #file.close() 
       

class AskConfig(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        messages = []
        datas = [
        [0x31, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x34, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x01, 0x95, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x01, 0x99, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00],
        [0x31, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00],
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
            

class ReadAdressMemory(threading.Thread):
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
		self.terminal.insert(INSERT, info)
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
		#time.sleep(0.3)

###################################################
"""class writeAdressMemory(threading.Thread):
    def __init__(self,adr,mem):
        threading.Thread.__init__(self)
        self.adresse = adr
        self.memoire = mem
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
"""
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
	
	
