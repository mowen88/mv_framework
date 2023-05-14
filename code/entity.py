import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf, z = LAYERS['blocks']):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)	
		self.z = z				

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, zone, char, groups, pos, z = LAYERS['BG0']):
		super().__init__(groups)

		self.game = game
		self.zone = zone
		self.char = char
		self.z = z
		
		# animation
		self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
		self.animation_type = ''
		self.import_images(self.animations)
		self.state = 'idle'
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

		# jumping
		self.jump_speed = 7


	def import_images(self, animation_states):

		char_path = f'../assets/{self.char}/'

		for animation in animation_states.keys():
			full_path = char_path + animation
			animation_states[animation] = self.game.get_folder_images(full_path)


	def collisions(self, direction):

		for sprite in self.zone.block_sprites:
			if sprite.rect.colliderect(self.hitbox):

				if direction == 'x':
					if self.vel.x > 0:
						self.hitbox.right = sprite.rect.left

					elif self.vel.x < 0:
						self.hitbox.left = sprite.rect.right

					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

				if direction == 'y':
					if self.vel.y > 0:
						self.hitbox.bottom = sprite.rect.top
						self.on_ground = True
						self.vel.y = 0
			
					elif self.vel.y < 0:
						self.hitbox.top = sprite.rect.bottom
						self.on_ceiling = True
						self.vel.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

	def jump(self, height):
		self.vel.y = -height		

	def animate(self, dt):

		self.frame_index += 0.15 * dt

		if self.frame_index >= len(self.animations[self.state]):
			if self.animation_type == 'loop': self.frame_index = 0
			elif self.animation_type == 'end': self.frame_index = len(self.animations[self.state]) -1
			else: self.kill()
		
		if pygame.mouse.get_pos()[0] + self.zone.rendered_sprites.offset[0] > self.rect.centerx: self.image = self.animations[self.state][int(self.frame_index)]
		else: self.image = pygame.transform.flip(self.animations[self.state][int(self.frame_index)], True, False)

	def change_state(self, new_state, new_animation_type):
		if self.state != new_state:
			self.frame_index = 0
			self.state = new_state
			self.animation_type = new_animation_type

	def set_state(self):
		if not self.on_ground:
			if self.vel.y < 0: self.change_state('jump', 'end')
			else: self.change_state('fall', 'end')
		else:
			if self.vel.x != 0: self.change_state('run', 'loop')
			else: self.change_state('idle', 'loop')

			# jumping
		self.jump_speed = 7
	
	def physics_x(self, dt):
		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.acc.x) * dt
		#self.vel.x = max(-self.max_speed, min(self.vel.x, self.max_speed))
		self.hitbox.centerx = round(self.pos.x)
		self.collisions('x') 
		self.rect.centerx = self.hitbox.centerx

		if abs(self.vel.x) < 0.1: self.vel.x = 0

	def physics_y(self, dt):
		if not (pygame.key.get_pressed()[pygame.K_UP]) and self.vel.y < 0: self.vel.y += (self.acc.y * 2) * dt
		else:self.vel.y += self.acc.y * dt

		self.pos.y += self.vel.y * dt + (0.5 * self.acc.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.collisions('y') 
		self.rect.centery = self.hitbox.centery

		if self.vel.y >= 8: self.vel.y = 8
		if abs(self.vel.y) >= 0.5: self.on_ground = False