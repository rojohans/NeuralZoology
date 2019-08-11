import numpy as np
import matplotlib
matplotlib.use('TkAgg') # This makes the plot-window pop up as the active window. This is only needed on mac.
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
# The collections library contains functions to generate several disjointed lines in the same object.

import time
import cProfile

import Animal
import Prey

# ==================== PARAMETER SETUP ============================
MAPSIZE = 100
TIMETICK = 1
numberOfInitialPrey = 1000
maxSpeed = 5
numberOfAnimationSteps = 500
numberOfTraceValues = 4 # The number of previous positions stored and visualized.
printStatsTOGGLE = False

visionArcPrey = 120*np.pi/180
visionRangePrey = 15
# test...

# ====================== PLOT SETUP ===============================
mainFigure = plt.figure()
mainAxes = plt.axes()
preyPlotHandle = plt.plot(0, 0, marker = '.', linestyle = 'none')
preyLineHandle = plt.plot(0, 0, marker = None, linestyle = '-')
plt.axis([0, MAPSIZE, 0, MAPSIZE])
mainAxes.set_aspect('equal')


# ====================== ANIMAL SETUP =============================
Animal.AnimalClass.InitializeGlobalParameters(mapSize = MAPSIZE,
                                              timeTick = TIMETICK,
                                              visionArc=110,
                                              visionRange=15,
                                              numberOfRangeValues=5)
preyList = [Prey.PreyClass(acceleration=0, maxSpeed = maxSpeed, speed = 1) for i in range(numberOfInitialPrey)]
if printStatsTOGGLE:
    for prey in preyList:
        prey.PrintStats()
        print('--------------')
Prey.PreyClass.LinkLists(preyList)


randomPoints = [(100*np.random.rand(), 100*np.random.rand())for i in range(1000000)]
specificPoint = (30, 30)

from scipy import spatial


'''
pr = cProfile.Profile()
pr.enable()

tic = time.clock()


shortestDistance = None
closestIndex = None

for index, point in enumerate(randomPoints):
    distance = np.sqrt(pow(specificPoint[0]-point[0],2) + pow(specificPoint[1]-point[1],2))
    if shortestDistance is None:
        shortestDistance = distance
        closestIndex = index
    else:
        if distance < shortestDistance:
            shortestDistance = distance
            closestIndex = index
'''

'''
tree = spatial.KDTree(randomPoints)
queryResult = tree.query(specificPoint)

print(queryResult)

shortestDistance = queryResult[0]
closestIndex = queryResult[1]

print('specific point: ', specificPoint)
print(shortestDistance)
print(randomPoints[closestIndex])

toc = time.clock()
print('elapsed time : %s sec' % (toc - tic))

pr.disable()
pr.print_stats(2)
quit()
'''

# ======================= ANIMATION ===============================
xHistory = np.zeros((numberOfAnimationSteps+1, numberOfInitialPrey))
yHistory = np.zeros((numberOfAnimationSteps+1, numberOfInitialPrey))
preyTrace = [[[preyList[iPrey].x, preyList[iPrey].y] for iStep in range(numberOfTraceValues)] for iPrey in range(numberOfInitialPrey)]


lc = mc.LineCollection(preyTrace, linewidths=2)
ax = plt.axes()
ax.add_collection(lc)
# plt.plot(*testList1)




'''
# The vision nodes are created.
angleSpan = 110*np.pi/180
rangeSpan = 15
numberOfRangeValues = 6

# The rangeDistribution is calculated in order to distribute the vision nodes such that they are uniformly spaced.
rangeVector = np.linspace(rangeSpan/numberOfRangeValues, rangeSpan, numberOfRangeValues)
rangeDistribution = np.round(2*rangeVector/np.min(rangeVector))
visionTolerance = rangeVector[-1]*angleSpan/rangeDistribution[-1]

visionNodesTemplate = [[range*np.cos(angle), range*np.sin(angle)]
                       for iRange, range in enumerate(rangeVector)
                       for angle in np.linspace(-angleSpan/2, angleSpan/2, rangeDistribution[iRange])]
visionNodesArrayTemplate=np.array(visionNodesTemplate)

rotationAngle = 60*np.pi/180
rotationMatrix = np.array([[np.cos(rotationAngle), -np.sin(rotationAngle)], [np.sin(rotationAngle), np.cos(rotationAngle)]])


x = visionNodesArrayTemplate.transpose()
y = rotationMatrix.dot(x)
visionNodesArrayTemplate = y.transpose()


visionNodesArrayTemplate[:, 0] += preyList[0].x
visionNodesArrayTemplate[:, 1] += preyList[0].y
visionNodesArrayTemplate = (visionNodesArrayTemplate + MAPSIZE) % MAPSIZE


preyCoordinates = [[prey.x, prey.y]for prey in preyList]

tree = spatial.cKDTree(preyCoordinates)
queryResult = tree.query(visionNodesArrayTemplate)

logic1 = queryResult[0] < visionTolerance
logic2 = queryResult[1] != 0
logic3 = logic1 & logic2
visionNodes = logic3.astype(int)
'''

