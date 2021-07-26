import numpy as np
import math
from scipy.ndimage import gaussian_filter
import os
import cv2

def getSSIM(X, Y):
    """
       Computes the mean structural similarity between two images.
    """
    assert (X.shape == Y.shape), "Image-patche provided have different dimensions"
    nch = 1 if X.ndim==2 else X.shape[-1]
    mssim = []
    for ch in range(nch):
        Xc, Yc = X[...,ch].astype(np.float64), Y[...,ch].astype(np.float64)
        mssim.append(compute_ssim(Xc, Yc))
    return np.mean(mssim)


def compute_ssim(X, Y):
    """
       Compute the structural similarity per single channel (given two images)
    """
    # variables are initialized as suggested in the paper
    K1 = 0.01
    K2 = 0.03
    sigma = 1.5
    win_size = 5

    # means
    ux = gaussian_filter(X, sigma)
    uy = gaussian_filter(Y, sigma)

    # variances and covariances
    uxx = gaussian_filter(X * X, sigma)
    uyy = gaussian_filter(Y * Y, sigma)
    uxy = gaussian_filter(X * Y, sigma)

    # normalize by unbiased estimate of std dev
    N = win_size ** X.ndim
    unbiased_norm = N / (N - 1)  # eq. 4 of the paper
    vx  = (uxx - ux * ux) * unbiased_norm
    vy  = (uyy - uy * uy) * unbiased_norm
    vxy = (uxy - ux * uy) * unbiased_norm

    R = 255
    C1 = (K1 * R) ** 2
    C2 = (K2 * R) ** 2
    # compute SSIM (eq. 13 of the paper)
    sim = (2 * ux * uy + C1) * (2 * vxy + C2)
    D = (ux ** 2 + uy ** 2 + C1) * (vx + vy + C2)
    SSIM = sim/D
    mssim = SSIM.mean()

    return mssim

def getPSNR(X, Y):
    #assume RGB image
    target_data = np.array(X, dtype=np.float64)
    ref_data = np.array(Y, dtype=np.float64)
    diff = ref_data - target_data
    diff = diff.flatten('C')
    rmse = math.sqrt(np.mean(diff ** 2.) )
    if rmse == 0: return 100
    else: return 20*math.log10(255.0/rmse)

## data paths
GEN_im_dir  = "./test_result"  # generated im-dir with {f_gen.ext}
GTr_im_dir  = './gt'  # ground truth im-dir with {f.ext}

path_test = "./gt"
test = os.listdir(path_test)
path_lp = "./test_result"
results_lp = os.listdir(path_lp)


def measure_SSIM_PSNRs(GT_dir, Gen_dir):
    ssims, psnrs = [], []
    for i in range(0, 1200):
        t1 = cv2.imread(Gen_dir + "/" + results_lp[i])
        # t1 = cv2.resize(t1, (360, 240))
        print(Gen_dir + "/" + results_lp[i])

        t2 = cv2.imread(GT_dir + "/" + test[i])
        # t2 = cv2.resize(t2, (480, 320))
        print(GT_dir + "/" + test[i])

        # r_im = misc.imread(Gen_dir + "/" + results_lp[i])
        # g_im = misc.imread(GT_dir + "/" + test[i])
        # assert (r_im.shape==g_im.shape), "The images should be of same-size"
        ssim = getSSIM(t1, t2)
        psnr = getPSNR(t1, t2)
        print ("{0}, {1}: {2}".format(GT_dir + "/" + test[i],Gen_dir + "/" + results_lp[i], ssim))
        print ("{0}, {1}: {2}".format(GT_dir + "/" + test[i],Gen_dir + "/" + results_lp[i], psnr))
        ssims.append(ssim)
        psnrs.append(psnr)
    return np.array(ssims), np.array(psnrs)

### compute SSIM and PSNR
SSIM_measures, PSNR_measures = measure_SSIM_PSNRs(GTr_im_dir, GEN_im_dir)
print ("SSIM >> Mean: {0} std: {1}".format(np.mean(SSIM_measures), np.std(SSIM_measures)))
print ("PSNR >> Mean: {0} std: {1}".format(np.mean(PSNR_measures), np.std(PSNR_measures)))

