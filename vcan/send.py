import ics
device = ics.open_device()
msg = ics.SpyMessage()
msg.ArbIDOrHeader = 0x7BF
msg.NetworkID = ics.NETID_HSCAN
msg.Data = (31,0,0,4,0,0,0,0)
ics.transmit_messages(device, msg)
