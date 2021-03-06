# Computer-Vision
This repository contains all the contents of the 17-day crash-course from Pyimagesearch.

<h2> Day 1/Face Detection </h2>
<p>It is divided into <b>two</b> parts:<br> 
1. Face detection in <b>static images</b> which is present in the file named <b>detect_faces.py</b>.<br>
2. Face detection in <b>video streams</b> which if present in the file named <b>detect_faces_video.py</b>.<br>

For <b>detect_faces.py</b> put an image on the same folder and run as:<br>
$<b>python detect_faces.py --image <image_name> --prototxt prototxt.txt --model model.caffemodel</b><br>
  
For <b>detect_faces_video.py</b> run as:<br>
$<b>python detect_faces_video.py --prototxt prototxt.txt --model model.caffemodel</b><br></p>

<hr style="width:50%;text-align:left;margin-left:0">

<h2>Day 2/opencv-bootcamp</h2>
<p>This folder has <b>two</b> parts:<br>
  1. <b>bootcamp1.py</b> deals with:<br>
  <ul>
    <li> Loading and Displaying an Image. </li>
    <li> Accessing individual pixels. </li>
    <li> Array Slicing and Cropping. </li>
    <li> Resizing Images. </li>
    <li> Rotating an Image. </li>
    <li> Smoothing an Image. </li>
    <li> Drawing on an Image. </li>
   </ul>
   
  2. <b>bootcamp2.py</b> deals with:<br>
  <ul>
    <li> Convert images to grayscale with OpenCV. </li>
    <li> Performing edge detection. </li>
    <li> Thresholding a grayscale image. </li>
    <li> Finding, counting, and drawing contours. </li>
    <li> Rotating an Image. </li>
    <li> Conducting erosion and dilation. </li>
    <li> Masking an image. </li>
   </ul>
   
   For <b>bootcamp1.py</b> run the code as:<br>
  $<b>python bootcamp1.py</b><br>
  
   For <b>bootcamp2.py</b> run the code as:<br>
  $<b>python bootcamp2.py --image tetris_blocks.png</b><br></p>
  
  <hr style="width:50%;text-align:left;margin-left:0">
  
  <h2>Day 3/Document Scanner</h2>
  <p>The basic steps in creating a document scanner is:
  <ul>
    <li>Input the image.</li>
    <li>Detect the edges.</li>
    <li>Detect all the contours.</li>
    <li>Find all the contours with the maximum area and with four points.</li>
    <li>Draw that contour.</li>
    <li>Apply four point transforms to obtain a top-down view of the original image.</li>
    <li>Convert the image to gray scale.</li>
    <li>Threshold the image to obtain a 'black & white' paper effect.</li>
   </ul></p>
   
   Run the code as:<br> 
    $<b>python scan.py --image receipt.jpg</b>
    
   <hr style="width:50%;text-align:left;margin-left:0">
   
   <h2>Day 4/Optical Mark Recognition</h2>
   <p>The basic steps are: 
    <ul>
      <li>Input the image.</li>
      <li>Input the answer key.</li>
      <li>Detect the edges.</li>
      <li>Detect the contour with the maximum area and four points.</li>
      <li>Draw the contour.</li>
      <li>Apply four point transforms to obtain a top-down view of the original image.</li>
      <li>Apply Otsu's Thresholding to binarize the image.</li> 
      <li>Draw all the Question contours from the binarized image.</li>
      <li>Sort the contours in top-to-bottom approach.</li>
      <li>Find the masked contours.</li> 
      <li>Find the score corresponding to the masked contours.</li>
    </ul><p>
  
  Run the code as:<br>
  $<b>python test_grader.py --image images/test_01.png</b>
  
  <hr style="width:50%;text-align:left;margin-left:0">
  
  <h3>Day 5/Ball Tracking</h3>
  <p>The basic steps are:
  <ul>
    <li>Define the lower and upper boundaries of the object to be tracked using <b>range_detector.py</b>.</li>
    <li>Use a deque with a fixed buffer size which will help in forming the tail.</li> 
    <li>Input the video file. If the video file is not found start the camera.</li>
    <li>Read a frame.</li>
    <li>Resize it, Blur it and convert it to HSV color space.</li>
    <li>Construct a mask for the object, then perform a series of dilations and erotions to remove any small blobs left in the mask.</li>
    <li>Compute the contour of the ball and draw it in our frame.</li>
    <li>Only proceed if atleast one contour was found.</li>
    <li>Find the largest contour in the mask.</li>
    <li>Use it to form the minimum enclosing circle and centroid.</li>
    <li>Draw a circle around the object if the radius meets a minimum size.</li>
    <li>Insert the center coordinates in the deque.</li>
    <li>Track the points and draw the line.</li>
    <li>Show the frame.</li>
  </ul>
  
  Run the range detector as: <br>
  $<b>python range_detector.py --filter HSV --image <image_path></b><br>
  Run the ball tracker as: <br>
  $<b>python ball_tracker.py --video <video_path></b>(in order to stream a video file).<br>
  $<b>python ball_tracker.py</b>(for web-cam streaming).
  
  <hr style="width:50%;text-align:left;margin-left:0">
  
  
      
 
  
