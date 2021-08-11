# -*- coding: utf-8 -*-
"""
Exercise 8.4 Simple Pendulum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from vpython import *

g = 9.81  # kg/m^2
l1 = 0.4  # meters
l2 = 2*l1  # meters

cmToPixel = 37.7952755906
pixelToCm = 1/ cmToPixel
R = 5 # pixels

width = 640
height = 400

def f(r,t):
    x1 = r[0] # theta1
    x2 = r[1] # theta2
    x3 = r[2] # oemga1
    x4 = r[3] # omega2
    fx1 = x3
    fx2 = x4
    numerator = x3**2 * np.sin(2*x1-2*x2) + 2 * x4**2 * np.sin(x1-x2)\
                + (g/l1) *( np.sin(x1-2*x2) + 3*np.sin(x1) )
    denominator = 3 - np.cos(2*x1-2*x2)
    fx3 = -numerator / denominator
    numerator = 4 * x3**2 * np.sin(x1-x2) + x4**2 * np.sin(2*x1-2*x2)\
                + 2 * (g/l1) *( np.sin(2*x1-x2) - np.sin(x2) )
    fx4 = numerator / denominator
    return np.array([fx1,fx2,fx3,fx4],float)

cv = canvas(center=vector(width/2.0,height/2.0,0.0), 
            width = width, height = height, background = color.white)

pivot = sphere(pos=vector(width/2.0,height,0),
               radius=5*R,color = color.blue)
bob0 = sphere(pos=vector(width/2.0,height-l1*100*cmToPixel,0.0),
             radius= 20*R,color = color.red)
bob1 = sphere(pos=vector(width/2.0,height-l1*100*cmToPixel-l2*100*cmToPixel,
                         0.0),
             radius= 20*R,color = color.red)
arm = curve(pos=[pivot.pos,bob0.pos,bob1.pos],
            radius = 10*R, color = color.black)

t0 = 0.0
tn = 100.0
N = 10000
h = (tn-t0)/N
theta0 = 45
theta1 = 60
omega0 = 10
omega1 = 5

tpoints = np.arange(t0,tn,h)
theta0points = []
theta1points = []
omega0points = []
omega1points = []

r = np.array([theta0*np.pi/180.0,theta1*np.pi/180.0,omega0,omega1],float)
for t in tpoints:
    theta0points.append(r[0])
    theta1points.append(r[1])
    omega0points.append(r[2])
    omega1points.append(r[3])
    k1 = h*f(r,t)
    k2 = h*f(r+0.5*k1,t+0.5*h)
    k3 = h*f(r+0.5*k2,t+0.5*h)
    k4 = h*f(r+k3,t+h)
    r += (k1+2*k2+2*k3+k4)/6

#import time
#time.sleep(10)

cv.title = "theta0Ini = 45, theta1Ini = 60, omega0Ini = 10, omega1Ini = 5"
for i in range(N):
    rate(100)
    theta0 = theta0points[i]
    theta1 = theta1points[i]

    if (i % 100 == 0):
        cv.caption="time = {}, theta0 = {:.3f}, theta1 = {:.3f}.".format(
                    h*i, theta0, theta1)
        #filename = "time_"+str(h*i)+".png"
        #cv.capture(filename) # NOT Working quite well!
    
    x1 = width/2.0+l1*100*cmToPixel*np.sin(theta0)
    y1 = height-l1*100*cmToPixel*np.cos(theta0) 
    x2 = width/2.0+l1*100*cmToPixel*np.sin(theta0)\
         + l2*100*cmToPixel*np.sin(theta1)
    y2 = height-l1*100*cmToPixel*np.cos(theta0)-l2*100*cmToPixel*np.cos(theta1)
    bob0.pos = vector(x1,y1,0)
    bob1.pos = vector(x2,y2,0)
    arm.modify( 1, pos = bob0.pos )
    arm.modify( 2, pos = bob1.pos )