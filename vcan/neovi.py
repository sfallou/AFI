import ics

device = ics.find_devices(ics.NEODEVICE_VCAN3)[0]
print(device.Name, device.SerialNumber)



