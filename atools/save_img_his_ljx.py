import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
import os
import shutil
imgs = glob.glob(r'D:\A2_ok\*.jpg')
save_p = r'D:\A2_ok_hist'
c = 0
lptc = 0

def get_detect_class(img,channel,save_lp,show_flag=False):
    bins = np.arange(257)
    item = img[:,:,1]
    hist,bins = np.histogram(item,bins,density=True)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center', width = width)
    plt.savefig(save_lp)
    if show_flag:
        plt.show()
    qx_qujian = hist[40:100]
    qujian_max = max(qx_qujian)
    # print('qujianmax:',qujian_max)
    max_index = list(qx_qujian).index(qujian_max)
    result_class = 0
    if channel=='14':
        if qujian_max<0.06 and qujian_max>0.053:
            result_class='0'
        else:
            result_class='1'
    else:
        print('channel1:',channel)
    return qujian_max,result_class
if not os.path.exists(save_p):
    os.makedirs(save_p)
for i in imgs:
    img = cv2.imread(i)
    name = i.split('\\')[-1]
    save_lp = os.path.join(save_p,name)
    classes_dic = {'0':'lvjixian','1':'other'}
    qujian_max,class_index = get_detect_class(img,'14',save_lp)
    print('qujianmax:{}---classname:{}'.format(qujian_max,classes_dic[class_index]))


