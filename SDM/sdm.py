# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import testReception as tR

bgColor = 'white' # Background color
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
        self.geometry("1170x630")
        self.resizable(0, 0)
        self.configure(bg=bgColor)
	self.menu()
	self.test_reception()
	
    def menu(self):
        # creation du menu principale
        menubar = Menu(self,bg=bgColor)
        self.config(menu=menubar)
        menuTestReception = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label="Test de Reception", menu=menuTestReception)
        menuCalibration = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "Calibration", menu=menuCalibration)
        menuPAB = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "PAB", menu=menuPAB)
        menuHelp = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "Help", menu=menuHelp)
        menuAbout = Menu(menubar,tearoff=0, bg='#03224C', postcommand=self.quit)
        menubar.add_cascade(label= "About", menu=menuAbout) 
        
        ################################
        #L'entete
        ################################
        self.entete = Frame(self, bd =1, relief =RAISED)
        self.entete.pack(side=TOP)
        self.textEntete=Label(self.entete,text='Air France Industrie ', width=900,bd=1, bg ='#03224C', relief=RAISED, fg="#ff0000", font=('Helvetica', 14))
        #self.textEntete.grid(row =0, column =0, columnspan =3, padx =1, pady =1)
        self.textEntete.pack(side=TOP)
	
    def test_reception(self):
	tR.TestReception(fenetre_principale=self)

##############################################################################

if __name__ == '__main__':
    Sdm = SDM()
    Sdm.mainloop()
