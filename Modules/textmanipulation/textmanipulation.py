#last updates : 13/07/2022
import os
import re
import math
from cv2 import WINDOW_NORMAL
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from deskew import determine_skew #pip install deskew

""" 
    this module has 3 functions that can be used to convert
    
    image file to a text file
        image_to_text(input_file:str,output_file:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    
    highlighting a given text in the image
        highlighting_text(input_file: str,output_file:str,search_str: str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    
    extracting text from a selected region
        text_from_region_of_interest(input_file:str,output_file:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}

"""
#pytesseractpath
pytesseract.pytesseract.tesseract_cmd =r"C:/Program Files/Tesseract-OCR/tesseract.exe"

#-----------filters-----------------
class Filters:
    """
        this class contains all the filters used for preprocessing to enhance the output
    """
# Increase contrast
    def contrast(self,img):
        self.contrast_image = cv2.normalize(img, None, alpha=0, beta=1.2, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.contrast_image = np.clip(self.contrast_image, 0, 1)
        self.contrast_image = (255*self.contrast_image).astype(np.uint8)
        return self.contrast_image
        
    # Convert to grayscale
    def grayscale(self,img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #dilation
    def dilation(self,img,kernel):
        return cv2.dilate(img, kernel, iterations = 1)

    #rotate the image 
    def rotate(self,img):
        """
        checks if the image is aligned correclty or not
        """
        self.gray_image = self.grayscale(img)
        self.angle = determine_skew(self.gray_image)
        self.background=(0,0,0)
        self.old_width, self.old_height = img.shape[:2]
        self.angle_radian = math.radians(self.angle)
        self.width = abs(np.sin(self.angle_radian) * self.old_height) + abs(np.cos(self.angle_radian) * self.old_width)
        self.height = abs(np.sin(self.angle_radian) * self.old_width) + abs(np.cos(self.angle_radian) * self.old_height)

        self.image_center = tuple(np.array(img.shape[1::-1]) / 2)
        self.rot_mat = cv2.getRotationMatrix2D(self.image_center, self.angle, 1.0)
        self.rot_mat[1, 2] += (self.width - self.old_width) / 2
        self.rot_mat[0, 2] += (self.height - self.old_height) / 2
        self.rotated= cv2.warpAffine(img, self.rot_mat, (int(round(self.height)), int(round(self.width))), borderValue=self.background)
        return self.rotated
        
    #converts image to binary image
    def convert_img2bin(self,img):
        """
        Pre-processes the image and generates a binary output
        """
        # Convert the image into a grayscale image
        self.output_img = self.grayscale(img)
        # Invert the grayscale image by flipping pixel values.
        # All pixels that are grater than 0 are set to 0 and all pixels that are = to 0 are set to 255
        self.output_img = cv2.bitwise_not(self.output_img)
        # Converting image to binary by Thresholding in order to show a clear separation between white and blacl pixels.
        #output_img = threshold(output_img)
        self.output_img=cv2.threshold(self.output_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return self.output_img

#not used anywhere

    #increase sharpness
    # def sharp(self,img):
    #     self.kernel = np.array([[0, -1, 0],
    #                 [-1, 5,-1],
    #                 [0, -1, 0]])
    #     self.sharp_image = cv2.filter2D(src=img, ddepth=-1, kernel=self.kernel)
    #     return self.sharp_image
    
    # Thresholding
    #def threshold(img,type):
            #return cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
            #return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#-------------filters end--------------------------

#custom exception
class DataNotFound(Exception):
    error_data="no text found on the image or the image is too blur to read..!"

class CustomError(Exception):
    pass

#------function 1----------
def image_to_text(input_file:str,output_file:str):
    """
        this functions extracts the text in the given image
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    # Read image from which text needs to be extracted
    try:
        img = cv2.imread(input_file)
        #filters class object
        filters=Filters()
        # Preprocessing the image starts
        img=filters.rotate(img)
        gray_image = filters.grayscale(img)
        gray_image=filters.contrast(gray_image)
        ret,image_threshold=cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        #image_threshold = threshold(gray_image)
        
        # Specify structure shape and kernel size.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        # Applying dilation on the threshold image
        dilation_image =filters.dilation(image_threshold,kernel) 

        # Finding contours
        contours,hierarchy= cv2.findContours(dilation_image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        # Creating a copy of image
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Cropping the text block for giving input to OCR
            cropped = img[y:y + h, x:x + w]
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            #writing data on text file
            if text=="":
                raise DataNotFound
            with open(output_file,"w")as txt_file:
                txt_file.write(text)
                txt_file.write("\n")
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except DataNotFound as e:
        #removing output file if an error occurs
        os.remove(output_file)
        #writing error
        return_data['error']=e.error_data
    except Exception as e:
        #writing error
        #removing output file if an error occurs
        os.remove(output_file)
        return_data['error']=e  
    return return_data   



#------function 2----------
def highlighting_text(input_file: str,output_file:str,search_str: str):
    """
        this functions can be used to highlight text specified by the user
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        filters=Filters()
        #reading image file
        img = cv2.imread(input_file) 
        #copy the original image
        highlighted_img = img.copy()
        #preprocessing
        img=filters.rotate(img)
        img=filters.contrast(img)
        # Convert image to binary
        bin_img = filters.convert_img2bin(img)
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
        else:
            return_data['error']="no data found"
            raise CustomError
        # save the image
        cv2.imwrite(output_file, highlighted_img)  
        # cv2.imshow("image",highlighted_img)
        # cv2.waitKey(0)  
        # cv2.destroyAllWindows() 
        #storing output in dictionary
        if(return_data["error"]==""):
            return_data['output']="done"
            return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing output file if an error occurs
        os.remove(output_file)
    except Exception as e:
        #removing output file if an error occurs
        os.remove(output_file)
        #writing error
        return_data['error']=e  
    return return_data   

        

#------function 3----------  
# initializing the list for storing the coordinates
#it must be global so that i can use it inside the child function
coordinates = []   
enter_pressed=False
def text_from_region_of_interest(input_file:str,output_file:str):
    """
        this function lets the user select a region on the image and extracts text from that image
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try: 
        # Defining the event listener (callback function)
        def shape_selection(event, x, y, flags, param): 
            # making coordinates global
            global coordinates 
            # Storing the (x1,y1) coordinates when left mouse button is pressed  
            if event == cv2.EVENT_LBUTTONDOWN: 
                coordinates = [(x, y)] 
            # Storing the (x2,y2) coordinates when the left mouse button is released and make a rectangle on the selected region
            elif event == cv2.EVENT_LBUTTONUP: 
                coordinates.append((x, y)) 
                # Drawing a rectangle around the region of interest (roi)
                cv2.rectangle(image, coordinates[0], coordinates[1], (0,0,255), 2) 
                cv2.imshow("select region", image) 


        # load the image, clone it, and setup the mouse callback function 
        filters=Filters()
        #reading the image
        image = cv2.imread(input_file) 
        image_copy = image.copy()
        #creating a named window to track the mouse events
        cv2.namedWindow("select region",WINDOW_NORMAL) 
        cv2.setMouseCallback("select region", shape_selection) 
        # keep looping until the 'q' key is pressed
        
        while True: 
            # display the image and wait for a keypress 
            if cv2.getWindowProperty('select region', cv2.WND_PROP_VISIBLE)==0.0:
                cv2.destroyAllWindows()
                break
            else:
                cv2.imshow("select region", image)
            #reading the keypress
            key = cv2.waitKey(1) & 0xFF
            # If 'enter' is pressed, apply OCR
            if key==13: #enter key
                global enter_pressed
                enter_pressed=True
                break
            elif key == 27: #esc key
                cv2.destroyAllWindows()
                break     

            # Clear the selection when 'c' is pressed
            if key == ord("c"):  
                image = image_copy.copy()      
        #creating an image of captured coordinate
        if len(coordinates) == 2 and enter_pressed==True: 
            image_roi = image_copy[coordinates[0][1]:coordinates[1][1], 
                                    coordinates[0][0]:coordinates[1][0]] 
            # closing all open windows 
            cv2.destroyAllWindows()
        else:
            raise CustomError
        #OPTICAL CHARACTER RECOGNITION (OCR) ON ROI
        text = pytesseract.image_to_string(image_roi)
        if text=="":
            raise DataNotFound
        #writing the text on text file
        with open(output_file,"w")as txt_file:
                txt_file.write("The text in the selected region is as follows:\n")
                txt_file.write(text)
                txt_file.write("\n")
        #print("The text in the selected region is as follows:")
        #print(text)
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing output file if an error occurs
        os.remove(output_file)
        return_data['error']="No region was selected and the image was closed..!"
    except DataNotFound as e:
        #removing output file if an error occurs
        os.remove(output_file)
        return_data['error']="No data found in the selected region"
    except Exception as e:
        #removing output file if an error occurs
        os.remove(output_file)
        #writing error
        return_data['error']=e 
    return return_data   

#input_image=r"C:/Users/vivek/OneDrive/Pictures/Saved Pictures/minions.jpg"
#input_image=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/textmanipulation/image6.jpg"
#output_image=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/textmanipulation/output.png"
#print(highlighting_text(input_image,output_image,"your"))