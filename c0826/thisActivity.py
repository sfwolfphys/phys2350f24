## Import packages to make it go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#############################################################
#
# Stuff for the first problem
# This is the exact answer for the differential equation \ddot{x} = e^-t for our Boundary Conditions
# x(t) = t - (1-e^-t)
def realPos(t):
    x = t - (1 - np.exp(-t))
    return x
# v(t) = 1-e^-t
def realVel(t):
    v = 1 - np.exp(-t)
    return v
# The given acceleration in the problem
def realAcc(t):
    a = np.exp(-t)
    return a

# Given a state [t,x,v] and a time interval δt, find the state a bit later: [t+δt, x+δx, v+δv]
def incrementMotion(t,x,v,δt):
    a = realAcc(t)
    u = np.array([t, x, v])
    δu = np.array([δt, v*δt, a*δt])
    return u+δu
# Given initial conditions [ti,xi,vi], the time you want to stop [tf], and a step size δt,
# calculate the entire motion
def calcMotion(ti,xi,vi,tf,δt):
    # put initial values into output arrays
    time = np.array([ti])
    pos = np.array([xi])
    vel = np.array([vi])
    
    # create working variables
    t = ti
    x = xi
    v = vi
    # calculate the initial acceleration
    acc = np.array([realAcc(t)])
    n = int(np.ceil((tf-ti)/δt))
    for j in range(n):
        # find t,x,v a short bit later
        [t, x, v] = incrementMotion(t,x,v,δt)
        # put these values into the output arrays
        time = np.append(time,t)
        pos = np.append(pos, x)
        vel = np.append(vel, v)
        # calculate new acceleration and put it into the output array
        acc = np.append(acc, realAcc(t))
    # make the output array into a dataframe and return it    
    motion = pd.DataFrame({'time':time, 'pos':pos, 'vel':vel, 'acc':acc})
    return motion

# This is the caption that I wanted to put in my table. It is called an f-string which allows me to insert given
# numerical values into a string, and format them so that we don't get number vomit.
cap = f"At t = 5 s the actual position is {realPos(5):.4f} m and the actual velocity is {realVel(5):.4f} m/s. <br> ***How can we account for the discrepancy?***"

# This makes the plots for the end of the activity
def makeTriPlot(ti,xi,vi,tf,deltat):
    # Calculate the exact answer at a whole bunch of points. Note, the solutions are only valid for the initial conditions
    # given in the problem, namely at t=0, x(0)=0 and v(0)=0. However, the calculation is more flexible
    tt = np.linspace(0,tf,1000)
    xx = realPos(tt)
    vv = realVel(tt)
    aa = realAcc(tt)
    # Calculate the approximate answer using the function above
    m = calcMotion(ti,xi,vi,tf,deltat)
    # Make a figure
    fig,ax = plt.subplots(nrows=3, sharex=True)
    fig.set_size_inches(8,6)
    ax[0].plot(m.time,m.pos,'bo',label='approx')
    ax[0].plot(tt,xx,'r-',label='actual')
    ax[0].legend(fontsize='x-small')
    ax[0].set_ylabel(r'$x (m)$')
    ax[1].plot(m.time,m.vel,'bo',label='approx')
    ax[1].plot(tt,vv,'r-',label='actual')
    ax[1].set_ylabel(r'$v (m/s)$')
    ax[1].legend(fontsize='x-small')
    ax[2].plot(m.time,m.acc,'bo',label='approx')
    ax[2].plot(tt,aa,'r-',label='actual')
    ax[2].set_ylabel(r'$a (m/s^2)$')
    ax[2].set_xlabel(r'$t (s)$')
    ax[2].legend(fontsize='x-small')
    fig.suptitle(f'Motion of object, approximate solution has δt={deltat:.4f} s')
    plt.show()