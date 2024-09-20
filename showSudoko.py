import pygame
import configuration as confi
import os
import numpy as np

import imageProcessing as Ip

pygame.init()
font = pygame.font.SysFont(None, 55)

def draw_rounded_rect(surface, color, rect, corner_radius):
    # Create a surface with transparency (using SRCALPHA)
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw a filled rounded rectangle on this surface
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)

    # Blit the surface onto the main screen at the specified location
    surface.blit(rounded_rect_surface, rect.topleft)

upload_button = pygame.Rect(confi.ssbutton_x, confi.ssbutton_y, confi.ssbutton_width, confi.ssbutton_height)
def handle_landingScreen_events(events, screen):
    pass

def draw_showSudoku_Screen(screen):
    output_image_rgb = Ip.imageProcessing(confi.file_path)
    output_image_rgb = np.array(output_image_rgb)
    output_image_rgb = np.transpose(output_image_rgb, (1, 0, 2))  # Swap axes if needed
    surface = pygame.surfarray.make_surface(output_image_rgb)

    screen.blit(surface, (0, 0))

