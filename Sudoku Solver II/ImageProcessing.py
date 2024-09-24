import cv2
import numpy as np
import matplotlib.pyplot as plt
import configuration as confi

def extract_grid_lines(thresh_image):
    # Define kernels for extracting horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))  # (40,1) for horizontal lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))  # (1,40) for vertical lines

    # Detect horizontal lines
    horizontal_lines = cv2.erode(thresh_image, horizontal_kernel, iterations=2)
    horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=3)

    # Detect vertical lines
    vertical_lines = cv2.erode(thresh_image, vertical_kernel, iterations=2)
    vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=3)

    # Combine horizontal and vertical lines
    grid_lines = cv2.add(horizontal_lines, vertical_lines)

    # Remove small components (numbers or noise) using connected components analysis
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(grid_lines, connectivity=8)

    # Filter components based on size (removing small numbers)
    min_line_length = 50  # Minimum size of a line to keep (adjust as needed)
    filtered_grid = np.zeros_like(grid_lines)

    for i in range(1, num_labels):  # Skip background (label 0)
        if stats[i, cv2.CC_STAT_HEIGHT] > min_line_length or stats[i, cv2.CC_STAT_WIDTH] > min_line_length:
            filtered_grid[labels_im == i] = 255

    return filtered_grid

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

    # Extract only the grid lines
    grid_lines = extract_grid_lines(thresh)

    # Show the grid lines
    plt.imshow(grid_lines, cmap='gray')
    plt.title("Extracted Sudoku Grid Lines")
    plt.axis('off')
    plt.show()

# Call the function with the image path from the configuration
image_processing(confi.file_path_test)
