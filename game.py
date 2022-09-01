import pygame
from sys import exit

class Game:
  def __init__(self):

    pygame.init()
    self.screen = pygame.display.set_mode((800,450))
    self.clock = pygame.time.Clock()

    self.box = pygame.Rect(100, 100, 20, 20)
    self.movementSpeed = 4

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      keys = pygame.key.get_pressed()

      if keys[pygame.K_w]:
        self.box.move_ip(0, -self.movementSpeed)
      if keys[pygame.K_a]:
        self.box.move_ip(-self.movementSpeed, 0)
      if keys[pygame.K_s]:
        self.box.move_ip(0, self.movementSpeed)
      if keys[pygame.K_d]:
        self.box.move_ip(self.movementSpeed, 0)

      self.screen.fill("black")
      pygame.draw.rect(self.screen, "yellow", self.box)

      pygame.display.update()
      self.clock.tick(60)

if __name__ == "__main__":
  game = Game()
  game.run()