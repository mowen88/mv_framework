import pygame
from math import atan2, degrees, pi
from os import walk
from settings import *
from state import State
from player import Player
from weapons import Gun

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		self.melee_sprite = pygame.sprite.GroupSingle()

		# sprite groups
		self.rendered_sprites = pygame.sprite.Group()
		self.updated_sprites = pygame.sprite.Group()

		self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (40, 100), pygame.Surface((40, 40)))

		self.create_melee()

	def create_melee(self):
		self.melee_sprite = Gun(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center)

	def update(self, dt):
		if ACTIONS['return']: self.exit_state()
		self.game.reset_keys()
		self.updated_sprites.update(dt)
		
	
	def render(self, screen):
		screen.fill(LIGHT_GREY)
		self.game.render_text(round(self.melee_sprite.angle, 2), WHITE, self.game.small_font, RES/2)
		self.rendered_sprites.draw(screen)


