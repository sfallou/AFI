# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import testReception as tR
import configuration as conf

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
    
# la classe SDM (Smoke Detector Maintenance)
class SDM(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Smoke Detector Maintenance')
        self.resizable(0, 0)
        self.configure(bg=bgColor)
	self.geometry("1170x630")
	"""x = (self.winfo_screenwidth() - self.winfo_reqwidth())/50
	y = (self.winfo_screenheight() - self.winfo_reqheight())/50
	self.geometry("+%d+%d"%(x,y))
	"""
	####
	self.menu()
	###@
	self.testReceptionPage = tR.TestReception(fenetre_principale=self)
	self.testReceptionPage.pack()
	self.configurationPage = conf.Configuration(fenetre_principale=self)
	
    def menu(self):
        # creation du menu principale
        """menubar = Menu(self,bg=bgColor)
        self.config(menu=menubar)
        menuTestReception = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.test_reception)
        menubar.add_cascade(label="Test de Reception", menu=menuTestReception)
	menuConfiguration = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.configuration)
        menubar.add_cascade(label= "Configuration", menu=menuConfiguration)
        menuCalibration = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.rien)
        menubar.add_cascade(label= "Calibration", menu=menuCalibration)
        menuPAB = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.rien)
        menubar.add_cascade(label= "PAB", menu=menuPAB)
        menuHelp = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.rien)
        menubar.add_cascade(label= "Help", menu=menuHelp)
        menuAbout = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.rien)
        menubar.add_cascade(label= "About", menu=menuAbout) 
	"""
	self.FenetreMenu = Frame(self, bd =5, relief =RAISED, bg=bgColor)
	self.FenetreMenu.pack(side=TOP)
	################################
        #Menu
        ################################
	self.test_menu = Button(self.FenetreMenu,text="Test Reception",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.test_reception)
        self.test_menu.grid(padx=2,row=0,column=0)
	self.config_menu = Button(self.FenetreMenu,text="Configuration",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.configuration)
        self.config_menu.grid(padx=2,row=0,column=1)
	self.calib_menu = Button(self.FenetreMenu,text="Calibration",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.configuration)
        self.calib_menu.grid(padx=2,row=0,column=2)
	self.pab_menu = Button(self.FenetreMenu,text="PAB",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.configuration)
        self.pab_menu.grid(padx=2,row=0,column=3)
	self.help_menu = Button(self.FenetreMenu,text="Help",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.configuration)
        self.help_menu.grid(padx=2,row=0,column=4)
	self.about_menu = Button(self.FenetreMenu,text="About",bd=2, width=9, relief=RAISED, overrelief=RIDGE, bg=buttonColor,command=self.configuration)
        self.about_menu.grid(padx=2,row=0,column=5)
        ################################
        #L'entete
        ################################
        
        self.textEntete=Label(self.FenetreMenu,text='Air France Industrie ', width=50,bd=1, bg ='#03224C', relief=RAISED, fg="#ff0000", font=('Helvetica', 14))
        self.textEntete.grid(row =0, column =6, padx =2)
        
	
    def cacher(self):
	self.testReceptionPage.pack_forget()
	self.configurationPage.pack_forget()
    
    def test_reception(self):
	self.cacher()
	self.testReceptionPage.pack()
	
    def configuration(self):
	self.cacher()
	self.configurationPage.pack()
    
    def rien(self):
	pass
	

##############################################################################

if __name__ == '__main__':
    Sdm = SDM()
    Sdm.mainloop()
