import numpy as np
import cv2
from matplotlib import pyplot as plt 
import sys 
import os 

def getInputArgs():
    if len(sys.argv) < 2 or len(sys.argv) >= 4:
        print (f'\nFormat:\n    {sys.argv[0]}  {"{image path/filename}"} {"{image path/filename}"}\n')
        exit()

    if not os.path.isfile(sys.argv[1]):
        print (f'\nInvalid file:  {sys.argv[1]}\n')
        exit()

    if not os.path.isfile(sys.argv[2]):
        print (f'\nInvalid file:  {sys.argv[2]}\n')
        exit()

    return sys.argv[1], sys.argv[2]

def waitKey(keys):
    while True:
        k = cv2.waitKey(50) & 0xFF # 0xFF? To get the lowest byte.
        if k in keys:
            break
    return

def getLaplaceOfGauss(img, ksize=5, sigma=0, scale=5):
    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2flt = img_grayscale
    flt2gauss = cv2.GaussianBlur(img2flt, (ksize, ksize), sigma)
    gauss2lap = cv2.Laplacian(flt2gauss, -1, ksize, scale = scale)
    lap2gauss = cv2.GaussianBlur(gauss2lap, (ksize, ksize), sigma)

    return lap2gauss

def convertToFloat32(img):
    if img.dtype == "uint8":
        return np.float32(img / 255)
    return img

def convertToInt8(img):
    if img.dtype == "float32":
        print("changing")
        return np.uint8(img * 255)
    return img

def getSobelEdgesFloat32(img, sobel_ksize=5):
    sobel_xflt = cv2.Sobel(img, -1, 1, 0, sobel_ksize)
    sobel_yflt = cv2.Sobel(img, -1, 0, 1, sobel_ksize)
    sobel_xflt_sq = np.square(sobel_xflt)
    sobel_yflt_sq = np.square(sobel_yflt)
    total = sobel_xflt_sq + sobel_yflt_sq 
    return np.sqrt(total)

if __name__ == "__main__":
    
    file1, file2 = getInputArgs()
    keys = [27, 32] # Define the keys to wait on
    ksize = 5
    sigma = 2
    scale = 7
    sobel_ksize = min(ksize, 7)

    # Load an color images and resize
    img1_raw = cv2.imread(file1)
    img2 = cv2.imread(file2)
    img1 = cv2.resize(img1_raw, (img2.shape[1], img2.shape[0]))
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Gaussian blur to first image, LoG to the second image
    img1_gaussian = cv2.GaussianBlur(img1, (ksize, ksize), sigma)
    img2_LoG = getLaplaceOfGauss(img2, ksize, sigma, scale)

    # Combine the gaussian and LoG images
    gray3 = cv2.merge([img2_LoG, img2_LoG, img2_LoG]) # Convert LoG to 3-channel grayscale
    merged = cv2.bitwise_and(img2, img2, gray3) # Merge the colored version to the 3-channel grayscale
    weighted_hybrid = cv2.addWeighted(img1_gaussian, 0.7, merged, .5, 0) # Merge LoG w/ Gaussian

    # Show images for LoG/Gaussian/Hybrid
    cv2.imshow("Gaussian Laplacian Hybrid: ", weighted_hybrid)
    # cv2.imshow('Gaussian', img1_gaussian)
    # cv2.imshow('Laplacian of Gaussian', img2_LoG)

    # Convert to Float32 and generate sobel magnitude
    img2_float32 = convertToFloat32(img2)
    img1_gaussian_float32 = convertToFloat32(img1_gaussian)
    img2_sobel_float32 = getSobelEdgesFloat32(img2_float32, ksize)

    # Combine gaussian and sobol
    gaussian_sobol_hybrid = cv2.addWeighted(img1_gaussian_float32, .7, img2_sobel_float32, 0.2, 0) # Merge LoG w/ Gaussian
    # cv2.imshow("Sobelized:", img2_sobel_float32)
    cv2.imshow("Gaussian Sobol Hybrid:", gaussian_sobol_hybrid)

    # save images
    save = convertToInt8(gaussian_sobol_hybrid)
    cv2.imwrite("hybrid.jpg", save)

    waitKey(keys) # Wait for a key to be pressed
    cv2.destroyAllWindows() 

