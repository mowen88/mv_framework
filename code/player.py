import pygame
from settings import *
from entity import Entity

class Player(Entity):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.gravity = 0.2
		self.fric = -0.1
		self.acc = pygame.math.Vector2(0,0)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()

		#weapons
		self.weapon_index = 0
		self.weapon = None

		self.hitbox = self.rect.copy().inflate(0,0)

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.acc.x += 0.5
		if keys[pygame.K_LEFT]:
			self.acc.x -= 0.5

	def switch_weapon(self):
		if ACTIONS['scroll_up']:
			pass

	def physics(self, dt):
		
		# x direction
		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x
		self.pos.x += self.vel.x + (0.5 * self.acc.x) * dt
		#self.vel.x = max(-self.max_speed, min(self.vel.x, self.max_speed))
		self.hitbox.centerx = round(self.pos.x)
		#self.collisions('x')
		self.rect.centerx = self.hitbox.centerx

	def update(self, dt):
		self.acc.x = 0
		self.input()
		self.physics(dt)

		


		
		