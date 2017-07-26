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

valeurTop = 0
valeurSmokeP = 0
valeurConcentration = 0
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
	fic = open("params.txt","w")
	fic.write(str(top)+"\n"+str(bottom))
	fic.close()
	
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
		self.widgets[1][1].configure(text=str(self.listSmokeP[0]))
		self.widgets[1][2].configure(text=str(self.listConcen[0]))
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
		self.widgets[2][1].configure(text=str(self.listSmokeP[1]))
		self.widgets[2][2].configure(text=str(self.listConcen[1]))
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
		self.widgets[3][1].configure(text=str(self.listSmokeP[2]))
		self.widgets[3][2].configure(text=str(self.listConcen[2]))
		
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
		self.widgets[4][1].configure(text=str(self.listSmokeP[3]))
		self.widgets[4][2].configure(text=str(self.listConcen[3]))
	    else:
		pass
	print self.listSmokeP
	print self.listConcen
	
    def stop(self):
	self.flag = 0

##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,concen):
        threading.Thread.__init__(self)
        self.concentration = concen
	

    def run(self):
	self.flag = 1
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	    
        while self.flag:
	    #os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt tmp2.txt')
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp2.txt')
	    file = open("tmp.txt","rb")
	    resultat = float(file.readlines()[-1].replace(",",""))
	    file.close()
	    self.concentration.delete(0,tk.END)
	    y = round(resultat,4)
	    x = -(y-2.6815)/0.0257
	    self.concentration.insert(0,round(x,1))
	    
    def stop(self):
	self.flag = 0
################################################
class MonGraphe2(tk.Frame):
    def __init__(self,smkP,conc,fenetre_principale=None):
        tk.Frame.__init__(self)
	self.fenP = fenetre_principale
	self.fenSmokeP = smkP
	self.fenConc = conc
	self.configure(bg=bgColor)
	
	self.fig = plt.Figure(figsize=(7, 3)) 
	self.ax = self.fig.add_subplot(111)
    
	self.canvas = FigureCanvasTkAgg(self.fig, master=self.fenP)
	self.canvas.get_tk_widget().pack()
	
	self.lineSmoke, = self.ax.plot([], [], 'r', lw=1)
	self.lineConc, = self.ax.plot([], [], 'b', lw=1)
	self.ax.grid()
	self.ax.legend(["Concen","SmokeP"], loc="best", frameon=False, labelspacing=0)
	self.xdata, self.ydata, self.concData = [], [], []
	self.ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, blit=False, interval=10,
                              repeat=False, init_func=self.init)

    def data_gen(self,t=0):
	global valeurSmokeP, valeurConcentration
	while 1:
	    t += 0.1
	    try:
		if self.fenSmokeP.get():
		    valeurSmokeP = float(self.fenSmokeP.get())
		if self.fenConc.get():
		    valeurConcentration = float(self.fenConc.get())
		yield t, valeurConcentration, valeurSmokeP 
	    except:
		pass
	    
	    
	   


    def init(self):
	self.ax.set_ylim(-1, 12)
	self.ax.set_xlim(0, 10)
	del self.xdata[:]
	del self.ydata[:]
	del self.concData[:]
	self.lineSmoke.set_data(self.xdata, self.ydata)
	self.lineConc.set_data(self.xdata, self.concData)
	return self.lineSmoke,self.lineConc,


    def run(self,data):
	# update the data
	t, y, conc = data
	self.xdata.append(t)
	self.ydata.append(y)
	self.concData.append(conc)
	self.xmin, self.xmax = self.ax.get_xlim()
	self.ymin, self.ymax = self.ax.get_ylim()

	if t >= self.xmax:
	    self.ax.set_xlim(self.xmin, 2*self.xmax)
	    self.ax.figure.canvas.draw()
	if y >= self.ymax:
	    self.ax.set_ylim(self.ymin, 2*self.ymax)
	    self.ax.figure.canvas.draw()
	if self.ymax >= 100 and y <= 20:
	    self.ax.set_ylim(self.ymin, 20)
	    self.ax.figure.canvas.draw()
	self.lineSmoke.set_data(self.xdata, self.ydata)
	self.lineConc.set_data(self.xdata, self.concData)
	


	return self.lineSmoke,self.lineConc,
###################################################
class HornCancel(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
       
    def run(self):
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x16, 0x00, 0x00, 0x00, 0xff, 0x7f, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")

#########################################################
if __name__ == "__main__":
    #app = ExampleApp()
    #app.mainloop()
    root = tk.Tk()
    root.title("Calibration")
    root.configure(bg=bgColor)
    #graphe = MonGraphe(fenetre_principale=root)
    #graphe.mainloop()
    
