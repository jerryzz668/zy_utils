import os
import os.path as osp
import re
from crop import Cropper

# print ("os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__)))

cropper  = Cropper(None)
cropper.CreateBoundingBox(os.path.dirname(os.path.realpath(__file__)), os.path.dirname(os.path.realpath(__file__))+'/cropped', 'whitecat_0_1.jpg', True,  "0", None)