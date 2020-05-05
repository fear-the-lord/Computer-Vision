# Import the necessary packages 

import cv2 
import imutils 
import argparse
import numpy as np
from skimage.filters import threshold_local
from imutils.perspective import four_point_transform

# def order_points(pts):
# 	# initialzie a list of coordinates that will be ordered
# 	# such that the first entry in the list is the top-left,
# 	# the second entry is the top-right, the third is the
# 	# bottom-right, and the fourth is the bottom-left
# 	rect = np.zeros((4, 2), dtype = "float32")
# 	# the top-left point will have the smallest sum, whereas
# 	# the bottom-right point will have the largest sum
# 	s = pts.sum(axis = 1)
# 	rect[0] = pts[np.argmin(s)]
# 	rect[2] = pts[np.argmax(s)]
# 	# now, compute the difference between the points, the
# 	# top-right point will have the smallest difference,
# 	# whereas the bottom-left will have the largest difference
# 	diff = np.diff(pts, axis = 1)
# 	rect[1] = pts[np.argmin(diff)]
# 	rect[3] = pts[np.argmax(diff)]
# 	# return the ordered coordinates
# 	return rect

# def four_point_transform(image, pts):
# 	# obtain a consistent order of the points and unpack them
# 	# individually
# 	rect = order_points(pts)
# 	(tl, tr, br, bl) = rect
# 	# compute the width of the new image, which will be the
# 	# maximum distance between bottom-right and bottom-left
# 	# x-coordiates or the top-right and top-left x-coordinates
# 	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
# 	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
# 	maxWidth = max(int(widthA), int(widthB))
# 	# compute the height of the new image, which will be the
# 	# maximum distance between the top-right and bottom-right
# 	# y-coordinates or the top-left and bottom-left y-coordinates
# 	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
# 	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
# 	maxHeight = max(int(heightA), int(heightB))
# 	# now that we have the dimensions of the new image, construct
# 	# the set of destination points to obtain a "birds eye view",
# 	# (i.e. top-down view) of the image, again specifying points
# 	# in the top-left, top-right, bottom-right, and bottom-left
# 	# order
# 	dst = np.array([
# 		[0, 0],
# 		[maxWidth - 1, 0],
# 		[maxWidth - 1, maxHeight - 1],
# 		[0, maxHeight - 1]], dtype = "float32")
# 	# compute the perspective transform matrix and then apply it
# 	M = cv2.getPerspectiveTransform(rect, dst)
# 	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
# 	# return the warped image
# 	return warped

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required = True, help = "path to the input image")

args = vars(ap.parse_args())

# Input the image from the disk 
image = cv2.imread(args["image"])
# Make a copy of the image 
orig = image.copy()
image = imutils.resize(image, height = 500)
image = imutils.rotate_bound(image, -90)
cv2.imshow("Original",image)
cv2.waitKey(0)

# Convert the image to gray scale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Blur the image to reduce noise 
gray = cv2.GaussianBlur(gray, (5, 5), 0)
# Detect the edges of the image 
edged = cv2.Canny(gray, 75, 200)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Find the contours of the edged image
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# Sort the contours on descending order of their contour area and keep anly 5 of it 
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# Loop over the contours
for c in cnts: 
	# Approximate the contours 
	# Calculates the perimeter of the contours
	per = cv2.arcLength(c, True)
	# Approximate the no:of points on the contour
	approx = cv2.approxPolyDP(c, 0.02 * per, True)

	# If our approximated contour has 4 points then we can assume that we have found our screen
	if len(approx) == 4:
		screenContour = approx
		break 

cv2.drawContours(image, [screenContour], -1, (0, 255, 0), 2)
cv2.imshow("Contoured", image)
cv2.waitKey(0)

# Apply four-point transforms to obtain a top down view of the original image
(h, w) = orig.shape[:2]
ratio = h / 500.0
orig =  imutils.rotate_bound(orig, -90)
warped = four_point_transform(orig, screenContour.reshape(4, 2) * ratio)

# Convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# Compute a threshold mask image based on local pixel neighborhood
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255

warped = imutils.resize(warped, height = 600)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
