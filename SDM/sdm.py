# -*-coding:Utf-8 -*

from Tkinter import *
from PIL import ImageTk, Image
from tkMessageBox import *
import testReception as tR
import configuration as conf
import calibration as calib
import autres as autr


############################################
bgColor = 'light yellow' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Couleur des boutons
buttonColorMenu = 'steel blue' # Couleur des boutons du menu
tailleBorder = 2 # borderwidth
##############################################    
# la classe SDM (Smoke Detector Maintenance)
class SDM(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Smoke Detector Maintenance')
        self.resizable(0, 0)
	#self.wm_attributes('-type','splash')
        self.configure(bg=bgColor)
	self.geometry("1170x800")
	self.protocol("WM_DELETE_WINDOW", self.quit)
	x = (self.winfo_screenwidth() - self.winfo_reqwidth())/50
	y = (self.winfo_screenheight() - self.winfo_reqheight())/50
	self.geometry("+%d+%d"%(x,y))
	
	####
	self.menu()
	###
	self.testReceptionPage = tR.TestReception(fenetre_principale=self)
	self.testReceptionPage.pack()
	self.configurationPage = conf.Configuration(fenetre_principale=self)
	self.calibrationPage = calib.Calibration(fenetre_principale=self)
	self.autrePage = autr.Autres(fenetre_principale=self)
	
    def menu(self):
        # creation du menu principale
	self.zoneMenu = Frame(self, bd =5, relief =RAISED, bg=bgColor)
	self.zoneMenu.pack(side=TOP)
	self.FenetreMenu = Frame(self.zoneMenu, bd =5, relief =RAISED, bg=bgColor)
	self.FenetreMenu.grid(ipadx=5,row=0, column=0)
	
	self.zoneQuitter = Frame(self.zoneMenu, bd =5, relief =RAISED, bg=bgColor)
	self.zoneQuitter.grid(padx=1,row=0, column=1)
	try:
	    #self.imgExit = ImageTk.PhotoImage(Image.open("./docs/img/exit.png"))
	    self.panelExit = Button(self.zoneQuitter, text="Close", bg="red", bd=1, width=5)
	    self.panelExit.pack()
	except:
	    pass
	################################
        #Logo à gauche entete
        ################################
        
	try:
	    self.frameEntete0 = Frame(self.FenetreMenu, bg =bgColor)
	    self.frameEntete0.grid(row =0, column =0, padx =2)
	    self.logo0 = ImageTk.PhotoImage(Image.open("./docs/img/logo2.jpg"))
	    self.panel0 = Button(self.frameEntete0, image = self.logo0, bd=1, command=self.new)
	    self.panel0.pack( fill = "both", expand = "yes")
	except:
	    pass
	################################
        #Menu
        ################################
	self.test_menu = Button(self.FenetreMenu,text="Test Reception",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.test_reception)
        self.test_menu.grid(padx=2,row=0,column=1)
	self.config_menu = Button(self.FenetreMenu,text="Configuration",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.configuration)
        self.config_menu.grid(padx=2,row=0,column=2)
	self.calib_menu = Button(self.FenetreMenu,text="Calibration",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.calibration)
        self.calib_menu.grid(padx=2,row=0,column=3)
	self.pab_menu = Button(self.FenetreMenu,text="PAB",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.configuration)
        self.pab_menu.grid(padx=2,row=0,column=4)
	self.autre_menu = Button(self.FenetreMenu,text="Options",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.autre)
        self.autre_menu.grid(padx=2,row=0,column=5)
	self.help_menu = Button(self.FenetreMenu,text="Help",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.configuration)
        self.help_menu.grid(padx=2,row=0,column=6)
	self.about_menu = Button(self.FenetreMenu,text="About",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColorMenu,command=self.autre)
        self.about_menu.grid(padx=2,row=0,column=7)
        
	
	################################
        #Logo à droite entete
        ################################
       
	"""self.frameEntete = Frame(self.FenetreMenu, bg =bgColor)
	self.frameEntete.grid(row =0, column =7, padx =2)
	self.logo = ImageTk.PhotoImage(Image.open("./docs/img/logo1.jpg"))
	self.panel = Label(self.frameEntete, image = self.logo, bd=1)
        self.panel.pack( fill = "both", expand = "yes")
	"""
    def new(self):
	self.testReceptionPage.destroy()
	self.configurationPage.destroy()
	self.calibrationPage.destroy()
	self.autrePage.destroy()
	
	self.testReceptionPage = tR.TestReception(fenetre_principale=self)
	self.testReceptionPage.pack()
	self.configurationPage = conf.Configuration(fenetre_principale=self)
	self.calibrationPage = calib.Calibration(fenetre_principale=self)
	self.autrePage = autr.Autres(fenetre_principale=self)
    
    def cacher(self):
	self.testReceptionPage.pack_forget()
	self.configurationPage.pack_forget()
	self.calibrationPage.pack_forget()
	self.autrePage.pack_forget()
    
    def test_reception(self):
	self.cacher()
	self.testReceptionPage.pack()
	
    def configuration(self):
	self.cacher()
	self.configurationPage.pack()
	
    def calibration(self):
	self.cacher()
	self.calibrationPage.pack()
    
    def autre(self):
	self.cacher()
	self.autrePage.pack()
    def rien(self):
	pass
    
     ######################################################
    def quit(self):
	# On arrete le processus python
	try:
	    os.system('sudo pkill python')
	except:
	    print ("impossible d'arrêter python")

##############################################################################

if __name__ == '__main__':
    Sdm = SDM()
    Sdm.mainloop()
