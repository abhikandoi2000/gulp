from objects import WorldObject, PlayerObject
import random, math
import constants
import pygame
from pygame.locals import *
from pykinect import nui
from pykinect.nui import JointId, SkeletonTrackingState

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

class World:
  objects = []
  known_players = {}
  def __init__(self):
    self.randomise()
    self.dispInfo = pygame.display.Info()
    # self.createPlayers()
    pass
  def addObject(self, obj):
    self.objects.append(obj)
  def randomise(self):
    for i in range(0, constants.ASPECT_RATIO[0], constants.GRID_SIDE):
      for j in range(0, constants.ASPECT_RATIO[1], constants.GRID_SIDE):
        # movementVector = (random.uniform(0, 2 * math.pi), random.randint(-constants.VEL_RANGE, constants.VEL_RANGE))
        speed = random.randint(2, constants.VEL_RANGE)
        direction = random.uniform(-1 * (math.pi / 2), (3 * math.pi) / 2)
        velocity = speed * math.cos(direction) + speed * math.sin(direction)*1j
        # print velocity
        radius = random.randint(constants.RAD_RANGE/2, constants.RAD_RANGE)
        randX = int(random.uniform(0,1)*(constants.GRID_SIDE-radius))
        randY = int(random.uniform(0,1)*(constants.GRID_SIDE-radius))
        pos = (i + randX, j + randY)
        self.addObject(WorldObject(pos, velocity, radius, self))
  def createPlayer(self, color):
    direction = 0
    velocity = 0 + 0*1j
    radius = constants.PLAYER_RADIUS
    randX = int(random.uniform(0,1)*(constants.GRID_SIDE-radius))
    randY = int(random.uniform(0,1)*(constants.GRID_SIDE-radius))
    pos = (randX, randY)
    player = PlayerObject(pos, velocity, radius, self, color)
    self.addObject(player)
    return player
  def process_kinect_event(self, event):
    for skeleton in event.skeletons:
      if skeleton.eTrackingState == SkeletonTrackingState.TRACKED:
          player = self.known_players.get(skeleton.dwTrackingID)
          if player is None:
              # we found a new player, figure out their color.
              # TODO: We should do something to try and see if any 
              # of the existing players are actually this player. 
              # http://social.msdn.microsoft.com/Forums/is/kinectsdk/thread/b0ef83e1-970a-4c80-bc8f-02af218a0568
              color = 'red'
              for existing_player in self.known_players.values():
                  if existing_player.active:
                      if existing_player.color == 'red':
                        color = 'blue'
                      break
              player = createPlayer(color)
              self.known_players[skeleton.dwTrackingID] = player
              right_hand = skeleton.SkeletonPositions[JointId.HandRight]
              right_pos = skeleton_to_depth_image(right_hand, self.dispInfo.current_w, self.dispInfo.current_h)
              print "Player", player.color "has hand position"
              print right_pos
