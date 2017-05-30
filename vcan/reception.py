# -*-coding:Utf-8 -*

import can

can_interface = 'ics0can0'
bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')

file = open("trame.txt","w")
compteur = 0
while 1:
	compteur = compteur + 1
	message = bus.recv(5)
	if message is None:
		break	
	else :
		print(message)
		info = str(message)+"\n" 
		file.write(info)
file.close() 
		
