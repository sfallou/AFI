#!/usr/bin/python
"""
- read output from a subprocess in a background thread
- show the output in the GUI
"""
import sys
from threading import Thread
from classes import *

try:
    import Tkinter as tk
    from Queue import Queue, Empty
except ImportError:
    import tkinter as tk # Python 3
    from queue import Queue, Empty # Python 3

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class DisplayLogs:
    def __init__(self, root):
        self.root = root
        #    Output chain: file.readline -> queue -> label)
        q = Queue(maxsize=1024)  # limit output buffering
        t = Thread(target=self.reader_thread, args=[q])
        t.daemon = True # close pipe if GUI process exits
        t.start()

        self.update(q) # start update loop

    def reader_thread(self, q):
        """Read file output and put it into the queue."""
        try:
            fic = open("trame.txt","r")
            for line in fic:
                q.put(line)
        finally:
            q.put(None)

    def update(self, q):
        """Update GUI with items from the queue."""
        for line in iter_except(q.get_nowait, Empty): # display all content
            tk.Label(self.root.scrollable_canvas.interior, text=line, bg="white", font=(None,10)).pack(padx=2, fill='both')
            break # display no more than one line per 40 milliseconds
        self.root.after(40, self.update, q) # schedule next update

    def quit(self):
        #self.process.kill() # exit subprocess if GUI is closed (zombie!)
        self.root.destroy()

##############################################################################

if __name__ == '__main__':
    interface = Tk()
    interface.configure(bg='white')
    root = Terminal(fenetre_principale=interface)

    #root = tk.Tk()
    #root.configure(bg="white")
    app = DisplayLogs(root)
    #root.protocol("WM_DELETE_WINDOW", app.quit)
    # center window
    #root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.mainloop()
