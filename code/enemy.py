from turtle import position
import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_type, position, groups, obstacle_sprites, damage_player, trigger_end_particles, add_exp):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_type)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_type
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.enemy_cooldown = 400
        self.damage_player = damage_player
        self.trigger_end_particles = trigger_end_particles
        self.add_exp = add_exp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'02 - setup/02 - setup/graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_info(self, player):
        # return a distance and a direction, ie a vector
        enemy_vect = pygame.math.Vector2(self.rect.center)
        player_vect = pygame.math.Vector2(player.rect.center)
        # vector is converted to distance
        distance = (player_vect - enemy_vect).magnitude()
        # we have to normalise the vector to use it, otherwise the enemy will go past the point where the player is.
        # vector is converted to direction
        if distance > 0:
            direction = (player_vect - enemy_vect).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_info(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_info(player)[1]
        else:
            # enemies stop moving when we move further away
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed  # we get this from entity
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        # we move the hitbox not the rectangle
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker when they're hit
        if not self.vulnerable:
            # flicker, set alpha to a particular bvalue
            # toggle between 0 and 255
            alpha = self.flicker()
            self.image.set_alpha(alpha)

        else:
            # full opaqueness
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.enemy_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_info(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_life(self):
        if self.health <= 0:
            self.kill()
            self.trigger_end_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)

    def staggering(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.staggering()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_life()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
