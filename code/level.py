import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()  # magic and weapons in this group
        self.attackable_sprites = pygame.sprite.Group()  # enemies in this group
        # we can then check for collisions between these two spriet groups to determine how much damage is to be dealt

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        # particles
        self.animation_player = AnimationPlayer()

        # magic
        self.magic_player = MagicPlayer(self.animation_player)

# we use this to setup our world

    def create_map(self):
        # import_csv_layout is a custom function
        layouts = {'boundary': import_csv_layout(
            '05 - level graphics/5 - level graphics/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('05 - level graphics/5 - level graphics/map/map_Grass.csv'),
            'objects': import_csv_layout('05 - level graphics/5 - level graphics/map/map_Objects.csv'),
            'entities': import_csv_layout('10 - Enemies/10 - Enemies/map/map_Entities.csv')}

        graphics = {'grass': import_folder(
            '05 - level graphics/5 - level graphics/graphics/grass'),
            'objects': import_folder('05 - level graphics/5 - level graphics/graphics/objects')
        }

        for style, layout in layouts.items():  # style is boundary, layout is the map
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites, self.attackable_sprites],
                                 'grass', random_grass_image)
                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':  # in tiled, the tileset in indexed in such a way
                                # we pass the function, we don't call the function
                                self.player = Player((x, y), [
                                                     self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.despawn_weapon,
                                                     self.create_magic)
                            else:
                                if col == '390':
                                    monster_type = 'bamboo'
                                elif col == '391':
                                    monster_type = 'spirit'
                                elif col == '392':
                                    monster_type = 'raccoon'
                                else:
                                    monster_type = 'squid'
                                Enemy(monster_type, (x, y),
                                      [self.visible_sprites,
                                          self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player, self.trigger_end_particles, self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [
                                   self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [
                self.visible_sprites, self.attack_sprites])

        print(style, strength, cost)

    def despawn_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        # cycle through attack sprites and check for collisions with attackable sprites
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # sprite, group and DOKILL were the parameters
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            # add abit more logic to spawn particles
                            position = target_sprite.rect.center
                            # just to make the animation effect a little higher
                            offset = pygame.math.Vector2(0, 75)
                            # to generate multiple leaves instead of a single leaf
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    position - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        # function to damage the player
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn some particles
            self.animation_player.create_attack_particles(
                attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_end_particles(self, position, particle_type):
        self.animation_player.create_attack_particles(
            particle_type, position, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, font_size) -> None:
        font_size = EXPLAIN_FONT_SIZE
        self.efont = pygame.font.Font(EXPLAIN_FONT, font_size)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.back = pygame.Surface((self.width, self.height))
        self.back.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(
            center=(self.width/2, self.height/2))
        self.back.blit(self.text, self.text_rect)

    def is_pressed(self, position, pressed):
        if self.rect.collidepoint(position):
            if pressed[0]:
                return True
            return False
        return False


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # create the floor
        # change the path with something more suited for the internet
        self.floor_surf = pygame.image.load(
            '05 - level graphics/5 - level graphics/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        # draws all of our elements. we wnat to draw the floor, too. But we can't add it to the sprites
        # our floor ALWAYS has to be below. As it is a giant image, it would cover the entire field.
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
