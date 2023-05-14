import pygame
from settings import *
from entity import Entity

class Player(Entity):
	def __init__(self, game, zone, char, groups, pos, z):
		super().__init__(game, zone, char, groups, pos, z)

		self.game = game
		self.char = char

		self.data = DATA['abilities']

		# player animation
		self.import_images(self.animations)

		# jumping
		self.jump_speed = 7
		self.jump_counter = 0
		self.cyote_timer = 0
		self.cyote_timer_threshold = 10

		# player collide type
		self.on_ground = False
		self.on_ceiling = False

		# weapons
		self.gun_index = 0
		self.gun = list(DATA['guns'].keys())[self.gun_index]

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

	def jump(self, height):
		if self.cyote_timer < self.cyote_timer_threshold:
			self.vel.y = -height
			self.jump_counter = 1
		elif self.jump_counter == 1 and self.data['double_jump']:
			self.vel.y = -height
			self.jump_counter = 0
	
	def handle_jumping(self, dt):
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.vel.y < 0:
			self.gravity += self.gravity

		if not self.on_ground: self.cyote_timer += 1 * dt
		else: self.cyote_timer = 0

		# if falling, this gives the player one jump if they have double jump
		if self.jump_counter == 0 and self.data['double_jump'] and self.cyote_timer < self.cyote_timer_threshold:
			self.jump_counter = 1

	def update(self, dt):
		self.acc.x = 0
		self.input()
		self.physics_x(dt)
		self.physics_y(dt)
		self.handle_jumping(dt)
		self.set_state()
		self.animate(dt)



		


		
		