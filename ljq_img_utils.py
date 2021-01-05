import numpy as np
import cv2
from pycocotools.mask import decode

#mask转二值图 黑白两色
def mask2bw(mask):
    # print('mask_shape',mask)
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            if mask[i][j]==1:
                mask[i][j]=255
    return mask
#提取二值图轮廓
def getContoursBinary(blimg):
    ret, binary = cv2.threshold(blimg, 127, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
#获取图像内容
def getReadImg(img_path):
    img = cv2.imread(img_path)
    return img
#提取二值图轮廓
def getContoursBinary(blimg):
    ret, binary = cv2.threshold(blimg, 127, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
#提取二值图轮廓并将轮廓画在原图上
def drawContours2Img(img,contours,save_path=None):
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
    if save_path:
        cv2.imwrite(save_path, img)
    return img
#显示图
def playImg(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
#保存图
def saveImg(img,save_path):
    cv2.imwrite(save_path, img)
#coco格式图像的分割标注转label图
def cocoSeg2LabelMask(segmentation,save_path=None):
    img = decode(segmentation)
    if save_path:
        saveImg(img, save_path)
    return img
#seg2sourceimg
def seg2sourceimg(seg,img):
    # print('seg',seg)
    mask = cocoSeg2LabelMask(seg)
    mask = mask2bw(mask)
    contours= getContoursBinary(mask)
    img = drawContours2Img(img, contours)
    return img

#coco 分割结果转mask  "segmentation": {"size": [1024, 1024], "counts": "enmg08fo03N3M2N2O1O000000000000000000O2N2N2N^Q_7"}
# dic_seg = {"size": [1024, 1024], "counts": "enmg08fo03N3M2N2O1O000000000000000000O2N2N2N"}
# mask = decode(dic_seg)
# print('mask',np.shape(mask))
# img_p = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\guashang\result\0336-0001-14616_3292_1640_4316.jpg'
# save_path = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\guashang\result\ljq.jpg'
# mask = mask2bw(mask)
# contours= getContoursBinary(mask)
# img=getReadImg(img_p)
# drawContours2Img(img,contours,save_path)
# playImg(img)




