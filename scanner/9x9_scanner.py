import cv2
import numpy as np

from scanner.cham_utils import reoderPoints, findBiggestContour, preProcessImg, splitImgToBoxes

# imgPath = "../sudoku_images/1.jpg"
# imgHeight = 450
# imgWidth = 450
# boxSize = 9

# imgPath = "../sudoku_images/2.jpg"
imgPath = "../generate_images/skewed_vertical.jpg"
imgHeight = 480
imgWidth = 480
boxSize = 16

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

    # show boxes
    for image in boxes:
        cv2.imshow("box", image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # print(len(boxes))
    # # cv.imshow("Sample Box", boxes[0])
    # print("----predicting digits----")
    # detectedDigits = predictDigits(boxes, digitsClassModel)
    # print(detectedDigits)
    # imgDetectedDigits = blankImg.copy()
    # imgDetectedDigits = displayDigitsOnImg(
    #     imgDetectedDigits, detectedDigits, color=(255, 0, 255))
    #
    # detectedDigits = np.array(detectedDigits)
    # posArray = np.where(detectedDigits > 0, 0, 1)
    # print("posArray :", posArray)
    #
    # puzzleLines = [' '.join(map(str, detectedDigits[i:i + 9]))
    #                for i in range(0, len(detectedDigits), 9)]
    #
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
    # puzzleConers = np.float32(
    #     [[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
    # # create perspective transform matrix
    # transformMatrix = cv.getPerspectiveTransform(puzzleConers, bigContourPts)
    #
    # imgInvWarpColored = img.copy()
    # imgInvWarpColored = cv.warpPerspective(
    #     imgSolvedDigits, transformMatrix, (imgWidth, imgHeight))
    #
    # solutionBlendedImg = cv.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
    #
    # imgDetectedDigits = drawSudokuGrid(imgDetectedDigits)
    # imgSolvedDigits = drawSudokuGrid(imgSolvedDigits)
    #
    # # stack images
    # imgArray = ([img, imgThreshold, imgContours],
    #             [imgBigContours, imgWarpColored, imgDetectedDigits],
    #             [imgSolvedDigits, imgInvWarpColored, solutionBlendedImg])
    # stackedImg = stackImages(imgArray, 0.5)
    # cv.imshow("Stacked Images", stackedImg)

else:
    print("No sudoku found")

cv2.waitKey(0)
