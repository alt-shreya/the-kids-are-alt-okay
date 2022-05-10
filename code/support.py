from csv import reader
from email.mime import image
from os import walk  # walk through the file system
import pygame


def import_csv_layout(path):
    # how to read a csv file.
    # python has a module to do that
    terrain_map = []  # this will be the list that contains the list
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')  # CSV object
        for row in layout:
            # now we can see the actual files: the lists
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


# import_folder('05 - level graphics/5 - level graphics/graphics/grass')
