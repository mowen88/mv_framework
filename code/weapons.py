import pygame
from math import atan2, degrees, pi
from settings import *

class Gun(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos):
		super().__init__(groups)

		self.zone = zone
		self.gun_type = 'purple'
		self.original_image = pygame.image.load(f'../assets/weapons/{self.gun_type}.png').convert_alpha()
		self.image = self.original_image
		self.flipped_image = pygame.transform.flip(self.original_image, True, False)
		self.rect = self.image.get_rect(center = pos)
		self.angle = 0

	def get_angle(self, target):
		radians = atan2(self.zone.player.hitbox.center[0] - target[0], self.zone.player.hitbox.center[1] - target[1])
		radians %= 2 * pi
		self.angle = int(degrees(radians))

	def rotate(self):

		if self.angle >= 180: self.image = pygame.transform.rotate(self.flipped_image, self.angle)
		else: self.image = pygame.transform.rotate(self.original_image, self.angle)

		#self.angle += 5
		self.angle = self.angle % 360
		self.rect = self.image.get_rect(center = self.rect.center)

	def update(self, dt):
		self.get_angle(pygame.mouse.get_pos())
		self.rotate()
		self.rect.center = self.zone.player.hitbox.center


