import numpy as np
import math

"""Parameters for all files"""

"""main.py"""
stkf = True
sequentialUpdate = True  # Does not work with truncation!
fastCalc = False  # True: Fast Calculation, only one plot in the end; False: Live updating and plotting
truncation = False
PIControl = False

fieldType = 'predefined' # 'peak','sine' or 'predefined'
temporal = False  # True: time varying field

if not PIControl:
    CBTS = True
else:
    CBTS = False

exploitingRate = 0

nIter = 1000  # number of iterations
dt = 1  # timesteps per iteration
nMeas = 100  # number of measurements for bayesian inference (nMeas = nIter for inference without truncation)
ov2 = 0.01  # measurement variance
ov2Real = ov2
dX = dY = 0.01  # discretizaton in x and y for Plotting

(x0, y0, alpha0) = (0, 0, math.pi/4)  # initial state
maxStepsize = 0.1  # maximum change in every state per iteration
xVel = maxStepsize
yVel = maxStepsize

dxdt = 0.001  # Shift of true field in x direction
dydt = 0.001  # Shift of true field in y direction
pulseTime = nIter / 2  # Duration of sinusodial pulsation

"""GMRF class"""
xMin = 0  # GMRF dimensions
xMax = 10
nGridX = 10
yMin = 0
yMax = 10
nGridY = 10
nBeta = 1  # regression coefficients
nEdge = 5
valueT = 1e-3  # Prior precision value for regression vector bet

"""STKF class"""
sigmaT = 1e5 #1e3    # determines exponential decay of time kernel
lambdSTKF = 1  # influences time kernel value
sigma2 = 0.01

"""PI2 controller"""
H = 20  # control horizon steps
controlCost = 5# 5e-1   # affects noise of path roll-outs (negatively)
R = controlCost*np.eye(H)   # input cost matrix
g = np.ones((H,1))
lambd = 1e-1 # 1e-2 # rescales state costs, affects noise of path roll-outs (positively)
K = 15  # number of path roll outs
ctrSamplingTime = 0.1  # time discretization
nUpdated = 5   # number of iterations
outOfGridPenaltyPI2 = 10 # each observation outside of grid adds a negative reward

"""CBTS controller"""
trajStepSize = 1  # determines number of measurement points along trajectory (depends on maxStepsize)
trajScaling = 1  # scales trajectories (cx and cy in case of quadratic trajectories)
CBTSIterations = 20  # determines runtime of algorithm, could also be done with time limit
branchingFactor = 5  # number of actions that can be evaluated at max for each path segment
maxDepth = 3 # depth of search tree
kappa = 10  # large: evaluate more untried actions; small: concentrate on actions which already lead to high rewards
nTrajPoints = int(trajStepSize/maxStepsize) # number of measurement points along trajectory
kappaChildSelection = 1 # high value: expand nodes with less visits, low: expand nodes with high accumulated reward
UCBRewardFactor = 0.01  # reward = variance + UCBRewardFactor*mean
outOfGridPenaltyCBTS = 1

thetaMin = -1 # determines curvature of generated trajectories
thetaMax = 1 # determines curvature of generated trajectories
thetaExpMin = thetaMin # determines curvature of generated trajectories for node exploration
thetaExpMax = thetaMax # determines curvature of generated trajectories for node exploration
trajOrder = 1 # if higher order is used check trajectory generation function
initialTheta = np.zeros(trajOrder) # leads to first trajectory being straight
discountFactor = 0.5 # discounts future rewards

#Gaussian Process for action reward mapping
kernelPar = 10 # used in exponential kernel to determine variance between to inputs
nThetaSamples = 100 # number of samples thetas which are candidates for next theta

if not truncation:
    nMeas = nIter

if stkf:
    nBeta = 0

class plotOptions:
    showExploredPaths = False
    showActionRewardMapping = False
    showAcquisitionFunction = True