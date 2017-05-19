from __future__ import print_function
import can
import time


def send_one():
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x7bf,
                      data=[0xB1, 0x00, 0x00, 0x24, 0x19, 0x05, 0x17, 0x20],
                      extended_id=False)
    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")


      
if __name__ == "__main__":
    send_one()
    
