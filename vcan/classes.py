# -*-coding:Utf-8 -*
from __future__ import print_function
import can
import time
from threading import Thread

#can_interface = 'ics0can0'
#bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')

 
        


class Communication(Thread):
    def __init__(self,canal):
        Thread.__init__(self)
        self.can_interface = canal
        self.bus = can.interface.Bus(self.can_interface, bustype='socketcan_ctypes')

    def formatage_trame(self,trame):
        self.resultat = []
        self.tab = trame.split()
        self.timestamp = tab[1]
        self.arbID = tab[3]
        self.dlc = tab[6]
        self.data = " ".join(tab[7:])
        self.resultat.append(timestamp)
        self.resultat.append(arbID)
        self.resultat.append(dlc)
        self.resultat.append(data)
        return self.resultat

    def reception_trame(self,duree):
        file = open("trames.txt","w")
        while 1:
            message = self.bus.recv(duree)
            if message is None:
                break
            else :
                print(message)
                info = str(message)+"\n" 
                file.write(info)
                compteur = compteur+1

        file.close()

    def read_config(self):
        # Les données à envoyées
        datas = [
            [0x31, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x34, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x01, 0x95, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x01, 0x99, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00],
            [0x31, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00],
        ]
        messages = []
        bus_can = can.interface.Bus()
        for d in datas:
            messages.append(can.Message(arbitration_id=0x7bf,data=d,extended_id=False))
        for msg in messages:
            try:
                bus_can.send(msg)
                print("Message sent on {}".format(bus_can.channel_info))
            except can.CanError:
                print("Message NOT sent")
            time.sleep(0.3)

    def run(self):
        self.reception_trame(15)
        self.read_config()
        
        

        

##############################################################################

if __name__ == '__main__':
    #trame = Trame()
    #msg = " Timestamp: 1495615614.564641        ID: 07bf    000    DLC: 8    31 00 00 14 00 00 00 00"
    #print trame.formatage_trame(msg)

    # création des threads
    comm_1 = Communication('ics0can0')
    comm_2 = Communication('ics0can0')

    # Lancement des threads
    comm_1.start()
    comm_2.start()

    # Attend que les threads se terminent
    comm_1.join()
    comm_2.join()

