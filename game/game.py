import pygame
from sys import exit
import random

import map


class Game:
    def __init__(self):
        pygame.init()

        self.active = True

        self.SIZEFACTOR = 50
        SCREENRATIO = [16, 9]

        self.resolution = {"x": SCREENRATIO[0] * self.SIZEFACTOR, "y": SCREENRATIO[1] * self.SIZEFACTOR}
        
        self.screen = pygame.display.set_mode((self.resolution["x"], self.resolution["y"]))
        self.clock = pygame.time.Clock()

    def run(self):
        while self.active:

            player.input()
            player.movement()

            cannon.selection()


            self.screen.fill("deepskyblue")

            terrain.drawLevel()
            pygame.draw.rect(self.screen, "yellow", player.rect)
            for ball in cannon.balls:
                ball.move()
                pygame.draw.rect(self.screen, "black", ball.rect, 0, 12)


            pygame.display.update()
            self.clock.tick(60)


class Player:
    def __init__(self):
        self.rect = pygame.Rect(15, 0, 20, 20)

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
        self.rect.x, self.rect.y = 100, 50

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
        colliding_i = self.rect.collidelist(terrain.ground)

        if colliding_i != -1:

            if self.xspeed > 0:
                self.rect.right = terrain.ground[colliding_i].left
                self.rightWall = True
            else:
                self.rect.left = terrain.ground[colliding_i].right
                self.leftWall = True

        else:
            self.leftWall = self.rightWall = False

    def vCollision(self):
        colliding_i = self.rect.collidelist(terrain.ground)

        if colliding_i != -1:

            if self.yspeed > 0:
                self.rect.bottom = terrain.ground[colliding_i].top
                self.grounded = True
            else:
                self.rect.top = terrain.ground[colliding_i].bottom
                self.grounded = False

            self.yspeed = 1

        else:
            self.pCollision()

    def pCollision(self):
        colliding_i = self.rect.collidelist(terrain.platforms)

        if colliding_i != -1:

            if self.yspeed >= 0:
                self.rect.bottom = terrain.platforms[colliding_i].top
                self.platformed = True

                self.yspeed = 1

        else:
            self.yspeed += self.gravity
            self.grounded = False
            self.platformed = False

    def movement(self):
        self.rect.x += self.xspeed
        self.hCollision()

        self.rect.y += self.yspeed
        self.vCollision()


class Cannon:
    def __init__(self):
        self.positions = {"left": [], "right": []}
        self.balls = []

        for tile in range(map.grid["y"] - 1):
            self.positions["left"].append([-terrain.tilesize, terrain.tilesize * tile])
            self.positions["right"].append([game.resolution["x"], terrain.tilesize * tile])
    
    def selection(self):
        side = random.randint(0, 1)
        cannon = random.randint(0, 16)
        chance = random.randint(1, 60)

        if chance == 60:
            if side == 0:
                self.balls.append(Cannonball(self.positions["left"][cannon], len(self.balls)))
            else:
                self.balls.append(Cannonball(self.positions["right"][cannon], len(self.balls)))


class Cannonball:
    def __init__(self, pos: list[int], index: int):
        self.rect = pygame.Rect(pos[0], pos[1], terrain.tilesize, terrain.tilesize)
        self.index = index
        self.xspeed = 0
        if pos[0] < game.resolution["x"] / 2: # If cannonball postion is to the left of the middle of the screen
            self.xspeed = 6
        else:
            self.xspeed = -6

    def move(self):
        self.rect.move_ip(self.xspeed, 0)

        if self.xspeed > 0 and self.rect.x > game.resolution["x"] or self.xspeed < 0 and self.rect.x < -terrain.tilesize:
            for ball in cannon.balls:
                if ball.index > self.index:
                    ball.index -= 1
            del cannon.balls[self.index]
        
        self.hit()

    def hit(self):
        if self.rect.colliderect(player.rect):
            game.active = False


class Terrain:
    def __init__(self):
        self.tilesize = game.SIZEFACTOR / 2

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

def start():
    global game 
    game = Game()

    global player
    player = Player()

    global terrain
    terrain = Terrain()

    global cannon
    cannon = Cannon()

if __name__ == "__main__":
    start()
    game.run()