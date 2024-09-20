import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def turbDrag(c,v):
    ''' Calculates the turbulent drag force.
    Inputs:
        c = Drag coefficient
        v = Velocity vector (two components)
    '''
    [vx, vy] = v
    spd = np.sqrt(vx**2+vy**2)
    vhat = v/spd
    FdragMag = c*spd**2
    Fdrag = - FdragMag * vhat
    return Fdrag

def netForce(u, m, c):
    g=9.81
    [t, x, y, vx, vy] = u
    v = [vx, vy]
    Fgrav = [0,-m*g]
    Fdrag = turbDrag(c,v)
    Fnet = Fgrav + Fdrag
    return Fnet

def velComps(vLaunch,launchAngleDeg):
    launchAngleRad = launchAngleDeg * np.pi/180
    velocity = vLaunch * np.array([np.cos(launchAngleRad), np.sin(launchAngleRad)])
    return velocity

def eulerCromerStep(u, m, c, dt):
    [t, x, y, vx, vy] = u
    v = np.array([vx, vy])
    r = np.array([x,y])

    # Update the velocity
    accel = np.array(netForce(u, m, c)/m)
    dv = accel * dt
    v = v + dv
    [vx, vy] = v

    # Update the position and time
    dr = v * dt
    r = r + dr
    [x, y] = r
    t = t + dt

    u = [t, x, y, vx, vy]
    return u

def projectileMotion(ui, dt, m, c):
    [ti, xi, yi, vxi, vyi] = ui
    time = np.array([ti])
    xpos = np.array([xi])
    ypos = np.array([yi])
    xvel = np.array([vxi])
    yvel = np.array([vyi])
  
    # create working variables
    u = ui
    [t, x, y, vx, vy] = u
    [ax, ay] = netForce(u, m, c)/m
    xacc = np.array([ax])
    yacc = np.array([ay])
    while y>0:
        # update the state
        u = eulerCromerStep(u,m,c,dt)
        [t, x, y, vx, vy] = u
        [ax, ay] = netForce(u, m, c)/m
        # append to arrays
        time = np.append(time, t)
        xpos = np.append(xpos, x)
        ypos = np.append(ypos, y)
        xvel = np.append(xvel, vx)
        yvel = np.append(yvel, vy)
        xacc = np.append(xacc, ax)
        yacc = np.append(yacc, ay)

    # Make the output array into a dataframe and return
    motion = pd.DataFrame({'time':time, 'xpos':xpos, 'ypos':ypos, 'xvel':xvel, 'yvel':yvel, 'xacc':xacc, 'yacc':yacc})
    return motion

def genProjectilePlot(xi,yi,vLaunch,thetaLaunch, dt, m, c):
    [vx, vy] = velComps(vLaunch,thetaLaunch)
    u = [0, xi, yi, vx, vy]
    mA = projectileMotion(u, dt, m, c)
    mI = projectileMotion(u, dt, m, 0)

    # Make the plot
    fig, ax = plt.subplots(nrows=2,ncols=2, sharex=True)
    ax[0,0].plot(mA.time, mA.xpos,label='drag')
    ax[0,0].plot(mI.time, mI.xpos,label='no drag')
    ax[0,0].set_title('x-component')
    ax[0,0].set_ylabel('position')
    ax[0,0].legend()
    ax[0,1].plot(mA.time, mA.ypos,label='drag')
    ax[0,1].plot(mI.time, mI.ypos,label='no drag')
    ax[0,1].set_title('y-component')
    ax[0,1].legend()
    ax[1,0].plot(mA.time, mA.xvel,label='drag')
    ax[1,0].plot(mI.time, mI.xvel,label='no drag')
    ax[1,0].set_ylabel('velocity')
    ax[1,0].legend()
    ax[1,1].plot(mA.time, mA.yvel,label='drag')
    ax[1,1].plot(mI.time, mI.yvel,label='no drag')
    ax[1,1].legend()
    plt.show()