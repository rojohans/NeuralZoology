#
#
#

import Animal
import numpy as np


class PreyClass(Animal.AnimalClass):
    def __init__(self,
                 x = None,
                 y = None,
                 directionAngle = None,
                 acceleration = 0,
                 speed = 0,
                 maxSpeed = 5,
                 maxDirectionChange = 0.1,
                 age = 0,
                 hunger = 100):
        super().__init__(x,
                         y,
                         directionAngle,
                         acceleration,
                         speed,
                         maxSpeed = maxSpeed,
                         maxDirectionChange = maxDirectionChange,
                         age = 0,
                         hunger = 100)


    def PrintStats(self):
        print('x = ', self.x)
        print('y = ', self.y)
        print('direction angle = ', self.directionAngle)
        print('acceleration = ', self.acceleration)
        print('speed = ', self.speed)
        print('age = ', self.age)
        print('hunger = ', self.hunger)







