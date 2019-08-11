#
# The directionAngle is given in radians.
#

import numpy as np
from scipy import spatial

'''
class KatarinaAnimalClass():
    def __init__(self,
                 x=None,
                 y=None,):
        if x:
            self.x = x
        else:
            self.x = self.mapSize * np.random.rand()
        if y:
            self.y = y
        else:
            self.y = self.mapSize * np.random.rand()


    def PrintStats(self):
        print('x = ',self.x)
        print('y = ',self.y)


    @classmethod
    def InitializeGlobalParameters(cls, mapSize):
        cls.mapSize = mapSize
'''















class AnimalClass():
    def __init__(self,
                 x = None,
                 y = None,
                 directionAngle = None,
                 acceleration = 0,
                 speed = 0,
                 maxSpeed = 5,
                 maxDirectionChange = 0.1,
                 age=0,
                 hunger=100,
                 ):
        #
        # hasWrapped: Determines if either the x- or y-coordinate has wrapped around. This is usefull to know when
        #             visualizing traces.
        # visionArc: The angle in which the animal can see.
        # visionRange: The maximum distance at which detection can be done.
        #
        #
        if x == None:
            self.x = self.mapSize * np.random.rand()
        else:
            self.x = x
        if y == None:
            self.y = self.mapSize * np.random.rand()
        else:
            self.y = y


        if directionAngle == None:
            self.directionAngle = 2*np.pi*np.random.rand()
        else:
            self.directionAngle = directionAngle
        self.acceleration = acceleration
        self.speed = speed
        self.directionChange = 0.5
        self.maxSpeed = maxSpeed
        self.maxDirectionChange = maxDirectionChange
        self.hasWrapped = False



        self.age = age
        self.hunger = hunger


        #ID = 0
        #turnRate = 0.1
        #maxVelocity = 10
        #acceleration = 0.1
        #visionRange = 40
        #visionArc = 110

    def Look(self, ID):
        #self.directionAngle

        rotationMatrix = np.array([[np.cos(self.directionAngle),
                                    -np.sin(self.directionAngle)],
                                   [np.sin(self.directionAngle),
                                    np.cos(self.directionAngle)]])

        visionNodesCoordinates = rotationMatrix.dot(self.visionNodesTemplate.transpose())
        visionNodesCoordinates = visionNodesCoordinates.transpose()
        visionNodesCoordinates[:, 0] += self.x
        visionNodesCoordinates[:, 1] += self.y
        visionNodesCoordinates = (visionNodesCoordinates + self.mapSize) % self.mapSize

        queryResult = self.preykdTree.query(visionNodesCoordinates)

        logic1 = queryResult[0] < self.visionTolerance
        logic2 = queryResult[1] != ID
        logic3 = logic1 & logic2
        visionNodesInput = logic3.astype(int)

        return visionNodesCoordinates, visionNodesInput


    def Move(self):
        self.hasWrapped = False
        self.x += self.timeTick * self.speed * np.cos(self.directionAngle)
        self.y += self.timeTick * self.speed * np.sin(self.directionAngle)

        self.speed += self.timeTick * self.acceleration
        self.speed = np.min([np.max([self.speed, 0]), self.maxSpeed])

        #self.directionAngle += self.directionChange
        self.directionAngle += 2*(np.random.rand()-0.5)


    @classmethod
    def InitializeGlobalParameters(cls,
                                   mapSize = 100,
                                   timeTick = 1,
                                   visionArc = 120*np.pi/180,
                                   visionRange = 15,
                                   numberOfRangeValues = 5):
        # mapSize: The scale of the world. xLim = [0, mapSize], yLim = [0, mapSize]
        # timeTick: The time between each action. A smaller value would mean smaller but more precise value adjustments.
        cls.mapSize = mapSize
        cls.timeTick = timeTick

        rangeVector = np.linspace(visionRange / numberOfRangeValues, visionRange, numberOfRangeValues)
        rangeDistribution = np.round(2 * rangeVector / np.min(rangeVector))
        cls.visionTolerance = rangeVector[-1] * visionArc / rangeDistribution[-1]
        visionNodesTemplate = [[range * np.cos(angle), range * np.sin(angle)]
                               for iRange, range in enumerate(rangeVector)
                               for angle in np.linspace(-visionArc / 2, visionArc / 2, rangeDistribution[iRange])]
        cls.visionNodesTemplate = np.array(visionNodesTemplate)

    @classmethod
    def LinkLists(cls, preyList):
        # The kd-Tree is created in order to quickly find the nearest objects to a set of vision nodes.
        cls.preyList = preyList
        cls.preyCoordinates = [[prey.x, prey.y] for prey in preyList]
        cls.preykdTree = spatial.cKDTree(cls.preyCoordinates)

    @classmethod
    def updateCoordinateList(cls):
        for iPrey, prey in enumerate(cls.preyList):
            cls.preyCoordinates[iPrey][0] = prey.x
            cls.preyCoordinates[iPrey][1] = prey.y
            cls.preykdTree = spatial.cKDTree(cls.preyCoordinates)


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = self._Periodic(value)
        if abs(value - self._x) > self.mapSize / 2:
            self.hasWrapped = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = self._Periodic(value)
        if abs(value - self._y)>self.mapSize/2:
            self.hasWrapped = True

    def _Periodic(self, value):
        return (value + self.mapSize) % self.mapSize


