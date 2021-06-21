# @Description: 输入两个路径下的文件名一定要相同！！ 测试图像质量PSNR and SSIM
# @Author     : zhangyan
# @Time       : 2021/6/3 上午10:56

import os
import cv2
import numpy as np
import math
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='', type=str, help='image file which need to be test')
parser.add_argument('--gt_dir', default='', type=str, help='image groundtruth file')
args = parser.parse_args()

# calc psnr
def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

# calc ssim
def correlation(img,kernal):
    kernal_heigh = kernal.shape[0]
    kernal_width = kernal.shape[1]
    cor_heigh = img.shape[0] - kernal_heigh + 1
    cor_width = img.shape[1] - kernal_width + 1
    result = np.zeros((cor_heigh, cor_width), dtype=np.float64)
    for i in range(cor_heigh):
        for j in range(cor_width):
            result[i][j] = (img[i:i + kernal_heigh, j:j + kernal_width] * kernal).sum()
    return result

def gaussian_2d_kernel(kernel_size=11, sigma=1.5):
    kernel = np.zeros([kernel_size, kernel_size])
    center = kernel_size // 2

    if sigma == 0:
        sigma = ((kernel_size - 1) * 0.5 - 1) * 0.3 + 0.8

    s = 2 * (sigma ** 2)
    sum_val = 0
    for i in range(0, kernel_size):
        for j in range(0, kernel_size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / s)
            sum_val += kernel[i, j]
    sum_val = 1 / sum_val
    return kernel * sum_val

def ssim(img1,img2):

    gaussian_sigma = 1.5
    K1 = 0.01
    K2 = 0.03
    window_size = 11
    img1 = np.array(img1, dtype=np.float64)
    img2 = np.array(img2, dtype=np.float64)
    if not img1.shape == img2.shape:
        raise ValueError("Input Image must have the same dimensions")

    kernal = gaussian_2d_kernel(window_size, gaussian_sigma)
    kernal.resize(11,11,3)

    ux = correlation(img1, kernal)
    uy = correlation(img2, kernal)
    HR_sqr = img1 ** 2
    Results_sqr = img2 ** 2
    dis_mult_ori = img1 * img2
    uxx = correlation(HR_sqr, kernal)
    uyy = correlation(Results_sqr, kernal)
    uxy = correlation(dis_mult_ori, kernal)
    ux_sqr = ux ** 2
    uy_sqr = uy ** 2
    uxuy = ux * uy
    sx_sqr = np.around(uxx - ux_sqr, decimals=10)
    sy_sqr = np.around(uyy - uy_sqr, decimals=10)
    sxy = uxy - uxuy
    C1 = (K1 * 255) ** 2
    C2 = (K2 * 255) ** 2
    C3 = 0.5 * C2

    l = (2 * uxuy + C1) / (ux_sqr + uy_sqr + C1)

    sxsy = np.sqrt(sx_sqr) * np.sqrt(sy_sqr)
    c = (2 * sxsy + C2) / (sx_sqr + sy_sqr + C2)
    s = (sxy + C3) / (sxsy + C3)

    ssim = l * c * s

    return np.mean(ssim)


def calu_psnr_ssim(test_dir, gt_dir):

    avg_psnr, avg_ssim = [], []
    test_img_list = os.listdir(test_dir)
    num_img = len(test_img_list)

    for i in tqdm(range(num_img)):
        test_img = cv2.imread(os.path.join(test_dir, test_img_list[i]))
        gt_img = cv2.imread(os.path.join(gt_dir, test_img_list[i]))

        PNSR_value = psnr(test_img, gt_img)
        avg_psnr.append(PNSR_value)

        SSIM_value = ssim(test_img, gt_img)
        avg_ssim.append(SSIM_value)

        print("{}\' PSNR:".format(test_img_list[i]) + str(PNSR_value),"SSIM:" + str(SSIM_value))

    print('{} images\' AVG_PSNR:'.format(num_img), np.mean(avg_psnr), 'AVG_SSIM:', np.mean(avg_ssim))


if __name__ == '__main__':
    calu_psnr_ssim(args.test_dir, args.gt_dir)

