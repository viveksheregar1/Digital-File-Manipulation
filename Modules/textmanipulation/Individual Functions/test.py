import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd =r"C:/Program Files/Tesseract-OCR/tesseract.exe"

coordinates = [] 
  
# Defining the event listener (callback function)
  
  
# load the image, clone it, and setup the mouse callback function 
def fun():
    input_img=cv2.imread(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/textmanipulation/image4.jpg")
    img_rotated =input_img
    image = img_rotated
    image_copy = image.copy()
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
            cv2.imshow("image", image) 
    
    cv2.namedWindow("image") 
    cv2.setMouseCallback("image", shape_selection) 

    
    
    
    # keep looping until the 'q' key is pressed 
    while True: 
        # display the image and wait for a keypress 
        cv2.imshow("image", image) 
        key = cv2.waitKey(1) & 0xFF
    
        if key==13: # If 'enter' is pressed, apply OCR
            break
        
        if key == ord("c"): # Clear the selection when 'c' is pressed 
            image = image_copy.copy() 

    if len(coordinates) == 2: 
        image_roi = image_copy[coordinates[0][1]:coordinates[1][1], 
                                coordinates[0][0]:coordinates[1][0]] 
        cv2.waitKey(0) 
        # closing all open windows 
        cv2.destroyAllWindows()
    ##################################################################### OPTICAL CHARACTER RECOGNITION (OCR) ON ROI
    text = pytesseract.image_to_string(image_roi)
    print("The text in the selected region is as follows:")
    print(text)

fun()