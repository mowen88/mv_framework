import pygame
from settings import *
from entity import Entity

class Player(Entity):
	def __init__(self, game, zone, groups, pos, z):
		super().__init__(game, zone, groups, pos, z)

		self.game = game

		self.import_images()
		self.state = 'idle'
		self.frame_index = 0

		self.image = self.animations[self.state][self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		self.gravity = 0.3
		self.fric = -0.2
		self.acc = pygame.math.Vector2(0, self.gravity)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.vel = pygame.math.Vector2()

		self.jump_speed = 6

		self.on_ground = False
		self.on_ceiling = False

		#weapons
		self.weapon_index = 0
		self.weapon = None

		self.hitbox = self.rect.copy().inflate(-12,-6)

	def import_images(self):
		char_path = f'../assets/player/'
		self.animations = {'idle':[], 'run':[]}

		for animation in self.animations.keys():
			full_path = char_path + animation
			self.animations[animation] = self.game.get_folder_images(full_path)

	def input(self):
		keys = pygame.key.get_pressed()

		if ACTIONS['up']:
			self.jump(self.jump_speed)

		if ACTIONS['left_click']:
			self.zone.beam()

		if keys[pygame.K_RIGHT]:
			self.acc.x += 0.6
		elif keys[pygame.K_LEFT]:
			self.acc.x -= 0.6

		self.game.reset_keys()


		# if self.cyote_timer < self.cyote_timer_thresh:
		# 	self.vel.y = -height
		# 	self.jump_counter = 1
		# elif self.jump_counter == 1:
		# 	self.vel.y = -height
		# 	self.jump_counter = 0

	def physics(self, dt):
		
		# x direction
		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.acc.x) * dt
		#self.vel.x = max(-self.max_speed, min(self.vel.x, self.max_speed))
		self.hitbox.centerx = round(self.pos.x)
		self.collisions('x') 
		self.rect.centerx = self.hitbox.centerx

		if abs(self.vel.x) < 0.1: self.vel.x = 0

		# y direction
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.vel.y < 0: self.vel.y += (self.acc.y * 2) * dt
		else:self.vel.y += self.acc.y * dt

		self.pos.y += self.vel.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y') 
		self.rect.centery = self.hitbox.centery

		if self.vel.y >= 8: self.vel.y = 8
		if abs(self.vel.y) >= 0.5: self.on_ground = False
		
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.vel.y < 0:
			self.gravity += 1


	def update(self, dt):
		self.acc.x = 0
		self.input()
		self.physics(dt)
		self.set_state()
		self.animate('loop', dt)



		


		
		