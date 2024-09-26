import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('contour_image.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply binary threshold to the image
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through the contours and filter based on shape
squares = []
for contour in contours:
    # Approximate the contour to remove unnecessary points
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Check if the contour has 4 points and is a square
    if len(approx) == 4:
        squares.append(approx)

print(squares)

# Draw the contours (for visualization)
cv2.drawContours(image, squares, -1, (0, 255, 0), 3)
# Convert the image from BGR to RGB for matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Plot the result image using matplotlib
plt.figure(figsize=(6, 6))
plt.imshow(image_rgb)
plt.title('Detected Squares')
plt.axis('off')
plt.show()

# Create a copy of the original image for numbering the squares
image_numbered = image_rgb.copy()

# Number the squares by placing text at the center of each detected square
font = cv2.FONT_HERSHEY_SIMPLEX
for i, square in enumerate(squares):
    # Calculate the center point of the square
    M = cv2.moments(square)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # Put the square number at the center of the square
        cv2.putText(image_numbered, str(i+1), (cx-10, cy+10), font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

# Plot the result image with numbered squares
plt.figure(figsize=(6, 6))
plt.imshow(image_numbered)
plt.title('Numbered Squares')
plt.axis('off')
plt.show()

# getting square size
# Loop through the squares and calculate the size
square_sizes = []
for i, square in enumerate(squares):
    # Get the bounding rectangle of each square
    x, y, w, h = cv2.boundingRect(square)
    square_sizes.append((w, h))
    # print(f"Square {i+1}: Width = {w} pixels, Height = {h} pixels")

def my_median(square_sizes):
    square_sizes = np.array(square_sizes)
    # Separate x and y coordinates
    x_coords = square_sizes[:, 0]
    y_coords = square_sizes[:, 1]
    # Compute the median for x and y coordinates
    median_x = np.median(x_coords)
    median_y = np.median(y_coords)
    # Median of the 2D points
    median_point = (median_x, median_y)
    return median_point

# Now square_sizes contains the width and height of all detected squares

