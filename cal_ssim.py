import torch
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from math import exp
import math
import os
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', default='result/Urban100', type=str, help='image file which need to be test')
parser.add_argument('--gt_dir', default='testsets/Urban100', type=str, help='image groundtruth file')
args = parser.parse_args()


def gaussian(window_size, sigma):
    gauss = torch.Tensor([exp(-(x - window_size//2)**2/float(2*sigma**2)) for x in range(window_size)])
    return gauss/gauss.sum()

def create_window(window_size, channel):
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous())
    return window

def _ssim(img1, img2, window, window_size, channel, size_average = True):
    mu1 = F.conv2d(img1, window, padding = window_size//2, groups = channel)
    mu2 = F.conv2d(img2, window, padding = window_size//2, groups = channel)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1*mu2

    sigma1_sq = F.conv2d(img1*img1, window, padding = window_size//2, groups = channel) - mu1_sq
    sigma2_sq = F.conv2d(img2*img2, window, padding = window_size//2, groups = channel) - mu2_sq
    sigma12 = F.conv2d(img1*img2, window, padding = window_size//2, groups = channel) - mu1_mu2

    C1 = 0.01**2
    C2 = 0.03**2

    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))

    if size_average:
        return ssim_map.mean()
    else:
        return ssim_map.mean(1).mean(1).mean(1)

class SSIM(torch.nn.Module):
    def __init__(self, window_size = 11, size_average = True):
        super(SSIM, self).__init__()
        self.window_size = window_size
        self.size_average = size_average
        self.channel = 3
        self.window = create_window(window_size, self.channel)

    def forward(self, img1, img2):
        (_, channel, _, _) = img1.size()

        if channel == self.channel and self.window.data.type() == img1.data.type():
            window = self.window
        else:
            window = create_window(self.window_size, channel)
            
            if img1.is_cuda:
                window = window.cuda(img1.get_device())
            window = window.type_as(img1)
            
            self.window = window
            self.channel = channel


        return _ssim(img1, img2, window, self.window_size, channel, self.size_average)

def ssim(img1, img2, window_size = 11, size_average = True):
    # (_, channel, _, _) = img1.size()
    # window = create_window(window_size, channel)
    window = create_window(window_size, 3)

    if img1.is_cuda:
        window = window.cuda(img1.get_device())
    window = window.type_as(img1)
    
    # return _ssim(img1, img2, window, window_size, channel, size_average)
    return _ssim(img1, img2, window, window_size, 3, size_average)


def PSNR(img1, img2):
    # b,_,_,_=img1.shape
    #mse=0
    #for i in range(b):
    img1=np.clip(img1,0,255)
    img2=np.clip(img2,0,255)
    mse = np.mean((img1/ 255. - img2/ 255.) ** 2)#+mse
    if mse == 0:
        return 100
    #mse=mse/b
    PIXEL_MAX = 1
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def calu_psnr_ssim(test_dir, gt_dir):

    avg_psnr, avg_ssim = [], []
    test_img_list = os.listdir(test_dir)
    num_img = len(test_img_list)

    for i in range(num_img):
        test_img = cv2.imread(os.path.join(test_dir, test_img_list[i]))
        gt_img = cv2.imread(os.path.join(gt_dir, test_img_list[i]))

        PNSR_value = PSNR(test_img, gt_img)
        avg_psnr.append(PNSR_value)

        SSIM_value = ssim(test_img, gt_img)
        avg_ssim.append(SSIM_value)

        print("{}\' ".format(test_img_list[i]),"SSIM:" + str(SSIM_value))

    print('{} images\' '.format(num_img),  'AVG_SSIM:', np.mean(avg_ssim))


if __name__ == '__main__':
    calu_psnr_ssim(args.test_dir, args.gt_dir)