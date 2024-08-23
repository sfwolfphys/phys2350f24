import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def pos(time):
    x = time**2 - 6*time + 10
    return x

def xvtPlt(tmin, tmax):
    tRange = tmax - tmin
    tdMag = np.ceil(np.log10(tRange))
    deltaTick = 10**(tdMag-1) /2
    
    tlist = np.linspace(tmin,tmax,1000)
    xlist = pos(tlist)
    
    xmax = np.max(xlist)
    xmin = np.min(xlist)
    xRange =  xmax - xmin
    xdMag = np.ceil(np.log10(xRange))
    deltaX = 10**(xdMag - 1)/2
    if xRange > 4:
        xmin = 0
    
    fig, ax = plt.subplots()
    ax.plot(tlist,xlist)
    ax.grid(which='both',color='k',linestyle='dotted')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(ymin=xmin)
    return [fig, ax]

def realPos(t):
    x = t - (1 - np.exp(-t))
    return x

def realVel(t):
    v = 1 - np.exp(-t)
    return v

def realAcc(t):
    a = np.exp(-t)
    return a

def incrementMotion(t,x,v,δt):
    a = realAcc(t)
    u = np.array([t, x, v])
    δu = np.array([δt, v*δt, a*δt])
    return u+δu

def calcMotion(ti,xi,vi,tf,δt):
    time = np.array([ti])
    pos = np.array([xi])
    vel = np.array([vi])
    
    t = ti
    x = xi
    v = vi

    acc = np.array([realAcc(t)])
    n = int(np.ceil((tf-ti)/δt))
    for j in range(n):
        [t, x, v] = incrementMotion(t,x,v,δt)
        time = np.append(time,t)
        pos = np.append(pos, x)
        vel = np.append(vel, v)
        acc = np.append(acc, realAcc(t))
    motion = pd.DataFrame({'time':time, 'pos':pos, 'vel':vel, 'acc':acc})
    return motion

cap = f"At t = 5 s the actual position is {realPos(5):.4f} m and the actual velocity is {realVel(5):.4f} m/s. <br> ***How can we account for the discrepancy?***"

tt = np.linspace(0,5,1000)
xx = realPos(tt)
vv = realVel(tt)
aa = realAcc(tt)