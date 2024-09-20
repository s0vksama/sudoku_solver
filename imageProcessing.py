import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import configuration as confi

def imageProcessing(path):
    # Load the image
    image_path = path
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    a, b = image.shape

    # Initialize an empty output array with the same size as the original image
    my_output = np.zeros((a, b), dtype=np.uint8)

    # Apply a binary threshold to convert the image to binary
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    # Detect grid lines using morphological operations
    kernel = np.ones((3, 3), np.uint8)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 100))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 1))

    # Extract vertical and horizontal lines
    vertical_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, vertical_kernel)
    horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel)

    # Combine vertical and horizontal lines to get the grid
    grid_lines = cv2.addWeighted(vertical_lines, 1, horizontal_lines, 1, 0)

    # Subtract grid from the binary image to isolate the numbers
    isolated_numbers = cv2.subtract(binary_image, grid_lines)

    # Find contours of the isolated numbers
    contours, _ = cv2.findContours(isolated_numbers, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a copy of the original image to display detected numbers
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Initialize a 9x9 matrix to store the detected numbers
    sudoku_grid = np.zeros((9, 9), dtype=int)

    # Calculate the size of each grid cell based on the image dimensions
    cell_height = a // 9
    cell_width = b // 9

    # Iterate through the contours and extract the numbers
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > 5 and w > 5:  # Set a minimum size for contours (to ignore noise)
            # Ensure the ROI fits within bounds
            x_end = min(x + w, b)
            y_end = min(y + h, a)

            # Extract the region of interest (ROI) where the number is
            roi = binary_image[y-7:y_end+7, x-7:x_end+7]

            # Use Tesseract OCR to recognize the digit (config for single characters)
            digit = pytesseract.image_to_string(roi, config='--psm 10 digits')
            digit = digit.strip()

            if not digit.isdigit():
                # Retry with grayscale image if the binary image fails
                roi = image[y-7:y_end+7, x-7:x_end+7]
                digit = pytesseract.image_to_string(roi, config='--psm 10 digits')

            # Ensure only digits are recognized
            digit = digit.strip()

            if digit.isdigit():
                # Calculate row and column based on contour position
                row = y // cell_height
                col = x // cell_width

                # Store the digit in the sudoku matrix
                sudoku_grid[row, col] = int(digit)

                # Draw a rectangle around the detected number
                cv2.rectangle(output_image, (x-7, y-7), (x_end+7, y_end+7), (0, 0, 255), 2)

                # Draw the recognized digit near the ROI
                cv2.putText(output_image, digit.strip(), (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

    # Display the final image with rectangles around the numbers
    # plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    # plt.title('Detected Numbers with Rectangles')
    # plt.axis('off')
    # plt.show()

    confi.sudoku_board = sudoku_grid
    return output_image_rgb
    # # Print or display the Sudoku matrix
    # print("Sudoku Grid:")
    # print(sudoku_grid)
