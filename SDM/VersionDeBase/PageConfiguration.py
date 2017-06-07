# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *
import ConfigPage_connexion as Connexion
#import ConfigPage_lecture as Lecture
#import ConfigPage_ecriture as Ecriture

import LeCorps as Corps

bgColor = 'white' # Background color
fgColor = "#03224C" 
WinWidth = 400 # largeur fenetre
WinHigh = 200 # hauteur fenetre
titreFont = ('Helvetica', 14) # Police des Titres 
fontSimple =('Helvetica', 12) # police des textes basiques
entryLength = 10 # Taille des Entry
buttonLength = 10 # Taille des boutons
buttonColor = '#C0C0C0' # Taille des boutons

    
# la classe PageConfiguration
class PageConfiguration(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
        self.pack()
	self.configure(bg=bgColor)
	# Les différentes zone de l'interface
	self.zoneConnexion = Frame(self,bg=bgColor)
	self.zoneConnexion.pack()
	self.zonePrincipale = Frame(self,bg=bgColor)
	self.zonePrincipale.pack()
	
	# Le contenu des zone
	self.page_connexion = Connexion.Connexion(fenetre_principale=self.zoneConnexion)
	self.page_principale = Corps.LeCorps(fenetre_principale=self.zoneConnexion)

##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Configuration")
    root.configure(bg=bgColor)
    pageConfiguration = PageConfiguration(fenetre_principale=root)
    pageConfiguration.mainloop()
    
