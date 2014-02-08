#!/usr/bin/python

try:
  import sys
  import random
  import math
  import os
  import getopt
  import pygame
  import random
  from time import sleep
  from socket import *
  from pygame.locals import *
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)

ASPECT_RATIO = (640, 480)
SCALE = 10
GRID_SIDE = 160
VEL_RANGE = 2
RAD_RANGE = 6

def load_png(name):
  """ Load image and return image object"""
  fullname = os.path.join('data', name)
  try:
    image = pygame.image.load(fullname)
    if image.get_alpha is None:
      image = image.convert()
    else:
      image = image.convert_alpha()
  except pygame.error, message:
    print 'Cannot load image:', fullname
    raise SystemExit, message
  return image


class World:
  objects = []
  def __init__(self):
    pass
  def addObject(self, obj):
    self.objects.append(obj)
  def randomise(self):
    for i in range(0, ASPECT_RATIO[0], GRID_SIDE):
      for j in range(0, ASPECT_RATIO[1], GRID_SIDE):
        movementVector = (random.uniform(0, 2 * math.pi), random.randint(-VEL_RANGE, VEL_RANGE))
        radius = random.randint(RAD_RANGE/2, RAD_RANGE)
        randX = int(random.uniform(0,1)*GRID_SIDE)
        randY = int(random.uniform(0,1)*GRID_SIDE)
        pos = (i + randX, j + randY)
        self.addObject(RandomBall(pos, movementVector, radius))

