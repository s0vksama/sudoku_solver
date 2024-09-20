import pygame
import configuration as confi
import tkinter as tk
from tkinter import filedialog
import os

pygame.init()
font = pygame.font.SysFont(None, 55)

# Create a tkinter root window and hide it
root = tk.Tk()
root.withdraw()

# Define the button's rectangle (position and size)
upload_button = pygame.Rect(confi.lsbutton_x, confi.lsbutton_y, confi.lsbutton_width, confi.lsbutton_height)

def draw_rounded_rect(surface, color, rect, corner_radius):
    # Create a surface with transparency (using SRCALPHA)
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw a filled rounded rectangle on this surface
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)

    # Blit the surface onto the main screen at the specified location
    surface.blit(rounded_rect_surface, rect.topleft)

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

def draw_landingScreen(screen):
    screen.fill(confi.background)  # Set the background color
    text = font.render("Sudoku Solver", True, confi.font_color)  # Render the text
    screen.blit(text, (50, 50))  # Display the text at (50, 50)

    # Draw the button (as a filled rectangle)
    pygame.draw.rect(screen, confi.button_color, upload_button)  # Button color
    button_text = font.render("Upload Puzzle", True, confi.font_color)

    mouse_pos = pygame.mouse.get_pos()
    if upload_button.collidepoint(mouse_pos):
        draw_rounded_rect(screen, confi.button_hover_color, upload_button, 15)  # Radius 15 for rounded corners
    else:
        draw_rounded_rect(screen, confi.button_color, upload_button, 15)

    screen.blit(button_text, (confi.lsbutton_x + 10, confi.lsbutton_y + 10))  # Draw the button text

def handle_landingScreen_events(events, screen):
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if upload_button.collidepoint(mouse_pos):  # Check if the button was clicked
                print("show sudoku")  # Transition to the next screen
                file_path = filedialog.askopenfilename(
                    title="Select an image",
                    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
                )
                if file_path:
                    confi.uploaded_image = load_image(file_path)
                    confi.file_path = file_path

                return "show sudoku"


    return "landing screen"
