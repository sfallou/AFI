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
arraySmokeP = []
arrayConcen = []
smkP = []
conc = []
#####################################################
class TerminalLog(threading.Thread):
    def __init__(self,interface,terminal,leds,pots,backgrounds,top,bottom,smokeP,concen,widgets,Boutoncalib,Boutonclear):
        threading.Thread.__init__(self)
        self.interface = interface
	self.terminal = terminal
	self.leds = leds
	self.pots = pots
	self.bgcks = backgrounds
	self.top = top
	self.bottom = bottom
	self.smokeP = smokeP
	self.concen = concen
	#self.listSmokeP = []
	#self.listConcen = []
	self.widgets = widgets
	self.BoutonCalib = Boutoncalib
	self.BoutonClear = Boutonclear
	#self.smkP = []
	#self.conc = []
	self.SN = ""
	self.PN = ""
	
	
    def run(self):
	global arraySmokeP, arrayConcen, smkP, conc
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
		    print(message)
		    for i in range(4):
			self.pots[i].delete(0,tk.END)
		    self.pots[0].insert(0,info[68:70])
		    self.pots[1].insert(0,info[71:73])
		    self.pots[2].insert(0,info[74:76])
		    self.pots[3].insert(0,info[77:79])
		
		elif info[36:44] == "06121d03":
		   
		    for i in range(4):
			self.bgcks[i].delete(0,tk.END)
		    self.bgcks[0].insert(0,info[65:70].replace(" ","").lstrip("0"))
		    self.bgcks[1].insert(0,info[71:76].replace(" ","").lstrip("0"))
		    self.bgcks[2].insert(0,info[77:82].replace(" ","").lstrip("0"))
		    self.bgcks[3].insert(0,info[83:88].replace(" ","").lstrip("0"))
		    
		elif info[36:44] == "06125903":
		    self.SN = info[65:88].replace(" ","").decode("hex")
		    
		elif info[36:44] == "06107903":
		    self.PN = info[65:76].replace(" ","")
		#print("PN: ", self.PN)
		#print("SN :", self.SN)
		
		
	
		
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
	global arraySmokeP, arrayConcen, smkP, conc
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
	    
	if val[5] == '0':
	    self.leds[5].create_oval(0,0,15,15, fill="grey")
	if val[5] == '1':
	    self.leds[5].create_oval(0,0,15,15, fill="green2")
	    
	if val[6] == '0':
	    self.leds[6].create_oval(0,0,15,15, fill="grey")
	    if len(arraySmokeP) == 1:
		# on récupere la concentration et la valeur du smoke P pour Alarm Lav OFF
		arraySmokeP.append(float(self.smokeP.get()))
		arrayConcen.append(self.concen.get())
		# On affiche les valeurs
		self.widgets[2][1].configure(text=str(arraySmokeP[1]))
		self.widgets[2][2].configure(text=str(arrayConcen[1]))
		
		if len(smkP) >= 100 :
		    #self.flag = 0
		    # On ajoute les valeurs moyennes
		    arraySmokeP.append(round(np.mean(smkP),3))
		    arrayConcen.append(round(np.mean(conc),3))
		    # On ajoute les valeurs Max
		    arraySmokeP.append(round(np.max(smkP),3))
		    arrayConcen.append(round(np.max(conc),3))
		    # On ajoute les valeurs min
		    arraySmokeP.append(round(np.min(smkP),3))
		    arrayConcen.append(round(np.min(conc),3))
		    
		    # On affiche les resultats dans le tableau
		   
		    self.widgets[3][1].configure(text=str(arraySmokeP[2]))
		    self.widgets[4][1].configure(text=str(arraySmokeP[3]))
		    self.widgets[5][1].configure(text=str(arraySmokeP[4]))
		    		    
		    self.widgets[3][2].configure(text=str(arrayConcen[2]))
		    self.widgets[4][2].configure(text=str(arrayConcen[3]))
		    self.widgets[5][2].configure(text=str(arrayConcen[4]))
		    # On active le bouton calibrer
		    self.BoutonCalib.configure(state='normal')
		    # On active le bouton clear
		    self.BoutonClear.configure(state='normal')
		    # on affiche une message d'information
		    showinfo("Test de fumée Terminé","Les résultats sont affichés dans le tableau. Merci de vider complètement la fumée avant de calibrer si nécessaire.")
		   
		else:
		    # on affiche une message d'information
		    showerror("Données insuffisantes!","Pas assez d'acquisitions pour calculer convenablement les valeurs moyennes.Veuillez recommencer")
		
	if val[6] == '1':
	    self.leds[6].create_oval(0,0,15,15, fill="green2")
	    #self.flag = 0
	    val1 = self.smokeP.get()
	    val2 = self.concen.get()
	    if len(arraySmokeP) == 0:
		# on récupere la concentration et la valeur du smoke P pour Alarm Lav ON
		arraySmokeP.append(float(val1))
		arrayConcen.append(val2)
		# On affiche les resultats dans le tableau
		self.widgets[1][1].configure(text=str(arraySmokeP[0]))
		self.widgets[1][2].configure(text=str(arrayConcen[0]))
		
	    
	    if val2 != '' and float(val2) >= 1 and float(val2) <=1.4:
		conc.append(float(val2))
		smkP.append(float(val1))
		if len(smkP) == 100 :
		    # on affiche une message d'information
		    showinfo("Données suffisantes!","Vous pouvez videz doucement la fumée")
	    
	if val[7] == '0':
	    self.leds[7].create_oval(0,0,15,15, fill="grey")
	if val[7] == '1':
	    self.leds[7].create_oval(0,0,15,15, fill="green2")
	    
	print arraySmokeP
	print arrayConcen
	print len(conc)
    
   
	
    def stop(self):
	self.flag = 0

