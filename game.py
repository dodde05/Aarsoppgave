import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,450))
pygame.display.set_caption("Jons spill")
clock = pygame.time.Clock()

box = pygame.Rect(100, 100, 20, 20)
movementSpeed = 4

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  keys = pygame.key.get_pressed()

  if keys[pygame.K_w]:
    box.move_ip(0, -movementSpeed)
  if keys[pygame.K_a]:
    box.move_ip(-movementSpeed, 0)
  if keys[pygame.K_s]:
    box.move_ip(0, movementSpeed)
  if keys[pygame.K_d]:
    box.move_ip(movementSpeed, 0)

  screen.fill("black")
  pygame.draw.rect(screen, "yellow", box)

  pygame.display.update()
  clock.tick(60)