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
			print([player.grounded, player.platformed, player.yspeed])
			player.input()
			player.movement()

			self.screen.fill("black")

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
        
			if event.type == pygame.KEYUP: ...

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


class Terrain:
	def __init__(self):
		tilesize = map.TILESIZE

		self.ground = []
		self.platforms = []

		for row_i, row in enumerate(map.map_layout):
			for col_i, col in enumerate(row):
				if col == "o":
					self.ground.append(pygame.Rect(col_i * tilesize - tilesize, row_i * tilesize - tilesize, tilesize, tilesize))
				elif col == "x":
					self.platforms.append(pygame.Rect(col_i * tilesize - tilesize, row_i * tilesize - tilesize, tilesize, 10))

	def drawLevel(self):
		for i, rect in enumerate(self.ground):
			pygame.draw.rect(game.screen, "red", self.ground[i])
		for i, rect in enumerate(self.platforms):
			pygame.draw.rect(game.screen, "coral4", self.platforms[i])


if __name__ == "__main__":
	game = Game()
	player = Player()
	terrain = Terrain()

	game.run()