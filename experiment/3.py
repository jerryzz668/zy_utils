import os
import cv2
import numpy as np
import math
import argparse
from tqdm import tqdm
from skimage.measure import compare_ssim
from skimage.measure.simple_metrics import compare_psnr
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='result/Urban100', type=str, help='image file which need to be test')
parser.add_argument('--gt_dir', default='testsets/Urban100', type=str, help='image groundtruth file')
args = parser.parse_args()



def ssim(img1, img2):
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()
def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')




def calu_psnr_ssim(test_dir, gt_dir):

    avg_psnr, avg_ssim = [], []
    test_img_list = os.listdir(test_dir)
    num_img = len(test_img_list)

    for i in range(num_img):
        test_img = cv2.imread(os.path.join(test_dir, test_img_list[i]))
        gt_img = cv2.imread(os.path.join(gt_dir, test_img_list[i]))

        # PNSR_value = compare_psnr(test_img, gt_img)
        # avg_psnr.append(PNSR_value)

        SSIM_value = calculate_ssim(test_img, gt_img)
        avg_ssim.append(SSIM_value)

        print("{}\' ".format(test_img_list[i]),"SSIM:" + str(SSIM_value))

    print('{} images\' '.format(num_img),  'AVG_SSIM:', np.mean(avg_ssim))


if __name__ == '__main__':
    calu_psnr_ssim(args.test_dir, args.gt_dir)
