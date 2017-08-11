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

##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,interface1,interface2):
        threading.Thread.__init__(self)
        self.interface1 = interface1
	self.interface2 = interface2

    def run(self):
        MonGraphe(fenetre_principale=self.interface1)
	MonGraphe(fenetre_principale=self.interface2)
        
################################################
class MonGraphe(tk.Frame):
    def __init__(self,fenetre_principale=None):
        tk.Frame.__init__(self)
	self.fenP = fenetre_principale
	#self.fenP.protocol("WM_DELETE_WINDOW", self.quit)
        self.pack()
	self.configure(bg=bgColor)
	
	self.conc = [0]
	self.fig = plt.Figure(figsize=(4, 3)) 
	self.ax = self.fig.add_subplot(111)
	self.x = np.arange(0, 8, 0.01)        # x-array
    
	self.canvas = FigureCanvasTkAgg(self.fig, master=self.fenP)
	self.canvas.get_tk_widget().grid(column=0,row=1)
	
	self.line, = self.ax.plot(self.x, np.sin(self.x), lw=1)
	self.ax.grid()
	self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)
    
    def animate(self,i):
	#self.mesure()
	self.line.set_ydata(np.sin(self.x+i/10.0))  # update the data
	return self.line,
    
    ### calcule la moyenne de l'acquisition
   
    def mesure(self):
	try:
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 500 -t 10000 -v > tmp.txt')
	    file = open("tmp.txt","rb")
	    resultat = file.readlines()[6:]
	    resultat = [s.strip(',\n') for s in resultat]
	    file.close()
	    #print resultat
	    dim = len(resultat)
	    somme = 0
	    for val in resultat:
		somme += float(val)
	    self.conc.append(somme/dim)
	    	
	except:
	    print ("impossible")
	    

#########################################################
if __name__ == "__main__":
    #app = ExampleApp()
    #app.mainloop()
    root = tk.Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    graphe = MonGraphe(fenetre_principale=root)
    graphe.mainloop()
    
