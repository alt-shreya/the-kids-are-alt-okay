import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.image = pygame.image.load(
            '02 - setup/2 - setup/code/graphics/test/rock.png').convert_alpha()
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface

        if sprite_type == 'object':
            # do an offset
            self.rect = self.image.get_rect(
                topleft=(position[0], position[1] - TILESIZE))
        else:
            # do what we already done
            self.rect = self.image.get_rect(topleft=position)
        # shrink by 5 pixels on each side
        self.hitbox = self.rect.inflate(0, y_offset)
