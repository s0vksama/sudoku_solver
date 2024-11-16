import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time
import joblib  # joblib for saving/loading complex models like custom classes

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

# SVM Single Class for Binary Classification
class SVM_single:
    def __init__(self, learning_rate, no_of_iterations, lambda_parameter):
        self.learning_rate = learning_rate
        self.no_of_iterations = no_of_iterations
        self.lambda_parameter = lambda_parameter

    def fit(self, X, Y):
        self.m, self.n = X.shape
        self.w = np.zeros(self.n)
        self.b = 0
        for _ in range(self.no_of_iterations):
            self.update_weights(X, Y)

    def update_weights(self, X, Y):
        for i in range(len(Y)):
            condition = Y[i] * (np.dot(X[i], self.w) - self.b) >= 1
            dw = 2 * self.lambda_parameter * self.w if condition else 2 * self.lambda_parameter * self.w - np.dot(X[i], Y[i])
            db = 0 if condition else Y[i]
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db

    def decision_function(self, X):
        return np.dot(X, self.w) - self.b

# Multi-Class SVM Classifier with Confidence Score
class SVM_classifier:
    def __init__(self, learning_rate, no_of_iterations, lambda_parameter):
        self.learning_rate = learning_rate
        self.no_of_iterations = no_of_iterations
        self.lambda_parameter = lambda_parameter
        self.models = {}

    def fit(self, X, Y):
        self.classes = np.unique(Y)
        for cls in self.classes:
            y_binary = np.where(Y == cls, 1, -1)
            model = SVM_single(self.learning_rate, self.no_of_iterations, self.lambda_parameter)
            model.fit(X, y_binary)
            self.models[cls] = model

    def softmax(self, scores):
        exp_scores = np.exp(scores - np.max(scores, axis=1, keepdims=True))  # Stability improvement
        return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

    def predict_with_confidence(self, X):
        scores = {cls: model.decision_function(X) for cls, model in self.models.items()}
        scores_matrix = np.array(list(scores.values())).T  # Shape: (num_samples, num_classes)
        confidences = self.softmax(scores_matrix)
        predicted_indices = np.argmax(confidences, axis=1)
        predictions = np.array([list(scores.keys())[i] for i in predicted_indices])
        prediction_confidences = np.max(confidences, axis=1) * 100
        return predictions, prediction_confidences

# Main Training Function
def main_train():
    start = time.time()
    file_path = 'E:/sublime/Sudoku/HOG/Dataset/numbers.csv'
    data_df = pd.read_csv(file_path)

    data = []
    labels = []
    base_path = "E:/sublime/Sudoku/HOG/Dataset/numbers/"

    for idx, row in data_df.iterrows():
        label = row['label']
        img_path = base_path + row['file']
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Warning: {img_path} could not be loaded.")
            continue
        image = cv2.resize(image, (64, 128))
        hog_features = hog_descriptor(image)
        data.append(hog_features)
        labels.append(label)

    if len(data) == 0:
        print("Error: No images were loaded. Please check the image paths.")
        return

    data = np.array(data)
    labels = np.array(labels)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    # Train SVM classifier
    svm = SVM_classifier(learning_rate=0.01, no_of_iterations=1000, lambda_parameter=0.01)
    svm.fit(X_train, y_train)

    # Save the model
    model_path = "svm_number_model_confidence_hand.pkl"
    joblib.dump(svm, model_path)
    print(f"Model saved to {model_path}")

    # Get predictions and confidence scores
    predictions, confidences = svm.predict_with_confidence(X_test)

    # Display some predictions with confidence scores
    for i in range(10):
        print(f"Prediction: {predictions[i]}, Confidence: {confidences[i]:.2f}%")

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions) * 100
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Training Time: {time.time() - start:.2f} seconds")

if __name__ == '__main__':
    main_train()
