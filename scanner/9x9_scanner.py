from typing import Any

import cv2
import numpy as np
from numpy import ndarray, dtype, generic

from digit.ocr import recognize_digit
from scanner.cham_utils import reoderPoints, findBiggestContour, preProcessImg, splitImgToBoxes, displayDigitsOnImg, \
    drawSudokuGrid, stackImages, predictDigits, predict_digits_tesseract, list_to_file

from solver.ninebynine import solve_sudoku_9x9
from solver.hexbyhex import solve_sudoku_16x16

# imgPath = "../sudoku_images/1.jpg"
# imgHeight = 450
# imgWidth = 450
# boxSize = 9

# # imgPath = "../sudoku_images/2.jpg"
# imgPath = "../generate_images/skewed_vertical.jpg"
# imgHeight = 480
# imgWidth = 480
# boxSize = 16

# imgPath = "../sudoku_images/2.jpg"
imgPath = "../sudoku_gen/sudoku 16x16.png"
imgHeight = 800
imgWidth = 800
boxSize = 16

# # imgPath = "../sudoku_images/2.jpg"
# imgPath = "../sudoku_gen/sudoku 9x9.png"
# imgHeight = 450
# imgWidth = 450
# boxSize = 9

# prepare image
img = cv2.imread(imgPath)
img = cv2.resize(img, (imgHeight, imgWidth))  # Resize the image
blankImg = np.zeros((imgHeight, imgWidth, 3), np.uint8)  # Create a blank image
imgThreshold = preProcessImg(img)  # Preprocess the image

# show image
# cv2.imshow("Original", img)
# cv2.imshow("Threshold", imgThreshold)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# find contours
imgContours = img.copy()  # Copy the image - all contours
imgBigContours = img.copy()  # Copy the image - biggest contour
contours, hierarchy = cv2.findContours(
    imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find all contours - external
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)  # Draw all contours

# cv2.imshow("Contours", imgContours)

# find biggest contour
biggestContourPoints, maxArea = findBiggestContour(contours)
print("biggest contour", biggestContourPoints)

if biggestContourPoints.size != 0:
    biggestContourPoints = reoderPoints(biggestContourPoints)
    print("reordered contour", biggestContourPoints)

    # draw biggest contour
    cv2.drawContours(imgBigContours, biggestContourPoints, -1, (0, 0, 255), 25)
    cv2.imshow("Biggest Contour", imgBigContours)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # get sudoku using warp perspective
    sourcePoints = np.float32(biggestContourPoints)
    destinationPoints = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
    transformMatrix = cv2.getPerspectiveTransform(sourcePoints, destinationPoints)
    imgWarpColored = cv2.warpPerspective(img, transformMatrix, (imgWidth, imgHeight))
    imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Warp", imgWarpColored)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # split image and find digits
    imgSolvedDigits = blankImg.copy()
    boxes = splitImgToBoxes(imgWarpColored, boxSize)

    # # show boxes
    # image: ndarray[Any, dtype[generic | generic | Any]]
    # for image in boxes:
    #     if image is not None and image.size != 0:
    #         cv2.imshow("box", image)
    #         cv2.waitKey(0)
    #     else:
    #         print("Empty or invalid image detected.")
    # cv2.destroyAllWindows()

    # print(len(boxes))
    # cv.imshow("Sample Box", boxes[0])

    sudoku_list = predict_digits_tesseract(boxes)
    print(sudoku_list)

    input_path = list_to_file(sudoku_list, boxSize)
    input_path = 'sudoku_puzzle.txt'
    # input_path = '../Sudoku Sample Puzzles/Sample Inputs/input_hex1.txt'

    if boxSize == 9:
        # Initialize an empty 2D array for the Sudoku puzzle
        sudoku_puzzle = []

        # Read the text file and convert it into a 2D array
        with open(input_path, 'r') as f:
            for line in f:
                # Split each line into individual values and convert them to integers
                row = [int(x) for x in line.strip().split()]
                sudoku_puzzle.append(row)

        if solve_sudoku_9x9(sudoku_puzzle):
            # Print the solved Sudoku puzzle
            for row in sudoku_puzzle:
                print(row)
        else:
            print("No solution exists for the given Sudoku puzzle.")
    elif boxSize == 16:
        if solve_sudoku_16x16(input_path):
            print("Sudoku solved!")
        else:
            print("No solution exists for the given Sudoku puzzle.")

    # imgDetectedDigits = blankImg.copy()
    # imgDetectedDigits = displayDigitsOnImg(imgDetectedDigits, detectedDigits, color=(255, 0, 255))
    #
    # detectedDigits = np.array(detectedDigits)
    # posArray = np.where(detectedDigits > 0, 0, 1)
    # print("posArray :", posArray)
    #
    # puzzleLines = [' '.join(map(str, detectedDigits[i:i + 9]))
    #                for i in range(0, len(detectedDigits), 9)]

    # # print(puzzleLines)
    # print("----solving sudoku----")
    # try:
    #     solvedSudoku = sudokuSolver.sudokuSolver(puzzleLines)
    # except:
    #     print("Error in solving sudoku")
    #     pass
    #
    # print("solved", solvedSudoku)
    #
    # # convert to flat list
    # flatList = []
    # for sublist in solvedSudoku:
    #     for item in sublist:
    #         flatList.append(int(item))
    #
    # print("flat", flatList)
    #
    # # display solved digits
    # # make puzzle values 0
    # solvedDigits = flatList * posArray
    # imgSolvedDigits = displayDigitsOnImg(
    #     imgSolvedDigits, solvedDigits, color=(0, 255, 0))
    #
    # # overlay solved digits onto original image
    # bigContourPts = np.float32(biggestContourPoints)
    # puzzleConers = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
    # # create perspective transform matrix
    # transformMatrix = cv2.getPerspectiveTransform(puzzleConers, bigContourPts)
    #
    # imgInvWarpColored = img.copy()
    # imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, transformMatrix, (imgWidth, imgHeight))
    #
    # solutionBlendedImg = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
    #
    # imgDetectedDigits = drawSudokuGrid(imgDetectedDigits)
    # imgSolvedDigits = drawSudokuGrid(imgSolvedDigits)
    #
    # # stack images
    # imgArray = ([img, imgThreshold, imgContours],
    #             [imgBigContours, imgWarpColored, imgDetectedDigits],
    #             [imgSolvedDigits, imgInvWarpColored, solutionBlendedImg])
    # stackedImg = stackImages(imgArray, 0.5)
    # cv2.imshow("Stacked Images", stackedImg)

else:
    print("No sudoku found")

cv2.waitKey(0)
