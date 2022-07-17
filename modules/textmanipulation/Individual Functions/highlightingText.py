import re
import pytesseract
from pytesseract import Output
import cv2
import numpy as np

# Path Of The Tesseract OCR engine
# Include tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

#-----------filters-----------------
# Convert to grayscale
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Thresholding
def threshold(img):
    # return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# skew correction
def deskew(img1):
    img=np.asarray(img1)
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated
#converts image to binary image
def convert_img2bin(img):
    """
    Pre-processes the image and generates a binary output
    """
    # Convert the image into a grayscale image
    output_img = grayscale(img)
    # Invert the grayscale image by flipping pixel values.
    # All pixels that are grater than 0 are set to 0 and all pixels that are = to 0 are set to 255
    output_img = cv2.bitwise_not(output_img)
    # Converting image to binary by Thresholding in order to show a clear separation between white and blacl pixels.
    output_img = threshold(output_img)
    return output_img
#-------------filters end--------------------------

def highlighting_text(input_file: str, search_str: str):
    img = cv2.imread(input_file) 
    #copy the original image
    highlighted_img = img.copy()
    # Convert image to binary
    bin_img = convert_img2bin(img)
    # Tesseract Configuration parameters
    # oem --> OCR engine mode = 3 
    # psm --> page segmentation mode = 6
    config_param = r'--oem 3 --psm 6'
    # Feeding image to tesseract
    details = pytesseract.image_to_data(
        bin_img, output_type=Output.DICT, config=config_param, lang='eng')
    # The details dictionary contains the information of the input image
    # such as detected text, region, position, information, height, width, confidence score.
    boxed_img = None
    # Total matches found
    ss_matches = 0
    for seq in range(len(details['text'])):
        # Searches for the string
        results = re.findall(search_str, details['text'][seq], re.IGNORECASE)
        for result in results:
            ss_matches += 1
            # Details of the rectangle
            (x, y, w, h) = (details['left'][seq], details['top']
                            [seq], details['width'][seq], details['height'][seq])
            # Starting coordinate representing the top left corner of the rectangle
            start_point = (x, y)
            # Ending coordinate representing the botton right corner of the rectangle
            end_point = (x + w, y + h)
            #Color in BGR -- Blue, Green, Red
            color = (0, 255, 255)  # Yellow
            # Thickness in px (-1 will fill the entire shape)
            thickness = -1
            boxed_img = cv2.rectangle(img, start_point, end_point, color, thickness)                            
    # Highlight found matches of the search string
    if ss_matches > 0:
        cv2.addWeighted(boxed_img, 0.4, highlighted_img,
                        1 - 0.4, 0, highlighted_img)
    # save the image
    cv2.imwrite("highlighted-text-image.png", highlighted_img)  
    cv2.imshow("image",highlighted_img)
    cv2.waitKey(0)  
    cv2.destroyAllWindows() 
    print(details['text'])
    
input_image=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/textmanipulation/image4.jpg"
highlighting_text(input_file=input_image, search_str="best")