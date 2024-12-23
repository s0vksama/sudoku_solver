import pygame
import cv2
import numpy as np
import matplotlib.pyplot as plt
import configuration as confi
import configuration2 as confi2
import pytesseract
# import HOG_digit as Hd

# Pygame initialization
pygame.init()
font = pygame.font.Font(None, 50)

def plot_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Numbers with Rectangles')
    plt.axis('off')
    plt.show()

def get_digit(old_image, x, y, w, h, tol):
    w_p = int(w * tol)
    h_p = int(h * tol)

    tshow_image = old_image[y+h_p:y+h-h_p, x+w_p:x+w-w_p]

    # # Single call to Pytesseract after initial preprocessing
    # digit = pytesseract.image_to_string(tshow_image, config='--psm 6 digits').strip()

    # if not digit.isdigit() or digit == '0':
    #     # Apply binary thresholding once instead of multiple times
    #     _, show_image = cv2.threshold(tshow_image, 128, 255, cv2.THRESH_BINARY_INV)
    #     digit = pytesseract.image_to_string(show_image, config='--psm 10 digits').strip()

    #     if not digit.isdigit() or digit == '0':
    #         # Use erosion to preprocess the image further
    #         kernel = np.ones((3, 3), np.uint8)
    #         show_image = cv2.erode(show_image, kernel, iterations=1)
    #         digit = pytesseract.image_to_string(show_image, config='--psm 10 digits').strip()

    # if len(digit) > 1:
    #     return get_digit(old_image, x, y, w, h, tol * 2)
    # return digit if digit.isdigit() else '0'

    digit = Hd.predict_image(tshow_image)
    return digit

def image_processing(image, screen, events):
    pygame.display.flip()
    c_old_image = cv2.imread(confi.file_path)
    old_image = cv2.cvtColor(c_old_image, cv2.COLOR_BGR2GRAY)

    board = np.zeros((9, 9), dtype=int)

    # Preprocess image once (convert to grayscale and thresholding)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Use NumPy for storing widths and heights
    squares = []
    widths, heights = [], []

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # Select squares (4-point contours)
            squares.append(approx)
            x, y, w, h = cv2.boundingRect(contour)
            widths.append(w)
            heights.append(h)

    # Calculate median values
    widths = np.array(widths)
    heights = np.array(heights)
    median_width = np.median(widths)
    median_height = np.median(heights)

    # Filter out squares that don't match the median sizes (use vectorized operations)
    tolerance = 0.1
    filtered_squares = [
        squares[i] for i in range(len(squares))
        if (median_width * (1 - tolerance) <= widths[i] <= median_width * (1 + tolerance)) and
           (median_height * (1 - tolerance) <= heights[i] <= median_height * (1 + tolerance))
    ]

    # Process each filtered square
    for i, square in enumerate(filtered_squares):
        screen.fill(confi.lsbackground_col)
        cv2.drawContours(image, [square], -1, (0, 255, 0), 3)
        x, y, w, h = cv2.boundingRect(square)
        text_position = (x + 10, y + 30)

        digit = get_digit(old_image, x, y, w, h, 0.05)

        # Display digits on the image
        font_scale = 0.5 if digit == '0' else 1
        color = (255, 0, 0) if digit == '0' else (0, 0, 255)
        cv2.putText(c_old_image, str(digit), text_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2)

        # Update the board
        board[8 - (i // 9)][8 - (i % 9)] = int(digit)

        # Display progress on the screen
        percent = str(int(i * 100 / 81))
        text_upload = font.render("PROCESSING", True, (149, 121, 104))
        text_upload_percent = font.render(f"{percent} %", True, (149, 121, 104))

        UPLOAD_rect = text_upload.get_rect(center=(300, 250))
        UPLOAD_PERCENT_rect = text_upload_percent.get_rect(center=(300, 375))

        pygame.draw.rect(screen, (194, 207, 215), (99, 299, 80 * 5, 32))
        pygame.draw.rect(screen, (149, 121, 104), (100, 300, i * 5, 30))

        screen.blit(text_upload, UPLOAD_rect)
        screen.blit(text_upload_percent, UPLOAD_PERCENT_rect)
        pygame.display.flip()

    confi2.sudoku_board = board
    print(confi2.sudoku_board)
    return c_old_image
