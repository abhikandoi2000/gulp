import pygame, os, math
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

  def __init__(self, initPos, velocity, radius, world):
    pygame.sprite.Sprite.__init__(self)
    self.world = world
    self.image = load_png('osmos_64.png')
    self.image = pygame.transform.scale(self.image, (radius*constants.SCALE, radius*constants.SCALE))
    
    self.rect = self.image.get_rect()
    self.rect.x = initPos[0]
    self.rect.y = initPos[1]
    
    screen = pygame.display.get_surface()
    
    self.area = screen.get_rect()
    self.velocity = velocity
    self.hit = 1

  def updateDirectionOnCollisionWith(self, objects, dx, dy):
    """
    checks if the `rect` on moving `(dx, dy)` collides with any of the
    object in `objects` and updates the direction of motion (`angle`)
    accordingly
    """
    collided = False
    
    (z, angle) = polar(self.velocity)
    
    # detect for each WorldObject
    for obj in [obj for obj in objects if self != obj]:
      if self.rect.colliderect(obj.rect):
        collided = True
        obj.rect.inflate(-3, -3)

        if not self.hit:
          # finalVelocity = 
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
          if bl and br:
            # hit from the top side
            self.rect.bottom = obj.rect.top
            angle = 2 * math.pi - angle
          if tl and tr:
            # hit from the bottom side
            self.rect.top = obj.rect.bottom
            angle = -1 * angle
          
          self.hit = not self.hit
        elif self.hit:
          self.hit = not self.hit

    # self.vector = (angle, z)

    return collided

  def move(self):
    """dpos - change in position
       eg: [1, 1] : move 1 unit in x and one in y
    """
    
    # (angle,z) = vector
    
    (dx, dy) = (self.velocity.real, self.velocity.imag)
    collided = self.updateDirectionOnCollisionWith(self.world.objects, dx, dy)
    if not collided:
      self.rect = self.rect.move(dx, dy)
    return collided
  
  def update(self):
    self.move()
    (z, angle) = polar(self.velocity)

    if not self.area.contains(self.rect):
      tl = not self.area.collidepoint(self.rect.topleft)
      tr = not self.area.collidepoint(self.rect.topright)
      bl = not self.area.collidepoint(self.rect.bottomleft)
      br = not self.area.collidepoint(self.rect.bottomright)
      if tr and tl or (br and bl):
        angle = -angle
      if tl and bl:
        angle = math.pi - angle
      if tr and br:
        angle = math.pi - angle
    
    self.velocity = z * math.cos(angle) + z * math.sin(angle)*1j
    
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