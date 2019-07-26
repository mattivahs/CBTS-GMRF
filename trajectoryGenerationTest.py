from parameters import par
from control import CBTS
from classes import node
from classes import agent
from classes import gmrf
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math

matplotlib.use('TkAgg')

N = 500

par = par('seqBayes', 'cbts', 'noUpdates', 'random', False, False, 1000, 0, 0, 0, 0, 0, 6, 3, 50, 50, 0.05, 0.5, 0.9)
cbts = CBTS(par)
auv = agent(par, par.x0, par.y0, par.alpha0)
gmrf1 = gmrf(par, par.nGridX, par.nGridY, par.nEdge)
v = node(par, gmrf, auv)

fig = plt.figure()
for i in range(N):
    theta = (-1+2*np.random.rand())*np.eye(1)
    tau, derivX, derivY = cbts.generateTrajectory(v,theta)
    stepSizes = []
    xOld = par.x0
    yOld = par.y0
    for i in range(tau.shape[1]-1):
        stepSizes.append(math.sqrt((xOld-tau[0,i+1])**2+(yOld-tau[1,i+1])**2))
        xOld = tau[0,i+1]
        yOld = tau[1,i+1]
    test = 1
    plt.plot(tau[0,:],tau[1,:])
    plt.scatter(tau[0,:],tau[1,:])
print(np.mean(stepSizes))
plt.show()
