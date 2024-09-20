import pygame
import configuration as confi
import os
import numpy as np

import imageProcessing as Ip

pygame.init()
font = pygame.font.SysFont(None, 40)

def draw_rounded_rect(surface, color, rect, corner_radius):
    # Create a surface with transparency (using SRCALPHA)
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw a filled rounded rectangle on this surface
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)

    # Blit the surface onto the main screen at the specified location
    surface.blit(rounded_rect_surface, rect.topleft)

upload_button = pygame.Rect(confi.ssbutton_x, confi.ssbutton_y, confi.ssbutton_width, confi.ssbutton_height)

def handle_landingScreen_events(events, screen):
    mouse_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if upload_button.collidepoint(mouse_pos):  # Check if the button was clicked
               return "show sudoku2"
    # screen.blit(button_text, (confi.lsbutton_x + 10, confi.lsbutton_y + 10))
    return "show sudoku"

def draw_showSudoku_Screen(screen):
    screen.fill(confi.background)
    if len(confi.sudoku_board) == 1:
        output_image_rgb = Ip.imageProcessing(confi.file_path)
        output_image_rgb = np.array(output_image_rgb)
        output_image_rgb = np.transpose(output_image_rgb, (1, 0, 2))  # Swap axes if needed
        confi.output_image_rgb = output_image_rgb

    surface = pygame.surfarray.make_surface(confi.output_image_rgb)
    surface = pygame.transform.scale(surface, (500, 500))
    screen.blit(surface, (50, 50))

    button_text = font.render("Next", True, confi.font_color)
    mouse_pos = pygame.mouse.get_pos()
    if upload_button.collidepoint(mouse_pos):
        draw_rounded_rect(screen, confi.button_hover_color, upload_button, 15)  # Radius 15 for rounded corners
    else:
        draw_rounded_rect(screen, confi.button_color, upload_button, 15)
    screen.blit(button_text, (confi.ssbutton_x+20, confi.ssbutton_y+10))
