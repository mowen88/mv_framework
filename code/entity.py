import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

class Entity(Tile):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(game, zone, groups, pos, surf)

		self.image = surf
		self.rect = self.image.get_rect(center = pos)

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