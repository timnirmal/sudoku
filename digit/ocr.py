import cv2
import pytesseract

# Configure Tesseract to recognize digits only
custom_config = r'--oem 3 --psm 6 outputbase digits'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def recognize_digit(img):
    # Check if the image is empty or invalid
    if img is None or img.size == 0:
        return "Empty Image"

    # Check the number of channels in the image
    if len(img.shape) == 2:
        # Image is already grayscale
        gray_img = img
    else:
        # Convert to grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # crop image to remove borders
    border_size = 8
    gray_img = gray_img[border_size:gray_img.shape[0] - border_size, border_size:gray_img.shape[1] - border_size]

    # # show image
    # cv2.imshow("Original", img)
    # cv2.imshow("Gray", gray_img)
    # cv2.waitKey(0)

    # Apply thresholding
    thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Configure Tesseract
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Extract text using Tesseract
    text = pytesseract.image_to_string(thresh_img, config=custom_config)

    return text.strip()

# # Test the function
# digit = recognize_digit('box.png')
# print(digit)