1. 'Collections' is a library that contains high performance data types. We will be using a 'dequeue' for our purpose. Dequeue is a list like data structure with super fast appends and pops on either end. It is used to maintain a list of past N (x, y) locations of the ball in out video stream. Maintaining such a queue allows us to draw a "contrail" of the ball being tracked.

2. vs.read() is a method of our camera pointer which returns a 2-tuple. The first entry in the tuple 'grabbed' is a boolean indicating whether the frame was successfully read or not.

3. In case we are reading a frame from a video file and the frame is not successfully read, then we will know that we have reached the end of the video file and break out of the while loop. 

4. Now we come to pre-processing our frame. We resize the frame to have a width of 600px. 'Downsizing' the frame allows us to process the frame faster, leading to increase in FPS. Then, we blur the image to reduce the high-frequency noise and allow us to focus on the structural objects inside the frame, such as the ball. Finally, we convert the frame to the HSV Color space. 

5. We can find the center of the blob using moments in OpenCV. But first of all, we should know what exactly Image moment is all about. Image Moment is a particular weighted average of image pixel intensities, with the help of which we can find some specific properties of an image, like radius, area, centroid etc. To find the centroid of the image, we generally convert it to binary format and then find its center.