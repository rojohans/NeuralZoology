#
# The directionAngle is given in radians.
#

import numpy as np


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

    def Move(self):
        self.hasWrapped = False
        self.x += self.timeTick * self.speed * np.cos(self.directionAngle)
        self.y += self.timeTick * self.speed * np.sin(self.directionAngle)

        self.speed += self.timeTick * self.acceleration
        self.speed = np.min([np.max([self.speed, 0]), self.maxSpeed])

        #self.directionAngle += self.directionChange
        self.directionAngle += 2*(np.random.rand()-0.5)


    @classmethod
    def InitializeGlobalParameters(cls, mapSize = 100, timeTick = 1):
        # mapSize: The scale of the world. xLim = [0, mapSize], yLim = [0, mapSize]
        # timeTick: The time between each action. A smaller value would mean smaller but more precise value adjustments.
        cls.mapSize = mapSize
        cls.timeTick = timeTick


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