##############################################
class CalibrationLog(threading.Thread):
    def __init__(self,concen):
        threading.Thread.__init__(self)
        self.concentration = concen

    def run(self):
	self.flag = 1
	# On calcule le Zero de reference reading en determinant la constante de l'équation
	os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp3.txt ')
	file = open("tmp.txt","rb")
	self.k = round(float(file.readlines()[-1].replace(",","")),4)
	file.close()
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	
	# on demande la valeur des backgrounds
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	
	# On demande la valeur des PN et SN
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
		    data=[0x03, 0x00, 0x00, 0x00, 0xff, 0x7f, 0x00, 0x00],
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
	    x = -(y-self.k)/0.0257
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
		if self.fenConc.get() and self.fenConc.get() != "INF":
		    valeurConcentration = float(self.fenConc.get())
		yield t, valeurConcentration, valeurSmokeP 
	    except:
		pass
	    
	    
	   


    def init(self):
	self.ax.set_ylim(-1, 15)
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
	if self.ymax >= 100 and y <= 12:
	    self.ax.set_ylim(self.ymin, 12)
	    self.ax.figure.canvas.draw()
	self.lineSmoke.set_data(self.xdata, self.ydata)
	self.lineConc.set_data(self.xdata, self.concData)
	


	return self.lineSmoke,self.lineConc,

class Annexes:
    def __init__(self):
	self.var = "OK"
	
    def clear(self):
	global arraySmokeP, arrayConcen, smkP, conc
	
	# On reinitialise les listes à 0
	smkP = []
	conc = []
	arraySmokeP = []
	arrayConcen = []
	
    def get_potars(self):
	# on demande la valeur des potars
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	
	# on demande la valeur des backgrounds
	bus = can.interface.Bus()
	msg = can.Message(arbitration_id=0x06103403,
                      data=[0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
    
    def set_potars(self,pots):
	bus = can.interface.Bus()
	#set
	msg1 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x00, 0x00],
                      extended_id=True)
	#clear
	msg2 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x01, 0x01],
                      extended_id=True)
	#clear
	msg3 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x01, 0x01],
                      extended_id=True)
	#Zero
	msg4 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, pots[0], pots[1], pots[2], pots[3], 0x00, 0x01],
                      extended_id=True)
	try:
	    bus.send(msg1)
	    bus.send(msg2)
	    bus.send(msg3)
	    bus.send(msg4)
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
    
