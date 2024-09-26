import cv2
import numpy as np
import matplotlib.pyplot as plt

def image_processing(image):
    # image = cv2.imread(path)
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
        # Draw the contour
        cv2.drawContours(filtered_image, [square], -1, (0, 255, 0), 3)

        # Get the bounding box for the square
        x, y, w, h = cv2.boundingRect(square)

        # Position for the number (slightly above the top-left corner of the bounding box)
        text_position = (x, y+20)

        # Put the number on the image
        cv2.putText(filtered_image, str(i + 1), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    return filtered_image

# # Load the image
# image = cv2.imread('contour_image.jpg')

# ans = image_processing(image)

# # Display the image with the numbered squares
# plt.imshow(cv2.cvtColor(ans, cv2.COLOR_BGR2RGB))
# plt.title('Filtered and Numbered Squares')
# plt.show()
