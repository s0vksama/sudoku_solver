import pygame
pygame.init()

import cv2
import numpy as np
import matplotlib.pyplot as plt
import configuration as confi
import configuration2 as confi2
import pytesseract

font = pygame.font.Font(None, 50)
def plot_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Numbers with Rectangles')
    plt.axis('off')
    plt.show()

def get_digit(old_image, x, y, w, h, tol):
    w_p =int(w*tol)  #width percent
    h_p =int(h*tol)  #width percent

    tshow_image = old_image[y+h_p:y+h-h_p, x+w_p:x+w-w_p]

    digit = pytesseract.image_to_string(tshow_image, config='--psm 6 digits')
    digit = digit.strip()

    if not digit.isdigit() or digit == '0':
        ff, show_image = cv2.threshold(tshow_image, 128, 255, cv2.THRESH_BINARY_INV)

        digit = pytesseract.image_to_string(show_image, config='--psm 10 digits')
        digit = digit.strip()

        if not digit.isdigit() or digit == '0':
            # Define the kernel for erosion (3x3 rectangular kernel in this example)
            kernel = np.ones((3, 3), np.uint8)

            # Apply erosion
            show_image = cv2.erode(show_image, kernel, iterations=1)
            digit = pytesseract.image_to_string(show_image, config='--psm 10 digits')
            digit = digit.strip()

    if len(digit) >1:
        digit = get_digit(old_image, x, y, w, h, tol*2)

    if not digit.isdigit():
        digit = 0

    return digit


def image_processing(image, screen, events):

    pygame.display.flip()
    c_old_image = cv2.imread(confi.file_path)
    old_image = cv2.cvtColor(c_old_image, cv2.COLOR_BGR2GRAY)

    board = [[0 for _ in range(9)] for _ in range(9)]
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold to the image
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Lists to store the widths and heights of squares
    widths = []
    heights = []

    # Loop through the contours and filter based on shape
    squares = []
    for contour in contours:
        # Approximate the contour to remove unnecessary points
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour has 4 points (likely a square or rectangle)
        if len(approx) == 4:
            squares.append(approx)

            # Get the bounding rectangle for the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Store the width and height
            widths.append(w)
            heights.append(h)

    # Calculate the median width and height
    median_width = np.median(widths)
    median_height = np.median(heights)

    # Set tolerance (for example, ±10%)
    tolerance = 0.1
    min_width = median_width * (1 - tolerance)
    max_width = median_width * (1 + tolerance)
    min_height = median_height * (1 - tolerance)
    max_height = median_height * (1 + tolerance)

    # Filter squares that are close to the median width and height
    filtered_squares = []
    for i, contour in enumerate(squares):
        w = widths[i]
        h = heights[i]

        # Check if the width and height are within the tolerance range
        if min_width <= w <= max_width and min_height <= h <= max_height:
            filtered_squares.append(contour)

    # Draw the filtered squares and number them
    filtered_image = image.copy()

    for i, square in enumerate(filtered_squares):
        screen.fill(confi.lsbackground_col)
        # Draw the contour
        cv2.drawContours(filtered_image, [square], -1, (0, 255, 0), 3)

        # Get the bounding box for the square
        x, y, w, h = cv2.boundingRect(square)

        # Position for the number (slightly above the top-left corner of the bounding box)
        text_position = (x+10, y+30)

        digit = get_digit(old_image, x, y, w, h, 0.05)

        if digit == 0:
            cv2.putText(c_old_image, str(digit), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        else:
            cv2.putText(c_old_image, str(digit), text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # print(digit)
        board[8 -(i//9)][8-(i%9)] = digit

        percent = str(int(i*100/81))

        text_UPLOAD = font.render("PROCESSING", True, (149, 121, 104))  # First pair "S U"
        text_UPLOAD_PERCENT = font.render("{} %".format(percent), True, (149, 121, 104))  # Second pair "D O"
        # upload scrren
        UPLOAD_rect = text_UPLOAD .get_rect(center=(300, 250))
        UPLOAD_PERCENT_rect = text_UPLOAD_PERCENT.get_rect(center=(300, 375))

        pygame.draw.rect(screen, (194, 207, 215), (99, 299, 80*5, 32))
        pygame.draw.rect(screen, (149, 121, 104), (100, 300, i*5, 30))

        screen.blit(text_UPLOAD, UPLOAD_rect)
        screen.blit(text_UPLOAD_PERCENT, UPLOAD_PERCENT_rect)
        pygame.display.flip()

    confi2.sudoku_board = board
    return c_old_image
