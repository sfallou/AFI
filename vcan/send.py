from __future__ import print_function
import can
import time


def send_one():
    bus = can.interface.Bus()
    msg1 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, 0x28, 0x28, 0x66, 0x14, 0x00, 0x00],
                      extended_id=True)
    msg2 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, 0x28, 0x28, 0x66, 0x14, 0x01, 0x01],
                      extended_id=True)
    
    msg4 = can.Message(arbitration_id=0x06103403,
                      data=[0x17, 0x0e, 0x28, 0x28, 0x66, 0x14, 0x00, 0x01],
                      extended_id=True)
    try:
        bus.send(msg1)
	bus.send(msg2)
	#bus.send(msg3)
	bus.send(msg4)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

def get_potars():
    # on demande la valeur des potars
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x06103403,
		    data=[0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
		    extended_id=True)
    try:
	bus.send(msg)
    except can.CanError:
	print("Message NOT sent")
	
    # on demande la valeur des backgrounds
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x06103403,
		    data=[0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
		    extended_id=True)
    try:
	bus.send(msg)
    except can.CanError:
	print("Message NOT sent")
      
if __name__ == "__main__":
    send_one() 
    get_potars()
    


