# Import the necessary packages 
from imutils import face_utils 
import imutils 
import cv2
import numpy as np 
import argparse 
import cv2 
import dlib

# Construct the argument parser and parse the arguments 
ap = argparse.ArgumentParser() 
ap.add_argument("-p", "--shape_predictor", required = True, help = "path to facial landmark predictor")
ap.add_argument("-i", "--image", required = True, help = "path to input image")
args = vars(ap.parse_args())

# Initialize dlib's face detector and then create the facial landmark predictor 
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Now, we need to detect the faces 
# Load the input image, resize it and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width = 500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the gray scale image
rects = detector(gray, 1)

# Now, we need to predict the landmarks in all the detected faces 
# Loop over all the detected faces 
for (i, rects) in enumerate(rects): 
	# Predict the landmarks in the face using dlib's predictor 
	shape = predictor(gray, rects)
	shape = face_utils.shape_to_np(shape)

	# Draw the bounding box around the face 
	(x, y, w, h) = face_utils.rect_to_bb(rects)
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# Show the face number 
	cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

	# Loop over the (x, y) co-ordinates for the facial landmarks and draw them on the image
	for (x, y) in shape: 
		cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

# Show the output image 
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()