import cv2
import numpy as np
import matplotlib.pyplot as plt
import Get_digit as Gd
from HOG_and_SVM import SVM_classifier, SVM_single

# Function to preprocess the image: grayscale, blur, threshold
def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 6)
    threshold_img = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    return threshold_img

# Function to find the contours of the sudoku grid and draw them
def find_and_draw_contours(image, threshold):
    contour_1 = image.copy()
    contour, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contour_1, contour, -1, (0, 255, 0), 3)
    return contour_1, contour

# Function to get the biggest contour (the Sudoku outline)
def main_outline(contour):
    biggest = np.array([])
    max_area = 0
    for i in contour:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area

# Reframe the perspective points
def reframe(points):
    points = points.reshape((4, 2))
    points_new = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    points_new[1] = points[np.argmin(diff)]
    points_new[2] = points[np.argmax(diff)]
    return points_new

# Split the image into 9x9 cells
def splitcells(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes

# Main function to extract and display the individual cells of the Sudoku grid
def show_sudoku_cells(image, contours):
    biggest, max_area = main_outline(contours)
    if biggest.size != 0:
        biggest = reframe(biggest)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imagewrap = cv2.warpPerspective(image, matrix, (450, 450))

        # Split the wrapped image into 9x9 cells
        sudoku_cells = splitcells(imagewrap)

        # Display all 81 cells in a grid
        fig, axes = plt.subplots(9, 9, figsize=(12, 12))
        for i in range(9):
            for j in range(9):
                ax = axes[i, j]

                # Convert cell to grayscale if needed
                cell_gray = cv2.cvtColor(sudoku_cells[i * 9 + j], cv2.COLOR_BGR2GRAY)

                # crop the image
                # cell_gray = cell_gray[5:45, 12:37]
                # Pass the grayscale cell to predict_image
                prediction = Gd.predict_image(cell_gray)

                # Display the cell image and prediction on the plot
                ax.imshow(cell_gray, cmap='gray')
                ax.text(0.5, 0.5, str(prediction), va='center', ha='center',
                        fontsize=12, color='red', weight='bold', transform=ax.transAxes)
                ax.axis('off')
        plt.show()
    else:
        print("No Sudoku grid detected.")

def sudoku_Extractor(image_path):
    sudoku_a = cv2.imread(image_path)

    # Resize image to make it more manageable
    sudoku_a = cv2.resize(sudoku_a, (450, 450))

    # Preprocess the image
    threshold = preprocess(sudoku_a)

    # Find and draw the contours of the Sudoku grid
    contour_image, contours = find_and_draw_contours(sudoku_a, threshold)

    # Show the individual cells with predictions
    show_sudoku_cells(sudoku_a, contours)

image_path = 'test (8).jpeg'
sudoku_Extractor(image_path)
