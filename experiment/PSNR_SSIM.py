# 提供相关的评价指标生成参数，以及一些预处理的相关函数

from math import exp
import math
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import cv2
from  torchvision.transforms import ToPILImage
import skimage.measure
import argparse
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='', type=str, help='image file which need to be test')
parser.add_argument('--gt_dir', default='', type=str, help='image groundtruth file')
args = parser.parse_args()


# 生成高斯分布函数
def gaussian(window_size, sigma):
    gauss = torch.Tensor([exp(-(x - window_size // 2) ** 2 / float(2 * sigma ** 2)) for x in range(window_size)])
    return gauss / gauss.sum()
# 暂时未知
def create_window(window_size, channel):
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous())
    return window
#
def _ssim(img1, img2, window, window_size, channel, size_average=True):
    mu1 = F.conv2d(img1, window, padding=window_size // 2, groups=channel)
    mu2 = F.conv2d(img2, window, padding=window_size // 2, groups=channel)
    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1 * mu2
    sigma1_sq = F.conv2d(img1 * img1, window, padding=window_size // 2, groups=channel) - mu1_sq
    sigma2_sq = F.conv2d(img2 * img2, window, padding=window_size // 2, groups=channel) - mu2_sq
    sigma12 = F.conv2d(img1 * img2, window, padding=window_size // 2, groups=channel) - mu1_mu2
    C1 = 0.01 ** 2
    C2 = 0.03 ** 2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    if size_average:
        return ssim_map.mean()
    else:
        return ssim_map.mean(1).mean(1).mean(1)


def ssim(img1, img2, window_size=11, size_average=True):
    img1=torch.clamp(img1,min=0,max=1)
    img2=torch.clamp(img2,min=0,max=1)
    # try:
    (_, channel, _, _) = img1.size()
    # except:
    #     channel = 3

    window = create_window(window_size, channel)
    if img1.is_cuda:
        window = window.cuda(img1.get_device())
    window = window.type_as(img1)
    return _ssim(img1, img2, window, window_size, channel, size_average)


def psnr(pred, gt):
    pred= pred.clamp(0,1).cpu().numpy()
    gt=gt.clamp(0,1).cpu().numpy()
    imdff = pred - gt
    rmse = math.sqrt(np.mean(imdff ** 2))
    if rmse == 0:
        return 100
    return 20 * math.log10(1.0 / rmse)

def data_arrange(img):
    img = torch.from_numpy(img)
    # print(img.shape)
    img = torch.unsqueeze(img, 0)
    img = img.permute(0, 3, 1, 2)
    # print(img.shape)
    img = img.type('torch.DoubleTensor')
    return img


# 直接使用即可已经查看相关代码其中的一些是别的论文也在用的参数无碍

def calu_psnr_ssim(test_dir, gt_dir):

    avg_psnr, avg_ssim, avg_skimage = [], [], []
    test_img_list = os.listdir(test_dir)
    num_img = len(test_img_list)

    for i in tqdm(range(num_img)):
        test_img = cv2.imread(os.path.join(test_dir, test_img_list[i]))
        gt_img = cv2.imread(os.path.join(gt_dir, test_img_list[i]))

        ssim_skimge = skimage.measure.compare_ssim(test_img, gt_img, data_range=255, multichannel=True, gaussian_weights=True)
        # print("skimage ssim ", ssim_skimge)
        avg_skimage.append(ssim_skimge)

        img1 = test_img / 255.
        img2 = gt_img / 255.
        # img1 = cv2.resize(img1, (544, 384))
        img1 = data_arrange(img1)
        img2 = data_arrange(img2)
        PSNR_value = psnr(img2, img1)
        SSIM_value = ssim(img1, img2)

        avg_psnr.append(PSNR_value)

        avg_ssim.append(SSIM_value)

        print("{}\' PSNR:".format(test_img_list[i]) + str(PSNR_value), "SSIM:" + str(SSIM_value.numpy()), "skimage_ssim:", ssim_skimge)

    print('{} images\' AVG_PSNR:'.format(num_img), np.mean(avg_psnr), 'AVG_SSIM:', np.mean(avg_ssim), 'skimage_ssim:', np.mean(avg_skimage))


if __name__ == '__main__':
    calu_psnr_ssim(args.test_dir, args.gt_dir)

