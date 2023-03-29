#last updates : 30/03/2023,1am
from os import remove,path
from re import findall,IGNORECASE
from math import radians
#pip install pytesseract
from pytesseract import Output ,pytesseract,image_to_string,image_to_data
from numpy import clip,uint8,cos,sin,array #pip install numpy
from deskew import determine_skew #pip install deskew
import cv2 #pip install opencv-python
from cv2 import WINDOW_NORMAL

""" 
    this module has 4 functions that can be used to convert
    
    image file to a text file
        image_to_text(input_file:str,output_file:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    
    highlighting a given text in the image
        highlighting_text(input_file: str,output_file:str,search_str: str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    
    extracting text from a selected region
        text_from_region_of_interest(input_file:str,output_file:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    
    face detection(puts squares around faces, if found)
        face_detection(input_file:str,output_file:str):
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
"""

#custom exception
class CustomError(Exception):
    error_data=""

#function to find file type
def file_type(input_file:str):    
    file_extension=path.splitext(input_file)
    return(file_extension[1].lower())

#function that returns the size of the file in MB
def filesize(input_file:str):
    return (path.getsize(input_file)/1048576)

#pytesseractpath
# pytesseract.tesseract_cmd =r"C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.tesseract_cmd='/tesseract.exe'
#-----------filters-----------------
class Filters:
    """
        this class contains all the filters used for preprocessing to enhance the output
    """
# Increase contrast
    def contrast(self,img):
        self.contrast_image = cv2.normalize(img, None, alpha=0, beta=1.2, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.contrast_image =  clip(self.contrast_image, 0, 1)
        self.contrast_image = (255*self.contrast_image).astype( uint8)
        return self.contrast_image
        
    # Convert to grayscale
    def grayscale(self,img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #rotate the image 
    def rotate(self,img):
        """
        checks if the image is aligned correclty or not
        """
        self.gray_image = self.grayscale(img)
        self.angle = determine_skew(self.gray_image)
        self.background=(0,0,0)
        self.old_width, self.old_height = img.shape[:2]
        self.angle_radian = radians(self.angle)
        self.width = abs( sin(self.angle_radian) * self.old_height) + abs( cos(self.angle_radian) * self.old_width)
        self.height = abs( sin(self.angle_radian) * self.old_width) + abs( cos(self.angle_radian) * self.old_height)

        self.image_center = tuple( array(img.shape[1::-1]) / 2)
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
#-------------filters end--------------------------


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
    try:
        #checking for correct file format
        input_file_types=[".jpeg",".jpg",".png",".webp",".svg",".raw",".xcf",".jpx",".tiff",".cr2",".bmp",".jxr",".psd",".ico",".heic",".dcm"]
        output_file_types=[".txt"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+" is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=5#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        image_file = cv2.imread(input_file)
        #filters class object
        filters=Filters()
        rotate=True
        #applying filters
        for i in range(2):
            if(rotate):
                img=filters.rotate(image_file)
            else:
                img=image_file
            img=filters.grayscale(img)
            img=filters.contrast(img)
            #passing image to tesseract ocr
            text = image_to_string(img)
            if text=="":
                rotate=False
            else:
                break
        #checking if there is any data
        if text=="":
            CustomError.error_data="no text found on the image or the image is too blur to read..!"
            raise CustomError
        #writing data on text file    
        with open(output_file,"w")as txt_file:
            txt_file.write(text)
            txt_file.write("\n")
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']= CustomError.error_data
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
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
        #checking for file extension
        input_file_types=[".jpeg",".jpg",".png",".webp",".svg",".raw",".xcf",".jpx",".tiff",".cr2",".bmp",".jxr",".psd",".ico",".heic",".dcm"]
        output_file_types=[".jpeg",".jpg",".png",".webp",".svg",".raw",".xcf",".jpx",".tiff",".cr2",".bmp",".jxr",".psd",".ico",".heic",".dcm"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+" is not supported..!"
            raise CustomError
        
        #cheking if the file is too big
        max_size=5#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        filters=Filters()
        #reading image file
        img = cv2.imread(input_file) 
        #copy the original image
        highlighted_img = img.copy()
        #preprocessing
        img=filters.contrast(img)
        # Convert image to binary
        bin_img = filters.convert_img2bin(img)
        # Tesseract Configuration parameters
        # oem --> OCR engine mode = 3 
        # psm --> page segmentation mode = 6
        config_param = r'--oem 3 --psm 6'
        # Feeding image to tesseract
        details = image_to_data(
            bin_img, output_type=Output.DICT, config=config_param, lang='eng')
        # The details dictionary contains the information of the input image
        # such as detected text, region, position, information, height, width, confidence score.
        boxed_img = None
        # Total matches found
        ss_matches = 0
        for seq in range(len(details['text'])):
            # Searches for the string
            results = findall(search_str, details['text'][seq], IGNORECASE)
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
            CustomError.error_data="no matching data found..!"
            raise CustomError
        # save the image
        cv2.imwrite(output_file, highlighted_img)  
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=CustomError.error_data
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
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
        #checking for correct file format
        input_file_types=[".jpeg",".jpg",".png",".webp",".svg",".raw",".xcf",".jpx",".tiff",".cr2",".bmp",".jxr",".psd",".ico",".heic",".dcm"]
        output_file_types=[".txt"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError
        
        #cheking if the file is too big
        max_size=5#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

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
                #destroy window if X(close) is pressed
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
            CustomError.error_data="No region was selected and the image was closed..!"
            raise CustomError
        #OPTICAL CHARACTER RECOGNITION (OCR) ON ROI
        text = image_to_string(image_roi)
        
        #checking if image has any data
        if text=="":
            CustomError.error_data="no text found on the selected region or the image is too blur to read..!"
            raise CustomError

        #writing the text on text file
        with open(output_file,"w")as txt_file:
                txt_file.write("The text in the selected region is as follows:\n")
                txt_file.write(text)
                txt_file.write("\n")
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=CustomError.error_data
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=e 
    return return_data   

#------function 4----------
def face_detection(input_file:str,output_file:str):
    """
        this functions will detect faces in a clean image and draws a square box around them
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for file extension
        input_file_types=[".jpeg",".jpg",".png",".webp",".svg",".raw",".xcf",".jpx",".tiff",".cr2",".bmp",".jxr",".psd",".ico",".heic",".dcm"]
        output_file_types=[".jpeg",".jpg",".png",".webp",".svg",".raw",".xcf",".jpx",".tiff",".cr2",".bmp",".jxr",".psd",".ico",".heic",".dcm"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+" is not supported..!"
            raise CustomError
        
        #cheking if the file is too big
        max_size=5#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier("./res/haarcascade_frontalface_default.xml")

        # Read the image
        image = cv2.imread(input_file)
        filters=Filters()
        gray_image=filters.grayscale(image)
        gray_image=filters.contrast(gray_image)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        # print("Found {0} faces!".format(len(faces)))
        if len(faces)!=0:
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 8)
            cv2.imwrite(output_file, image)
            return_data['output']="done"
            return_data['output_file']=output_file #path of saved file
        else:
            return_data['error']='no Faces found..!'
    except CustomError:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=CustomError.error_data
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=e  
    return return_data