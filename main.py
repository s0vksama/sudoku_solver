# importing library
import os
import pygame
import tkinter as tk
from tkinter import filedialog

# importing files
import landingPage as lp
import configuration as confi

# Initialize pygame
pygame.init()

# Fonts
font = pygame.font.SysFont(None, 36)

# Create a tkinter root window and hide it
root = tk.Tk()
root.withdraw()

window = pygame.display.set_mode((confi.screen_width, confi.screen_height))
pygame.display.set_caption('Image Uploader')


# Main loop
running = True
uploaded_image = None

# deciding which frame to render
landing_status = True
Sudoku_viewer = False
Animation = False
Result = False

while running:
    window.fill(confi.WHITE)

    if landing_status == True:
        lp.landing_page_func(window)

# Quit pygame
pygame.quit()
