import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,450))
pygame.display.set_caption("Jons spill")
clock = pygame.time.Clock()

test_surface = pygame.Surface((200,100))
test_surface.fill("Yellow")

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  screen.blit(test_surface,(200,100))

  pygame.display.update()
  clock.tick(60)