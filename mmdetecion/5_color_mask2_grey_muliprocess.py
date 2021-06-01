import os
import cv2
import multiprocessing
import time
def save_label(i):
    img_p,save_p = i
    img = cv2.imread(img_p)
    img0 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(save_p, img0)
    print('正在保存：',save_p)

if __name__ == '__main__':
    labelf1_rgb= r"/Users/zhangyan/Desktop/train_mask"
    labelf1_gray = r"/Users/zhangyan/Desktop/coco/stuffthingmaps/train2017"
    ls = []
    for i in os.listdir(labelf1_rgb):
        img_p = os.path.join(labelf1_rgb, i)
        save_p = os.path.join(labelf1_gray, i)
        ls.append((img_p,save_p))
    pool = multiprocessing.Pool(processes=16)
    start_time = time.time()
    pool.map(save_label,ls)
    print('run time:',time.time()-start_time)
    pool.close()
    pool.join()