'''
# =======================================
# ---------------------------------------
# .......................................
Prey.PreyClass.updateCoordinateList()
[visionNodesArrayTemplate, visionNodes] = preyList[0].Look(0)
# .......................................
# ---------------------------------------
# =======================================

plt.plot(preyList[0].x, preyList[0].y)
#plt.plot(visionNodesArrayTemplate[:, 0], visionNodesArrayTemplate[:, 1], marker='.', linestyle='none')
plt.scatter(visionNodesArrayTemplate[:, 0], visionNodesArrayTemplate[:, 1], c = visionNodes)
#plt.plot(visionNodesArrayTemplate[:, 0], visionNodesArrayTemplate[:, 1], marker = '.', c = 200*visionNodes, linestyle='none')
'''

pr = cProfile.Profile()
pr.enable()
tic = time.clock()

Prey.PreyClass.updateCoordinateList()
for iPrey, prey in enumerate(preyList):
    [visionNodesArrayTemplate, visionNodes] = prey.Look(iPrey)

toc = time.clock()
print(toc-tic)
pr.disable()
pr.print_stats(2)
quit()


preyX = []
preyY = []
for prey in preyList:
    preyX.append(prey.x)
    preyY.append(prey.y)
#plt.plot(preyX, preyY, marker = '.', linestyle = 'none')



Prey.PreyClass.updateCoordinateList()
for iPrey, prey in enumerate(preyList):
    [visionNodesArrayTemplate, visionNodes] = prey.Look(iPrey)
    plt.plot(preyX, preyY, marker='.', linestyle='none')
    #plt.plot(prey.x, prey.y)
    plt.scatter(visionNodesArrayTemplate[:, 0], visionNodesArrayTemplate[:, 1], c=visionNodes)
    plt.axis([0, MAPSIZE, 0, MAPSIZE])
    plt.pause(0.000001)
    plt.cla()

quit()



plt.show()

quit()

for iStep in range(numberOfAnimationSteps):
    for iPrey, prey in enumerate(preyList):
        prey.Move()
        if prey.hasWrapped:
            del preyTrace[iPrey][0]
            preyTrace[iPrey].append([None, None])
        del preyTrace[iPrey][0]
        preyTrace[iPrey].append([prey.x, prey.y])
    lc.set_segments(preyTrace)
    plt.pause(0.000001)


    # CHANGE TEST

    '''
    xToPlotPrey = np.zeros(np.shape(preyList))
    yToPlotPrey = np.zeros(np.shape(preyList))
    for iPrey, prey in enumerate(preyList):
        xToPlotPrey[iPrey] = prey.x
        yToPlotPrey[iPrey] = prey.y
        xHistory[iStep, iPrey] = prey.x
        xHistory[iStep+1, iPrey] = None
        print(xHistory)
        print(type(xHistory))
        print(' ')
        yHistory[iStep, iPrey] = prey.y
        yHistory[iStep+1, iPrey] = None
    preyPlotHandle[0].set_data(xToPlotPrey, yToPlotPrey)
    preyLineHandle[0].set_data(xHistory[0:iStep+1, :].transpose(), yHistory[0:iStep+1, :].transpose())
    plt.pause(0.000001)
    '''
plt.show()
quit()

# ====================== PREY PLOT ================================
xToPlotPrey = np.zeros(np.shape(preyList))
yToPlotPrey = np.zeros(np.shape(preyList))
for iPrey, prey in enumerate(preyList):
    xToPlotPrey[iPrey] = prey.x
    yToPlotPrey[iPrey] = prey.y
preyPlotHandle[0].set_data(xToPlotPrey, yToPlotPrey)
print('VISUALIZATION DONE')

plt.show()





print('PROGRAM DONE')