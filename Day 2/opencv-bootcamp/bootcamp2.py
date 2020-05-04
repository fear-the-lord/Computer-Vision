# Import necessary packages 

import cv2
import imutils
import argparse 

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required = True, help = "Path to the input image")

args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original Image", image)
cv2.waitKey(0)

# Convert an image to gray scale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# Detect edges of an image 
edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Threshold the image by setting all pixel values less than 225
# to 255 (white; foreground) and all pixel values >= 225 to 255
# (black; background), thereby segmenting the image.
threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_TOZERO_INV)[1]
cv2.imshow("Threshed", threshold)
cv2.waitKey(0)

# Detecting and drawing contours 
# Find contours (i.e., outlines) of the foreground objects in the
# thresholded image
cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

# Loop over the contours 
for i in cnts: 
	# Draw each contour on the output image with a 3px thick purple
	# outline, then display the output contours one at a time. 
	# We take original copy of the image to draw contours on the subsequent. 
	cv2.drawContours(output, [i], -1, (240, 0, 159), 3)
	cv2.imshow("Contours", output)
	cv2.waitKey(0)

# Draw the total number of contours found in purple
text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
	(240, 0, 159), 2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

# We apply erosions to reduce the size of foreground objects
mask = threshold.copy()
mask = cv2.erode(mask, None, iterations = 5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

# Similarly, dilations can increase the size of the ground object
mask = threshold.copy()
mask = cv2.dilate(mask, None, iterations=5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)

# A typical operation we may want to apply is to take our mask and
# apply a bitwise AND to our input image, keeping only the masked
# regions
mask = threshold.copy()
output = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Output", output)
cv2.waitKey(0)