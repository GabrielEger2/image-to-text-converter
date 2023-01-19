import cv2 as cv
import numpy as np
import pytesseract as tess
import re

tess.pytesseract.tesseract_cmd = r'C:\PYTESSERACT LOCATION.exe'


# Load Requirements
with open('requirements.txt') as f:
    requirements = f.readlines()

#importing and resizing the image, need to set a universal resize method for different papers sheet in the future

image = cv.imread("image.jpg")
w, h = image.shape[1], image.shape[0]
image = cv.resize(image, (827, 1170))
image_warp = image.copy()

# Apllying effects to find the canny and corners of papers

gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #turn image to gray
blurred_image = cv.GaussianBlur(gray_image, (5, 5), 1) #add blur
canny_image = cv.Canny(blurred_image, 190, 190) #trying to find the canny, this current value (190, 190) is not universal, but should work in the majority of the cases
contours, _ = cv.findContours(canny_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
countor_image = image.copy()
countor_image = cv.drawContours(countor_image, contours, -1, (255, 0, 255), 4)
corner_frame = image.copy()
max_area = 0
biggest_contour = []

for c in contours: #for to find all the edges of the opaper
    area = cv.contourArea(c)
    if area > 500:
        period = cv.arcLength(c, True)
        edges = cv.approxPolyDP(c, 0.02*period, True)
        if area > max_area and len(edges) == 4:
            biggest_contour = edges
            max_area = area

#drawing the edges of the paper with the drawRec func and resizing to a plain paper:

if len(biggest_contour) != 0:
    biggest_contour = biggest_contour.reshape((4, 2))
    new_biggest = np.zeros((4, 1, 2), dtype= np.int32)
    add = biggest_contour.sum(1)
    new_biggest[0] = biggest_contour[np.argmin(add)]
    new_biggest[3] = biggest_contour[np.argmax(add)]
    difference = np.diff(biggest_contour, axis = 1)
    new_biggest[1] = biggest_contour[np.argmin(difference)]
    new_biggest[2] = biggest_contour[np.argmax(difference)]
    corner_frame = cv.drawContours(corner_frame, new_biggest, -1, (255, 0, 255), 25)
    pts1 = np.float32(new_biggest)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    image_warp = cv.warpPerspective(image, matrix, (w, h))

#showing final image to user:
image_show = cv.resize(image_warp, (827, 1170))
cv.imshow('image', image_show)
cv.waitKey(0)

#converting image to text with pytesseract:

text = tess.image_to_string(image_warp)
united_text = text.replace("\n", "")
print(text)
medicine_text = text.replace("\n", "&")

#Filtering text with regular expression:

name = str(re.search(r'Name: (.*?)Age', united_text).group(1))
age = str(re.search(r'Age: (.*?)Address', united_text).group(1))
address = str(re.search(r'Address: (.*?)Date', united_text).group(1))
date = str(re.search(r'Date: (.*?)Rx', united_text).group(1))
medicine = str(re.search(r'Rx&&(.*?)Refill', medicine_text).group(1)).replace('&', ' ') #text manipulation with & in order to get the spaces in medicine
refill = str(re.search(r'(?<=Refill: )(.*)', united_text).group(1))


important_data = [name, age, address, date, medicine, refill]

for data in important_data:
    print(data)
