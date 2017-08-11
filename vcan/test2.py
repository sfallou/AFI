#!/usr/bin/python
"""
- read output from a subprocess in a background thread
- show the output in the GUI
"""
import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
from Tkinter import *
from Queue import Queue, Empty
import time

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class DisplayLogs(Frame):
    def __init__(self, cmd, master=None):
	Frame.__init__(self, master)
        self.pack()
        self.build_widgets()
        self.consigne = cmd

        # start dummy subprocess to generate some output
        self.process = Popen(self.consigne, stdout=PIPE)
	
	self.t = Thread(target=self.reader_thread)
        self.t.daemon = True # close pipe if GUI process exits
        
    def run_script(self):
	self.t.start()
        sys.stdout = self
        sys.stdout = sys.__stdout__
	#sys.stderr = __stderr__

    
    def build_widgets(self):
        self.text1 = Text(self)
        self.text1.pack(side=TOP)
        self.button = Button(self)
        self.button["text"] = "Trigger script"
        self.button["command"] = self.run_script
        self.button.pack(side=TOP)

    def reader_thread(self):
        """Read subprocess output and put it into the queue."""
        try:
            with self.process.stdout as pipe:
		#self.text1.insert(INSERT, pipe.getvalue())
                for line in iter(pipe.readline, b''):
		    print(line)
		    self.text1.insert(INSERT, line)
		    time.sleep(0.4)
        finally:
            pass
    
    #def run_script(self):
    #	self.t.start()
	#self.t._stop()


if __name__ == '__main__':
    root = Tk()
    app = DisplayLogs(['python','communication.py'],master=root)
    app.mainloop()
