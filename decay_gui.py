#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:40:43 2020

@author: eric
"""

import tkinter as tk
from PIL import Image, ImageTk

import math
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# nuclides dictionary with half life in s
nuclides = {
        "O-15": [122.24, "Img/o15.png"],
        "N-13": [597.9, "Img/n13.png"],
		"Tc-99m": [21.624*10**3, "Img/tc99m.png"],
        "I-131": [693*10**3, "Img/i131.png"],
		"F-18": [6.586*10**3, "Img/f18.png"]
		}


# functions: decay
# definition decay constant factor
def decay_const(t):
	# λ = ln(2) / t (half)
	decay_const = math.log(2) / t
	return decay_const


# equation radioactive decay
def decay_equation(a0,c,t):
	# A = A0 * e^(- λ * t)
	a = int(a0 * math.exp(-c * t))
	return a

# functions: GUI
def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin, text="Do nothing button")
    button.pack()

def impressum():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin, text="Impressum: \n Author: Eric Einspänner \n (Institute of Nuclear Medicine, UMG (Germany)) \n This program is free software.")
    button.pack()

def buttonCalculate():
    # get the values
    nuclid_input = e1.get()
    activity = float(e2.get())
    date = e3.get()
    d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    start_time = time.mktime(d.timetuple())
    date = e4.get()
    d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    end_time = time.mktime(d.timetuple())

    # processing of the data
    for key in nuclides:
	    if nuclid_input == key:
	       nuclid = key
	       half_life = float(nuclides[key][0])
	       img_path = str(nuclides[key][1])

    elapsed_time = end_time - start_time
	
    activity_elapsed_time = decay_equation(activity, decay_const(half_life), elapsed_time)
    
	# set up loop
    dt = 1
    t = 0.0

    alist = []
    tlist = []


    # while loop until quadruple half life achieved
    while t < (half_life * 4):
	    a = decay_equation(activity, decay_const(half_life), t)

	    alist.append(a)
	    tlist.append(t)
	
	    t += dt


    # list with 1st, 2nd and 3rd half life for timesteps in plot
    half_life_timesteps = [half_life, half_life*2, half_life*3]
	
	# plot graph of activity depends on time
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line, = ax.plot(tlist, alist, color='#ee8d18', lw=2)

    # plot half life timesteps
    for xcoord in half_life_timesteps:
        plt.axvline(x = xcoord, color='red', linestyle='--', linewidth='0.33')

    # plot single point (elapsed time)
    ax.plot([elapsed_time], [activity_elapsed_time], 'o')
    ax.annotate('You are here!',
            xy=(elapsed_time, activity_elapsed_time),
            )

    # set up labeling
    plt.title('Nuclid: {}, Half life: {} s, Activity: {} Bq'.format(nuclid, half_life, activity))
    plt.xlabel('Time (s)')
    plt.ylabel('Activity (Bq)')
    plt.show()

    # show decay scheme
    img=mpimg.imread(img_path)
    imgplot = plt.imshow(img)
    plt.show()

    # results
    label6.config(text=str(elapsed_time))
    label8.config(text=str(activity_elapsed_time))


root = tk.Tk()
root.title("Radioactive Decay")
root.geometry("1000x700")

# define menu
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="Impressum", command=impressum)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# define labels for nuclid and activity
label1 = tk.Label(root, text="Nuclid (e.g. F-18):").grid(row=0)
label2 = tk.Label(root, text="Activity in Bq (e.g. 100):").grid(row=0, column=3)
label3 = tk.Label(root, text="Starting Time (d/m/Y H:M:S):").grid(row=1)
label4 = tk.Label(root, text="Ending Time (d/m/Y H:M:S):").grid(row=1, column=3)
label5 = tk.Label(root, text="Elapsed Time (s):").grid(row=3)
label6 = tk.Label(root, bg='gray', width='12', text="").grid(row=3, column=1)
label7 = tk.Label(root, text="Ending activity (Bq):").grid(row=3, column=3)
label8 = tk.Label(root, bg='gray', width='12', text="").grid(row=3, column=4)

# define entries for user input
e1 = tk.Entry(root).grid(row=0, column=1)
e2 = tk.Entry(root).grid(row=0, column=4)
e3 = tk.Entry(root).grid(row=1, column=1)
e4 = tk.Entry(root).grid(row=1, column=4)

# define button position
buttonStart = tk.Button(text='Calculate!', width='6', bg='red', command=buttonCalculate)
buttonStart.grid(row=1, column=5, padx='5', pady='5')

# image, radioactive decay
image1 = Image.open("/home/eric/Dokumente/PythonProjects/RadioactiveDecay/Img/f18.png")
image1 = image1.resize((250, 250))
image1 = ImageTk.PhotoImage(image1)
panel1 = tk.Label(root, image = image1)
panel1.grid(row=2, column=0, columnspan=2, rowspan=1)

# image, decay scheme
image2 = Image.open("/home/eric/Dokumente/PythonProjects/RadioactiveDecay/Img/f18.png")
image2 = image2.resize((250, 250))
image2 = ImageTk.PhotoImage(image2)
panel2 = tk.Label(root, image = image2)
panel2.grid(row=2, column=3, columnspan=2, rowspan=1)


root.mainloop()