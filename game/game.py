import pygame
from sys import exit
import random

import map


class Game:
    def __init__(self):
        pygame.init()

        self.SCREENSIZE = 50
        SCREENRATIO = [16, 9]

        self.resolution = [SCREENRATIO[0] * self.SCREENSIZE, SCREENRATIO[1] * self.SCREENSIZE]
        
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:

            player.input()
            player.movement()
            cannonball.launch()

            self.screen.fill("deepskyblue")

            terrain.drawLevel()
            pygame.draw.rect(self.screen, "yellow", player.box)

            pygame.display.update()
            self.clock.tick(60)


class Player:
    def __init__(self):
        self.box = pygame.Rect(15, 0, 20, 20)

        self.xspeed = 0
        self.xmax = 6
        self.acceleration = 1

        self.leftWall = False
        self.rightWall = False

        self.yspeed = 0
        self.gravity = 1

        self.grounded = False
        self.platformed = False

    def reset(self):
        self.box.x, self.box.y = 100, 50

        self.xspeed = 0
        self.yspeed = 0

    def input(self):
        keys = pygame.key.get_pressed()

        # Restart
        if keys[pygame.K_r]:
            self.reset()

        # Horizontal speed control
        self.leftInput = keys[pygame.K_a] or keys[pygame.K_LEFT]
        self.rightInput = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        if (self.leftInput and self.rightInput) or (not self.leftInput and not self.rightInput):
            if self.xspeed > 0:
                self.xspeed -= self.acceleration
            elif self.xspeed < 0:
                self.xspeed += self.acceleration
        else:

            if self.leftInput:
                self.xspeed -= self.acceleration

            if self.rightInput:
                self.xspeed += self.acceleration

        if self.xspeed > self.xmax:
            self.xspeed = self.xmax
        elif self.xspeed < -self.xmax:
            self.xspeed = -self.xmax

        # (Wall)Jumping
        if keys[pygame.K_SPACE] and (self.grounded or self.platformed):
            self.yspeed = -15

        elif (self.leftWall or self.rightWall) and self.yspeed > 0:
            self.yspeed = 5
            if keys[pygame.K_SPACE]:
                self.yspeed = -15
                if self.leftWall:
                    self.xspeed = self.xmax
                else:
                    self.xspeed = -self.xmax

        # Event inputs
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.KEYUP:
                ...

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def hCollision(self):
        colliding_i = self.box.collidelist(terrain.ground)

        if colliding_i != -1:

            if self.xspeed > 0:
                self.box.right = terrain.ground[colliding_i].left
                self.rightWall = True
            else:
                self.box.left = terrain.ground[colliding_i].right
                self.leftWall = True

        else:
            self.leftWall = self.rightWall = False

    def vCollision(self):
        colliding_i = self.box.collidelist(terrain.ground)

        if colliding_i != -1:

            if self.yspeed > 0:
                self.box.bottom = terrain.ground[colliding_i].top
                self.grounded = True
            else:
                self.box.top = terrain.ground[colliding_i].bottom
                self.grounded = False

            self.yspeed = 1

        else:
            self.pCollision()

    def pCollision(self):
        colliding_i = self.box.collidelist(terrain.platforms)

        if colliding_i != -1:

            if self.yspeed >= 0:
                self.box.bottom = terrain.platforms[colliding_i].top
                self.platformed = True

                self.yspeed = 1

        else:
            self.yspeed += self.gravity
            self.grounded = False
            self.platformed = False

    def movement(self):
        self.box.x += self.xspeed
        self.hCollision()

        self.box.y += self.yspeed
        self.vCollision()


class Cannonball:
    def __init__(self):
        self.positions = {"left": [], "right": []}

        for tile in range(map.grid["y"]):
            self.positions["left"].append([-terrain.tilesize, terrain.tilesize * tile])
        for i in range(map.grid["y"]):
            self.positions["right"].append([game.resolution[0], terrain.tilesize * tile])
    
    def launch(self):
        side = random.randint(0, 1)
        cannon = random.randint(0, 17)

        if side == 0:
            print(self.positions["left"][cannon])
        else:
            print(self.positions["right"][cannon])


class Terrain:
    def __init__(self):
        self.tilesize = game.SCREENSIZE / 2

        self.ground = []
        self.platforms = []

        for row_i, row in enumerate(map.LAYOUT):
            for col_i, col in enumerate(row):
                if col == "o" or col == "0":
                    self.ground.append(pygame.Rect(col_i * self.tilesize - self.tilesize, row_i * self.tilesize - self.tilesize, self.tilesize, self.tilesize))
                elif col == "x":
                    self.platforms.append(pygame.Rect(col_i * self.tilesize - self.tilesize, row_i * self.tilesize - self.tilesize, self.tilesize, 10))

    def drawLevel(self):
        for i, rect in enumerate(self.ground):
            pygame.draw.rect(game.screen, "darkgreen", self.ground[i])
        for i, rect in enumerate(self.platforms):
            pygame.draw.rect(game.screen, "coral4", self.platforms[i])


if __name__ == "__main__":
    game = Game()
    player = Player()
    terrain = Terrain()
    cannonball = Cannonball()

    game.run()