import pygame
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from state import State
from entity import Tile, Entity
from player import Player
from enemies import Guard
from weapons import Gun

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		self.melee_sprite = pygame.sprite.GroupSingle()

		# sprite groups
		self.rendered_sprites = pygame.sprite.Group()
		self.updated_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()

		self.player = Player(self.game, self, [self.updated_sprites, self.rendered_sprites], (40, 160))
		self.guard = Guard(self.game, self, [self.updated_sprites, self.rendered_sprites], (300, 200))

		self.create_melee()
		self.create_map()

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		# # add backgrounds
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[2]], (0,TILESIZE), pygame.image.load('../zones/0.png').convert_alpha())

		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Tile(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)
			

	def create_melee(self):
		self.melee_sprite = Gun(self.game, self, [self.updated_sprites, self.rendered_sprites], self.player.hitbox.center)

	def update(self, dt):
		if ACTIONS['return']: self.exit_state()
		self.game.reset_keys()
		self.updated_sprites.update(dt)

	
	def render(self, screen):
		screen.fill(LIGHT_GREY)
		pygame.draw.line(screen, PINK, self.player.rect.center, self.guard.rect.center)
		self.game.render_text(self.player.acc, WHITE, self.game.small_font, RES/2)
		self.rendered_sprites.draw(screen)


