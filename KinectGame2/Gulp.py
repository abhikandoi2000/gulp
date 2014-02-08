#!/usr/bin/python

try:
  import sys
  import getopt
  import pygame
  import random, constants
  from world import World
  from time import sleep
  from socket import *
  from pygame.locals import *
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)

def main():
  # Initialise screen
  pygame.init()
  screen = pygame.display.set_mode(constants.ASPECT_RATIO)
  pygame.display.set_caption(constants.APP_TITLE)

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  world = World()
  world.randomise()

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
      """
      elif event.type == KEYDOWN:
        pass
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
          pass
          # ball.vel = [0, 0]
          # ball.state = "still"
        if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
          pass
          # ball2.vel = [0, 0]
          # ball2.state = "still"
        if event.key == K_w or event.key == K_s:
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
    ballsprites.draw(screen)

    pygame.display.flip()

if __name__ == '__main__':
  main()
