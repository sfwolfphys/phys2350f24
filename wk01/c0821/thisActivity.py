import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

tVals = [0,1,3,5]
xVals = [2,2,8,10]
lett = ["A","B","C","D"]


x = pd.Series(xVals, index=tVals)

def makeMyPlot():
    fig, ax = plt.subplots()
    x.plot(style='ko-')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (cm)')
    ax.set_ylim(ymin=-0.1)
    ax.set_xlim(xmin=-0.05)
    ax.set_xticks(np.arange(0,5.5,0.5),minor=True)
    ax.grid(which='both',color='k',linestyle='dotted')
    ax.set_yticks(np.arange(0,10,1),minor=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i, txt in enumerate(lett):
        ax.annotate(txt,(tVals[i]+0.1,xVals[i]-0.6))
    plt.tight_layout()
    
    plt.savefig(fname="problem1.png")

    return [fig, ax]

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