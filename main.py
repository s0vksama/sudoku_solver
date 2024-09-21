import pygame
pygame.init()

import sys
import configuration as confi
import landingScreen as Ls
import showSudoko as Ss
import animation as ani
import numpy as np
import showSudoko2 as Ss2

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
            current_screen = Ls.handle_landingScreen_events(events, screen)
            Ls.draw_landingScreen(screen)

        elif current_screen == "show sudoku":
            current_screen = Ss.handle_landingScreen_events(events, screen)
            Ss.draw_showSudoku_Screen(screen)

        elif current_screen == "show sudoku2":
            current_screen = Ss2.handle_landingScreen_events(events, screen)
            Ss2.draw_showSudoku_Screen(screen)

        elif current_screen == "animation":
            current_screen = ani.handle_landingScreen_events(events, screen)
            ani.draw_showSudoku_Screen(screen)

        elif current_screen == "go back":
            pass
        pygame.display.flip()

if __name__ == "__main__":
    main()

