import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd =r"C:/Program Files/Tesseract-OCR/tesseract.exe"
# Read image from which text needs to be extracted
img = cv2.imread(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/textmanipulation/image4.jpg")

# Preprocessing the image starts
# Convert the image to gray scale
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = img.copy()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
	# Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]
	# Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
    with open("text.txt","w")as txt_file:
        txt_file.write(text)
        txt_file.write("\n")

