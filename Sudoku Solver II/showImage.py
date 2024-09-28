import pygame
pygame.init()

import numpy as np
import working as wk
import configuration as confi
import ImageProcessing as iP

def handle_Screen_events(events, screen):
    pass

def draw_Screen(screen):
    screen.fill(confi.lsbackground_col)

    my_image = iP.image_processing(confi.file_path)
    my_image = wk.image_processing(my_image, screen)

    output_image_rgb = np.array(my_image)
    output_image_rgb = np.transpose(output_image_rgb, (1, 0, 2))  # Swap axes if needed

    surface = pygame.surfarray.make_surface(output_image_rgb)
    surface = pygame.transform.scale(surface, (500, 500))
    screen.blit(surface, (50, 50))
