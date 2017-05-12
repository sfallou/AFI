# -*-coding:Utf-8 -*

import ics
print("---- Reception -----")
device = ics.open_device()
messages, errors = ics.get_messages(device)
#print(messages[0])

for i in range((50):
	print("-------------------------")
	print("message  ", i)
	print("ArbIDOrHeader ", hex(messages[i].ArbIDOrHeader))
	print("Data ", messages[i].Data)
	print("MiscData ", hex(messages[i].MiscData))
	print("AckBytes ", messages[i].AckBytes)
	print("NetworkID ", hex(messages[i].NetworkID))
	print("NumberBytesData ", hex(messages[i].NumberBytesData))
	print("NumberBytesHeader ", hex(messages[i].NumberBytesHeader ))
	print("Protocol ", hex(messages[i].Protocol ))
	print("StatusBitField ",hex( messages[i].StatusBitField ))
	print("Nombre Erreurs", errors)


