import cv2
import numpy as np


# Function to rotate an image using cv2
def rotate_image_cv2(image, angle, scale=1.0):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

# Function to skew an image using cv2 (horizontal skew)
def skew_image_horizontal_cv2(image, skew_amount):
    (h, w) = image.shape[:2]
    skew_matrix = np.float32([
        [1, skew_amount, 0],
        [0, 1, 0]
    ])
    size = (w + int(skew_amount * h), h)
    skewed = cv2.warpAffine(image, skew_matrix, size)
    return skewed

# Function to skew an image using cv2 (vertical skew)
def skew_image_vertical_cv2(image, skew_amount):
    (h, w) = image.shape[:2]
    skew_matrix = np.float32([
        [1, 0, 0],
        [skew_amount, 1, 0]
    ])
    size = (w, h + int(skew_amount * w))
    skewed = cv2.warpAffine(image, skew_matrix, size)
    return skewed

# Function to apply arbitrary perspective transformation using cv2
def perspective_transform_cv2(image, src_points, dst_points):
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
    return warped


# image path
imgPath = "../sudoku_images/2.jpg"

# prepare image
img = cv2.imread(imgPath)

# # rotate image
# rotated = rotate_image_cv2(img, 90)
# cv2.imshow("Rotated", rotated)
#
# # skew image
# skewed_horizontal = skew_image_horizontal_cv2(img, 0.5)
# cv2.imshow("Skewed Horizontal", skewed_horizontal)

skewed_vertical = skew_image_vertical_cv2(img, 0.5)
cv2.imshow("Skewed Vertical", skewed_vertical)
# save
cv2.imwrite("skewed_vertical.jpg", skewed_vertical)

# perspective transform
src_points = np.float32([[0, 0], [img.shape[1], 0], [0, img.shape[0]], [img.shape[1], img.shape[0]]])
dst_points = np.float32([[0, 0], [img.shape[1], 0], [0, img.shape[0]], [img.shape[1] - 100, img.shape[0] - 100]])
warped = perspective_transform_cv2(img, src_points, dst_points)
cv2.imshow("Warped", warped)
cv2.imwrite("warped.jpg", warped)

cv2.waitKey(0)
