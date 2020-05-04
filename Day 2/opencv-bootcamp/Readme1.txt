1. (h, w, d) = image.size
It is of the form (rows, columns, depth). 
But in case of storing it in an array it is stored in (x, y, z) format where x = width, y = height, z = channels.
Since, an image is actually a numpy array so its dimensions are written as (height, width, channels).

2. We need to click on the open OpenCV window and press a key, otherwise openCV will not be able to monitor any key typed on the terminal. 

3. Pixels are building blocks of an image. A 640 x 480 sized image has 640 * 480 = 307200 pixels in the image. In a grayscale image the pixel values range from 0-255 which indicate that there are 256 shades of gray. Pixels closer to 255 are brighter pixels whereas pixels closer to 0 are darker. 

In OpenCV color images in the RGB format has a 3-tuple color space: (B, G, R). Each value in the BGR-3tuple has values within the range [0, 255]. So the color possibilities are 256 * 256 * 256 = 16777216. 

4. imutils.resize() resizes the image according to an aspect ratio. This function takes as input either the 'width' or 'height'.

5. Rotating an image using openCV requires 3 steps: 
	a. Calculate the center point of the image using width and height of the image. 
	b. Form the rotation matrix using cv2.getRotationMatrix2D().
	c. Use the rotation matrix to warp the image using cv2.warpAffine(). 

We can do the same using imutils.rotate() in a single step. 

OpenCV does not care if our image is clipped and out-of-view after the rotation. So, in order to keep the entire image in view we use imutils.rotate_bound(). 

6. In many image processing pipelines, we must blur an image to reduce high frequency noise and thus making it easier for our algorithms to detect and understand the actual contents of the image.

7. cv2.circle(img, center, radius, color, thickness)
img - output image. 
center - center of the circle. 
radius - radius of the circle in pixels. 
thickness - (-ve) value gives a solid circle. 

