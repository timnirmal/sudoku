import tensorflow as tf
import numpy as np
import cv2

# Load the model
loaded_model = tf.keras.models.load_model('mnist_cnn_model.h5')

def segment_digits(img):
    # Enhance image quality
    img = cv2.equalizeHist(img)

    # Apply Gaussian Blur for noise reduction
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # show image
    cv2.imshow("guassian blur", img)
    # cv2.waitKey(0)

    # Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Morphological operations to close gaps in between digit parts
    kernel = np.ones((3,3),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # show image
    cv2.imshow("adaptive thresholding", thresh)
    # cv2.waitKey(0)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # show image
    imgContours = img.copy()  # Copy the image - all contours
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)  # Draw all contours
    cv2.imshow("Contours", imgContours)
    cv2.waitKey(0)

    digit_images = []
    for contour in contours:
        # Consider contour area to filter out non-digit contours
        if cv2.contourArea(contour) > 50:  # Adjust this threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            digit_img = img[y:y+h, x:x+w]
            digit_img = cv2.resize(digit_img, (28, 28), interpolation=cv2.INTER_AREA)
            digit_images.append(digit_img)

    return digit_images


def classify_digits(digit_images, model):
    digits = []
    for img in digit_images:
        img = np.expand_dims(img, axis=-1)  # Add channel dimension
        img = img / 255.0  # Normalize
        img = img.reshape(1, 28, 28, 1)  # Reshape for the model
        prediction = model.predict(img)
        digit = np.argmax(prediction)
        digits.append(digit)
    return digits

def process_and_classify_image(img):
    digit_images = segment_digits(img)
    classified_digits = classify_digits(digit_images, loaded_model)
    return classified_digits

# Load your image
img = cv2.imread('box.png', cv2.IMREAD_GRAYSCALE)

# Process and classify the image
result = process_and_classify_image(img)
print(f"Classified digits: {result}")
