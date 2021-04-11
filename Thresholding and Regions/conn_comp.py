import numpy as np
import os
import sys
import random as rnd
import cv2

def getInputArgs():
    if len(sys.argv) != 3:
        print(f'Useage: {sys.argv[0]} {"{image path/filename}"} {"kernalSize"}\n')
        exit()

    if not os.path.isfile(sys.argv[1]):
        print(f'Invalid file: {sys.argv[1]}\n')
        exit()

    return sys.argv[1], sys.argv[2]

def draw_contours(pix_labels, thresh):
    num_labels = np.max(pix_labels) + 1

    boxed_comps_img = np.zeros([pix_labels.shape[0], pix_labels.shape[1], 3], dtype=np.uint8)
    boxed_comps_img[:, :, :] = 0

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]

    rnd.seed()

    # fill regions with random colors
    for i, cnt in enumerate(contours):
        # find the bounding boxes
        mask = np.zeros(pix_labels.shape[:2], dtype = pix_labels.dtype) # mask for removing the bad contours based off of a criteria
        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)
        box = np.int0(cv2.boxPoints(rect))
        boundingArea = np.linalg.norm(box[0] - box[1]) * np.linalg.norm(box[1] - box[2])
        extent = float(area)/boundingArea

        (x, y), (width, height), angle = rect
        aspectRatio = max(width, height) / min(width, height) 
        upperBound = 2.0
        lowerBound = 1.1

        one_pix_hsv = np.zeros([1, 1, 3], dtype=np.uint8)
        one_pix_hsv[0, 0, :] = [rnd.randint(0, 255), rnd.randint(150, 255), rnd.randint(200, 255)]
        bgr_color = cv2.cvtColor(one_pix_hsv, cv2.COLOR_HSV2BGR)[0, 0].tolist()
        mask = np.zeros(thresh.shape, np.uint8)

        # only display the bounding box and region if the following conditions are met
        if extent > 0.7 and lowerBound <= aspectRatio <= upperBound and area > 5000:
            print(f"Box: {box}")
            print(f"Area: {area:<10} Bounding area: {boundingArea:^10} Extent: {extent:^10} Aspect ratio: {aspectRatio}")
            print(f"Width: {width}, Height: {height}")
            cv2.drawContours(boxed_comps_img, contours, i, bgr_color, -1)
            cv2.drawContours(boxed_comps_img, [box], 0, (0, 0, 255), 2)

    return boxed_comps_img

def getAreas(num_labels, stats):
    areas = []
    for i in range(num_labels):
        areas.append(stats[i, cv2.CC_STAT_AREA])
    return areas

def filter_unwanted(num_labels, pix_labels, stats):
    min_size = 15000
    ret = np.zeros((pix_labels.shape))
    sizes = stats[1:, -1]
    num_labels = num_labels - 1
    for i in range(num_labels):
        if sizes[i] >= min_size:
            ret[pix_labels == i + 1] = 255
    return ret

if __name__ == "__main__":
    # get input
    filename, kSize = getInputArgs()
    kernal = np.ones((int(kSize), int(kSize)), np.uint8)

    # read in the image
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply blur and threshold using otsu 
    medianBlur = cv2.medianBlur(gray, 5)
    thresh = cv2.threshold(medianBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # otsu's thresholding

    # apply morphology
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernal)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernal)

    # use connected components to draw contours
    output = cv2.connectedComponentsWithStats(closing)
    num_labels, pix_labels, stats = output[0], output[1], output[2]
    areas = getAreas(num_labels, stats)

    # filter the unwanted small stuff 
    filteredImg = filter_unwanted(num_labels, pix_labels, stats)
    boxed_conn_comps = draw_contours(pix_labels, np.uint8(filteredImg))

    cv2.imshow('original', img)
    cv2.imshow('thresholded', thresh)
    cv2.imshow('morphed', opening)
    cv2.imshow('filter unwanted', filteredImg)
    cv2.imshow('boxed_conn_comps', boxed_conn_comps)


    cv2.waitKey()
