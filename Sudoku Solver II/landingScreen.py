import pygame
pygame.init()

import tkinter as tk
from tkinter import filedialog
import configuration as confi
import os

font = pygame.font.Font(None, 36) #using default font
fontBold = pygame.font.Font(None, 100)
uploadfont = pygame.font.Font(None, 60)

# Create a tkinter root window and hide it
root = tk.Tk()
root.withdraw()

# Define the button's rectangle (position and size)
upload_button_rect = pygame.Rect(confi.lsbotton_x, confi.lsbotton_y, confi.lsbotton_width, confi.lsbotton_hight)

# Function to load an image from a file path
def load_image(file_path):
    if os.path.exists(file_path):
        try:
            image = pygame.image.load(file_path)
            return pygame.transform.scale(image, (confi.screen_width, confi.screen_height))
        except pygame.error as e:
            print(f"Cannot load image: {e}")
    else:
        print("File does not exist.")
    return None

def draw_rounded_rect(surface, color, color2, rect, corner_radius):
    # Create a surface with transparency (using SRCALPHA)
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw a filled rounded rectangle on this surface
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)

    # Blit the surface onto the main screen at the specified location
    surface.blit(rounded_rect_surface, rect.topleft)

    # add text
    text_UPLOAD = uploadfont.render("UPLOAD", True, color2)
    UPLOAD_rect = text_UPLOAD.get_rect(center=(confi.lsbotton_x+confi.lsbotton_width//2,
                                                 confi.lsbotton_y+confi.lsbotton_hight//2))
    surface.blit(text_UPLOAD, UPLOAD_rect)

def handle_Screen_events(events, screen):
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if upload_button_rect.collidepoint(mouse_pos):  # Check if the button was clicked
                file_path = filedialog.askopenfilename(
                    title="Select an image",
                    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
                )
                if file_path:
                    confi.uploaded_image = load_image(file_path)
                    confi.file_path = file_path
                return "show image"

    return "landing screen"

def draw_sudoku_text(screen):
    screen.fill(confi.lsbackground_col)

    # Draw rectangle at the center of the screen
    rect_width, rect_height = 200, 200
    rect_x = confi.screen_width / 2 - rect_width / 2
    rect_y = confi.screen_height / 4 - rect_height / 2
    pygame.draw.rect(screen, confi.lsSudoku_board_col, pygame.Rect(rect_x, rect_y+25, rect_width, rect_height-50))

    # Render text pairs
    text_SU = font.render("S  U", True, confi.lsbackground_col)  # First pair "S U"
    text_DO = font.render("D  O", True, confi.lsbackground_col)  # Second pair "D O"
    text_KU = font.render("K  U", True, confi.lsbackground_col)  # Third pair "K U"

    # Calculate vertical and horizontal positioning for each pair
    text_spacing = 30  # Vertical spacing between each pair of letters
    center_x = confi.screen_width / 2  # Horizontal centering

    # Position each pair centered horizontally and vertically aligned
    SU_rect = text_SU.get_rect(center=(center_x-35, rect_y + rect_height / 2 - text_spacing))
    DO_rect = text_DO.get_rect(center=(center_x, rect_y + rect_height / 2))
    KU_rect = text_KU.get_rect(center=(center_x+35, rect_y + rect_height / 2 + text_spacing))

    # vertical lines drawing
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-70, rect_y, 2, 200))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-35, rect_y, 2, 200))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x, rect_y, 2, 200))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x+35, rect_y, 2, 200))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x+70, rect_y, 2, 200))

    # horizontal lines drawing
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 1*text_spacing -5, 500, 2))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 2*text_spacing -5, 500, 2))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 3*text_spacing -5, 500, 2))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 3*text_spacing -5, 500, 2))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 4*text_spacing -5, 500, 2))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 5*text_spacing -5, 500, 2))
    pygame.draw.rect(screen, confi.lsbackground_col, pygame.Rect(center_x-100, rect_y + 6*text_spacing -5, 500, 2))

    text_SOLVER = fontBold.render("SOLVER", True, confi.lsSolver_col)
    SOLVER_rect = text_SU.get_rect(center=(187, 300))
    screen.blit(text_SOLVER, SOLVER_rect)
    # Blit the text onto the screen
    screen.blit(text_SU, SU_rect)
    screen.blit(text_DO, DO_rect)
    screen.blit(text_KU, KU_rect)

def draw_Screen(screen):
    draw_sudoku_text(screen)
    mouse_pos = pygame.mouse.get_pos()

    if upload_button_rect.collidepoint(mouse_pos):
        draw_rounded_rect(screen, confi.ls_botton_hovor_font_col, confi.lsbotton_col, upload_button_rect, 20)  # Radius 15 for rounded corners
    else:
        draw_rounded_rect(screen, confi.lsbotton_col, confi.ls_botton_hovor_font_col,upload_button_rect, 20)



