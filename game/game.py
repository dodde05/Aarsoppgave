import pygame
from sys import exit
import random
import time
import tkinter as tk
import mysql.connector

import map


class Game:
    """Main class containing game loop, variables and database upload code"""

    def __init__(self):
        pygame.init()

        self.active = True

        self.timer = 0
        self.difficulty = 0

        self.prompt = False

        self.SIZEFACTOR = 50
        SCREENRATIO = [16, 9]

        self.resolution = {"x": SCREENRATIO[0] * self.SIZEFACTOR, "y": SCREENRATIO[1] * self.SIZEFACTOR} # x: 800, y: 450
        
        self.screen = pygame.display.set_mode((self.resolution["x"], self.resolution["y"]))
        self.clock = pygame.time.Clock()

    def run(self):
        while self.active:
            self.time()


            player.events()
            player.movement()

            cannon.selection()


            self.screen.fill("deepskyblue")

            terrain.drawLevel()
            pygame.draw.rect(self.screen, "yellow", player.rect)
            for ball in cannon.balls:
                ball.move()
                pygame.draw.rect(self.screen, "black", ball.rect, 0, 12)

            pygame.display.set_caption(f"Your score: {round(self.timer, 2)}")
            pygame.display.update()
            self.clock.tick(60)
        
        self.end()
    
    def time(self):
        self.timer += 1 / 60
        self.difficulty += 1 / 60

        if self.difficulty > 10:
            self.difficulty -= 10
            if cannon.fireChance > 10:
                cannon.fireChance -= 2

    def end(self):
        text = pygame.display

        text.set_caption("YOU DIED")
        time.sleep(3)
        text.set_caption(f"Final score: {round(self.timer, 2)}")
        time.sleep(3)

        text.set_caption("Would you like to upload your score? y/n")
        while not self.prompt:
            if player.events():
                root = tk.Tk()
                root.title("Score Upload")
                root.geometry("400x225")

                inputtxt = tk.Text(root, height = 5, width = 40)
                inputtxt.insert("1.0", "Enter a name")
                inputtxt.pack()

                def upload():
                    conn = mysql.connector.connect(
                        host="10.2.2.4",
                        user="client",
                        password="79E76w864dcKbja",
                        database="highscores"
                    )

                    cursor = conn.cursor()

                    text = inputtxt.get(1.0, "end-1c")
                    query = f"INSERT INTO attempt (navn, score, dato) VALUES ('{text}', {self.timer}, CURDATE())"
                    cursor.execute(query)

                    conn.commit()

                    root.destroy()
                
                button = tk.Button(root, text = "Upload", command = upload)
                button.pack()

                lbl = tk.Label(root, text = "")
                lbl.pack()

                root.mainloop()


class Player:
    """Class containing player rectangle and all its variables, as well as the input function"""
    def __init__(self):
        self.rect = pygame.Rect(game.resolution["x"] / 2 - 10, 405, 20, 20)

        self.xspeed = 0
        self.xmax = 6
        self.acceleration = 1

        self.leftWall = False
        self.rightWall = False

        self.yspeed = 0
        self.gravity = 1

        self.grounded = False
        self.platformed = False

    def events(self):
        keys = pygame.key.get_pressed()

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

        # y/n prompts
        if keys[pygame.K_y]:
            game.prompt = True
            return True
        elif keys[pygame.K_n]:
            game.prompt = True

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

        self.fireChance = 60

        for tile in range(map.grid["y"] - 1):
            self.positions["left"].append([-terrain.tilesize, terrain.tilesize * tile])
            self.positions["right"].append([game.resolution["x"], terrain.tilesize * tile])
    
    def selection(self):
        side = random.randint(0, 1)
        height = random.randint(0, 16)
        chance = random.randint(1, self.fireChance)
        speed = random.randint(6, 10)

        if chance == self.fireChance:
            if side == 0:
                self.balls.append(Cannonball(self.positions["left"][height], len(self.balls), speed))
            else:
                self.balls.append(Cannonball(self.positions["right"][height], len(self.balls), speed))


class Cannonball:
    def __init__(self, pos: list[int], index: int, speed: int):
        self.rect = pygame.Rect(pos[0], pos[1], terrain.tilesize, terrain.tilesize)
        self.index = index
        self.xspeed = 0
        if pos[0] < game.resolution["x"] / 2: # If cannonball postion is to the left of the middle of the screen
            self.xspeed = speed
        else:
            self.xspeed = -speed

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
    global game, player, terrain, cannon

    game = Game()
    player = Player()
    terrain = Terrain()
    cannon = Cannon()

if __name__ == "__main__":
    start()
    game.run()