import pygame
import configuration2 as config

pygame.init()

font = pygame.font.SysFont(None, 40)
thin_font = pygame.font.SysFont('roboto', 40, bold=False)
heading_font = pygame.font.Font(None, 48)
button_font = pygame.font.Font(None, 36)

button_rect = pygame.Rect(config.button_x, config.button_y, config.button_width, config.button_height)
stop_button_rect = pygame.Rect(config.stop_button_x + config.button_width + 50, config.stop_button_y, config.button_width, config.button_height)

selected_cell = None  # Keeps track of the selected cell for editing

def draw_rounded_rect(surface, color, rect, corner_radius):
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)
    surface.blit(rounded_rect_surface, rect.topleft)

def draw_board(screen, selected_cell=None):
    screen.fill(config.background)

    heading_surface = heading_font.render("Sudoku Solver", True, config.heading_color)
    heading_rect = heading_surface.get_rect(center=(config.screen_width / 2, config.t_padding / 2))
    screen.blit(heading_surface, heading_rect)

    h_start = config.t_padding
    v_start = config.l_padding
    for x in range(10):
        if x % 3 == 0:
            pygame.draw.line(screen, config.border_color, (v_start, config.t_padding), (v_start, config.t_padding + config.board_size), config.bold_line)
            pygame.draw.line(screen, config.border_color, (config.l_padding, h_start), (config.l_padding + config.board_size, h_start), config.bold_line)
            v_start += config.cell_size + config.bold_line
            h_start += config.cell_size + config.bold_line
        else:
            pygame.draw.line(screen, config.border_color, (v_start, config.t_padding), (v_start, config.t_padding + config.board_size), config.thin_line)
            pygame.draw.line(screen, config.border_color, (config.l_padding, h_start), (config.l_padding + config.board_size, h_start), config.thin_line)
            v_start += config.cell_size + config.thin_line
            h_start += config.cell_size + config.thin_line

    for row in range(9):
        for col in range(9):
            if config.sudoku_board[row][col] != 0:
                color = config.font_color
                value_surface = font.render(str(config.sudoku_board[row][col]), True, color)
                value_rect = value_surface.get_rect()
                cell_x = config.l_padding + col * (config.cell_size + config.thin_line) + (col // 3) * (config.bold_line - config.thin_line) + config.offset
                cell_y = config.t_padding + row * (config.cell_size + config.thin_line) + (row // 3) * (config.bold_line - config.thin_line) + config.offset
                value_rect.center = (cell_x + config.cell_size / 2, cell_y + config.cell_size / 2)
                screen.blit(value_surface, value_rect)

    if selected_cell:
        row, col = selected_cell
        cell_x = config.l_padding + col * (config.cell_size + config.thin_line) + (col // 3) * (config.bold_line - config.thin_line) + config.offset - 1.5
        cell_y = config.t_padding + row * (config.cell_size + config.thin_line) + (row // 3) * (config.bold_line - config.thin_line) + config.offset - 1.5
        pygame.draw.rect(screen, config.highlight_color, (cell_x, cell_y, config.cell_size + config.offset, config.cell_size + config.offset), 5)

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        draw_rounded_rect(screen, config.button_hover_color, button_rect, 15)
    else:
        draw_rounded_rect(screen, config.button_color, button_rect, 15)

    button_text_surface = button_font.render("Solve", True, config.botton_font_color)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    screen.blit(button_text_surface, button_text_rect)

    if stop_button_rect.collidepoint(mouse_pos):
        draw_rounded_rect(screen, config.button_hover_color, stop_button_rect, 15)
    else:
        draw_rounded_rect(screen, config.button_color, stop_button_rect, 15)

    stop_button_text_surface = button_font.render("Stop", True, config.botton_font_color)
    stop_button_text_rect = stop_button_text_surface.get_rect(center=stop_button_rect.center)
    screen.blit(stop_button_text_surface, stop_button_text_rect)

def handle_Screen_events(events, screen):
    global selected_cell
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos):
                return "animation"
            elif stop_button_rect.collidepoint(mouse_pos):
                return "stop"

            col = (mouse_pos[0] - config.l_padding) // (config.cell_size + config.thin_line)
            row = (mouse_pos[1] - config.t_padding) // (config.cell_size + config.thin_line)

            if 0 <= row < 9 and 0 <= col < 9:
                selected_cell = (row, col)

        elif event.type == pygame.KEYDOWN and selected_cell:
            row, col = selected_cell
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                config.sudoku_board[row][col] = 0
            elif pygame.K_1 <= event.key <= pygame.K_9:
                num = event.key - pygame.K_0
                config.sudoku_board[row][col] = num

    return "show sudoku"

def draw_Screen(screen):
    draw_board(screen, selected_cell)
