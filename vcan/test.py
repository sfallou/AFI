import ics

devices = ics.find_devices()
#ics.open_device(device)
#ics.load_default_settings(device)
#ics.get_messages(device,False,0.1)

for device in devices:
	print(device.Name,device.SerialNumber)
