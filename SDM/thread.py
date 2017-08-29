import threading
import Queue
import random
import math
import time
import Tkinter
import can

can_interface = 'ics0can0'
bus = can.interface.Bus(can_interface, bustype='socketcan_ctypes')
bgColor = 'light yellow' # Background color
random.seed(0)

class App:
    def __init__(self, queue, width=100, height=150):
        self.width, self.height = width, height
	#self.trame, self.concentration = "", ""
        self.canvas = Tkinter.Text(width=width, height=height, bg="white")
        self.canvas.pack(fill='none', expand=False)
        

        self.queue = queue
        self.canvas.after(1, self.check_queue)

    def check_queue(self):
        try:
            trame, concentration = self.queue.get(block=False)
        except Queue.Empty:
            pass
        else:
            self.write_message(trame, concentration)
        self.canvas.after(1, self.check_queue)

    

    def write_message(self, trame="", conc=""):
        self.canvas.insert(Tkinter.INSERT,trame)
	self.canvas.insert(Tkinter.INSERT,conc)
	
def queue_create(queue, running):
    while True:
	message = bus.recv()
        if message:
	    conc = 1.2
            queue.put((trame, conc))
        time.sleep(0) # Effectively yield this thread.

root = Tkinter.Tk()


queue = Queue.Queue()

app = App(queue)
app.write_message()
app.canvas.bind('<Destroy>', lambda x: (running.pop(), x.widget.destroy()))

thread = threading.Thread(target=queue_create, args=queue)
thread.start()

root.mainloop()
