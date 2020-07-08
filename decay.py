#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:48:31 2020

@author: eric
"""
import math
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


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

# set and convert start time
date = input('Enter the start time (d/m/Y H:M:S): ')
d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
start_time = time.mktime(d.timetuple())


# set and convert end time
date = input('Enter the end time (d/m/Y H:M:S): ')
d = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
end_time = time.mktime(d.timetuple())


# calculate the elapsed time
elapsed_time = end_time - start_time
print('Elapsed Time: {} s'.format(elapsed_time))


# set starting activity
activity = float(input('Starting activity in Bq: '))


# nuclid and half life
nuclid = 'Carbon-10'
half_life = 19.29 # carbon-10


# print all relevant infos
print('Radioactive Decay - Nuclid: {}, Half life: {} s, Activity: {} Bq'.format(nuclid, half_life, activity))


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


# plot graph of activity depends on time
fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot(tlist, alist, color='#ee8d18', lw=3)
# plot single point (elapsed time)
ax.plot([elapsed_time], [activity_elapsed_time], 'o')
ax.annotate('You are here!',
            xy=(elapsed_time, activity_elapsed_time),
            #xytext=(0.1, 0.1),    # fraction, fraction
            #textcoords='figure fraction',
            #arrowprops=dict(facecolor='black', shrink=0.05),
            #horizontalalignment='left',
            #verticalalignment='bottom',
            )
plt.title('Radioactive Decay')
plt.xlabel('Time (s)')
plt.ylabel('Activity (Bq)')
plt.show()
