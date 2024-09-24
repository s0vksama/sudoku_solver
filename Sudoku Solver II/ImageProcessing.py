import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import configuration as confi

def get_sudoku_size(thresh_image):
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and get the largest one (which should be the Sudoku grid)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    sudoku_contour = contours[0]

    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(sudoku_contour)
    return w, h

def image_porcessing(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to smoothen the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # plt.imshow(blurred)
    # plt.title('blurred image')
    # plt.axis('off')  # Hide axes for a cleaner look
    # plt.show()
    # Apply adaptive thresholding to detect edges
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # Invert the image to make the grid lines white
    thresh = cv2.bitwise_not(thresh)
    # plt.imshow(thresh)
    # plt.title('after threshold')
    # plt.axis('off')  # Hide axes for a cleaner look
    # plt.show()
    # Find contours
    print(get_sudoku_size(thresh))


image_porcessing(confi.file_path_test)


