# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
from classes import *

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
        # on arrête le thread emission
        #emission._stop()

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
            

class ReadContentMemory(threading.Thread):
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
        # on arrête le thread emission
        #emission._stop()

class AskContentMemory(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.adresse = None
        self.taille = None
        self.type_memoire = None
    
	def set_infos(self,adresse,octet,type_memoire):
		self.adresse = adresse
		self.octet = octet
		self.type_memoire = type_memoire
		
	def get_infos(self):
		if self.taille == 4 and self.memoir == "nvm":
			commande = 0x31
		if self.taille == 3 :
			commande = 0x31
		if self.taille == 4 :
			commande = 0x31
		if self.taille == 4 :
			commande = 0x31
	
    def run(self):Ò
        data = [0x31, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00]
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
	ask_config = AskConfig()
	read_config = ReadConfig(interface)
	read_config.start()
	ask_config.start()

