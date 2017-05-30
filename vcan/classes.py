# -*-coding:Utf-8 -*

from Tkinter import *
import time
 
class ScrollableCanvas(Frame):
     def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
         
        canvas=Canvas(self,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
  
        vbar=Scrollbar(self,orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
         
        canvas.config(width=450,height=300)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=LEFT,expand=True,fill=BOTH)
         
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW )
 
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)
 
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
 
 
 
class Terminal(Frame):
    # Init
    def __init__(self, fenetre_principale=None):
        Frame.__init__(self, fenetre_principale)
        self.grid()
        self.scrollable_canvas = ScrollableCanvas(self)
        self.scrollable_canvas.grid(row=1,column=1)
#####################################

class Trame:
    def __init__(self):
        self.id=0

    def formatage_trame(self,fichier):
        self.trames = []
        self.timestamp = []
        self.arbID = []
        self.dlc = []
        self.data = []
        file = open(fichier,"r")
        for line in file:
            #resultat = []
            tab = line.split()
            self.timestamp.append(tab[1])
            self.arbID.append(tab[3])
            self.dlc.append(tab[6])
            self.data.append(" ".join(tab[7:]))
            self.trames.append(self.timestamp)
            self.trames.append(self.arbID)
            self.trames.append(self.dlc)
            self.trames.append(self.data)
        return self.trames

    def formatage_trame2(self,fichier):
        self.resultat = []
        file = open(fichier,"r")
        for line in file:
            tab = line.split()
            self.resultat.append([tab[1],tab[3],tab[6]," ".join(tab[7:])])
        return self.resultat

    def valeurs_config(self,fichier):
        donnees_brutes = self.formatage_trame(fichier)[3] 
        self.pn = donnees_brutes[1].replace(" ","")[8:14]+"-"+donnees_brutes[1].replace(" ","")[14:]
        self.sn = donnees_brutes[3].replace(" ","")[8:].decode("hex")
        self.sn = self.sn+donnees_brutes[5].replace(" ","")[8:14].decode("hex")
        self.date_fab = donnees_brutes[13].replace(" ","")[8:12]+"/"+donnees_brutes[13].replace(" ","")[12:14]+"/"+donnees_brutes[13].replace(" ","")[14:]
        self.crc_mep = donnees_brutes[25].replace(" ","")[8:]
        self.crc_bbp = donnees_brutes[27].replace(" ","")[8:]

        return self.pn,self.sn,self.date_fab,self.crc_mep,self.crc_bbp

    #def reception(fichier):

##############################################################################

if __name__ == "__main__":
    trame= Trame()
    datas = trame.formatage_trame2("trame.txt")
    #print(trame.valeurs_config("trame.txt")[0])
    root = Tk()
    root.title("tk")
    interface = Terminal(fenetre_principale=root)
    #interface.ajouter_trame(datas[0],0)
    interface.mainloop()
