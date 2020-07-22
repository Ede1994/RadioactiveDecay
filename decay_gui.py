#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:40:43 2020

@author: eric
"""

import tkinter as tk

import math
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# nuclides dictionary with half life in s
nuclides = {
		"C-11": [1224.0, "Img/c11.png"],
		"N-13": [597.9, "Img/n13.png"],
        "O-15": [122.24, "Img/o15.png"],
        "F-18": [6.586*10**3, "Img/f18.png"],
		"Cu-62": [582, "Img/cu62.png"],
		"Cu-64": [45721.1, "Img/cu64.png"],
		"Ga-68": [4080, "Img/ga68.png"],
		"Ge-68": [2.376*10**7, "Img/ge68.png"],
		"Br-76": [58700, "Img/br76.png"],
		"Rb-82": [75, "Img/rb82.png"],
		"Zr-89": [4704*60, "Img/zr89.png"],
		"Tc-99m": [21.624*10**3, "Img/tc99m.png"],
        "I-124": [6013.44*60, "Img/i124.png"],
        "I-125": [59.49*24*60*60, "Img/i125.png"],
		"I-131": [693*10**3, "Img/i131.png"]
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
# do nothing button
def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin,
                       text="Do nothing button"
                       )
    button.pack()

# function for current time button
def currentTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    e4.insert(10,dt_string)

# text for impressum button
def helpButton():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin,
                       text="Possible nuclides: C-11, N-13, O-15, F-18, Cu-62, Cu-64, Ga-68, Ge-68, Br-76, Rb-82, Zr-89, Tc-99m, I-124, I-125, I-131"
                       )
    button.pack()

# text for impressum button
def impressum():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin,
                       text="Impressum: \nAuthor: Eric Einspänner \n (Institute of Nuclear Medicine, UMG (Germany)) \n This program is free software."
                       )
    button.pack()

def buttonCalculate():
    # get the values
	# nuclid
    nuclid_input = e1.get()
    if nuclid_input == '':
	    print('Error: No nuclid choosen!')
	# activity
    activity = e2.get()
    if activity == '':
	    print('Error: No activity choosen!')
    else:
	    activity = float(activity)
	# starting time
    date = e3.get()
    if date == '':
	    print('Error: No starting time choosen!')
    d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    start_time = time.mktime(d.timetuple())
	# ending time
    date = e4.get()
    if date == '':
	    print('Error: No ending time choosen!')
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
    ax = fig.add_subplot(221)
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
 
    # show decay scheme
    ax2 = fig.add_subplot(222)
    img=mpimg.imread(img_path)
    ax2 = plt.imshow(img)
    plt.show()

    # results
    label6.config(text=str(elapsed_time))
    label8.config(text=str(activity_elapsed_time))


# start GUI
root = tk.Tk()
root.title("Radioactive Decay")
root.geometry("1000x300")

# define menu
menubar = tk.Menu(root)

# file menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

# help menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=helpButton)
helpmenu.add_command(label="Impressum", command=impressum)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# define labels for nuclid and activity
label1 = tk.Label(root, text="Nuclid (e.g. F-18):").grid(row=0)
label2 = tk.Label(root, text="Activity in Bq (e.g. 100):").grid(row=0, column=3)
label3 = tk.Label(root, text="Starting Time (d/m/Y H:M:S):").grid(row=1)
label4 = tk.Label(root, text="Ending Time (d/m/Y H:M:S):").grid(row=1, column=3)
label5 = tk.Label(root, text="Elapsed Time (s):").grid(row=3)
label6 = tk.Label(root, bg='gray', width='12', text="")
label6.grid(row=3, column=1)
label7 = tk.Label(root, text="Ending activity (Bq):").grid(row=3, column=3)
label8 = tk.Label(root, bg='gray', width='12', text="")
label8.grid(row=3, column=4)

# define entries for user input
e1 = tk.Entry(root)
e1.grid(row=0, column=1)
e2 = tk.Entry(root)
e2.grid(row=0, column=4)
e3 = tk.Entry(root)
e3.grid(row=1, column=1)
e4 = tk.Entry(root)
e4.grid(row=1, column=4)

# define button position
buttonCalculate = tk.Button(text='Calculate!', width='10', bg='red', command=buttonCalculate)
buttonCalculate.grid(row=3, column=5, padx='5', pady='5')

buttonTime = tk.Button(text='Time', width='10', bg='yellow', command=currentTime)
buttonTime.grid(row=1, column=5, padx='5', pady='5')

root.mainloop()