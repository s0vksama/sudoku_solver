import cv2
import matplotlib.pyplot as plt
import configuration as confi
# Load the image
image = cv2.imread(confi.file_path_test)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to smoothen the image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding to detect edges
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# Invert the image to make the grid lines white
thresh = cv2.bitwise_not(thresh)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area (optional, if you only want to show sorted contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Create a copy of the original image for drawing
drawing = image.copy()

# Draw each contour
for i, contour in enumerate(contours):
    color = (0, 255, 0)  # Green color for contours
    cv2.drawContours(drawing, [contour], -1, color, 3)

# Convert the drawing image from BGR to RGB format for Matplotlib
drawing_rgb = cv2.cvtColor(drawing, cv2.COLOR_BGR2RGB)

# Display the image with Matplotlib
plt.imshow(drawing_rgb)
plt.title(f'All Detected Contours: {len(contours)} Total')
plt.axis('off')  # Hide axes for a cleaner look
plt.show()
