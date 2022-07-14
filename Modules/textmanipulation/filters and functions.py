import os
import re
import argparse
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
import fitz
from io import BytesIO
from PIL import Image
import pandas as pd
import filetype

# Path Of The Tesseract OCR engine
TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
# Include tesseract executable
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


#-----------filters-----------------
# Image Pre-Processing Functions to improve output accurracy
# Convert to grayscale
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Remove noise
def remove_noise(img):
    return cv2.medianBlur(img, 5)
# Thresholding
def threshold(img):
    # return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# dilation
def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)
# erosion
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)
# opening -- erosion followed by a dilation
def opening(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
# canny edge detection
def canny(img):
    return cv2.Canny(img, 100, 200)
# skew correction
def deskew(img):
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
# template matching
def match_template(img, template):
    return cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
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

def display_img(title, img):
    """Displays an image on screen and maintains the output until the user presses a key"""
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.setWindowTitle('img', title)
    cv2.resizeWindow('img', 1200, 900)
    # Display Image on screen
    cv2.imshow('img', img)
    # Mantain output until user presses a key
    cv2.waitKey(0)
    # Destroy windows when user presses a key
    cv2.destroyAllWindows()


def generate_ss_text(ss_details):
    """Loops through the captured text of an image and arranges this text line by line.
    This function depends on the image layout."""
    # Arrange the captured text after scanning the page
    parse_text = []
    word_list = []
    last_word = ''
    # Loop through the captured text of the entire page
    for word in ss_details['text']:
        # If the word captured is not empty
        if word != '':
            # Add it to the line word list
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == ss_details['text'][-1]):
            parse_text.append(word_list)
            word_list = []
    return parse_text


def search_for_text(ss_details, search_str):
    """Search for the search string within the image content"""
    # Find all matches within one page
    results = re.findall(search_str, ss_details['text'], re.IGNORECASE)
    # In case multiple matches within one page
    for result in results:
        yield result

def save_page_content(pdfContent, page_id, page_data):
    """Appends the content of a scanned page, line by line, to a pandas DataFrame."""
    if page_data:
        for idx, line in enumerate(page_data, 1):
            line = ' '.join(line)
            pdfContent = pdfContent.append(
                {'page': page_id, 'line_id': idx, 'line': line}, ignore_index=True
            )
    return pdfContent


def ocr_img(
        img: np.array, input_file: str, search_str: str, 
        highlight_readable_text: bool = False, action: str = 'Highlight', 
        show_comparison: bool = False, generate_output: bool = True):
    """Scans an image buffer or an image file.
    Pre-processes the image.
    Calls the Tesseract engine with pre-defined parameters.
    Calculates the confidence score of the image grabbed content.
    Draws a green rectangle around readable text items having a confidence score > 30.
    Searches for a specific text.
    Highlight or redact found matches of the searched text.
    Displays a window showing readable text fields or the highlighted or redacted text.
    Generates the text content of the image.
    Prints a summary to the console."""
    # If image source file is inputted as a parameter
    if input_file:
        # Reading image using opencv
        img = cv2.imread(input_file)
    # Preserve a copy of this image for comparison purposes
    initial_img = img.copy()
    highlighted_img = img.copy()
    # Convert image to binary
    bin_img = convert_img2bin(img)
    # Calling Tesseract
    # Tesseract Configuration parameters
    # oem --> OCR engine mode = 3 >> Legacy + LSTM mode only (LSTM neutral net mode works the best)
    # psm --> page segmentation mode = 6 >> Assume as single uniform block of text (How a page of text can be analyzed)
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
        # Consider only text fields with confidence score > 30 (text is readable)
        # Searches for the string
        if search_str:
            results = re.findall(
                search_str, details['text'][seq], re.IGNORECASE)
            for result in results:
                ss_matches += 1
                if action:
                    # Draw a red rectangle around the searchable text
                    (x, y, w, h) = (details['left'][seq], details['top']
                                    [seq], details['width'][seq], details['height'][seq])
                    # Details of the rectangle
                    # Starting coordinate representing the top left corner of the rectangle
                    start_point = (x, y)
                    # Ending coordinate representing the botton right corner of the rectangle
                    end_point = (x + w, y + h)
                    #Color in BGR -- Blue, Green, Red
                    if action == "Highlight":
                        color = (0, 255, 255)  # Yellow
                    elif action == "Redact":
                        color = (0, 0, 0)  # Black
                    # Thickness in px (-1 will fill the entire shape)
                    thickness = -1
                    boxed_img = cv2.rectangle(
                        img, start_point, end_point, color, thickness)
                            
    if highlight_readable_text and not (ss_matches > 0 and action=="Highlight"):
        highlighted_img = boxed_img.copy()
    # Highlight found matches of the search string
    if ss_matches > 0 and action == "Highlight":
        cv2.addWeighted(boxed_img, 0.4, highlighted_img,
                        1 - 0.4, 0, highlighted_img)
    # save the image
    cv2.imwrite("highlighted-text-image.jpg", highlighted_img)  
    # Displays window showing readable text fields or the highlighted or redacted data
    if show_comparison and (highlight_readable_text or action):
        title = input_file if input_file else 'Compare'
        conc_img = cv2.hconcat([initial_img, highlighted_img])
        display_img(title, conc_img)
    # Generates the text content of the image
    output_data = None
    if generate_output and details:
        output_data = generate_ss_text(details)
    # Prints a summary to the console
    if input_file:
        summary = {
            "File": input_file, "Total matches": ss_matches,
        }
        # Printing Summary
        print("## Summary ########################################################")
        print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
        print("###################################################################")
    return highlighted_img, ss_matches, output_data
    
input_image=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/textmanipulation/image2.png"
ls=ocr_img(img=np.array, input_file=input_image, search_str="best", 
        highlight_readable_text= False, action='Highlight', 
        show_comparison= False, generate_output= True)
print(ls)