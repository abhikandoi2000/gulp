#!/usr/bin/python
#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml
#
# Released under the GNU General Public License
VERSION = "0.4"

try:
  import sys
  import random
  import math
  import os
  import getopt
  import pygame
  from socket import *
  from pygame.locals import *
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)

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
  return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
  """A ball that will move across the screen
  Returns: ball object
  Functions: update, calcnewpos
  Attributes: area, vector"""

  def __init__(self, (xy), vector):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_png('ball.png')
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.vector = vector
    self.speed = 10
    self.hit = 0
    self.state = "still"
    self.movepos = [0,0]

  def update(self):
    #newpos = self.calcnewpos(self.rect,self.vector)
    newpos = self.rect.move(self.movepos)
    self.rect = newpos
    (angle,z) = self.vector

    if not self.area.contains(newpos):
      tl = not self.area.collidepoint(newpos.topleft)
      tr = not self.area.collidepoint(newpos.topright)
      bl = not self.area.collidepoint(newpos.bottomleft)
      br = not self.area.collidepoint(newpos.bottomright)
      if tr and tl or (br and bl):
        angle = -angle
      if tl and bl:
        #self.offcourt()
        angle = math.pi - angle
      if tr and br:
        angle = math.pi - angle
        #self.offcourt()
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
    self.vector = (angle,z)

  def calcnewpos(self, rect, vector):
    (angle,z) = vector
    (dx,dy) = (z * math.cos(angle),z * math.sin(angle))
    return rect.move(dx,dy)
  
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

class Bat(pygame.sprite.Sprite):
  def __init__(self, side):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_png('bat.png')
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.side = side
    self.speed = 10
    self.state = "still"
    self.reinit()

  def reinit(self):
    self.state = "still"
    self.movepos = [0,0]
    if self.side == "left":
      self.rect.midleft = self.area.midleft
    elif self.side == "right":
      self.rect.midright = self.area.midright

  def update(self):
    newpos = self.rect.move(self.movepos)
    if self.area.contains(newpos):
      self.rect = newpos
    pygame.event.pump()

  def moveup(self):
    self.movepos[1] = self.movepos[1] - (self.speed)
    self.state = "moveup"

  def movedown(self):
    self.movepos[1] = self.movepos[1] + (self.speed)
    self.state = "movedown"


def main():
  # Initialise screen
  pygame.init()
  screen = pygame.display.set_mode((640, 480))
  pygame.display.set_caption('The Masculine Ping Pong Game')

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  # Initialise players
  global player1
  global player2
  player1 = Bat("left")
  player2 = Bat("right")

  # Initialise ball
  speed = 13
  rand = ((0.1 * (random.randint(5,8))))
  ball = Ball((0,0),(0.47,speed))
  ball2 = Ball((0,0),(0.47,speed))

  # Initialise sprites
  playersprites = pygame.sprite.RenderPlain((player1, player2))
  ballsprites = pygame.sprite.RenderPlain(ball, ball2)

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
        if event.key == K_w:
          ball.moveup()
          #player1.moveup()
        if event.key == K_s:
            ball.movedown()
        if event.key == K_a:
            ball.moveleft()
        if event.key == K_d:
            ball.moveright()
          #player1.movedown()
        if event.key == K_UP:
          ball2.moveup()
          #player2.moveup()
        if event.key == K_DOWN:
          ball2.movedown()
        if event.key == K_LEFT:
          ball2.moveleft()
        if event.key == K_RIGHT:
          ball2.moveright()
          #player2.movedown()
      elif event.type == KEYUP:
        if event.key == K_w or event.key == K_s or event.key == K_a or event.key == K_d:
          ball.movepos = [0, 0]
          ball.state = "still"
        if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
          ball2.movepos = [0, 0]
          ball2.state = "still"
        """if event.key == K_w or event.key == K_s:
          ball.state = "still"
          #player1.movepos = [0,0]
          #player1.state = "still"
        if event.key == K_UP or event.key == K_DOWN:
          #player2.movepos = [0,0]
          #player2.state = "still"
        """

    screen.blit(background, ball.rect, ball.rect)
    screen.blit(background, ball2.rect, ball2.rect)
    screen.blit(background, player1.rect, player1.rect)
    screen.blit(background, player2.rect, player2.rect)
    ballsprites.update()
    playersprites.update()
    ballsprites.draw(screen)
    playersprites.draw(screen)
    pygame.display.flip()

if __name__ == '__main__':
  main()
