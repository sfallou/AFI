"""import nidaqmx.system

system = nidaqmx.system.System.local()

for device in system.devices:
    print(device)
"""


import os
import time

def mean(fichier):
    file = open(fichier,"rb")
    resultat = file.readlines()[6:505]
    resultat = [s.strip(',\n') for s in resultat]
    file.close()
    print resultat
    dim = len(resultat)
    somme = 0
    for val in resultat:
	somme += float(val)
    print ("Moyenne : ", somme/dim)
    
def mesure():
	try:
	    os.system('sudo /usr/local/bin/natinst/rpi/aiondemand -c 0 -s 500 -t 10000 -v > tmp.txt')
	    mean("tmp.txt")
	except:
	    print ("impossible")



while 1:
    mesure()
    #mean("tmp.txt")
    #time.sleep(0.5)  
