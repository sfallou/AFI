import ics

device = ics.find_devices()

print(device[0].Name, device[0].SerialNumber)



