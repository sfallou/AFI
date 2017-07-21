#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import Tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
#---------End of imports

fig = plt.Figure()

x = np.arange(0, 2*np.pi, 0.01)        # x-array

def animate(i):
    line.set_ydata(np.sin(i/10.0))  # update the data
    time.sleep(1)
    return line,

root = Tk.Tk()

label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ax = fig.add_subplot(111)
line, = ax.plot(x, np.sin(x))
ani = animation.FuncAnimation(fig, animate, np.arange(1, 900), interval=25, blit=False)

Tk.mainloop()
