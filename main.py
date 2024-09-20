
import pygame
pygame.init()

import sys
import configuration as confi
import landingScreen as Ls

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
            pass

        elif current_screen == "animation":
            pass

        elif current_screen == "go back":
            pass

        pygame.display.flip()


if __name__ == "__main__":
    main()

