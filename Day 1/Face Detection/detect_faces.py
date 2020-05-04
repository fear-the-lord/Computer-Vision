# Import the necessary packages
import numpy as np
import argparse
import cv2 

# Construct the argument parser and parse the arguments 
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required = True, help = "path to input image")
ap.add_argument("-p", "--prototxt", required = True, help = "path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required = True, help = "path to pre-trained Caffe model")
# This is a default argument and we can overwrite the default value of 0.5 if we want
ap.add_argument("-c", "--confidence", type = float, default = 0.5, help = "minimum probability to filter weak detections")

args = vars(ap.parse_args())

# Load our serialized model from disk
print("[INFO]Loading Model....")
# We load our model using "--prototxt" and "--model" file paths and store the model in net
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# We now load the image using "--image" path 
image = cv2.imread(args["image"])
# Extract the dimensions of the image 
(h, w) = image.shape[:2]
# Resize the image to (300, 300)
# We create a blob that takes care of pre-processing
blob = cv2.dnn.blobFromImage(cv2.resize(image,(300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

# Pass the blob through the network and obtain the detections and predictions
print("[INFO] Computing Object Detections....")
net.setInput(blob)
detections = net.forward()

# Loop over the detections
for i in range(0 , detections.shape[2]):
	# Extract the confidence score(i.e, probability associated with the detection)
	confidence = detections[0, 0, i, 2]
	# Filter out the confidence which is less than the threshold "--confidence"
	if confidence > args["confidence"]: 
		# If the confidence meets minimum threshold then we proceed to draw the box and print the confidence
		# Compute the (x, y) coordinates of the bounding box for the object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		# Draw the bounding box of the face with the associated probability 
		text = "{:.2f}%".format(confidence * 100)
		# In case our text goes above the image(such as when face detection occurs at the very top of an image), we shift if down by 10 pixels 
		y = startY - 10 if startY - 10 > 10 else startY + 10 
		cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
		cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# Show the output image 
cv2.imshow("Output", image)
cv2.waitKey(0)






