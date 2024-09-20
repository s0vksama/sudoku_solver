
import pygame
pygame.init()

import sys
import configuration as confi

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
            pass

        elif current_screen == "show sudoku":
            pass

        elif current_screen == "animation":
            pass

        elif current_screen == "go back":
            pass


if __name__ == "__main__":
    main()

