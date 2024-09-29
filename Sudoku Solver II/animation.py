import pygame
import configuration2 as config
import time
pygame.init()


# Fonts
font = pygame.font.SysFont('roboto', 40, bold=False)
thin_font = pygame.font.SysFont('roboto', 40, bold=False)
heading_font = pygame.font.Font(None, 48)
button_font = pygame.font.Font(None, 36)

button_rect = pygame.Rect(config.button_x, config.button_y, config.button_width, config.button_height)
stop_button_rect = pygame.Rect(config.stop_button_x + config.button_width + 50, config.stop_button_y, config.button_width, config.button_height)

def draw_rounded_rect(surface, color, rect, corner_radius):
    # Create a surface with transparency (using SRCALPHA)
    rounded_rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw a filled rounded rectangle on this surface
    pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=corner_radius)

    # Blit the surface onto the main screen at the specified location
    surface.blit(rounded_rect_surface, rect.topleft)

# Function to draw the board grid, heading, numbers, and buttons
def draw_board(screen, selected_cell=None, k=[]):
    screen.fill(config.background)

    if len(k) == 3:
        highlight_connections(screen, k[0],k[1],k[2])

    # Draw the heading
    heading_surface = heading_font.render("Sudoku Solver", True, config.heading_color)
    heading_rect = heading_surface.get_rect(center=(config.screen_width / 2, config.t_padding / 2))
    screen.blit(heading_surface, heading_rect)

    h_start = config.t_padding
    v_start = config.l_padding
    for x in range(10):
        if x % 3 == 0:
            # Bold line for every third line
            pygame.draw.line(screen, config.border_color, (v_start, config.t_padding), (v_start, config.t_padding + config.board_size), config.bold_line)
            pygame.draw.line(screen, config.border_color, (config.l_padding, h_start), (config.l_padding + config.board_size, h_start), config.bold_line)
            v_start += config.cell_size + config.bold_line
            h_start += config.cell_size + config.bold_line
        else:
            # Thin lines for the regular grid
            pygame.draw.line(screen, config.border_color, (v_start, config.t_padding), (v_start, config.t_padding + config.board_size), config.thin_line)
            pygame.draw.line(screen, config.border_color, (config.l_padding, h_start), (config.l_padding + config.board_size, h_start), config.thin_line)
            v_start += config.cell_size + config.thin_line
            h_start += config.cell_size + config.thin_line

    # Draw the numbers, centered
    for row in range(9):
        for col in range(9):
            if config.sudoku_board[row][col] != 0:
                color = config.font_color
                if (row, col) in config.solved_set:
                    color = config.solved_font_color
                    value_surface = thin_font.render(str(config.sudoku_board[row][col]), True, color)
                else:
                    value_surface = font.render(str(config.sudoku_board[row][col]), True, color)
                value_rect = value_surface.get_rect()

                # Calculate the position to center the number within the cell
                cell_x = config.l_padding + col * (config.cell_size + config.thin_line) + (col // 3) * (config.bold_line - config.thin_line) + config.offset
                cell_y = config.t_padding + row * (config.cell_size + config.thin_line) + (row // 3) * (config.bold_line - config.thin_line) + config.offset

                # Center the text inside the cell
                value_rect.center = (cell_x + config.cell_size / 2, cell_y + config.cell_size / 2)

                screen.blit(value_surface, value_rect)

    # Highlight selected cell
    if selected_cell:
        row, col = selected_cell
        cell_x = config.l_padding + col * (config.cell_size + config.thin_line) + (col // 3) * (config.bold_line - config.thin_line) + config.offset - 1.5
        cell_y = config.t_padding + row * (config.cell_size + config.thin_line) + (row // 3) * (config.bold_line - config.thin_line) + config.offset - 1.5

        # Adjust the size and position for the highlighted square
        pygame.draw.rect(screen, config.highlight_color, (cell_x, cell_y, config.cell_size + config.offset, config.cell_size + config.offset), 5)

    # Draw the "Solve" button with rounded corners
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        draw_rounded_rect(screen, config.button_hover_color, button_rect, 15)  # Radius 15 for rounded corners
    else:
        draw_rounded_rect(screen, config.button_color, button_rect, 15)

    button_text_surface = button_font.render("Solve", True, config.botton_font_color)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    screen.blit(button_text_surface, button_text_rect)

    # Draw the "Stop" button with rounded corners
    if stop_button_rect.collidepoint(mouse_pos):
        draw_rounded_rect(screen, config.button_hover_color, stop_button_rect, 15)  # Radius 15 for rounded corners
    else:
        draw_rounded_rect(screen, config.button_color, stop_button_rect, 15)

    stop_button_text_surface = button_font.render("Stop", True, config.botton_font_color)
    stop_button_text_rect = stop_button_text_surface.get_rect(center=stop_button_rect.center)
    screen.blit(stop_button_text_surface, stop_button_text_rect)


# Convert mouse position to grid coordinates
def get_cell_from_mouse(pos):
    x, y = pos
    if config.l_padding <= x <= config.l_padding + config.board_size and config.t_padding <= y <= config.t_padding + config.board_size:
        col = (x - config.l_padding) // (config.cell_size + config.thin_line)
        row = (y - config.t_padding) // (config.cell_size + config.thin_line)
        return row, col
    return None

def highlight_connections(screen, row, col, value):
    # Set the color for highlighting
    highlight_color = config.highlight_color2  # Choose an appropriate color

    cell_x = config.l_padding + col * (config.cell_size + config.thin_line) + (col // 3) * (config.bold_line - config.thin_line) + config.offset
    cell_y = config.t_padding + row * (config.cell_size + config.thin_line) + (row // 3) * (config.bold_line - config.thin_line) + config.offset
    # coloring the entire row
    pygame.draw.rect(screen, highlight_color, (config.l_padding-2, cell_y-1, config.board_size, config.cell_size+3))
    pygame.draw.rect(screen, highlight_color, (cell_x-1, config.t_padding-2, config.cell_size+3, config.board_size))

    # 3. Color the 3x3 square
    srs= (row // 3) * 3
    scs = (col // 3) * 3

    cell_x = config.l_padding + scs * (config.cell_size + config.thin_line) + (scs // 3) * (config.bold_line - config.thin_line) + config.offset
    cell_y = config.t_padding + srs * (config.cell_size + config.thin_line) + (srs // 3) * (config.bold_line - config.thin_line) + config.offset

    pygame.draw.rect(screen, highlight_color, (cell_x-3, cell_y-3, config.small_square_size, config.small_square_size))

# Function to animate the solver step-by-step
def draw_solver_step(screen, row, col, value):
    # need to color the possible the whole square and the row and column
    draw_board(screen, None, [row, col, value])
    value_surface = font.render(str(value), True, config.solver_color)
    value_rect = value_surface.get_rect()

    # Calculate the position to center the number within the cell
    cell_x = config.l_padding + col * (config.cell_size + config.thin_line) + (col // 3) * (config.bold_line - config.thin_line) + config.offset
    cell_y = config.t_padding + row * (config.cell_size + config.thin_line) + (row // 3) * (config.bold_line - config.thin_line) + config.offset

    # Center the text inside the cell
    value_rect.center = (cell_x + config.cell_size / 2, cell_y + config.cell_size / 2)

    screen.blit(value_surface, value_rect)
    pygame.display.update()
    time.sleep(config.delay)  # delay for animation

# Check if the current board state is valid
def is_valid(board, row, col, num):
    # Check the row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check the column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check the 3x3 sub-grid
    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False

    return True

# Convert mouse position to grid coordinates
def get_cell_from_mouse(pos):
    x, y = pos
    if config.l_padding <= x <= config.l_padding + config.board_size and config.t_padding <= y <= config.t_padding + config.board_size:
        col = (x - config.l_padding) // (config.cell_size + config.thin_line)
        row = (y - config.t_padding) // (config.cell_size + config.thin_line)
        return row, col
    return None


# Check if the current board state is valid
def is_valid(board, row, col, num):
    # Check the row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check the column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check the 3x3 sub-grid
    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False

    return True


def obvious(screen):
    global stop_solver
    flag = False
    for row in range(9):
        for col in range(9):
            if stop_solver:
                return False

            if config.sudoku_board[row][col] == 0:
                # Start with all possible numbers 1-9
                x = list(range(1, 10))


                for k in range(9):
                    # Remove numbers from the same column
                    if config.sudoku_board[k][col] in x:
                        x.remove(config.sudoku_board[k][col])

                    # Remove numbers from the same row
                    if config.sudoku_board[row][k] in x:
                        x.remove(config.sudoku_board[row][k])

                # Identify the top-left corner of the 3x3 subgrid
                top_left_row = 3 * (row // 3)
                top_left_col = 3 * (col // 3)

                # Remove numbers from the 3x3 subgrid
                for r in range(top_left_row, top_left_row + 3):
                    for c in range(top_left_col, top_left_col + 3):
                        if config.sudoku_board[r][c] in x:
                            x.remove(config.sudoku_board[r][c])

                if len(x) == 1:
                    config.sudoku_board[row][col] = x[0]
                    flag = True
                    config.solved_set.add((row, col))
                    draw_solver_step(screen, row, col, x[0])

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if stop_button_rect.collidepoint(mouse_pos):
                                stop_solver = True  # Set the stop flag when "Stop" is clicked
    if flag == True:
        obvious(screen)

def backtrack(screen):
    global stop_solver
    for row in range(9):
        for col in range(9):
            if stop_solver:
                return False
            if config.sudoku_board[row][col] == 0:
                # backtrack algo
                for num in range(1, 10):
                    if is_valid(config.sudoku_board, row, col, num):
                        config.sudoku_board[row][col] = num
                        draw_solver_step(screen, row, col, num)
                        if backtrack(screen):
                            return True
                        config.sudoku_board[row][col] = 0
                        draw_solver_step(screen, row, col, 0)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()
                                if stop_button_rect.collidepoint(mouse_pos):
                                    stop_solver = True  # Set the stop flag when "Stop" is clicked
                return False
    return True

def solve_sudoku_animated(screen):
    obvious(screen)
    backtrack(screen)

def handle_landingScreen_events(events, screen):
    global stop_solver
    selected_cell = None

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                stop_solver = False  # Reset stop flag when "Solve" is clicked
                solve_sudoku_animated(screen)
            if stop_button_rect.collidepoint(mouse_pos):
                stop_solver = True  # Set the stop flag when "Stop" is clicked
            selected_cell = get_cell_from_mouse(mouse_pos)
    draw_board(screen, selected_cell)
    pygame.display.update()
    return "animation"

def draw_showSudoku_Screen(screen):

    screen.fill(config.background)
    draw_board(screen, None)
