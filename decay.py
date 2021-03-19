#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Eric Einspänner, Institute of Nuclear Medicine, UMG (Germany)

This program is free software.
"""
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


#%% print a list of all nuclides
list_nuclides = []
for key in nuclides:
	list_nuclides.append(key)

print('All available nuclides:', list_nuclides)


# set up nuclid (user input)
nuclid_input = input('Nuclid (e.g. F-18): ')


# compare user input with nuclides dict and extract correct half life and img path
for key in nuclides:
	if nuclid_input == key:
		nuclid = key
		half_life = float(nuclides[key][0])
		img_path = str(nuclides[key][1])


# set starting activity
activity = float(input('Starting activity in Bq: '))


# set (user input) and convert start time
date = input('Enter the start time (d/m/Y H:M:S): ')
d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
start_time = time.mktime(d.timetuple())


# set (user input) and convert end time
date = input('Enter the end time (d/m/Y H:M:S): ')
d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
end_time = time.mktime(d.timetuple())


# calculate the elapsed time
elapsed_time = end_time - start_time


# print all relevant infos
print('Radioactive Decay - Nuclid: {}, Half life: {} s, Activity: {} Bq, Elapsed Time: {} s'.format(nuclid, half_life, activity, elapsed_time))


# specific activity
activity_elapsed_time = decay_equation(activity, decay_const(half_life), elapsed_time)
print('Ending activity: {} Bq'.format(activity_elapsed_time))


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


