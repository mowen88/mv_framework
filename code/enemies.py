import pygame
from settings import *
from entity import Entity

class Guard(Entity):
	def __init__(self, game, zone, groups, pos):
		super().__init__(game, zone, groups, pos)

		self.image = pygame.Surface((30,40))
		self.image.fill(LIGHT_BLUE)
		self.rect = self.image.get_rect(center = pos)