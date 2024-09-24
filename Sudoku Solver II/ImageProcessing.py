import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import configuration as confi

SUDOKU = [[0 for _ in range(9)] for _ in range(9)]

def get_sudoku_size(thresh_image):
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and get the largest one (which should be the Sudoku grid)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    sudoku_contour = contours[0]

    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(sudoku_contour)
    print(x,y)
    return x, y, w, h

def image_processing(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to smoothen the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to detect edges
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # Invert the image to make the grid lines white
    thresh = cv2.bitwise_not(thresh)

    # Get the size of the Sudoku grid
    x, y, board_length, board_height = get_sudoku_size(thresh)
    box_length, box_height = board_length // 9, board_height // 9

    # Extract each of the 9x9 blocks
    box_images = []
    for i in range(9):
        for j in range(9):
            # Define the current block
            r_start = i * box_length + y
            r_end = (i + 1) * box_length + y

            c_start = j * box_height + x
            c_end = (j + 1) * box_height + x

            # Extract the block from the image
            block = thresh[r_start:r_end, c_start:c_end]
            box_images.append(block)

    # Display the extracted blocks using matplotlib
    fig, axes = plt.subplots(9, 9, figsize=(8, 8))
    plt.suptitle("Sudoku")
    axes = axes.ravel()

    for idx, ax in enumerate(axes):
        ax.imshow(box_images[idx], cmap='gray')
        ax.axis('off')

    plt.tight_layout()
    plt.show()

# Call the function with the image path from the configuration
image_processing(confi.file_path_test)
