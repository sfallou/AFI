from __future__ import print_function
import can
import time


def send_one():
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x00400103,
                      data=[0x01, 0x80, 0x03, 0x93, 0x00, 0x00, 0x00, 0x01],
                      extended_id=True)
    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")


      
if __name__ == "__main__":
    send_one()
    
#01 80 03 93 00 00 00 01 not good

