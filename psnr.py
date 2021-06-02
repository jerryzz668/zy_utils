#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from math import exp
import math
import cv2
# import pandas as pd
import datetime
import time
import os,sys
from skimage.measure import compare_ssim as ssim

average=[]
average_SSIM=[]
path_test = "/home/zj-1/Documents/ReMAEN-master/comparison_experiment/GCANet/Rain1400_gt"
test = os.listdir( path_test )
path_lp = "/home/zj-1/Documents/ReMAEN-master/comparison_experiment/GCANet/Rain1400_test"
results_lp = os.listdir( path_lp )

deblur="/home/zj-1/Documents/ReMAEN-master/comparison_experiment/GCANet/Rain1400_test"
true="/home/zj-1/Documents/ReMAEN-master/comparison_experiment/GCANet/Rain1400_gt"

def PSNR(img1, img2):
	mse = np.mean( (img1/255. - img2/255.) ** 2 )
	if mse == 0:
		return 100
	PIXEL_MAX = 1
	return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def SSIM(image_vis,output_image):
	image_ssim = ssim(
						image_vis,
						output_image,
						data_range=output_image.max() - output_image.min(),
						multichannel=True)
	return image_ssim
def main():
	for i in range (1400):
		# t1=cv2.imread(deblur+"/"+"{}.png".format(i))
		# t2=cv2.imread(true+"/"+"{}.jpg".format(i))
		
		t1=cv2.imread(deblur+"/"+results_lp[i])
		print(deblur+"/"+results_lp[i])
		t1 = cv2.resize(t1, (320, 480))
		t2=cv2.imread(true+"/"+test[i])
		print(true+"/"+test[i])
		t2 = cv2.resize(t2,(320, 480))
		psnrMetric = PSNR(t1,t2)
		average.append(psnrMetric)
		print("第{}张PSNR为:   ".format(i)+str(psnrMetric))

		ssimMetric = SSIM(t1,t2)
		average_SSIM.append(ssimMetric)
		print("第{}张SSIM为:   ".format(i)+str(ssimMetric))

main()
print('测试PSNR的平均值为：')
print(np.mean(average))
print('测试SSIM的平均值为：')
print(np.mean(average_SSIM))


