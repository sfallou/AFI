import ics
print("---- Reception -----")
device = ics.open_device()
messages, errors = ics.get_messages(device)
print("ARB-ID ", hex(messages[0].ArbIDOrHeader))
print("Data ", messages[0].Data)
print("Erreur", errors)

