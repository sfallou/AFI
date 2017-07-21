#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import Tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports
import os
import time





def mean(fichier):
    file = open(fichier,"rb")
    resultat = file.readlines()[6:]
    resultat = [s.strip(',\n') for s in resultat]
    file.close()
    #print resultat
    dim = len(resultat)
    somme = 0
    for val in resultat:
	somme += float(val)
    #print ("Moyenne : ", somme/dim)
    return somme/dim
    
def mesure(i):
    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 500 -t 10000 -v > tmp.txt')
    line.set_ydata(mesure(mean("tmp.txt")))  # update the data
    return line,
    

fig = plt.Figure()

x = np.arange(0, 500)        # x-array
"""print len(x)
def animate(i):
    line.set_ydata(mesure())  # update the data
    return line,
"""
root = Tk.Tk()

label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ax = fig.add_subplot(111)
line, = ax.plot(1, mean("tmp.txt"))
ani = animation.FuncAnimation(fig, mesure, np.arange(1, 200), interval=25, blit=False)

Tk.mainloop()
