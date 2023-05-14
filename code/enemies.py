import pygame
from settings import *
from entity import Entity

class Enemy(Entity):
	def __init__(self, game, zone, char, groups, pos, z):
		super().__init__(game, zone, char, groups, pos)

		self.import_images(self.animations)
		self.frame_index = 0
		self.image = self.animations[self.state][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.2)

		# physics
		self.gravity = 0.3
		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, self.gravity)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()

		# weapons
		self.gun = DATA['enemy_guns'][self.char]
		print(self.gun)

	def update(self, dt):
		self.physics_x(dt)
		self.physics_y(dt)


