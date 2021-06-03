# @Description: 输入两个路径下的文件名一定要相同！！ 测试图像质量PSNR and SSIM
# @Author     : zhangyan
# @Time       : 2021/6/3 上午10:56

import os
import cv2
import numpy as np
import math
from scipy.ndimage import gaussian_filter
from numpy.lib.stride_tricks import as_strided as ast
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='', type=str, help='image file which need to be test')
parser.add_argument('--gt_dir', default='', type=str, help='image groundtruth file')
args = parser.parse_args()


def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


def block_view(A, block=(3, 3)):

    shape = (A.shape[0]/ block[0], A.shape[1]/ block[1])+ block
    strides = (block[0]* A.strides[0], block[1]* A.strides[1])+ A.strides
    return ast(A, shape= shape, strides= strides)


def ssim(img1, img2, C1=0.01**2, C2=0.03**2):

    bimg1 = block_view(img1, (4,4))
    bimg2 = block_view(img2, (4,4))
    s1  = np.sum(bimg1, (-1, -2))
    s2  = np.sum(bimg2, (-1, -2))
    ss  = np.sum(bimg1*bimg1, (-1, -2)) + np.sum(bimg2*bimg2, (-1, -2))
    s12 = np.sum(bimg1*bimg2, (-1, -2))

    vari = ss - s1*s1 - s2*s2
    covar = s12 - s1*s2

    ssim_map = (2*s1*s2 + C1) * (2*covar + C2) / ((s1*s1 + s2*s2 + C1) * (vari + C2))
    return np.mean(ssim_map)

# FIXME there seems to be a problem with this code
def ssim_exact(img1, img2, sd=1.5, C1=0.01**2, C2=0.03**2):

    mu1 = gaussian_filter(img1, sd)
    mu2 = gaussian_filter(img2, sd)
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = gaussian_filter(img1 * img1, sd) - mu1_sq
    sigma2_sq = gaussian_filter(img2 * img2, sd) - mu2_sq
    sigma12 = gaussian_filter(img1 * img2, sd) - mu1_mu2

    ssim_num = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2))

    ssim_den = ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    ssim_map = ssim_num / ssim_den
    return np.mean(ssim_map)


def calu_psnr_ssim(test_dir, gt_dir):

    avg_psnr, avg_ssim = [], []
    test_img_list = os.listdir(test_dir)
    num_img = len(test_img_list)

    for i in range(num_img):
        test_img = cv2.imread(os.path.join(test_dir, test_img_list[i]))
        gt_img = cv2.imread(os.path.join(gt_dir, test_img_list[i]))

        PNSR_value = psnr(test_img, gt_img)
        avg_psnr.append(PNSR_value)

        SSIM_value = ssim(test_img, gt_img)
        avg_ssim.append(SSIM_value)

        print("{}的PSNR:".format(test_img_list[i]) + str(PNSR_value),"SSIM:" + str(SSIM_value))

    print('{} images\' AVG_PSNR:'.format(num_img), np.mean(avg_psnr), 'AVG_SSIM:', np.mean(avg_ssim))


if __name__ == '__main__':
    calu_psnr_ssim(args.test_dir, args.gt_dir)