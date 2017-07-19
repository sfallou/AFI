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


#####################################################
class TerminalLog(threading.Thread):
    def __init__(self,interface,terminal,leds,pots,top,bottom,smokeP,concen,widgets):
        threading.Thread.__init__(self)
        self.interface = interface
	self.terminal = terminal
	self.leds = leds
	self.pots = pots
	self.top = top
	self.bottom = bottom
	self.smokeP = smokeP
	self.concen = concen
	self.listSmokeP = []
	self.listConcen = []
	self.widgets = widgets

    def run(self):
        can_interface = self.interface
        bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
	self.flag = 1
        while self.flag:
            message = bus.recv()
            if message is None:
                break   
            else :
                print(message)
                info = str(message)+"\n"
		if info[36:44] == "00400103":
		    self.clignotant(info[65:67])
		    self.parametres(info)
		    self.terminal.insert('0.0', info)
		    
		elif info[36:44] == "0611e103":
		    for i in range(4):
			self.pots[i].delete(0,tk.END)
		    self.pots[0].insert(0,info[68:70])
		    self.pots[1].insert(0,info[71:73])
		    self.pots[2].insert(0,info[74:76])
		    self.pots[3].insert(0,info[77:79])

    def parametres(self,msg):
	top = float(int(msg[77:82].replace(" ",""),16))/float(204)
	bottom = float(int(msg[83:88].replace(" ",""),16))/float(204)
	smokeP = top/bottom
	self.top.delete(0,tk.END)
	self.bottom.delete(0,tk.END)
	self.smokeP.delete(0,tk.END)
	self.top.insert(0,round(top,4))
	self.bottom.insert(0,round(bottom,4))
	self.smokeP.insert(0,round(smokeP,4))
	
    def clignotant(self, val):
	val =  '{0:08b}'.format(int(val,16))[::-1]
	if val[0] == '0':
	    self.leds[0].create_oval(0,0,15,15, fill="grey")
	if val[0] == '1':
	    self.leds[0].create_oval(0,0,15,15, fill="green2")
	if val[1] == '0':
	    self.leds[1].create_oval(0,0,15,15, fill="grey")
	if val[1] == '1':
	    self.leds[1].create_oval(0,0,15,15, fill="green2")
	if val[2] == '0':
	    self.leds[2].create_oval(0,0,15,15, fill="grey")
	if val[2] == '1':
	    self.leds[2].create_oval(0,0,15,15, fill="green2")
	if val[3] == '0':
	    self.leds[3].create_oval(0,0,15,15, fill="grey")
	if val[3] == '1':
	    sel.leds[3].create_oval(0,0,15,15, fill="green2")
	if val[4] == '0':
	    self.leds[4].create_oval(0,0,15,15, fill="grey")
	if val[4] == '1':
	    self.leds[4].create_oval(0,0,15,15, fill="green2")
	    if len(self.listSmokeP) < 1:
		# on récupere la concentration et la valeur du smoke P
		self.listSmokeP.append(self.smokeP.get())
		self.listConcen.append(self.concen.get())
	    else:
		pass
	if val[5] == '0':
	    self.leds[5].create_oval(0,0,15,15, fill="grey")
	if val[5] == '1':
	    self.leds[5].create_oval(0,0,15,15, fill="green2")
	    if len(self.listSmokeP) < 2:
		# on récupere la concentration et la valeur du smoke P
		self.listSmokeP.append(self.smokeP.get())
		self.listConcen.append(self.concen.get())
	    else:
		pass
	if val[6] == '0':
	    self.leds[6].create_oval(0,0,15,15, fill="grey")
	if val[6] == '1':
	    self.leds[6].create_oval(0,0,15,15, fill="green2")
	    #self.flag = 0
	    if len(self.listSmokeP) < 3:
		# on récupere la concentration et la valeur du smoke P
		self.listSmokeP.append(self.smokeP.get())
		self.listConcen.append(self.concen.get())
	    else:
		pass
	if val[7] == '0':
	    self.leds[7].create_oval(0,0,15,15, fill="grey")
	if val[7] == '1':
	    self.leds[7].create_oval(0,0,15,15, fill="green2")
	    if len(self.listSmokeP) < 4:
		# on récupere la concentration et la valeur du smoke P
		self.listSmokeP.append(self.smokeP.get())
		self.listConcen.append(self.concen.get())
		#self.flag = 0
		self.widgets[1][1].configure(text=str(self.listSmokeP[0]))
		self.widgets[2][1].configure(text=str(self.listSmokeP[1]))
		self.widgets[3][1].configure(text=str(self.listSmokeP[2]))
		self.widgets[4][1].configure(text=str(self.listSmokeP[3]))
		
		self.widgets[1][2].configure(text=str(self.listConcen[0]))
		self.widgets[2][2].configure(text=str(self.listConcen[1]))
		self.widgets[3][2].configure(text=str(self.listConcen[2]))
		self.widgets[4][2].configure(text=str(self.listConcen[3]))
	    else:
		pass
	print self.listSmokeP
	print self.listConcen
	
##############################################
"""class Calcul(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
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
"""	    
##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,concen):
        threading.Thread.__init__(self)
        self.concentration = concen
	

    def run(self):
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	    
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
	    #time.sleep(0.3)
	    y = round(somme/dim,4)
	    x = -(y-2.6815)/0.0257
	    self.concentration.insert(0,round(x,1))
	    
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
    
