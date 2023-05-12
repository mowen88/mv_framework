import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos):
		super().__init__(groups)

		self.zone = zone

		self.image = pygame.Surface((40,40))
		self.rect = self.image.get_rect(center = pos)

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
						self.acc.y = 0
			
					elif self.vel.y < 0:
						self.hitbox.top = sprite.rect.bottom
						self.acc.y = 0

					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery
					



	def animate(self, animation_type, dt):

		self.frame_index += 0.15 * dt

		if self.frame_index >= len(self.animations[self.state]):
			if animation_type == 'loop': self.frame_index = 0
			elif animation_type == 'end': self.frame_index = len(self.animations[self.state]) -1
			else: self.kill()
		
		if pygame.mouse.get_pos() > self.rect.center: self.image = self.animations[self.state][int(self.frame_index)]
		else: self.image = pygame.transform.flip(self.animations[self.state][int(self.frame_index)], True, False)

	def change_state(self, new_state, new_animation_type):
		if self.state != new_state:
			self.frame_index = 0
			self.state = new_state
			self.animation_type = new_animation_type

	def set_state(self):
		if self.vel.x != 0: self.change_state('run', 'loop')
		else: self.change_state('idle', 'loop')