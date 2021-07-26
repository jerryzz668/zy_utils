# -*- coding: utf-8 -*-
# author：Xu
# datetime： 2020/9/17 20:30 
# ide：PyCharm

import cv2
import os

path = r'D:\project\tools\img'
cameraCapture = cv2.VideoCapture(r"D:\project\tools\Fog20200313000026.mp4")

success, frame = cameraCapture.read()
# cv2.imwrite(os.path.join(path, '{}.jpg'.format(0)), frame)
c = 1
while success:
    # if cv2.waitKey(1) == 27:
    #     break
    # cv2.imshow('Test camera', frame)
    success, frame = cameraCapture.read()
    milliseconds = cameraCapture.get(cv2.CAP_PROP_POS_MSEC)
    seconds = milliseconds//1000

    milliseconds = milliseconds%1000
    if (seconds-4) % 15 == 0 and milliseconds == 40:
        cv2.imwrite(os.path.join(path,'{}.jpg'.format(c)),frame)
        c += 1
    minutes = 0
    hours = 0


    if seconds >= 60:
        minutes = seconds//60
        seconds = seconds % 60

    if minutes >= 60:
        hours = minutes//60
        minutes = minutes % 60

    print(int(hours), int(minutes), int(seconds), int(milliseconds))

cv2.destroyAllWindows()
cameraCapture.release()