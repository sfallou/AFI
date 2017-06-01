import sys
sys.path.append("/home/pi/AFI/vcan/")
import communication

print "Hello world!"

def HelloWorld():
    #print "HelloWorldFromDef!"
    interface = 'ics0can0'
    #ask_config = AskConfig()
    #read_config = ReadConfig(interface)
    #read_config.start()
    #ask_config.start()
	
    ask_adress_memory = AskAdressMemory(0x14,'4',"NVM")
    read_adress_memory = ReadAdressMemory(interface)
    read_adress_memory.start()
    ask_adress_memory.start()

