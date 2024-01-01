import cv2
import numpy as np
import tensorflow as tf


# Function to preprocess the digit for classification
def preprocess_for_classification(img, size=(28, 28)):
    img = cv2.resize(img, size)  # Resize image to match model's expected input
    img = img / 255.0  # Normalize pixel values to be between 0 and 1
    img = img.reshape(1, size[0], size[1], 1)  # Reshape to add batch dimension
    return img


# Function to classify a single digit
def classify_digit(digit_img, model):
    preprocessed = preprocess_for_classification(digit_img)
    prediction = model.predict(preprocessed)
    return np.argmax(prediction)


# Function to segment and classify digits
def segment_and_classify_digits(img, model):
    # Apply Gaussian Blur to reduce noise
    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply Adaptive Thresholding to binarize the image
    thresh_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    digit_rects = [cv2.boundingRect(cnt) for cnt in contours]

    # Sort the digit contours from left to right
    digit_rects.sort(key=lambda x: x[0])

    classified_digits = []

    for rect in digit_rects:
        x, y, w, h = rect
        # Extract the digit using the bounding rectangle
        digit_img = thresh_img[y:y + h, x:x + w]

        # Classify the digit
        digit = classify_digit(digit_img, model)
        classified_digits.append(digit)

    if len(classified_digits) == 2 and classified_digits[0] == 1:
        # If there are two digits and the first one is 1, we assume it's a two-digit number with 1 as the first digit
        return 10 + classified_digits[1]
    elif len(classified_digits) == 1:
        # If there's only one digit, return it
        return classified_digits[0]
    else:
        # If there are no digits or more than two, return None
        return None


# Load the model
loaded_model = tf.keras.models.load_model('mnist_cnn_model.h5')

# Load your image
img = cv2.imread('box.png', cv2.IMREAD_GRAYSCALE)

# Process and classify the image
number = segment_and_classify_digits(img, loaded_model)

if number is not None:
    print(f"Identified number: {number}")
else:
    print("No digits found or more than two digits present.")
