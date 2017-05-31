# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
#from classes import *

import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys

class ReadConfig(threading.Thread):
    def __init__(self,interface):
        threading.Thread.__init__(self)
        self.interface = interface

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
        file = open("configuration.txt","w")
        while 1:
            message = bus.recv(1)
            if message is None:
                break   
            else :
                print(message)
                info = str(message)+"\n" 
                file.write(info)
        file.close() 
       

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
    def __init__(self,interface):
        threading.Thread.__init__(self)
        self.interface = interface

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
        file = open("contentMemory.txt","w")
        while 1:
            message = bus.recv(1)
            if message is None:
                break   
            else :
                print(message)
                info = str(message)+"\n" 
                file.write(info)
        file.close() 
        

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
		time.sleep(0.3)
            

##############################################################################

if __name__ == '__main__':
	interface = 'ics0can0'
	#ask_config = AskConfig()
	#read_config = ReadConfig(interface)
	#read_config.start()
	#ask_config.start()
	
	ask_adress_memory = AskAdressMemory(0x14,'4',"NVM")
	read_adress_memory = ReadAdressMemory(interface)
	read_adress_memory.start()
	ask_adress_memory.start()

