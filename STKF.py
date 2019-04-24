import classes
import methods
import parameters as par
import math
import time
import scipy
from scipy import  integrate
import numpy as np
import matplotlib.pyplot as plt

# Only for one agent! If multiple agents are used, increase dimensions properly

T = 100
dt = 0.1
nIter = int(T/dt)

xMin = 0
xMax = 10
nX = 10
yMin = 0
yMax = 10
nY = 10
nBeta = 0

gmrf1 = classes.gmrf(xMin, xMax, nX, yMin, yMax, nY, nBeta)

# Plotting grid
x = np.arange(gmrf1.xMin, gmrf1.xMax, par.dX)
y = np.arange(gmrf1.yMin, gmrf1.yMax, par.dY)
X, Y = np.meshgrid(x, y)

trueField = classes.trueField(x[-1], y[-1], par.sinusoidal, par.temporal)

sigmaT = 0.01
lambd = 1

xHist = [par.x0]  # x-state history vector
yHist = [par.y0]  # y-state history vector
xMeas = par.x0
yMeas = par.y0

# Time measurement vectors
timeVec = []
iterVec = []

# State representation of Sr
F = -1/sigmaT * np.ones((1,1))
H = math.sqrt(2*lambd / sigmaT) * np.ones((1,1))
G = np.ones((1,1))
sigma2 = 0.01

# Kernels
Ks = methods.getPrecisionMatrix(gmrf1)
KsChol = np.linalg.cholesky(Ks)
h = lambda tau: lambd * math.exp(-abs(tau)/sigmaT)

sigmaZero = scipy.linalg.solve_lyapunov(F, G*G.T)

# Initialization
sZero = 0
cov = np.kron(np.eye(gmrf1.nP), sigmaT)

# Initialize Plot
fig = plt.figure()
methods.plotFields(fig, x, y, trueField, gmrf1, iterVec, timeVec, xHist, yHist)
plt.show()

tk = 0

skk = 1 #Fix this
covkk = 1#Fix this
for i in range(nIter):
    timeBefore = time.time()
    t = i*dt
    A = scipy.linalg.expm(np.kron(np.eye(gmrf1.nP), F) * (t - tk))

    zMeas = methods.getMeasurement(xMeas, yMeas, trueField, par.ov2)
    (xMeas, yMeas) = methods.getNextState(xMeas, yMeas, xHist[-1], yHist[-1], par.maxStepsize, gmrf1)
    xHist.append(xMeas)
    yHist.append(yMeas)

    if (t-tk)!=0:
        # Open loop prediciton
        sHead = A*skk
        sigmaS = np.dot(A,np.dot(covkk,A.T))
    else:
        Phi = methods.mapConDis(gmrf1, xMeas, yMeas)
        C = np.dot(Phi,np.dot(KsChol,np.kron(np.eye(gmrf1.nP), H)))
        QBar = scipy.integrate.quad(lambda tau: np.dot(scipy.linalg.expm(np.dot(F,tau)),np.dot(G,np.dot(G.T,scipy.linalg.expm(np.dot(F,tau).T)))),0,dt)
        Q = np.kron(np.eye(gmrf1.nP), QBar)
        R = sigma2

        #Kalman Regression
        sPred = np.dot(A,skk)
        covPred = np.dot(A,np.dot(covkk,A.T)) + Q

        kalmanGain = np.dot(covPred,np.dot(C.T,np.linalg.inv(np.dot(C,np.dot(covPred,C.T))+R)))
        sUpdated = sPred + np.dot(kalmanGain,zMeas - np.dot(C,sPred))
        covUpdated = np.dot(np.eye(gmrf1.nP)-np.dot(L,C),covPred)

        s = sUpdated
        cov = covUpdated
        tk = t

    hAug = np.dot(np.kron(np.eye(gmrf1.nP), H))
    gmrf1.meanCond = np.dot(KsChol,hAug,s)
    gmrf1.covCond = np.dot(KsChol,np.dot(hAug,np.dot(cov,np.dot(hAug.T,KsCholch))))
    gmrf1.diagCovCond = gmrf1.covCond.diagonal()

    # Time measurement
    timeAfter = time.time()
    iterVec.append(i)
    timeVec.append(timeAfter - timeBefore)

    # Plotting:
    if not par.fastCalc:
        methods.plotFields(fig, x, y, trueField, gmrf1, iterVec, timeVec, xHist, yHist)

    # Update ground truth:
    if par.temporal:
        trueField.updateField(i)

    methods.plotFields(fig, x, y, trueField, gmrf1, iterVec, timeVec, xHist, yHist)
    plt.show(block=True)