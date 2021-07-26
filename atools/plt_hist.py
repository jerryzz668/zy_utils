import cv2
import os
import matplotlib.pyplot as plt

path = '/Users/zhangyan/Desktop/huanxingdaowen50/1140-0011-13.jpg'

img = cv2.imread(path, 0)
img = img[1000:5000, 800:3500]
# plt.hist(img.ravel(), 256)
# plt.show()
a = plt.hist(img.ravel())
b = a[0].tolist()
index = b.index(max(b))
avg_piexl = a[1][index]
print(avg_piexl)
img = img - avg_piexl

cv2.namedWindow('img', 0)
cv2.imshow('img', img)
cv2.waitKey()