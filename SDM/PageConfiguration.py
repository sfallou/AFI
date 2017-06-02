# -*-coding:Utf-8 -*

from Tkinter import *
from tkMessageBox import *


    
# la classe PageConfiguration
class PageConfiguration(Frame):
    # Init
    def __init__(self,fenetre_principale=None):
        Frame.__init__(self)
        self.pack()
        self.configure(bg='white')
    

##############################################################################

if __name__ == '__main__':
    root = Tk()
    root.title("Configuration")
    pageConfiguration = PageConfiguration(fenetre_principale=root)
    pageConfiguration.mainloop()
    
