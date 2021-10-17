"""
@Description:
@Author     : zhangyan
@Time       : 2021/10/17 下午1:38
"""
import os.path
import shutil

import numpy
import numpy as np
import pandas as pd

input_dir = '/home/jerry/Desktop/10-17csv'
# input_dir = '/home/jerry/Desktop/10-17csv/1756-0057-16.csv'
output_dir = ''
for csv in os.listdir(input_dir):
    data = pd.read_csv(os.path.join(input_dir,csv))
    # print(data)
    np_arr = np.array(data)
    print(len(np_arr))
    if len(np_arr) > 0:
        shutil.copy(os.path.join(input_dir,csv), output_dir)
        shutil.copy(os.path.join(input_dir,csv).replace('.csv', '.jpg'), output_dir)
