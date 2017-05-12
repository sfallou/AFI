import ics

device = ics.find_devices(ics.NEODEVICE_VCAN3)[0]
print(device.Name, device.SerialNumber)

#device = ics.open_device(123224)
#message, error = ics.get_messages(device)
#print("longeur message", len(messages))
#print(hex(message[0].ArbIDOrHeader))


