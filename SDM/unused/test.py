"""
=====
Decay
=====

This example showcases a sinusoidal decay animation.
"""
# -*-coding:Utf-8 -*


import can
import time                    ## Time-related library
import threading               ## Threading-based Timer library
import sys

import Tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
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
	self.canvas.get_tk_widget().pack()
	
	self.line, = self.ax.plot([], [], lw=1)
	self.ax.grid()
	self.xdata, self.ydata = [], []
	self.ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, blit=False, interval=10,
                              repeat=False, init_func=self.init)
	#self.calc = Calcul()
	#self.calc.start()
	
    def data_gen(self,t=0):
	cnt = 0
	while 1:
	    t += 0.1
	    try:
		file = open("../tmp2.txt","rb")
		resultat = float(file.readlines()[-1].replace(",",""))
		file.close()
		y = round(resultat,4)
		x = -(y-2.6815)/0.0257
		yield t, x
	    except:
		pass
	    
	    
	   


    def init(self):
	self.ax.set_ylim(-1, 3)
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
	self.ymin, self.ymax = self.ax.get_ylim()

	if t >= self.xmax:
	    self.ax.set_xlim(self.xmin, 2*self.xmax)
	    self.ax.figure.canvas.draw()
	if y >= self.ymax:
	    self.ax.set_ylim(-1, 2*self.ymax)
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
    
