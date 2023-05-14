import pygame, math
from math import atan2, degrees, pi
from os import walk
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from state import State
from entity import Tile, Entity
from player import Player
from enemies import Guard
from weapons import BeamParticle, BeamBlast, Gun

class Zone(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game

		self.gun_sprite = pygame.sprite.Group()
		self.beam_particle =  pygame.sprite.Group()

		# sprite groups
		self.rendered_sprites = Camera(self.game, self)
		self.updated_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.gun_sprites = pygame.sprite.Group()

		self.create_map()

	def create_map(self):
		tmx_data = load_pygame(f'../zones/{self.game.current_zone}.tmx')

		# # add backgrounds
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[1]], (0,0), pygame.image.load('../assets/bg.png').convert_alpha())
		# Object(self.game, self, [self.rendered_sprites, Z_LAYERS[2]], (0,TILESIZE), pygame.image.load('../zones/0.png').convert_alpha())

		# add the player
		for obj in tmx_data.get_layer_by_name('entities'):
			if obj.name == 'player': self.player = Player(self.game, self, obj.name, [self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['player'])
			if obj.name == 'sg_guard': Guard(self.game, self, obj.name, [self.enemy_sprites, self.updated_sprites, self.rendered_sprites], (obj.x, obj.y), LAYERS['NPCs'])
			self.target = self.player
			
		self.create_guns()

		for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
			Tile(self.game, self, [self.block_sprites, self.updated_sprites, self.rendered_sprites], (x * TILESIZE, y * TILESIZE), surf)
			
	def create_guns(self):
		for sprite in self.rendered_sprites:
			if hasattr(sprite, 'gun'):
				if sprite == self.player:
					self.gun_sprite = Gun(self.game, self, sprite.gun, sprite, [self.gun_sprites, self.updated_sprites, self.rendered_sprites], sprite.hitbox.center, LAYERS['weapons'])
				else:
					Gun(self.game, self, sprite.gun, sprite, [self.gun_sprites, self.updated_sprites, self.rendered_sprites], sprite.hitbox.center, LAYERS['weapons'])

	def beam(self):
		angle = math.atan2(pygame.mouse.get_pos()[1]-self.gun_sprite.rect.centery + self.rendered_sprites.offset[1], pygame.mouse.get_pos()[0]-self.gun_sprite.rect.centerx + self.rendered_sprites.offset[0])
		x = math.hypot(WIDTH, HEIGHT) * math.cos(angle) + self.gun_sprite.rect.centerx
		y = math.hypot(WIDTH, HEIGHT) * math.sin(angle) + self.gun_sprite.rect.centery
		distance = ((x, y) - pygame.math.Vector2(self.gun_sprite.rect.center)).magnitude()
		point_list = self.get_equidistant_points(self.gun_sprite.rect.center, (x, y), int(distance/6))
		for num, point in enumerate(point_list):
			if num > 4: BeamParticle(self.game, self, 'railgun', [self.updated_sprites, self.rendered_sprites], point, LAYERS['particles'])
			for sprite in self.block_sprites:
				if sprite.rect.collidepoint(point):
					BeamBlast(self.game, self, 'beam_blast', [self.updated_sprites, self.rendered_sprites], point, LAYERS['explosions'])
					return True
					
		return(point_list)

	def lerp(self, v0, v1, t):
		return v0 + t * (v1 - v0)

	def get_equidistant_points(self, point_1, point_2, num_of_points):
		return [(self.lerp(point_1[0], point_2[0], 1./num_of_points * i), self.lerp(point_1[1], point_2[1], 1./num_of_points * i)) for i in range(num_of_points + 1)]

	def get_distance(self, point_1, point_2):
		distance = (pygame.math.Vector2(point_2) - pygame.math.Vector2(point_1))
		return distance

	def update(self, dt):
		
		if ACTIONS['return']: 
			self.exit_state()
			self.game.reset_keys()
		self.updated_sprites.update(dt)

	def render(self, screen):
		screen.fill(LIGHT_GREY)
		self.rendered_sprites.offset_draw(self.target)
		self.game.render_text(self.player.on_ground, WHITE, self.game.small_font, RES/2)

		# for point in self.get_equidistant_points(self.player.rect.center, self.guard.rect.center, int(self.get_distance(self.player.rect.center, self.guard.rect.center).magnitude())):
		# 	pygame.draw.circle(screen, BLUE, point, 10)

