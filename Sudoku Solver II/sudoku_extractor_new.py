import cv2
import numpy as np
import matplotlib.pyplot as plt
import Get_digit_confi as Gd
from HOG_and_SVM_confidence import SVM_classifier, SVM_single
import configuration2 as config

def process_and_display_cropped_sudoku(image):
    def crop_number(cell_gray, resize_dim=(50, 50)):
        # Apply binary threshold to detect dark blobs on a white background
        _, thresholded = cv2.threshold(cell_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found, process the largest one
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            # Get the bounding box of the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Crop the image to the bounding box
            cropped_cell = cell_gray[y+3:y+h-5, x+3:x+w-5]

            # Resize the cropped image to the desired dimensions
            cropped_cell = cv2.resize(cropped_cell, resize_dim)

            return cropped_cell
        else:
            return cv2.resize(cell_gray, resize_dim)

    def preprocess(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 6)
        return cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    def find_and_draw_contours(image, threshold):
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def main_outline(contours):
        biggest = np.array([])
        max_area = 0
        for c in contours:
            area = cv2.contourArea(c)
            if area > 50:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area
        return biggest

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

    def splitcells(img):
        rows = np.vsplit(img, 9)
        boxes = [np.hsplit(r, 9) for r in rows]
        return [box for row in boxes for box in row]

    threshold = preprocess(image)
    contours = find_and_draw_contours(image, threshold)
    biggest = main_outline(contours)

    if biggest.size != 0:
        biggest = reframe(biggest)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        warped = cv2.warpPerspective(image, matrix, (450, 450))

        cells = splitcells(warped)
        sudoku_array = np.zeros((9, 9), dtype=int)

        # Create an overlay for numbers on the cropped image
        warped_with_numbers = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        warped_with_numbers = cv2.cvtColor(warped_with_numbers, cv2.COLOR_GRAY2BGR)

        # # Plotting the cropped images
        # fig, axs = plt.subplots(9, 9, figsize=(10, 10))
        # fig.suptitle('Cropped Sudoku Cells', fontsize=16)

        for i in range(9):
            for j in range(9):
                cell_gray = cv2.cvtColor(cells[i * 9 + j], cv2.COLOR_BGR2GRAY)
                cropped_cell = crop_number(cell_gray)

                try:
                    prediction = Gd.predict_image(cropped_cell)
                    sudoku_array[i, j] = prediction

                    # Draw the prediction at the center of each cell
                    cell_x, cell_y = j * 50 + 20, i * 50 + 30
                    cv2.putText(warped_with_numbers, str(prediction), (cell_x, cell_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                except Exception as e:
                    print(f"Error processing cell at ({i}, {j}): {e}")
                    sudoku_array[i, j] = -1  # Mark invalid cells

        #         # Display the cropped cell in the grid
        #         axs[i, j].imshow(cropped_cell, cmap='gray')
        #         axs[i, j].axis('off')

        # plt.show()

        # Print the Sudoku grid
        print("Recognized Sudoku Grid:")
        print(sudoku_array)
        config.sudoku_board = sudoku_array
        return warped_with_numbers
    else:
        print("No Sudoku grid detected.")
        return None


# image_path = "E:/sublime/GIT python/Test sudokus/hardest2.png"
# image = cv2.imread(image_path)
# process_and_display_cropped_sudoku(image)
