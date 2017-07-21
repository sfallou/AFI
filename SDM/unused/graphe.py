"""
=====
Decay
=====

This example showcases a sinusoidal decay animation.
"""

import Tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def mean(fichier):
    file = open(fichier,"rb")
    resultat = file.readlines()[6:505]
    resultat = [s.strip(',\n') for s in resultat]
    file.close()
    #print resultat
    dim = len(resultat)
    somme = 0
    for val in resultat:
	somme += float(val)
    #print ("Moyenne : ", somme/dim)
    return somme/dim
    
def mesure():
	try:
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 500 -t 10000 -v > tmp.txt')
	    mean("tmp.txt")
	except:
	    print ("impossible")
	    
def data_gen(t=0):
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.1
	os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v > tmp.txt')
	file = open("tmp.txt","rb")
	resultat = float(file.readlines()[-1].replace(",",""))
	file.close()
	y = round(resultat,4)
	x = -(y-2.6815)/0.0257
        yield t, x #mesure() #np.sin(2*np.pi*t) * np.exp(-t/10.)


def init():
    ax.set_ylim(-1, 3)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    if y >= ymax:
        ax.set_ylim(-1, 2*ymax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
                              repeat=False, init_func=init)
plt.show()
