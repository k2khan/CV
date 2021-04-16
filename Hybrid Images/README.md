# Filtering and Hybrid Images

This essentially aims to implement a poor man's implementation of hybrid images. A true implementation requires the Fast Fourier Transform (FFT) for frequency filtering.

Instead, we use Gaussian blurring, Sobel edge detection, and the Laplacian of the Gaussian (LoG), also known as the 2nd derivative of the Gaussian).

## Here are some of the results:

<p float="left">
    <img src="./images/car.jpg" width="250">
    <img src="./images/rhino-car.jpg" width="250">
    <img src="./images/rhino.jpg" width="250">
</p>

<p float="left">
    <img src="./images/marilyn.jpg" width="250">
    <img src="./images/einstein-marilyn.jpg" width="250">
    <img src="./images/einstein.jpg" width="250">
</p>

<p float="left">
    <img src="./images/dog.jpg" width="250">
    <img src="./images/dog-cat.jpg" width="250">
    <img src="./images/cat.jpg" width="250">
</p>
