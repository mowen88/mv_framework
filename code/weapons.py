import pygame
from math import atan2, degrees, pi
from settings import *
from entity import Entity


class BeamParticle(Entity):
	def __init__(self, game, zone, groups, pos, z):
		super().__init__(game, zone, groups, pos, z)

		self.game = game
		self.zone = zone
		self.z = z
		self.frame_index = 0
		self.frames = self.game.get_folder_images('../assets/weapons/beam_particle/')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.alpha = 255
		self.angle = self.zone.gun_sprite.angle

	def animate(self, dt):
		self.frame_index += 0.18 * dt
		if self.frame_index >= len(self.frames)-1: self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def change_alpha(self, increment):
		self.alpha -= increment
		if self.alpha < 0: self.kill()
		self.image.set_alpha(self.alpha)

	def update(self, dt):
		self.animate(dt)
		self.change_alpha(2)
		self.image = pygame.transform.rotate(self.image, self.angle)


class BeamBlast(BeamParticle):
	def __init__(self, game, zone, groups, pos, z):
		super().__init__(game, zone, groups, pos, z)

		self.image = pygame.image.load('../assets/weapons/beam_blast.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self, dt):
		self.change_alpha(1)

class Gun(Entity):
	def __init__(self, game, zone, groups, pos, z):
		super().__init__( game, zone, groups, pos, z)

		self.zone = zone
		self.z = z
		self.gun_type = 'green'
		self.original_image = pygame.image.load(f'../assets/weapons/{self.gun_type}.png').convert_alpha()
		self.image = self.original_image
		self.flipped_image = pygame.transform.flip(self.original_image, True, False)
		self.rect = self.image.get_rect(center = pos)
		self.angle = 0

	def get_angle(self, point_1, point_2):
		dx = point_1[0] - point_2[0] - self.zone.rendered_sprites.offset[0]
		dy = point_1[1] - point_2[1] - self.zone.rendered_sprites.offset[1]
		radians = atan2(dx, dy)
		radians %= 2 * pi
		self.angle = int(degrees(radians))

	def rotate(self):
		if self.angle % 3 == 0:

			if self.angle >= 180: self.image = pygame.transform.rotate(self.flipped_image, self.angle)
			else: self.image = pygame.transform.rotate(self.original_image, self.angle)

		#self.angle += 5
		self.angle = self.angle % 360
		self.rect = self.image.get_rect(center = self.rect.center)

	def update(self, dt):
		self.get_angle(self.zone.player.hitbox.center, pygame.mouse.get_pos())
		self.rotate()
		self.rect.center = (self.zone.player.hitbox.centerx, self.zone.player.hitbox.centery - 5)


