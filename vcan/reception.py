# -*-coding:Utf-8 -*

import can

can_interface = 'ics0can0'
bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')

file = open("trame.txt","w")
print "---------- Welcome --------------"
while 1:	
    message = bus.recv()
    if message is None:
	pass
    else :
	print(message)
	file.write(str(message)+"\n")

file.close()
