import joblib
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import configuration2 as confi
from HOG_and_SVM_confidence import SVM_classifier, SVM_single

# Function to compute gradients
def compute_gradient(image):
    gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(gx ** 2 + gy ** 2)
    angle = np.arctan2(gy, gx) * (180 / np.pi) % 180
    return magnitude, angle

# Function to compute histogram of gradients for a cell
def cell_histogram(magnitude, angle, bin_size=20):
    bins = np.zeros(180 // bin_size)
    for i in range(magnitude.shape[0]):
        for j in range(magnitude.shape[1]):
            bin_index = int(angle[i, j] // bin_size)
            bins[bin_index] += magnitude[i, j]
    return bins

# HOG Descriptor Function
def hog_descriptor(image, cell_size=8, bin_size=20, block_size=2):
    h, w = image.shape
    h = (h // cell_size) * cell_size
    w = (w // cell_size) * cell_size
    image = cv2.resize(image, (w, h))
    magnitude, angle = compute_gradient(image)
    cell_histograms = []
    for i in range(0, h, cell_size):
        row_histograms = []
        for j in range(0, w, cell_size):
            cell_magnitude = magnitude[i:i + cell_size, j:j + cell_size]
            cell_angle = angle[i:i + cell_size, j:j + cell_size]
            hist = cell_histogram(cell_magnitude, cell_angle, bin_size)
            row_histograms.append(hist)
        cell_histograms.append(row_histograms)
    cell_histograms = np.array(cell_histograms)
    hog_features = []
    for i in range(cell_histograms.shape[0] - block_size + 1):
        for j in range(0, cell_histograms.shape[1] - block_size + 1):
            block = cell_histograms[i:i + block_size, j:j + block_size].ravel()
            norm = np.linalg.norm(block) + 1e-6
            block = block / norm
            hog_features.extend(block)
    return np.array(hog_features)

# Main Prediction Function
def main_predict():
    if confi.AImodel is None:
        # Load the trained SVM model
        model_path = "svm_number_model_confidence_hand.pkl"
        try:
            loaded_svm = joblib.load(model_path)
            confi.AImodel = loaded_svm
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("Error: Model file not found. Please check the model path.")
            return
    loaded_svm = confi.AImodel
    images = []
    predictions = []
    confidences = []

    for i in range(20):
        # Load and preprocess the image
        image_path = f'E:/sublime/Sudoku/HOG/TEST/test  ({i + 1}).png'
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Error: Image file not found for test ({i + 1}).png.")
            continue

        # Resize and extract HOG features
        image = cv2.resize(image, (64, 128))
        hog_features = hog_descriptor(image)

        # Make a prediction using the SVM model with confidence score
        prediction, confidence = loaded_svm.predict_with_confidence([hog_features])

        # Store image, prediction, and confidence score for display
        images.append(image)
        predictions.append(prediction[0])
        confidences.append(confidence[0])

    # Display images and predictions with confidence scores
    num_images = len(images)
    cols = 5
    rows = (num_images + cols - 1) // cols  # Calculate rows needed

    plt.figure(figsize=(15, rows * 3))
    for idx, (image, prediction, confidence) in enumerate(zip(images, predictions, confidences)):
        plt.subplot(rows, cols, idx + 1)
        plt.imshow(image, cmap='gray')
        plt.title(f"Pred: {prediction}\nConf: {confidence:.2f}%")
        plt.axis('off')

    plt.tight_layout()
    plt.show()

# Function for predicting a single image
def predict_image(image):
    if confi.AImodel is None:
        model_path = "svm_number_model_confidence_hand.pkl"
        try:
            loaded_svm = joblib.load(model_path)
            confi.AImodel = loaded_svm
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("Error: Model file not found. Please check the model path.")
            return
    loaded_svm = confi.AImodel
    # Resize and extract HOG features
    image = cv2.resize(image, (64, 128))
    hog_features = hog_descriptor(image)

    # Make a prediction using the SVM model with confidence score
    prediction, confidence = loaded_svm.predict_with_confidence([hog_features])
    if confidence[0] > 30:
        return prediction[0]
    else:
        return 0

if __name__ == '__main__':
    main_predict()
