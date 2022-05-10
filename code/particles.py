import pygame
from support import import_folder
from random import choice


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('12 - particles/12 - particles/graphics/particles/flame/frames'),
            'aura': import_folder('12 - particles/12 - particles/graphics/particles/aura'),
            'heal': import_folder('12 - particles/12 - particles/graphics/particles/heal/frames'),

            # attacks
            'claw': import_folder('12 - particles/12 - particles/graphics/particles/claw'),
            'slash': import_folder('12 - particles/12 - particles/graphics/particles/slash'),
            'sparkle': import_folder('12 - particles/12 - particles/graphics/particles/sparkle'),
            'leaf_attack': import_folder('12 - particles/12 - particles/graphics/particles/leaf_attack'),
            'thunder': import_folder('12 - particles/12 - particles/graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('12 - particles/12 - particles/graphics/particles/smoke_orange'),
            'raccoon': import_folder('12 - particles/12 - particles/graphics/particles/raccoon'),
            'spirit': import_folder('12 - particles/12 - particles/graphics/particles/nova'),
            'bamboo': import_folder('12 - particles/12 - particles/graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf1'),
                import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf2'),
                import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf3'),
                import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf4'),
                import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf5'),
                import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf6'),
                self.reflect_images(import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf1')),
                self.reflect_images(import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf2')),
                self.reflect_images(import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf3')),
                self.reflect_images(import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf4')),
                self.reflect_images(import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf5')),
                self.reflect_images(import_folder(
                    '12 - particles/12 - particles/graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        # once proper direction, once reflected to get a varaiblity
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, position, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(position, animation_frames, groups)

    def create_attack_particles(self, animation_type, position, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(position, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        # this gives the particle effect a sprite type and allows flame to interact with the enemies
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)
        super().__init__(groups)

    # we have a lot of particle and if pygame inputs everything when we destroy an enemy or a grass, the game will become very slow

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            # increasing frame index, then we pick from the list but if we go beyond then we destroy the sprite so as to only run the animation one time
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
