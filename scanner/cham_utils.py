import cv2 as cv
import numpy as np

from digit.ocr import recognize_digit


def preProcessImg(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)  # Add Gaussian blur
    imgThreshold = cv.adaptiveThreshold(
        imgBlur, 255, 1, 1, 11, 2)  # Apply adaptive threshold
    return imgThreshold


# stack images in one window
def stackImages(imgArray, scale):
    rows = len(imgArray)
    cols = len(imgArray[0])
    # check if imgArray[0] is a list
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:  # if imgArray[0] is a list
        for x in range(0, rows):
            for y in range(0, cols):
                # resize the image
                imgArray[x][y] = cv.resize(
                    imgArray[x][y], (0, 0), None, scale, scale)
                # check if the image is grayscale
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv.cvtColor(
                        imgArray[x][y], cv.COLOR_GRAY2BGR)
        # create a blank image
        imgBlank = np.zeros((height, width, 3), np.uint8)
        # create a horizontal stack of images
        hor = [imgBlank] * rows
        # create a vertical stack of images
        hor_con = [imgBlank] * rows
        for x in range(0, rows):
            # horizontal concatenation
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        # vertical concatenation
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:  # if imgArray[0] is not a list
        for x in range(0, rows):
            # resize the image
            imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            # check if the image is grayscale
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        # horizontal concatenation
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        # vertical concatenation
        ver = hor
    return ver


# find the biggest contour
def findBiggestContour(contours):
    biggestContour = np.array([])
    maxArea = 0
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 50:  # ignore small contours - noise
            perimeter = cv.arcLength(contour, True)
            # approximate the shape - find the vertices
            approx = cv.approxPolyDP(contour, 0.02 * perimeter, True)
            # select the biggest contour with 4 vertices
            if area > maxArea and len(approx) == 4:
                biggestContour = approx
                maxArea = area
    return biggestContour, maxArea


# reorder the points
def reoderPoints(points):
    points = points.reshape((4, 2))  # reshape the array to 4x2 matrix
    orderedPoints = np.zeros((4, 1, 2), np.int32)
    xyAddition = points.sum(1)  # sum of x and y coordinates of all points

    # top-left corner - minimum sum
    orderedPoints[0] = points[np.argmin(xyAddition)]
    # bottom-right corner - maximum sum
    orderedPoints[3] = points[np.argmax(xyAddition)]

    xyDifference = np.diff(points, axis=1)  # difference of x and y coordinates

    # top-right corner - minimum difference
    orderedPoints[1] = points[np.argmin(xyDifference)]
    # bottom-left corner - maximum difference
    orderedPoints[2] = points[np.argmax(xyDifference)]

    return orderedPoints


# split the image into 81 boxes
def splitImgToBoxes(img, boxesSize):
    rows = np.vsplit(img, boxesSize)  # split the image into 9 rows
    boxes = []
    for row in rows:
        cols = np.hsplit(row, boxesSize)  # split each row into 9 columns
        for box in cols:
            boxes.append(box)
    return boxes


# # initialize the model
#
#
# def initializePredectionModel():
#     # load the model
#     model = load_model('../digits_classification/model_trained.h5')
#     return model


# get the prediction of each box
def predictDigits(boxes, model):
    result = []
    for box in boxes:
        # prepare the image
        img = np.asarray(box)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]  # remove the border
        img = cv.resize(img, (32, 32))
        img = img / 255
        img = img.reshape(1, 32, 32, 1)

        # predict
        predictions = model.predict(img)
        classIndex = np.argmax(predictions)
        probabilityValue = np.amax(predictions)
        print(classIndex, probabilityValue)

        # check if probability is above threshold
        threshold = 0.8
        if probabilityValue > threshold:
            result.append(classIndex)
        else:
            result.append(0)  # empty cell
    return result


# get the prediction of each box
def predict_digits_tesseract(boxes):
    result = []
    for box in boxes:
        # call recognize_digit(image)
        digit = recognize_digit(box)
        print(digit)

        # if digit is not empty
        if digit != "":
            result.append(int(digit))
        else:
            result.append(0)

    return result


# display digits on image
def displayDigitsOnImg(img, digits, boxSize=9, color=(0, 255, 0)):
    boxWidth = int(img.shape[1] / boxSize)  # width of each box
    boxHeight = int(img.shape[0] / boxSize)  # height of each box
    for x in range(0, boxSize):
        for y in range(0, boxSize):
            if digits[(y * boxSize) + x] != 0:
                # put text on the image
                cv.putText(img, str(digits[(y * boxSize) + x]),
                           (x * boxWidth + int(boxWidth / 2) - 10, int((y + 0.8) * boxHeight)),
                           cv.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 2, cv.LINE_AA)
    return img


# draw grid on image
def drawSudokuGrid(img, boxSize=9):
    width = int(img.shape[1] / boxSize)
    height = int(img.shape[0] / boxSize)
    for i in range(0, boxSize):
        leftPt = (0, height * i)
        rightPt = (img.shape[1], height * i)
        topPt = (width * i, 0)
        bottomPt = (width * i, img.shape[0])
        cv.line(img, leftPt, rightPt, (255, 255, 0), 2)
        cv.line(img, topPt, bottomPt, (255, 255, 0), 2)
    return img


def list_to_file(sudoku_list, boxSize=9):
    # Convert the list into a 16x16 grid.
    sudoku_grid = [sudoku_list[i:i + boxSize] for i in range(0, len(sudoku_list), boxSize)]

    # Prepare the string to write to the text file.
    sudoku_string = '\n'.join(' '.join(str(num) if num != 0 else '0' for num in row) for row in sudoku_grid)

    # Path for the text file.
    file_path = 'sudoku_puzzle.txt'

    # Write the formatted string to a text file.
    with open(file_path, 'w') as file:
        file.write(sudoku_string)

    return file_path
