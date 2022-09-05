import pygame
from sys import exit
import level

class Game:
  def __init__(self):

    pygame.init()
    self.screen = pygame.display.set_mode((level.WIDTH, level.HEIGHT))
    self.clock = pygame.time.Clock()

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
      pygame.draw.rect(self.screen, "yellow", player.box)

      pygame.display.update()
      self.clock.tick(60)

class Player:
  def __init__(self):
    
    self.box = pygame.Rect(100, 100, 20, 20)
    self.movementSpeed = 4

if __name__ == "__main__":
  game = Game()
  player = Player()

  game.run()