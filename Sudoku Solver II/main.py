import pygame
pygame.init()

import sys
import numpy as np

import configuration as confi
import landingScreen as Ls
import showImage as Si
import showSudoku as Ss
import animation as ani
from HOG_and_SVM_confidence import SVM_classifier, SVM_single
import Get_digit_confi as Gd
import sudoku_extractor_new as Se
import cv2

screen = pygame.display.set_mode((confi.screen_width, confi.screen_height))
pygame.display.set_caption("sudoku solver")

def main():
    current_screen = "landing screen"

    while  True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_screen == "landing screen":
            current_screen = Ls.handle_Screen_events(events, screen)
            Ls.draw_Screen(screen)

        elif current_screen == "show image":
            current_screen = Si.handle_Screen_events(events, screen)
            Si.draw_Screen(screen, events)

        elif current_screen == "show sudoku":
            current_screen = Ss.handle_Screen_events(events, screen)
            Ss.draw_Screen(screen)

        elif current_screen == "animation":
            current_screen = ani.handle_landingScreen_events(events, screen)
            ani.draw_showSudoku_Screen(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
