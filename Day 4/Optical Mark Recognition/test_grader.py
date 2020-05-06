import cv2
import imutils 
import argparse 
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np

# Construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to an input image")
args = vars(ap.parse_args())

# Define the answer key that maps the question number to the correct answer 
answer = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

# Read the image from the memory 
image = cv2.imread(args["image"])
copy = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5, 5), 0)
# Find edges in the image
edged = cv2.Canny(blurred, 75, 200)

cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Find the contours in the edges image
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# Sort the contours in descending order of their areas
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
# Initialize the contours with the largest area i.e the area of the paper
docContour = None

# Loop over the contours
for c in cnts: 
	# Find the perimeter of the contour 
	peri = cv2.arcLength(c, True)
	# Approximate the no:of points on the contour
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# If our approximated contour has 4 points then we know that we have found our piece of paper 
	if len(approx) == 4:
		docContour = approx
		break

# Draw the countour around the piece of paper 
cv2.drawContours(image, [docContour], -1, (0, 255, 0), 2)
cv2.imshow("Contoured",image)
cv2.waitKey(0)

# Apply four point perspective transform to both the original as well as the gray scale image 
# to obtain a top-down birds eye view of the paper. 
warped_paper = four_point_transform(image, docContour.reshape(4, 2))
cv2.imshow("Warped Paper", warped_paper)
cv2.waitKey(0)
warped_paper_copy = warped_paper.copy()

warped_gray = four_point_transform(gray, docContour.reshape(4, 2))
cv2.imshow("Warped Gray", warped_gray)
cv2.waitKey(0)

# Apply Otsu's Thresholding to binarize the gray scale image 
threshed = cv2.threshold(warped_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow("Threshed", threshed)
cv2.waitKey(0)

# Find the contours in the thresholded image
cnts = cv2.findContours(threshed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# Initialize the contours that correspond to the questions
qstnContours = []
warped_gray_copy = warped_gray.copy()

for c in cnts: 
	# Compute the bounding box of the contours, then according to the bounding box compute the aspect ratio
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)
	'''In order to label the contour as a question, the bounding box should be 
	sufficiently tall, sufficiently wide and should have an aspect ratio 
	approximately equal to 1'''
	if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
		qstnContours.append(c)
	cv2.drawContours(warped_paper, qstnContours, -1, (255, 0, 0), 2)

cv2.imshow("Question Contours", warped_paper)
cv2.waitKey(0)

# Sort the qstnContours top-to-bottom
qstnContours = contours.sort_contours(qstnContours, method = "top-to-bottom")[0]
# Then initialize the counter corresponding to the total no:of correct answers 
correct = 0

# Each question has 5 possible answers, so loop over the questions in batch of 5
for (q, i) in enumerate(np.arange(0, len(qstnContours), 5)):
	cnts = contours.sort_contours(qstnContours[i : i + 5])[0]
	bubbled = None
	# Loop over the sorted contours
	for (j, c) in enumerate(cnts):
		# Construct a mask that reveals only the current "bubble" for the question 
		mask = np.zeros(threshed.shape, dtype = "uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		# Apply mask to the thresholded image, then count the no:of zero pixels in the bubble area 
		mask = cv2.bitwise_and(threshed, threshed, mask = mask)
		total = cv2.countNonZero(mask)
		# If the current total has a larger number of total
		# non-zero pixels, then we are examining the currently
		# bubbled-in answer
		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)
	# Initialize the contour color and the index of the
	# *correct* answer
	color = (0, 0, 255)
	k = answer[q]
	# Check to see if the bubbled answer is correct
	if k == bubbled[1]:
		color = (0, 255, 0)
		correct += 1
	# Draw the outline of the correct answer on the test
	cv2.drawContours(warped_paper_copy, [cnts[k]], -1, color, 3)

score = (correct / 5.0) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(warped_paper_copy, "{:.2f}%".format(score), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", copy)
cv2.imshow("Exam", warped_paper_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
