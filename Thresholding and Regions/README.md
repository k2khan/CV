# Thresholding and Regions

The goal of this project was to "detect" a computer screen. This same process can be used to detect a myriad of items.

First, thresholding was performed by using Otsu's method. This seperates every pixel in an image into two classes, a foreground and a background. Then, median filtering and morphology were used. Median filtering is a technique that reduces noise, and morphology applies a structuring element to an input image. I got the best results by applying erosion followed by dilation, and then dilation followed by erosion. Connected components were then used to remove any erraneous blobs that were of no use. Finally, the draw_contours() method was used to display regions as a rotated rectangular bounding box (because we are trying to detect screens). 

# Example of the Process
<p float="left">
    <img src="./images/sample/A-orig_img.jpg" width="250">
    <img src="./images/sample/B-thresh.jpg" width="250">
    <img src="./images/sample/C-filt_regions.jpg" width="250">
    <img src="./images/sample/D-boxed_conn_comps.jpg" width="250">
    <img src="./images/sample/G-final_result.png" width="250">
</p>

# Results
<p float="left">
    <img src="./images/1_final.jpg" width="350">
    <img src="./images/1_ms_surface.jpg" width="350">
</p>

<p float="left">
    <img src="./images/3_final.jpg" width="350">
    <img src="./images/3_laptop_light_bkgnd.jpg" width="350">
</p>

<p float="left">
    <img src="./images/4_final.jpg" width="350">
    <img src="./images/4_ms_surface_angled.png" width="350">
</p>

<p float="left">
    <img src="./images/5_final.jpg" width="350">
    <img src="./images/5_screen_in_bkgnd.png" width="350">
</p>

<p float="left">
    <img src="./images/6_final.jpg" width="350">
    <img src="./images/6_clipped_corner.jpg" width="350">
</p>
