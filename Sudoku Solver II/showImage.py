import pygame
pygame.init()

import numpy as np
import working as wk
import configuration as confi
import ImageProcessing as iP

font = pygame.font.Font(None, 36) #using default font
fontBold = pygame.font.Font(None, 100)
uploadfont = pygame.font.Font(None, 60)

NEXT_button_rect = pygame.Rect(confi.Sibotton_x, confi.Sibotton_y, confi.Sibotton_width, confi.Sibotton_hight)

def draw_rounded_rect(surface, color, color2, rect, corner_radius):
    # Create a surface with transparency (using SRCALPHA)
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw a filled rounded rectangle on this surface
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)

    # Blit the surface onto the main screen at the specified location
    surface.blit(rounded_rect_surface, rect.topleft)

    # add text
    text_UPLOAD = uploadfont.render("NEXT", True, color2)
    UPLOAD_rect = text_UPLOAD.get_rect(center=(confi.Sibotton_x+confi.Sibotton_width//2,
                                                 confi.Sibotton_y+confi.Sibotton_hight//2))
    surface.blit(text_UPLOAD, UPLOAD_rect)

def handle_Screen_events(events, screen):
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if NEXT_button_rect.collidepoint(mouse_pos):  # Check if the button was clicked
                return "show sudoku"

    return "show image"


def draw_Screen(screen, events):
    if len(confi.processed_image) ==0 :
        my_image = iP.image_processing(confi.file_path)
        my_image = wk.image_processing(my_image, screen, events)

        output_image_rgb = np.array(my_image)
        output_image_rgb = np.transpose(output_image_rgb, (1, 0, 2))  # Swap axes if needed

        confi.processed_image = output_image_rgb

    screen.fill(confi.lsbackground_col)
    surface = pygame.surfarray.make_surface(confi.processed_image)
    surface = pygame.transform.scale(surface, (500, 500))

    mouse_pos = pygame.mouse.get_pos()

    if NEXT_button_rect.collidepoint(mouse_pos):
        draw_rounded_rect(screen, confi.ls_botton_hovor_font_col, confi.lsbotton_col, NEXT_button_rect, 20)  # Radius 15 for rounded corners
    else:
        draw_rounded_rect(screen, confi.lsbotton_col, confi.ls_botton_hovor_font_col, NEXT_button_rect, 20)

    screen.blit(surface, (50, 50))

