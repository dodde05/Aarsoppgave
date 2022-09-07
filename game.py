import pygame
from sys import exit
import map

class Game:
  def __init__(self):
    
    pygame.init()
    self.screen = pygame.display.set_mode((800, 450))
    self.clock = pygame.time.Clock()

    self.player = Player()

  def run(self):
    while True:

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      player.movement()
      player.gravity()

      self.screen.fill("black")

      terrain.create_level()
      pygame.draw.rect(self.screen, "yellow", player.box)
      
      pygame.display.update()
      self.clock.tick(60)

class Player:
  def __init__(self):
    self.box = pygame.Rect(100, 100, 20, 20)

    self.movementSpeed = 4
    self.yspeed = 0

  def movement(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
      self.box.move_ip(-self.movementSpeed, 0)
    if keys[pygame.K_d]:
      self.box.move_ip(self.movementSpeed, 0)

  def gravity(self):
    if self.collision():
      self.yspeed = 0
      return
    else:
      self.yspeed += .3
      self.box.move_ip(0, self.yspeed)
  
  def collision(self):
    colliding_i = self.box.collidelist(terrain.rects)

    if colliding_i == -1:
      return False
    elif abs(self.box.bottom - terrain.rects[colliding_i].top) < 10:
      self.box.bottom = terrain.rects[colliding_i].top
      return True

class Terrain:
  def __init__(self):
    self.rects = []

    for row_i, row in enumerate(map.map_layout):
      for col_i, col in enumerate(row):
        if col == "o":
          self.rects.append(pygame.Rect(col_i * map.TILESIZE, row_i * map.TILESIZE, map.TILESIZE, map.TILESIZE))

  def create_level(self):
    for i, rect in enumerate(self.rects):
      pygame.draw.rect(game.screen, "red", self.rects[i])

if __name__ == "__main__":
  game = Game()
  player = Player()
  terrain = Terrain()

  game.run()