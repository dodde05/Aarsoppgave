import pygame
from sys import exit
import map


class Game:
  def __init__(self):
    
    pygame.init()
    self.screen = pygame.display.set_mode((800, 450))
    self.clock = pygame.time.Clock()

  def run(self):
    while True:

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
      
      player.movement()

      self.screen.fill("black")

      terrain.create_level()
      pygame.draw.rect(self.screen, "yellow", player.box)
      
      pygame.display.update()
      self.clock.tick(60)


class Player:
  def __init__(self):
    self.box = pygame.Rect(100, 100, 20, 20)

    self.xspeed = 0
    self.xmax = 4

    self.yspeed = 0
    self.ymax = 10

  def movement(self):
    keys = pygame.key.get_pressed()

    # Restart
    if keys[pygame.K_r]:
      self.__init__()
    
    # Horizontal movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.xspeed -= .5
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.xspeed += .5

    if not keys[pygame.K_a] and not keys[pygame.K_d]:
      if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        self.xspeed = 0
    
    if self.xspeed > self.xmax:
      self.xspeed = self.xmax
    elif self.xspeed < -self.xmax:
      self.xspeed = -self.xmax

    # Vertical movement
    collision = self.collision() # The collision detection shall only be done once per frame
    
    if collision:
      if keys[pygame.K_SPACE]:
        self.yspeed = -5
    elif collision == False:
      pass
    else:
      self.yspeed += .5

    self.box.move_ip(self.xspeed, self.yspeed)

  def collision(self):
    colliding_i = self.box.collidelist(terrain.rects)

    if colliding_i == -1:
      currentx = self.box.x
      currenty = self.box.y

      xquarter = self.xspeed / 4
      yquarter = self.yspeed / 4

      for i in range(1, 4):

        self.box.move_ip(xquarter * i, yquarter * i)
        colliding_i = self.box.collidelist(terrain.rects)
        if colliding_i != -1:

          if abs(self.box.bottom - terrain.rects[colliding_i].top) < 5:
            self.yspeed = 0
            self.box.bottom = terrain.rects[colliding_i].top + 1
            return True
          if abs(self.box.top - terrain.rects[colliding_i].bottom) < 5:
            self.yspeed = 0
            self.box.top = terrain.rects[colliding_i].bottom
            return False
          if abs(self.box.right - terrain.rects[colliding_i].left) < 5:
            self.xspeed = 0
            self.box.right = terrain.rects[colliding_i].left
            return False
          if abs(self.box.left - terrain.rects[colliding_i].right) < 5:
            self.xspeed = 0
            self.box.left = terrain.rects[colliding_i].right
            return False
          
          self.box.x, self.box.y = currentx, currenty
    else:
      if abs(self.box.bottom - terrain.rects[colliding_i].top) < 5:
        self.yspeed = 0
        self.box.bottom = terrain.rects[colliding_i].top + 1
        return True
      if abs(self.box.top - terrain.rects[colliding_i].bottom) < 5:
        self.yspeed = 0
        self.box.top = terrain.rects[colliding_i].bottom
        return False
      if abs(self.box.right - terrain.rects[colliding_i].left) < 5:
        self.xspeed = 0
        self.box.right = terrain.rects[colliding_i].left
        return False
      if abs(self.box.left - terrain.rects[colliding_i].right) < 5:
        self.xspeed = 0
        self.box.left = terrain.rects[colliding_i].right
        return False


class Terrain:
  def __init__(self):
    self.rects = []

    for row_i, row in enumerate(map.map_layout):
      for col_i, col in enumerate(row):
        if col == "o":
          self.rects.append(pygame.Rect(col_i * map.TILESIZE - map.TILESIZE, row_i * map.TILESIZE - map.TILESIZE, map.TILESIZE, map.TILESIZE))

  def create_level(self):
    for i, rect in enumerate(self.rects):
      pygame.draw.rect(game.screen, "red", self.rects[i])

if __name__ == "__main__":
  game = Game()
  player = Player()
  terrain = Terrain()

  game.run()