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

val = 0
##############################################
class Calcul(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
        while 1:
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
	    val = round(somme/dim,3)
	    time.sleep(0.3)
	    
##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,concen):
        threading.Thread.__init__(self)
        self.concentration = concen
	

    def run(self):
        while 1:
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
	    self.concentration.delete(0,tk.END)
	    time.sleep(0.3)
	    self.concentration.insert(0,round(somme/dim,3))
	    val = round(somme/dim,3)
################################################
class MonGraphe(tk.Frame):
    def __init__(self,fenetre_principale=None):
        tk.Frame.__init__(self)
	self.fenP = fenetre_principale
	#self.fenP.protocol("WM_DELETE_WINDOW", self.quit)
        self.pack()
	self.configure(bg=bgColor)
	
	self.fig = plt.Figure(figsize=(4, 3)) 
	self.ax = self.fig.add_subplot(111)
    
	self.canvas = FigureCanvasTkAgg(self.fig, master=self.fenP)
	self.canvas.get_tk_widget().grid(column=0,row=1)
	
	self.line, = self.ax.plot([], [], lw=1)
	self.ax.grid()
	self.xdata, self.ydata = [], []
	self.ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, blit=False, interval=10,
                              repeat=False, init_func=self.init)
	#self.calc = Calcul()
	#self.calc.start()
	
    def data_gen(self,t=0):
	cnt = 0
	while cnt < 1000:
	    cnt += 1
	    t += 0.1
	    
	    yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)


    def init(self):
	self.ax.set_ylim(-1.1, 1.1)
	self.ax.set_xlim(0, 10)
	del self.xdata[:]
	del self.ydata[:]
	self.line.set_data(self.xdata, self.ydata)
	return self.line,


    def run(self,data):
	# update the data
	t, y = data
	self.xdata.append(t)
	self.ydata.append(y)
	self.xmin, self.xmax = self.ax.get_xlim()

	if t >= self.xmax:
	    self.ax.set_xlim(self.xmin, 2*self.xmax)
	    self.ax.figure.canvas.draw()
	self.line.set_data(self.xdata, self.ydata)

	return self.line,
    

#########################################################
if __name__ == "__main__":
    #app = ExampleApp()
    #app.mainloop()
    root = tk.Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    graphe = MonGraphe(fenetre_principale=root)
    graphe.mainloop()
    
