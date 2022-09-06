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

      keys = pygame.key.get_pressed()

      if keys[pygame.K_w]:
        player.box.move_ip(0, -player.movementSpeed)
      if keys[pygame.K_a]:
        player.box.move_ip(-player.movementSpeed, 0)
      if keys[pygame.K_s]:
        player.box.move_ip(0, player.movementSpeed)
      if keys[pygame.K_d]:
        player.box.move_ip(player.movementSpeed, 0)

      self.screen.fill("black")

      terrain.create_level()
      pygame.draw.rect(self.screen, "yellow", player.box)
      
      pygame.display.update()
      self.clock.tick(60)

class Player:
  def __init__(self):
    
    self.box = pygame.Rect(100, 100, 20, 20)
    self.movementSpeed = 4

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