class RandomBall(pygame.sprite.Sprite):
  """A ball that keeps on moving in a particular direction
  Returns: randomball object
  Functions: update, calcnewpos
  Attributes: area, vector"""

  def __init__(self, initPos, movementVector, radius):
    pygame.sprite.Sprite.__init__(self)
    self.image = load_png('osmos_64.png')
    self.image = pygame.transform.scale(self.image, (radius*SCALE, radius*SCALE))
    
    self.rect = self.image.get_rect()
    self.rect.x = initPos[0]
    self.rect.y = initPos[1]
    
    screen = pygame.display.get_surface()
    
    self.area = screen.get_rect()
    self.vector = movementVector
    self.hit = 1

  def updateDirectionOnCollisionWith(self, objects, rect, vector, dx, dy):
    """
    checks if the `rect` on moving `(dx, dy)` collides with any of the
    object in `objects` and updates the direction of motion (`angle`)
    accordingly
    """
    collided = False
    (angle, z) = vector
    # detect for each RandomBall
    for obj in [obj for obj in objects if self != obj]:
      if rect.colliderect(obj.rect):
        collided = True
        obj.rect.inflate(-3, -3)

        if not self.hit:
          # angle = math.pi - angle
          tl = not obj.rect.collidepoint(self.rect.topleft)
          tr = not obj.rect.collidepoint(self.rect.topright)
          bl = not obj.rect.collidepoint(self.rect.bottomleft)
          br = not obj.rect.collidepoint(self.rect.bottomright)
          if tr and br:
            # hit from the left side
            self.rect.right = obj.rect.left
            angle = math.pi - angle
          elif bl and tl:
            # hit from the right side
            self.rect.left = obj.rect.right
            angle = math.pi - angle
          """if tl and tr:
            # hit from the top side
            self.rect.bottom = randomball.rect.top  
          if dy < 0:
            # hit from the bottom side
            self.rect.top = randomball.rect.bottom
          """
          self.hit = not self.hit
        elif self.hit:
          self.hit = not self.hit
    self.vector = (angle, z)
    return collided

  def move(self, rect, vector):
    """dpos - change in position
       eg: [1, 1] : move 1 unit in x and one in y
    """
    (angle,z) = vector
    (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
    collided = self.updateDirectionOnCollisionWith(world.objects, rect, vector, dx, dy)
    if not collided:
      self.rect = rect.move(dx, dy)
    return collided
  
  def update(self):
    self.move(self.rect, self.vector)
    (angle,z) = self.vector

    if not self.area.contains(self.rect):
      tl = not self.area.collidepoint(self.rect.topleft)
      tr = not self.area.collidepoint(self.rect.topright)
      bl = not self.area.collidepoint(self.rect.bottomleft)
      br = not self.area.collidepoint(self.rect.bottomright)
      if tr and tl or (br and bl):
        angle = -angle
      if tl and bl:
        #self.offcourt()
        angle = math.pi - angle
      if tr and br:
        angle = math.pi - angle
        #self.offcourt()
    self.vector = (angle,z)
    
    """
    else:
      # Deflate the rectangles so you can't catch a ball behind the bat
      player1.rect.inflate(-3, -3)
      player2.rect.inflate(-3, -3)

      # Do ball and bat collide?
      # Note I put in an odd rule that sets self.hit to 1 when they collide, and unsets it in the next
      # iteration. this is to stop odd ball behaviour where it finds a collision *inside* the
      # bat, the ball reverses, and is still inside the bat, so bounces around inside.
      # This way, the ball can always escape and bounce away cleanly
      if self.rect.colliderect(player1.rect) == 1 and not self.hit:
        angle = math.pi - angle
        self.hit = not self.hit
      elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
        angle = math.pi - angle
        self.hit = not self.hit
      elif self.hit:
        self.hit = not self.hit
    """

  def moveup(self):
    self.movepos[1] = self.movepos[1] - (self.speed)
    self.state = "moveup"

  def moveleft(self):
    self.movepos[0] = self.movepos[0] - (self.speed)
    self.state = "moveleft"

  def moveright(self):
    self.movepos[0] = self.movepos[0] + (self.speed)
    self.state = "moveright"

  def movedown(self):
    self.movepos[1] = self.movepos[1] + (self.speed)
    self.state = "movedown"

"""Group for random object testing
"""
class RandomObjectGroup(pygame.sprite.Group):
  def __init__(self):
    pygame.sprite.Group.__init__(self);

class Ball(pygame.sprite.Sprite):
  """Base class for general world objects
  Returns: ball object
  Functions: update, calcnewpos
  Attributes: area, vector"""

  def __init__(self, (pos), vel, rad):
    pygame.sprite.Sprite.__init__(self)

    screen = pygame.display.get_surface()

    self.image = load_png('ball.png')
    self.image = pygame.transform.scale(self.image, (rad*SCALE, rad*SCALE))

    self.rect = self.image.get_rect()
    self.rect.x = pos[0]
    self.rect.y = pos[1]

    self.speed = 1
    self.vel = vel
    self.state = "still"

  def update(self):
    newpos = self.rect.move(self.vel)
    self.rect = newpos
  def moveup(self):
    self.vel[1] = self.vel[1] - (self.speed)
    self.state = "moveup"

  def moveleft(self):
    self.vel[0] = self.vel[0] - (self.speed)
    self.state = "moveleft"

  def moveright(self):
    self.vel[0] = self.vel[0] + (self.speed)
    self.state = "moveright"

  def movedown(self):
    self.vel[1] = self.vel[1] + (self.speed)
    self.state = "movedown"

def main():
  # Initialise screen
  pygame.init()
  screen = pygame.display.set_mode(ASPECT_RATIO)
  pygame.display.set_caption('Gulp')

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  global world
  world = World()
  world.randomise()
  # ball = Ball((50,0),[0, 0], 5)
  # ball2 = Ball((0,50),[0, 0], 15)

  # Initialise sprites
  ballsprites = pygame.sprite.RenderPlain(world.objects)

  # Blit everything to the screen
  screen.blit(background, (0, 0))
  pygame.display.flip()

  # Initialise clock
  clock = pygame.time.Clock()

  # Event loop
  while 1:
    # Make sure game doesn't run at more than 60 frames per second
    clock.tick(60)

    for event in pygame.event.get():
      if event.type == QUIT:
        return
      elif event.type == KEYDOWN:
        pass
      #   if event.key == K_w:
      #     ball.moveup()
      #     #player1.moveup()
      #   if event.key == K_s:
      #       ball.movedown()
      #   if event.key == K_a:
      #       ball.moveleft()
      #   if event.key == K_d:
      #       ball.moveright()
      #     #player1.movedown()
      #   if event.key == K_UP:
      #     ball2.moveup()
      #     #player2.moveup()
      #   if event.key == K_DOWN:
      #     ball2.movedown()
      #   if event.key == K_LEFT:
      #     ball2.moveleft()
      #   if event.key == K_RIGHT:
      #     ball2.moveright()
      #     #player2.movedown()
      # elif event.type == KEYUP:
      #   if event.key == K_w or event.key == K_s or event.key == K_a or event.key == K_d:
      #     pass
      #     # ball.vel = [0, 0]
      #     # ball.state = "still"
      #   if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
      #     pass
          # ball2.vel = [0, 0]
          # ball2.state = "still"
        """if event.key == K_w or event.key == K_s:
          ball.state = "still"
          #player1.movepos = [0,0]
          #player1.state = "still"
        if event.key == K_UP or event.key == K_DOWN:
          #player2.movepos = [0,0]
          #player2.state = "still"
        """
    for obj in world.objects:
      screen.blit(background, obj.rect, obj.rect)

    ballsprites.update()
    # playersprites.update()
    ballsprites.draw(screen)
    # playersprites.draw(screen)
    pygame.display.flip()

if __name__ == '__main__':
  main()
