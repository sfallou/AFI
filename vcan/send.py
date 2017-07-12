from __future__ import print_function
import can
import time


def send_one():
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x06103403,
                      data=[0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=True)
    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")


      
if __name__ == "__main__":
    send_one() # permet d'avoir le numéro de série et le PN
    


