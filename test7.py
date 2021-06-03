import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
os.environ["CUDA_DEVICES_ORDER"]="PCI_BUS_IS"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
average=[]
average_SSIM=[]
path_test = "./data/test_data/gt"
test = os.listdir( path_test )
path_lp = "./data/test_data/test_result"
results_lp = os.listdir( path_lp )

deblur="./data/test_data/test_result"
true="./data/test_data/gt"

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

def ssim(HR,Results):

    gaussian_sigma = 1.5
    K1 = 0.01
    K2 = 0.03
    window_size = 11
    HR = np.array(HR, dtype=np.float64)
    Results = np.array(Results, dtype=np.float64)
    if not HR.shape == Results.shape:
        raise ValueError("Input Image must have the same dimensions")

    kernal = gaussian_2d_kernel(window_size, gaussian_sigma)
    kernal.resize(11,11,3)

    ux = correlation(HR, kernal)
    uy = correlation(Results, kernal)
    HR_sqr = HR ** 2
    Results_sqr = Results ** 2
    dis_mult_ori = HR * Results
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


def main():
    for i in range(0, 1400):

        t1 = cv2.imread(deblur + "/" + results_lp[i])
        print(deblur + "/" + results_lp[i])

        t2 = cv2.imread(true + "/" + test[i])
        t2 = cv2.resize(t2, (360, 240))
        print(true + "/" + test[i])

        ssimMetric = np.mean(ssim(t1,t2))
        average_SSIM.append(ssimMetric)
        print("第{}张SSIM为:   ".format(i) + str(ssimMetric))

main()
print('测试SSIM的平均值为：')
print(np.mean(average_SSIM))


