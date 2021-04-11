1./ For our purposes, it seems like Otsu's binarization with gaussian blur will work best. 
I tried the multiple parameters with regular thresholding (BINARY, BINARY_INV, TOZERO, TOZERO_INV). I believe that BINARY gave the best result after Otsu when I tried with the thresholding value of 150. However, one downside is that you would likely have to calculate the best thresholding value for every image. 
Adaptive thresholding just doesn't work for our task because it lightens/darkens based on the neighborhood area. I'm not sure how I would go about calculating the best "box" size.

2./ Kernal size should ideally change with image size. For example a 1000x1000 image would have a reasonable kernal size of (10, 10). However, using a kernal size of (10, 10) in a 100x100 image would not be reasonable. I considered resizing every image to something like 500x500, so that we could use the same kernal size on every image. Ideally, however, you might want to do a percentage of an image. So, for a 1000x1000 image, 1% would have a kernal size of (10, 10). I'm currently using opening and closing, in that order, to morph my image.

3./ I used a function filter_unwanted() to filter out regions of specific sizes. It basically checks for each reason to be of a minimum size. If it isn't it is filtered from the result.

4./ It seems like the aspect ratio and extent properties will work best for us. This is because laptops nowdays are around 16:9 aspect ratio. Furthermore, we would expect the contour area of the region with respect to the bounding rectangle area to be realively large.

5./ I used extent and aspect ratio aswell as the area of the contour to determine the final region (our laptop). My conditions are as follows. We only display the laptop screen if
        1./ The extent > 0.7.
        2./ The aspect ratio is in between 1.1 and 2.0.
        3./ The area of the contour is greater than 5000.
These conditions narrow down multiple options to just one computer screen in every case except one. The code does not work on the 2nd image.

The recommended usage is with a kernal size of 10. I get good results on every image except the 2nd image with a kernal size of 10.

