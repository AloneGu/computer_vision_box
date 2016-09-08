#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/8/16 10:55 AM
# @Author  : Jackling 


import cv2

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
img = cv2.imread('../data/699501183857412032.jpg')

(rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(32, 32), scale=1.05)
for (x, y, w, h) in rects:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
