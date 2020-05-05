A document scanner is used to scan a piece of paper. 
A piece of paper is assumed to be rectangle. 

We will assume that the largest contour in our image with four points is our piece of paper to be scanned. 

cv2.arcLength(contour, True). 
True specifies that the shape is closed. It is used to calculate the perimeter of the contour. 

We’ll pass two arguments into four_point_transform : the first is our original image we loaded off disk (not the resized one), and the second argument is the contour representing the document, multiplied by the resized ratio.

We multiply by the resized ratio because we performed edge detection and found contours on the resized image of height=500 pixels.

However, we want to perform the scan on the original image, not the resized image, thus we multiply the contour points by the resized ratio.

To obtain the black and white feel to the image, we then take the warped image, convert it to grayscale and apply adaptive thresholding o