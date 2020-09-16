#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2020

Author: Eric Einspänner, Institute of Nuclear Medicine, UMG (Germany)

This program is free software.
"""

import tkinter as tk
from tkinter import ttk

import math
import time
from datetime import datetime

import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#%% dictionary for nuclides and templates
# empty (template) lists


# for activity (calculation)
alist = []
# for time (calculation)
tlist = []


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


# list of nuclides
nuclides_list = []
for key in nuclides:
    nuclides_list.append(key)


#%% functions


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


# activity plot
def activity_plot(tlist, alist, half_life_timesteps, elapsed_time, activity_elapsed_time, nuclid, half_life, activity):
    fig = Figure(figsize=(5, 4), dpi=60)
    a = fig.add_subplot(111)

    a.plot(tlist, alist, color='#ee8d18', lw=2)

    # plot half life timesteps
    for xcoord in half_life_timesteps:
        a.axvline(x = xcoord, color='red', linestyle='--', linewidth='0.33')

    # plot single point (elapsed time)
    a.plot([elapsed_time], [activity_elapsed_time], 'o')
    a.annotate('You are here!',
            xy=(elapsed_time, activity_elapsed_time),
            )

    a.set_title ('Nuclid: {}, Half life: {} s, Activity: {} Bq'.format(nuclid, half_life, activity))
    a.set_ylabel('Activity (Bq)', fontsize=14)
    a.set_xlabel('Time (s)', fontsize=14)
    return fig


# plot image
def img_plot(img_path):
    # show decay scheme
    fig = Figure(figsize=(5, 4), dpi=60)

    ax2 = fig.add_subplot(111)
    img = mpimg.imread(img_path)
    ax2.imshow(img)
    
    return fig


# Convert seconds to H:M:S
def format_seconds_to_hms(s):
    h = s // (60*60)
    s %= (60*60)
    m = s // 60
    s %= 60
    return "%02i:%02i:%02i" % (h, m, s)


#%% buttons for GUI
# functions: GUI

# do nothing button
def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin,
                       text="Do nothing button"
                       )
    button.pack()


# delete all entries (entry boxes)
def delete_entries():
    cb_nuclid.delete(0, tk.END)
    entry_activity.delete(0, tk.END)
    entry_startingTime.delete(0, tk.END)
    entry_endingTime.delete(0, tk.END)


# function for current time button
def currentTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    entry_startingTime.insert(10,dt_string)
    entry_endingTime.insert(10,dt_string)


# text for impressum button
def helpButton():
    filewin = tk.Toplevel(root)
    filewin.title("Help")
    S = tk.Scrollbar(filewin)
    T = tk.Text(filewin, height=10, width=100)
    S.pack(side=tk.RIGHT , fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote= '''Possible nuclides: 
C-11, N-13, O-15, F-18, Cu-62, Cu-64, Ga-68, Ge-68, Br-76, Rb-82, Zr-89, Tc-99m, I-124, I-125, I-131
- Choose a nuclid (e.g. F-18)
- Define the start activity in Bq (e.g. 100)
- Define the starting date and time, format: d/m/Y H:M:S (e.g. 01/01/2020 10:00:00)
Tip: Press the "Time" Button!
- Define the ending date and time, format: d/m/Y H:M:S (e.g. 01/01/2020 10:50:00)'''
    T.insert(tk.END, quote)


# text for impressum button
def impressum():
    filewin = tk.Toplevel(root)
    filewin.title("Impressum")
    S = tk.Scrollbar(filewin)
    T = tk.Text(filewin, height=10, width=100)
    S.pack(side=tk.RIGHT , fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote= '''Author: Eric Einspänner (Institute of Nuclear Medicine, UMG (Germany))
This program is free software.
eric.einspaenner@med.uni-goettingen.de'''
    T.insert(tk.END, quote)


# calculation button
def buttonCalculate():
    # get the values

	# nuclid
    nuclid_input = cb_nuclid.get()
    if nuclid_input == '':
	    tk.messagebox.showerror(
            "Missing Nuclid",
            "Error: No nuclid choosen!"
        )

	# activity
    activity = entry_activity.get()
    if activity == '':
	    tk.messagebox.showerror(
            "Missing Activity",
            "Error: No activity choosen!"
        )
    else:
	    activity = float(activity)

	# starting time
    date = entry_startingTime.get()
    if date == '':
	    tk.messagebox.showerror(
            "Missing Starting Time",
            "Error: No starting time choosen!"
        )
    d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    start_time = time.mktime(d.timetuple())

	# ending time
    date = entry_endingTime.get()
    if date == '':
	    tk.messagebox.showerror(
            "Missing Ending Time",
            "Error: No ending time choosen!"
        )
    d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    end_time = time.mktime(d.timetuple())
    

    # processing of the data
    # select nuclid specific half-life time
    for key in nuclides:
	    if nuclid_input == key:
	       nuclid = key
	       half_life = float(nuclides[key][0])
	       img_path = str(nuclides[key][1])

    # calculate elapsed time (in s and H:M:S)
    elapsed_time = end_time - start_time
    elapsed_time_hms = format_seconds_to_hms(elapsed_time)


    # Note (for user) that elapsed time is negative
    if elapsed_time < 0:
	    tk.messagebox.showerror(
            "Negative elapsed time!",
            "Ignore time-activity plot!"
        )


	# calculate remaining activity
    activity_elapsed_time = decay_equation(activity, decay_const(half_life), elapsed_time)
 

    # calculation for activity-time plot
	# set up loop
    dt = 1
    t = 0.0

    # while-loop until quadruple half life achieved
    while t < (half_life * 4):
	    a = decay_equation(activity, decay_const(half_life), t)

	    alist.append(a)
	    tlist.append(t)
	
	    t += dt

    # list with 1st, 2nd and 3rd half life for timesteps in plot
    half_life_timesteps = [half_life, half_life*2, half_life*3]


    # call activity plot
    fig = activity_plot(tlist, alist, half_life_timesteps, elapsed_time, activity_elapsed_time, nuclid, half_life, activity)
    # A tk.DrawingArea.
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=6, rowspan=5, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)


    # call img plot    
    fig2 = img_plot(img_path)
    # A tk.DrawingArea.
    canvas = FigureCanvasTkAgg(fig2, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6, column=6, rowspan=5, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)


    # results; add in label areas
    label_areaElapsedTime.config(text=str(elapsed_time_hms))
    label_areaEndingActivity.config(text=str(activity_elapsed_time))


#%% GUI
# start GUI
root = tk.Tk()
root.title("Radioactive Decay")
root.geometry("1920x1080")

# define menu
menubar = tk.Menu(root)

# file menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Delete All", command=delete_entries)
menubar.add_cascade(label="Edit", menu=editmenu)

# help menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=helpButton)
helpmenu.add_command(label="Impressum", command=impressum)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# define labels for nuclid and activity
label_nuclid = tk.Label(root, text="Nuclid (e.g. F-18):").grid(row=0)
label_activity = tk.Label(root, text="Activity in Bq (e.g. 100):").grid(row=0, column=3)
label_startingTime = tk.Label(root, text="Starting Time (d/m/Y H:M:S):").grid(row=1)
label_endingTime = tk.Label(root, text="Ending Time (d/m/Y H:M:S):").grid(row=1, column=3)
label_elapsedTime = tk.Label(root, text="Elapsed Time (H:M:S):").grid(row=3)
label_areaElapsedTime = tk.Label(root, bg='gray', width='12', text="")
label_areaElapsedTime.grid(row=3, column=1)
label_endingActivity = tk.Label(root, text="Ending activity (Bq):").grid(row=3, column=3)
label_areaEndingActivity = tk.Label(root, bg='gray', width='12', text="")
label_areaEndingActivity.grid(row=3, column=4)

# define entries for user input
# combobox (drop-down menu) tkinter for nuclide selection
cb_nuclid = ttk.Combobox(root, values=nuclides_list)
cb_nuclid.grid(row=0, column=1)
entry_activity = tk.Entry(root)
entry_activity.grid(row=0, column=4)
entry_startingTime = tk.Entry(root)
entry_startingTime.grid(row=1, column=1)
entry_endingTime = tk.Entry(root)
entry_endingTime.grid(row=1, column=4)


# define button position
buttonCalculate = tk.Button(text='Calculate!', width='10', bg='red', command=buttonCalculate)
buttonCalculate.grid(row=3, column=5, padx='5', pady='5')

buttonTime = tk.Button(text='Time', width='10', bg='yellow', command=currentTime)
buttonTime.grid(row=1, column=5, padx='5', pady='5')

# plot areas
plot_frame = tk.Frame(width=500, height=400, bg="grey", colormap="new")
plot_frame.grid(row=0, column=6, rowspan=5, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)

plot_frame2 = tk.Frame(width=500, height=400, bg="grey", colormap="new")
plot_frame2.grid(row=6, column=6, rowspan=5, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)

root.mainloop()