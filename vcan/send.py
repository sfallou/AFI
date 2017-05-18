from __future__ import print_function
import can


def send_one():
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=0x7bf,
                      data=[49, 0, 0, 20, 0, 0, 0, 0],
                      extended_id=False)
    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

if __name__ == "__main__":
    send_one()
