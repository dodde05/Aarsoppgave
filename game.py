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
			print(player.grounded)
			player.input()
			player.movement()

			self.screen.fill("black")

			terrain.drawLevel()
			pygame.draw.rect(self.screen, "yellow", player.box)

			pygame.display.update()
			self.clock.tick(60)


class Player:
	def __init__(self):
		self.box = pygame.Rect(100, 50, 20, 20)

		self.xspeed = 0
		self.xmax = 6
		self.acceleration = 1

		self.yspeed = 0
		self.gravity = 1
		self.grounded = False

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
		left = keys[pygame.K_a] or keys[pygame.K_LEFT]
		right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

		if left and right:
			self.xspeed = 0
		else:

			if left:
				if self.xspeed > 0:
					self.xspeed = 0
				self.xspeed -= self.acceleration

			if right:
				if self.xspeed < 0:
					self.xspeed = 0
				self.xspeed += self.acceleration

		if not keys[pygame.K_a] and not keys[pygame.K_d]:
			if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
				self.xspeed = 0

		if self.xspeed > self.xmax:
			self.xspeed = self.xmax
		elif self.xspeed < -self.xmax:
			self.xspeed = -self.xmax

		# Jumping
		if keys[pygame.K_SPACE]:
			if self.grounded:
				self.yspeed -= 15
    
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
		colliding_i = self.box.collidelist(terrain.rects)

		if colliding_i != -1:
			rightDiff = abs(self.box.right - terrain.rects[colliding_i].left)
			leftDiff = abs(self.box.left - terrain.rects[colliding_i].right)

			if rightDiff < leftDiff:
				self.box.right = terrain.rects[colliding_i].left
				return True
			else:
				self.box.left = terrain.rects[colliding_i].right
				return True

	def vCollision(self):
		colliding_i = self.box.collidelist(terrain.rects)

		if colliding_i != -1:
			self.yspeed = 0

			botDiff = abs(self.box.bottom - terrain.rects[colliding_i].top)
			topDiff = abs(self.box.top - terrain.rects[colliding_i].bottom)

			if botDiff < topDiff:
				self.box.bottom = terrain.rects[colliding_i].top
				self.grounded = True
			else:
				self.box.top = terrain.rects[colliding_i].bottom
		else:
			self.yspeed += self.gravity
			self.grounded = False

	def movement(self):
		self.box.x += self.xspeed
		if self.hCollision():
			pass

		self.box.y += self.yspeed
		self.vCollision()


class Terrain:
	def __init__(self):
		self.rects = []

		for row_i, row in enumerate(map.map_layout):
			for col_i, col in enumerate(row):
				if col == "o":
					self.rects.append(pygame.Rect(col_i * map.TILESIZE - map.TILESIZE, row_i * map.TILESIZE - map.TILESIZE, map.TILESIZE, map.TILESIZE))

	def drawLevel(self):
		for i, rect in enumerate(self.rects):
			pygame.draw.rect(game.screen, "red", self.rects[i])

if __name__ == "__main__":
	game = Game()
	player = Player()
	terrain = Terrain()

	game.run()