# -*-coding:Utf-8 -*

import can
import Queue
import threading
import time
import os


can_interface = 'ics0can0'
bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')

#file = open("trame.txt","w")
print "---------- Welcome --------------"
"""while 1:	
    message = bus.recv()
    if message is None:
	pass
    else :
	print(message)
	#file.write(str(message)+"\n")

#file.close()
"""


def check_queue(q):
    while True:
	trame, conc = q.get()
	print(trame)
	print("conc: ",conc)

def queue_create(q):
    # On calcule le Zero de reference reading en determinant la constante de l'équation
    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp3.txt ')
    file = open("tmp.txt","rb")
    k = round(float(file.readlines()[-1].replace(",","")),4)
    file.close()
    while True:
	message = bus.recv()
        if message:
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 1 -t 1 -v | tee tmp.txt > tmp2.txt')
	    file = open("tmp.txt","rb")
	    resultat = float(file.readlines()[-1].replace(",",""))
	    file.close()
	    y = round(resultat,4)
	    x = -(y-k)/0.0257
            q.put((message,x))
        #time.sleep(0) # Effectively yield this thread.

def get_potars():
    # on demande la valeur des potars
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x06103403,
		    data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
		    extended_id=True)
    for i in range(20):
	try:
	    bus.send(msg)
	except can.CanError:
	    print("Message NOT sent")
	time.sleep(2)
	
    """# on demande la valeur des backgrounds
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x06103403,
		    data=[0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
		    extended_id=True)
    try:
	bus.send(msg)
    except can.CanError:
	print("Message NOT sent")
    """
    

q = Queue.Queue()
t = threading.Thread(target=check_queue,args=[q])
t.daemon = True
t.start()

t2 = threading.Thread(target=get_potars)
t2.daemon = True
t2.start()

queue_create(q)


