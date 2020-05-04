# Import the necessary packages 
import cv2 
import imutils 

'''Load the image and show its dimensions. We need to keep in mind that the image is a multi-dimensional numpy array 
shape no. rows(height) * no. columns(width) * no. channels(depth)'''

# Loading an image from disk into memory
image = cv2.imread("jp.png")
(h, w, d) = image.shape
print("width= {}, height= {}, depth= {}".format(w, h, d))

# Access the RGB Pixel located at position x=50, y=100 keeping in mind that opencv stores images in BGR order rather than RGB 
(B, G, R) = image[100, 50]
print("B= {}, G= {}, R= {}". format(B, G, R))

# Extract a region of interest(ROI) of 100*100 pixel square starting from x=320, y=60
roi = image[60:160, 320:420]
cv2.imshow("ROI", roi)
cv2.waitKey(0)

# Resizing images 
'''This image will be resized but distorted because we didn't take into account the aspect ratio'''
resized = cv2.resize(image, (200, 200))
cv2.imshow("CV Resized Image", resized)
cv2.waitKey(0)

# Resizing images based on a fixed aspect ratio.
'''We resize the width to be 300px and change the height based on the aspect ratio. '''
ratio = 300.0 / w
h = ratio * h
aspected = cv2.resize(image, (300, int(h)))
cv2.imshow("CV Aspected image", aspected)
cv2.waitKey(0)

'''We can use the imutils package to resize according to the aspect ratio. 
This package automatically calculates the aspect ratio. So, this is a one-step process
rather than the previous process using openCV which is a three-step process'''
imuitls_resized = imutils.resize(image, width = 300)
cv2.imshow("imutils Aspected image", imuitls_resized)
cv2.waitKey(0)

# Rotating an image 45 degree clockwise

# center = (w // 2, h // 2) '//'' is used to perform integer math. No floating point values. 
# # Get the rotation matrix 
# M = cv2.getRotationMatrix2D(center, -45, 1.0)
# rotated = cv2.warpAffine(image, M, (w, h))
# cv2.imshow("Rotated", rotated)
# cv2.waitKey(0)

# Rotation can also be easily accomplished via imutils with less code
rotated = imutils.rotate(image, -45)
cv2.imshow("imutils Rotated image", rotated)
cv2.waitKey(0)

# OpenCV doesn't "care" if our rotated image is clipped after rotation
# so we can instead use another imutils convenience function to help
# us out
rotated_bound = imutils.rotate_bound(image, 45)
cv2.imshow("imutils Rotate Bound", rotated_bound)
cv2.waitKey(0)

# Blur an image 
# Apply a Gaussian blur with a 11x11 kernel to the image to smooth it,
# useful when reducing high frequency noise
blur_image = cv2.GaussianBlur(image, (11, 11), 0)
cv2.imshow("Blurred Image", blur_image)
cv2.waitKey(0)

# Draw a rectangle on an image 
output = image.copy()
cv2.rectangle(output, (320, 60), (420, 160), (255, 0, 0), 2)
cv2.imshow("Rectangle", output)
cv2.waitKey(0)

# Draw a circle 
output = image.copy()
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
cv2.imshow("Circle", output)
cv2.waitKey(0)

# Draw a line 
# Draw a 5px thick red line from x=60, y=20 to x=400, y=200
output = image.copy()
cv2.line(output, (60, 20), (400, 200), (255, 0, 0), 2)
cv2.imshow("Line", output)
cv2.waitKey(0)

# Display a text on the image 
output = image.copy()
text = "OpenCV + Jurassic World!!!"
cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow("Text", output)
cv2.waitKey(0)

# Display the image on screen 
cv2.imshow("Original Image", image)
# Press a key to continue execution. This is important othewise our image would display and disappear faster than we would even see the image
cv2.waitKey(0)