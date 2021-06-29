"""
@Description: 输入两个路径下的文件名一定要相同！！ 测试图像质量PSNR and SSIM
@Author     : zhangyan
@Time       : 2021/6/21 下午3:12
"""

import cv2
import argparse
import os
from tqdm import tqdm
import numpy as np
import math

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='/home/jerry/Desktop/code/Deraining/results/Rain100H', type=str, help='image file which need to be test')
parser.add_argument('--gt_dir', default='/home/jerry/Desktop/code/Deraining/Datasets/test/Rain100H/target', type=str, help='image groundtruth file')
args = parser.parse_args()

class SSIM():
    def __init__(self):
        self.C1 = (0.01 * 255) ** 2
        self.C2 = (0.03 * 255) ** 2
        self.filterSize = 11
        self.filterX = 1.5

    def run(self, imgx, imgy):

        X_2 = cv2.multiply(imgx, imgx, dtype=cv2.CV_32F)  # imgx**2
        Y_2 = cv2.multiply(imgy, imgy, dtype=cv2.CV_32F)  # imgy**2
        X_Y = cv2.multiply(imgx, imgy, dtype=cv2.CV_32F)  # imgx*imgy

        mu1 = cv2.GaussianBlur(imgx, (self.filterSize, self.filterSize), self.filterX)  # GaussianBlur()函数用高斯滤波器（GaussianFilter）对图像进行平滑处理, 等价于期望E(X)
        mu2 = cv2.GaussianBlur(imgy, (self.filterSize, self.filterSize), self.filterX)

        mu1_2 = cv2.multiply(mu1, mu1, dtype=cv2.CV_32F)  # mu1**2
        mu2_2 = cv2.multiply(mu2, mu2, dtype=cv2.CV_32F)  # mu2**2
        mu1_mu2 = cv2.multiply(mu1, mu2, dtype=cv2.CV_32F)  # mu1*mu2

        sigma1_2 = cv2.GaussianBlur(X_2, (self.filterSize, self.filterSize), self.filterX)
        sigma2_2 = cv2.GaussianBlur(Y_2, (self.filterSize, self.filterSize), self.filterX)
        sigma12 = cv2.GaussianBlur(X_Y, (self.filterSize, self.filterSize), self.filterX)
        sigma1_2 -= mu1_2
        sigma2_2 -= mu2_2
        sigma12 -= mu1_mu2

        t1 = 2 * mu1_mu2 + self.C1
        t2 = 2 * sigma12 + self.C2
        t3 = cv2.multiply(t1, t2, dtype=cv2.CV_32F)

        t4 = mu1_2 + mu2_2 + self.C1
        t5 = sigma1_2 + sigma2_2 + self.C2
        t6 = cv2.multiply(t4, t5, dtype=cv2.CV_32F)

        resMap = cv2.divide(t3, t6, dtype=cv2.CV_32F)
        r = cv2.mean(resMap)
        res = abs((r[0] + r[1] + r[2]) / 3.0)
        return res

def PSNR(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def calu_psnr_ssim(test_dir, gt_dir):

    avg_psnr, avg_ssim = [], []
    test_img_list = os.listdir(test_dir)
    num_img = len(test_img_list)

    for i in tqdm(range(num_img)):
        test_img = cv2.imread(os.path.join(test_dir, test_img_list[i]))
        gt_img = cv2.imread(os.path.join(gt_dir, test_img_list[i]))

        PNSR_value = PSNR(test_img, gt_img)
        avg_psnr.append(PNSR_value)

        SSIM_value = SSIM().run(test_img, gt_img)
        avg_ssim.append(SSIM_value)

        print("{}\' PSNR:".format(test_img_list[i]) + str(PNSR_value),"SSIM:" + str(SSIM_value))

    print('{} images\' AVG_PSNR:'.format(num_img), np.mean(avg_psnr), 'AVG_SSIM:', np.mean(avg_ssim))


if __name__ == '__main__':
    calu_psnr_ssim(args.test_dir, args.gt_dir)
