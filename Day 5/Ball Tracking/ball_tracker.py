# Import the necessary packages
import cv2
import argparse 
import imutils 
from imutils.video import VideoStream
import time 
from collections import deque
import numpy as np 


# Construct and then parse the arguements 

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the (optional) video file")
# A smaller queue will form a shorter tail, whereas a larger queue will form longer tails since more points are being tracked
ap.add_argument("-b", "--buffer", type = int, default = 1024, help = "max buffer size")
args = vars(ap.parse_args())

# Define the lower and upper boundaries of the object to be tracked in the HSV color space 
greenLower = (0, 89, 0)
greenUpper = (19, 255, 255)

# Now initialize the list of traced points 
pts = deque(maxlen = args["buffer"])

# If a video path is not supplied grab a reference to the webcam 
if not args.get("video", False):
	vs = VideoStream(src = 0).start()

# Otherwise grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"]) 

# Allow the camera or video file to warm up 
time.sleep(2.0)

# Keep Looping
while True: 
	# Grab the current video frame
	frame = vs.read()
	# Handle the frame from video capture or video stream
	frame = frame[1] if args.get("video", False) else frame

	# If we are viewing a video file and didn't grab a frame then we have reached the end of the video file 
	if frame is None: 
		break

	# Resize the frame, Blur it and convert it to the HSV Color space
	frame = imutils.resize(frame, width = 600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# Construct a mask for the object, then perform a series of dilations and erotions to 
	# remove any small blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations = 5)
	mask = cv2.dilate(mask, None, iterations = 5)

	# Now, conpute the contour of the ball and draw it in our frame
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# Initialize the current (x, y) center of the ball 
	center = None

	# Only proceed if atleast one contour was found 
	if len(cnts) > 0: 
		# Find the largest contour in the mask 
		c =  max(cnts, key = cv2.contourArea)
		# Use it to form the minimum enclosing circle and centroid 
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# Only proceed if the radius meets a minimum size
		if radius > 10: 
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# Update the points in the queue
	pts.appendleft(center)

	# Loop over the set of tracked points 
	for i in range(1, len(pts)):
		# If either of the tracked points are 'None', ignore them
		# Indicating that the ball was not successfully detected in that given frame 
		if pts[i - 1] is None or pts[i] is None:
			continue

		# Otherwise, compute the thickeness of the line and draw the connecting lines 
		thickeness = int(np.sqrt(args["buffer"] / float(i + 1)) * 3)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickeness)

	# Show the frame 
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# If the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# If we are not using a video file, stop the camera video stream 
if not args.get("video", False):
	vs.stop()

# Otherwise release the camera 
else:
	vs.release()

# A bit of cleanup 
cv2.destroyAllWindows()











