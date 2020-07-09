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


# nuclides dictionary with half life in s
nuclides = {
        "O-15": 122.24,
        "N-13": 597.9,
		"Tc-99m": 21.624*10**3,
        "I-131": 693*10**3,
		"F-18": 6.586*10**3
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


# set up nuclid (user input)
nuclid_input = input('Nuclid (e.g. F-18): ')


# compare user input with nuclides dict
for key in nuclides:
	if nuclid_input == key:
		nuclid = key
		half_life = nuclides.get(key)


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
# print('Elapsed Time: {} s'.format(elapsed_time))


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
