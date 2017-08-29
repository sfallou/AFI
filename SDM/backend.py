# -*-coding:Utf-8 -*

import tkMessageBox 
import Tkinter as tk
import ttk
import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import Queue
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

#####################################################
can_interface = 'ics0can0'
bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
#####################################################
flag_start1 = True
flag_start2 = True
#####################################################


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        self.queue_create()
	
    def queue_create(self):
	# On calcule le Zero de reference reading en determinant la constante de l'équation
	os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp3.txt ')
	file = open("tmp.txt","rb")
	self.k = round(float(file.readlines()[-1].replace(",","")),4)
	file.close()
	while flag_start2:
	    message = bus.recv()
	    if message:
		os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp2.txt')
		file = open("tmp.txt","rb")
		resultat = float(file.readlines()[-1].replace(",",""))
		file.close()
		y = round(resultat,4)
		x = -(y-self.k)/0.0257
		self.queue.put((message,x))
#################################
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    calibration = Calibration(fenetre_principale=root)
    calibration.mainloop()
    
