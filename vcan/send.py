import ics
device = ics.open_device()
msg = ics.SpyMessage()
msg.ArbIDOrHeader = 0xFF
msg.NetworkID = ics.NETID_HSCAN
msg.Data = (0,1,2,3,4,5,6,7)
ics.transmit_messages(device, msg)
