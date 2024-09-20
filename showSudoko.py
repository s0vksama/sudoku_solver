import pygame
import configuration as confi
import os

pygame.init()
font = pygame.font.SysFont(None, 55)


def handle_landingScreen_events(events, screen):
    pass

def draw_showSudoku_Screen(screen):
    screen.blit(confi.uploaded_image, (0, 0))
