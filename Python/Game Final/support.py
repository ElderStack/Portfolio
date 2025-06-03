from csv import reader
from os import walk
import pygame

def load_spritesheet_image(sheet, width, height, color, scale = 1):
    spritesheet = pygame.image.load(sheet).convert_alpha()
    def load_image_from_spritesheet(frame,row):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(spritesheet, (0,0), (frame * width, row * width, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
    
        return image
    
    spritesheet_images = []
    for i in range(spritesheet.get_height() // height):
        for j in range(spritesheet.get_width() // width):
            spritesheet_images.append(load_image_from_spritesheet(j, i))
    
    return spritesheet_images



def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter= ",")
        for row in layout:
            terrain_map.append(list(row))
            
    return terrain_map

def import_folder(path):
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            #print(full_path)
            #print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    #print(surface_list)
    return surface_list