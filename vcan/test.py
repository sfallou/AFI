import ics

device = ics.find_devices(ics.NEODEVICE_VCAN3)[0]
ics.open_device(device)
#ics.load_default_settings(device)
#ics.get_messages(device,False,0.1)
#msg = 
