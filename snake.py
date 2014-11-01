import sys
import random
import pygame
from pygame import Rect
from pygame.locals import *

tile_size = 32
tiles_x = 32
tiles_y = 24

width = tiles_x * tile_size
height = tiles_y * tile_size

screen = None
clock = None
apple_tick = 0

segments = []
apples = []
walls = []

speed_x = 0
speed_y = 0
game_state = 'PLAY'


class Segment():
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
    self.color = (0, 255, 0)


class Apple():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.img = pygame.image.load('apple.png')


class Wall():
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
    self.img = pygame.image.load('wall.png')


def die():
  global game_state
  print 'die'
  game_state = 'DIE'


def reset():
  global game_state, segments, apples, speed_x, speed_y, apple_tick
  print 'reset'
  game_state = 'PLAY'

  speed_x = 0
  speed_y = -tile_size
  apple_tick = 0

  segments = []
  apples = []

  # Spawn snake
  segments.append(Segment(20*tile_size, 16*tile_size))
  segments.append(Segment(20*tile_size, 17*tile_size))


def update():
  global speed_x, speed_y, apple_tick, game_state
  print 'update'
  events = pygame.event.get()

  for event in events:
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  if game_state == 'PLAY':
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_RIGHT and speed_x == 0:
          print 'right'
          speed_x = tile_size
          speed_y = 0
        if event.key == K_LEFT and speed_x == 0:
          print 'left'
          speed_x = -tile_size
          speed_y = 0
        if event.key == K_UP and speed_y == 0:
          print 'up'
          speed_x = 0
          speed_y = -tile_size
        if event.key == K_DOWN and speed_y == 0:
          print 'down'
          speed_x = 0
          speed_y = tile_size
        break

    ## Infront of snakes head
    next_x = segments[0].x + speed_x
    next_y = segments[0].y + speed_y

    ## Check for collisions
    for seg in segments:
      if next_x == seg.x and next_y == seg.y:
        print 'snake collision'
        die()
    for wall in walls:
      if next_x == wall.x and next_y == wall.y:
        print 'wall collision'
        die()

    for apple in list(apples):
      if next_x == apple.x and next_y == apple.y:
        print 'apple collision'
        segments.append(Segment())
        apples.remove(apple)

    if game_state == 'PLAY':
      ## Move snake
      for i in reversed(range(1, len(segments))):
        segments[i].x = segments[i-1].x
        segments[i].y = segments[i-1].y
      segments[0].x = next_x
      segments[0].y = next_y

    ## Spawn apple
    if apple_tick == 0:
      ax = 0
      ay = 0
      while True:
        ax = random.randint(1, tiles_x)
        ay = random.randint(1, tiles_y)

        for seg in segments:
          if seg.x == ax and seg.y == ay:
            continue
        for apple in apples:
          if apple.x == ax and apple.y == ay:
            continue
        break
      apples.append(Apple(ax*tile_size, ay*tile_size))
      apple_tick = 20
    apple_tick -= 1

    ## Draw background
    screen.fill((0, 0, 20))

    ## Draw snake segments
    for seg in segments:
      pygame.draw.circle(screen, seg.color, (seg.x, seg.y), tile_size / 2)

    ## Draw apples
    for apple in apples:
      screen.blit(apple.img, Rect(apple.x-tile_size/2, apple.y-tile_size/2, tile_size, tile_size))

    ## Draw walls
    for wall in walls:
      screen.blit(wall.img, Rect(wall.x-tile_size/2, wall.y-tile_size/2, tile_size, tile_size))

  if game_state == 'DIE':
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_SPACE:
          reset()

    font = pygame.font.SysFont("monospace", 55)
    label = font.render("you dead, shit!", 1, (255,255,0))
    lrect = label.get_rect()
    screen.blit(label, (width/2 - lrect.width/2, height/2 - lrect.height/2))

  ## Update
  pygame.display.flip()


if __name__ == '__main__':
  pygame.init()
  screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption('SNAKE!')
  clock = pygame.time.Clock()

  # Create walls
  for i in range(0, tiles_x+1):
    walls.append(Wall(i*tile_size, 0))
  for i in range(0, tiles_x+1):
    walls.append(Wall(i*tile_size, height))
  for i in range(1, tiles_y):
    walls.append(Wall(0, i*tile_size))
  for i in range(1, tiles_y):
    walls.append(Wall(width, i*tile_size))

  reset()

  while True:
    clock.tick(5)
    update()
