import cv2 as cv

img = cv.imread('xuejie.jpg')


ret = cv.copyMakeBorder(img, 10, 20, 40, 80, cv.BORDER_CONSTANT, value=(0,0,0))
cv.namedWindow('img',0)
cv.imshow('img',ret)

cv.waitKey()
