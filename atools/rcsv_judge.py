"""
@Description:
@Author     : zhangyan
@Time       : 2021/10/17 下午1:38
"""
import os.path
import shutil
import glob
import numpy
import numpy as np
import pandas as pd

input_dir = '/home/jerry/Desktop/garbage/csv'
# input_dir = '/home/jerry/Desktop/10-17csv/1756-0057-16.csv'
output_dir = ''
csv_list = glob.glob('{}/*.csv'.format(input_dir))
for csv in csv_list:
    df = pd.read_csv(csv)
    class_name = df.iloc[:, 3]
    np_arr = np.array(class_name)
    class_num = list(set(np_arr))
    if 'jiaodaowen2' in class_num:
        shutil.copy(csv, output_dir)
        shutil.copy(csv.replace('.csv', '.jpg'), output_dir)

    # if len(np_arr) > 0:
    #     shutil.copy(csv, output_dir)
    #     shutil.copy(csv.replace('.csv', '.jpg'), output_dir)
