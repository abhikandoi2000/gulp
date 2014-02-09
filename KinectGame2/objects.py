import pygame, os, math
from time import sleep
import constants
from cmath import *

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

class WorldObject(pygame.sprite.Sprite):
  """A ball that keeps on moving in a particular direction
  Returns: WorldObject object
  Functions: update, calcnewpos
  Attributes: area, vector"""

  def __init__(self, initPos, velocity, radius, world, src = 'osmos_64.png'):
    pygame.sprite.Sprite.__init__(self)
    self.world = world
    self.image = load_png(src)
    # print radius
    self.image = pygame.transform.scale(self.image, (radius*constants.SCALE, radius*constants.SCALE))
    
    self.rect = self.image.get_rect()
    self.rect.x = initPos[0]
    self.rect.y = initPos[1]
    
    screen = pygame.display.get_surface()
    
    self.area = screen.get_rect()
    self.velocity = velocity
    self.radius = radius
    self.hit = 1

  def updateDirectionOnCollisionWith(self, objects, dx, dy):
    """
    checks if the `rect` on moving `(dx, dy)` collides with any of the
    object in `objects` and updates the direction of motion (`angle`)
    accordingly
    """
    collided = False
    
    (z, angle) = polar(self.velocity)
    
    newtopleft = (self.rect.topleft[0] + dx, self.rect.topleft[1] + dy)
    newtopright = (self.rect.topright[0] + dx, self.rect.topright[1] + dy)
    newbottomleft = (self.rect.bottomleft[0] + dx,  self.rect.bottomleft[1] + dy)
    newbottomright = (self.rect.bottomright[0] + dx, self.rect.bottomright[1] + dy)
    
    # detect for each WorldObject
    for obj in [obj for obj in objects if self != obj]:
      tl = not obj.rect.collidepoint(newtopleft)
      tr = not obj.rect.collidepoint(newtopright)
      bl = not obj.rect.collidepoint(newbottomleft)
      br = not obj.rect.collidepoint(newbottomright)
      if self.rect.colliderect(obj.rect):
        collided = True
        if self.radius > obj.radius:
          self.radius = self.radius + constants.RADIUS_CHANGE
          if obj.radius < 0:
            obj.radius = 0
            obj.rect.x = 5000
          return 1
        else:
          self.radius = self.radius - constants.RADIUS_CHANGE
          if self.radius < 0:
            self.radius = 0
            self.rect.x = 5000
          return -1
    return 0

  def move(self):
    """dpos - change in position
       eg: [1, 1] : move 1 unit in x and one in y
    """
    
    (dx, dy) = (math.ceil(self.velocity.real), math.ceil(self.velocity.imag))
    collided = self.updateDirectionOnCollisionWith(self.world.objects, dx, dy)
    self.rect = self.rect.move(dx, dy)
    if collided == 1:
      x = self.rect.x
      y = self.rect.y

      if type(self) == PlayerObject:
        src = 'osmos_player.png'
      else:
        src = 'osmos_64.png'
      
      self.image = load_png(src)
      self.image = pygame.transform.scale(self.image, (int(self.radius*constants.SCALE), int(self.radius*constants.SCALE)))
      
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
      # print self.rect, self.image
    elif collided == -1:
      x = self.rect.x
      y = self.rect.y
      
      if type(self) == PlayerObject:
        src = 'osmos_player.png'
      else:
        src = 'osmos_64.png'
      
      self.image = load_png(src)
      self.image = pygame.transform.scale(self.image, (int(self.radius * constants.SCALE), int(self.radius * constants.SCALE)))
      
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

    return collided
  
  def update(self):
    (z, angle) = polar(self.velocity)

    if not self.area.contains(self.rect):
      tl = not self.area.collidepoint(self.rect.topleft)
      tr = not self.area.collidepoint(self.rect.topright)
      bl = not self.area.collidepoint(self.rect.bottomleft)
      br = not self.area.collidepoint(self.rect.bottomright)

      if not(tr and tl and br and bl):
        if tr and tl:
          angle = -angle
          self.rect = self.rect.move(0, self.area.top-self.rect.top+1) 
        if br and bl:
          angle = -angle
          self.rect = self.rect.move(0, self.area.bottom-self.rect.bottom-1)
        if tl and bl:
          angle = math.pi - angle
          self.rect = self.rect.move(self.area.left-self.rect.left+1,0)  
        if tr and br:
          angle = math.pi - angle
          self.rect = self.rect.move(self.area.right-self.rect.right-1, 0)

      elif tr and tl and br and bl:
        if self.rect.top > self.area.bottom:
          angle = -angle
          self.rect = self.rect.move(0, self.area.bottom-self.rect.top-1)
        if self.rect.bottom < self.area.top:
          angle = -angle
          self.rect = self.rect.move(0, self.area.top-self.rect.bottom+1) 
        if self.rect.left > self.area.right:
          angle = math.pi - angle
          self.rect = self.rect.move(self.area.right-self.rect.left-1, 0)
        if self.rect.right < self.area.left:
          angle = math.pi - angle
          self.rect = self.rect.move(self.area.left-self.rect.right+1,0)  

    self.velocity = z * math.cos(angle) + z * math.sin(angle)*1j
    self.move()
    
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

class PlayerObject(WorldObject):
  def __init__(self, initPos, velocity, radius, world, color):
    super(PlayerObject, self).__init__(initPos, velocity, radius, world, 'osmos_player.png')
    self.action = "still"
    self.color = color
    # print self

  def update(self):
    # x = self.rect.x
    # y = self.rect.y
    # radius = self.radius

    # self.image = pygame.transform.scale(self.image, (0, 0))
    # self.rect.x = 5000
    # self.image = load_png('osmos_player.png')
    # self.image = pygame.transform.scale(self.image, (int(radius * constants.SCALE), int(radius * constants.SCALE)))
    # self.rect = self.image.get_rect()
    # self.rect.x = x
    # self.rect.y = y
    # dx = 0
    # dy = 0
    # speed = random.randint(2, constants.VEL_RANGE)
    # direction = random.uniform(-1 * (math.pi / 2), (3 * math.pi) / 2)
    direction = 0
    speed = 0
    if self.action == "moveup":
      direction = 3*math.pi/2
      speed = constants.VEL_CHANGE
      # dy = -10
    if self.action == "movedown":
      direction = math.pi/2
      speed = constants.VEL_CHANGE
      # dy = 10
    if self.action == "moveleft":
      direction = math.pi
      speed = constants.VEL_CHANGE
      # dx = -10
    if self.action == "moveright":
      direction = 0
      speed = constants.VEL_CHANGE

    self.velocity += speed * math.cos(direction) + speed * math.sin(direction)*1j
    (magnitude, direction) = polar(self.velocity)
    if  magnitude > constants.VEL_LIMIT:
      self.velocity = constants.VEL_LIMIT * math.cos(direction) + constants.VEL_LIMIT * math.sin(direction)*1j
      # dx = 10
    # self.rect.x += dx
    # self.rect.y += dy
    self.action = "still"
    super(PlayerObject, self).update()

  def moveup(self):
    self.action = "moveup"
    # self.rect = self.rect.move(0, -10)

  def movedown(self):
    self.action = "movedown"

  def moveleft(self):
    self.action = "moveleft"

  def moveright(self):
    self.action = "moveright"
    # self.rect = self.rect.move(10, 0)