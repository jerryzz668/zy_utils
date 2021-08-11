"""
@Description:
@Author     : zhangyan
@Time       : 2021/8/11 下午12:24
"""

import cv2
# 一寸413*295

def xywh_to_yicun(face_rec, img_w, img_h):
    x, y, w, h = face_rec[0]
    yicun_x = x - w//2
    yicun_y = y - h//2
    yicun_w = 2*w
    yicun_h = 2*h + h//4
    if yicun_x < 0: yicun_x = 3
    if yicun_y < 0: yicun_y = 3
    if yicun_w > img_w: yicun_w = img_w-8
    if yicun_h > img_h: yicun_h = img_h-8
    return [yicun_x, yicun_y, yicun_w, yicun_h]

img = cv2.imread("/home/jerry/Desktop/angle.jpeg")
img_h, img_w = img.shape[0], img.shape[1]
print(img_w,img_h)
classfier = cv2.CascadeClassifier('/home/jerry/anaconda3/envs/yolo/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
face_rec = classfier.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))
print(face_rec)
if len(face_rec) == 1:  # 大于0则检测到人脸
    x, y, w, h = xywh_to_yicun(face_rec, img_w, img_h)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  # 3控制绿色框的粗细

# cv2.imwrite('output.jpg', img)
cv2.namedWindow('Find Faces!', 0)
cv2.imshow("Find Faces!", img)
cv2.waitKey(0)