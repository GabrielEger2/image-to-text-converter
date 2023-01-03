import cv2 as cv
import numpy as np
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\PYTESSERCT LOCATION\tesseract.exe'

#This function is going to be useful to set the right canny in the GUI

def drawRec(biggestNew, mainFrame):
        cv.line(mainFrame, (biggestNew[0][0][0], biggestNew[0][0][1]), (biggestNew[1][0][0], biggestNew[1][0][1]), (0, 255, 0), 20)
        cv.line(mainFrame, (biggestNew[0][0][0], biggestNew[0][0][1]), (biggestNew[2][0][0], biggestNew[2][0][1]), (0, 255, 0), 20)
        cv.line(mainFrame, (biggestNew[3][0][0], biggestNew[3][0][1]), (biggestNew[2][0][0], biggestNew[2][0][1]), (0, 255, 0), 20)
        cv.line(mainFrame, (biggestNew[3][0][0], biggestNew[3][0][1]), (biggestNew[1][0][0], biggestNew[1][0][1]), (0, 255, 0), 20)

#importing and resizing the image, need to set a universal resize method for different papers sheet in the future

image = cv.imread("IMAGE_NAME.jpg")
w, h = 500, 700
image = cv.resize(image, (int(w * 2), int(h * 2)))
image_warp = image.copy()

# Apllying effects to find the canny and corners of papers

gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #turn image to gray
blurred_image = cv.GaussianBlur(gray_image, (5, 5), 1) #add blur
canny_image = cv.Canny(blurred_image, 190, 190) #trying to find the canny, this current value (190, 190) is not universal and will be set by the user with the drawRec func
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
    drawRec(new_biggest, corner_frame)
    corner_frame = cv.drawContours(corner_frame, new_biggest, -1, (255, 0, 255), 25)
    pts1 = np.float32(new_biggest)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    image_warp = cv.warpPerspective(image, matrix, (w, h))

#showing final image to user:

cv.imshow('image', image_warp)
cv.waitKey(0)

#converting image to text with pytesseract:

text = tess.image_to_string(image_warp)
print(text)