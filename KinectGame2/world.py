from objects import WorldObject
import random, math
import constants

class World:
  objects = []
  def __init__(self):
    pass
  def addObject(self, obj):
    self.objects.append(obj)
  def randomise(self):
    for i in range(0, constants.ASPECT_RATIO[0], constants.GRID_SIDE):
      for j in range(0, constants.ASPECT_RATIO[1], constants.GRID_SIDE):
        movementVector = (random.uniform(0, 2 * math.pi), random.randint(-constants.VEL_RANGE, constants.VEL_RANGE))
        print movementVector
        radius = random.randint(constants.RAD_RANGE/2, constants.RAD_RANGE)
        randX = int(random.uniform(0,1)*(constants.GRID_SIDE-radius))
        randY = int(random.uniform(0,1)*(constants.GRID_SIDE-radius))
        pos = (i + randX, j + randY)
        self.addObject(WorldObject(pos, movementVector, radius, self))
