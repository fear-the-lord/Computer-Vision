1. Edge Detection is useful for finding boundaries of objects of an image. It is usd for Segmentation purposes.
	cv2.Canny(img, minVal, maxVal, aperture_size)
	img - gray image.
	minVal - A minimum threshold. 
	maxVal - A maximun threshold. 
	aperture_size - The sobel kernel size, by default the value is 3.

2. Image thresholding is an important intermediary step for image processing pipelines. Thresholding can help us to remove lighter or darker regions and contours of images.

3. cv2.threshold(img, minVal, maxVal, style)
If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black). The function used is cv2.threshold. First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value. OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function. Different types are:

cv2.THRESH_BINARY
cv2.THRESH_BINARY_INV
cv2.THRESH_TRUNC
cv2.THRESH_TOZERO
cv2.THRESH_TOZERO_INV

4. cv2.findContours() is used to detect all the foreground white pixels in the threshold copy. 

imutils.grab_contours() is very important accounting to the fact that cv2.findContours implementation changed between OpenCV 2.4, OpenCV 3, and OpenCV 4. This compatibility line is present on the blog wherever contours are involved.

5. Erosions and dilations are typically used to reduce noise in binary images (a side effect of thresholding).

Using OpenCV we can erode contours, effectively making them smaller or causing them to disappear completely with sufficient iterations. This is typically useful for removing small blobs in mask image.

In an image processing pipeline if you ever have the need to connect nearby contours, you can apply dilation to the image. Shown in the figure is the result of dilating contours with five iterations, but not to the point of two contours becoming one.

6. Masks allow us to “mask out” regions of an image we are uninterested in. We call them “masks” because they will hide regions of images we do not care about.

When using the thresholded image as the mask in comparison to our original image, the colored regions reappear as the rest of the image is “masked out”. 