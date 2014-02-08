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
  # For full screen support flag
  # screen = pygame.display.set_mode(constants.ASPECT_RATIO, pygame.FULLSCREEN)
  screen = pygame.display.set_mode(constants.ASPECT_RATIO)
  pygame.display.set_caption(constants.APP_TITLE)

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  world = World()

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
        pygame.quit()
        return
      if event.type == KEYDOWN:
        # print "keydown"
        if event.key == K_ESCAPE:
          """ Use Escape Key to Quit """
          pygame.display.quit()
          pygame.quit()
        if event.key == K_UP:
          world.objects[-1:][0].moveup()
        if event.key == K_DOWN:
          world.objects[-1:][0].movedown()
        if event.key == K_LEFT:
          world.objects[-1:][0].moveleft()
        if event.key == K_RIGHT:
          world.objects[-1:][0].moveright()
        if event.key == K_w:
          world.objects[-2:-1][0].moveup()
        if event.key == K_s:
          world.objects[-2:-1][0].movedown()
        if event.key == K_a:
          world.objects[-2:-1][0].moveleft()
        if event.key == K_d:
          world.objects[-2:-1][0].moveright()
      elif event.type == KEYUP:
        # print "keyup"
        """
        if event.key == K_w or event.key == K_s or event.key == K_a or event.key == K_d:
          pass
          # ball.vel = [0, 0]
          # ball.state = "still"
        """
        if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
          pass
    for obj in world.objects:
      screen.blit(background, obj.rect, obj.rect)

    ballsprites.update()
    ballsprites.draw(screen)

    pygame.display.flip()

if __name__ == '__main__':
  main()
