# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
from classes import *

import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys

class Reception(threading.Thread):
    def __init__(self,interface):
        threading.Thread.__init__(self)
        self.interface = interface

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
        file = open("trame.txt","w")
        while 1:
            message = bus.recv(10)
            if message is None:
                break   
            else :
                print(message)
                info = str(message)+"\n" 
                file.write(info)
        file.close() 
        # on arrête le thread emission
        #emission._stop()

class Emission(threading.Thread):
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


interface = 'ics0can0'
emission = Emission()
reception = Reception(interface)

reception.start()
emission.start()

