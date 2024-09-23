# board variables
screen_height = 700
screen_width = 600

# Define the button dimensions and position landing screen
lsbutton_width = 300
lsbutton_height = 50
lsbutton_x = (screen_width-lsbutton_width)//2
lsbutton_y = (screen_height-lsbutton_height)//2

# colors
background = (235, 236, 239)
font_color = (240, 101, 49)
button_color = (58, 62, 62)
button_hover_color = (49, 83, 65)
BLACK = (0,0,0)

uploaded_image = None
file_path = ""
sudoku_board = [0]
output_image_rgb = None

ssbutton_width = 100
ssbutton_height = 50
ssbutton_x = (screen_width-ssbutton_width)//2
ssbutton_y = 600


# ---------------------------------------#
thin_line = 2  # line thickness
bold_line = 5

t_padding = 100  # Top padding for the board
l_padding = 50  # Left padding for the board

offset = 4

cell_size = 50  # cell size

# calculation
board_size = 9 * cell_size + bold_line * 4 + thin_line * 6 - 3
small_square_size = 3 * cell_size + bold_line + thin_line * 2 - 3

# colors
background = (235, 236, 239)
border_color = (8, 16, 27)
thin_line_color = (8, 16, 27)
font_color = (240, 101, 49)
highlight_color = (209, 86, 88)
highlight_color2 = (247, 255, 229)
heading_color = (0, 0, 0)  # Color for the heading
button_color = (58, 62, 62)  # Color for the button
button_hover_color = (49, 83, 65)
solver_color = (0, 0, 0)  # Color for solver animation
solved_font_color = (94, 106, 129)
botton_font_color = (237, 239, 243)


# Button variables
button_width = 150
button_height = 50
button_x = (screen_width - button_width) // 4
button_y = screen_height - button_height - 50

stop_button_x = button_x
stop_button_y = button_y  # Place it just above the "Solve" button

solved_set = set()

delay = 0.05 #animation delay

sudoku_board1 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
