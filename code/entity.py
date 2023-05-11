import pygame
from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, game, zone, groups, pos, surf):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(center = pos)