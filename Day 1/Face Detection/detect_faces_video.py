# Import necessary packages 
import numpy as np 
import cv2 
import argparse 
from imutils.video import VideoStream 
import imutils
import time 

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--prototxt", required = True, help = "path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required = True, help = "path to predefined Caffe Model" )
ap.add_argument("-c", "--confidence", type = float, default = 0.5, help = "minimum probability to filter weak detections")

args = vars(ap.parse_args())

# Load the serialized model from disk 
print("[INFO]Loading Model....")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Initialize the video stream and allow the camera sensor to warm up 
print("[INFO]Starting Video Stream....")
# This would be laptop's built in camera or desktop's first camera detected
'''If we want to parse a video file rather than a video stream
 swap out the VideoStream class for VideoFileStream '''
vs = VideoStream(src = 0).start()
# Allowing the camera sensor to warm up for 2 secs 
time.sleep(2.0)

# Loop over the frames from the video stream 
while True: 
	# Grab the frame from the threaded video stream and resize it to have a minumum of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width = 400)

	# Grab the frame dimensions 
	(h, w) = frame.shape[:2]
	# Converting the frame to a blob 
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

	# Pass the blob through the network and pass the detections and predictions
	net.setInput(blob)
	detections = net.forward()

	# Loop over the detections 
	for i in range (0, detections.shape[2]):
		# Calculate the confidence 
		confidence = detections[0, 0, i, 2]
		# Filter out weak detections by ensuring confidence is greater than the threshold confidence 
		if confidence > args["confidence"]:
			# Compute (x, y) co-ordinates of the bounding box for the object 
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# Draw bounding box of the face along with associated probability
			text = "{:.2f}%".format(confidence * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	# Show the output frame 
	cv2.imshow("Frame", frame)
	# Display the frame and wait for a key press 
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"): 
		break


# Do a bit of cleanup 
# Destroys all the windows created
cv2.destroyAllWindows()
vs.stop()




