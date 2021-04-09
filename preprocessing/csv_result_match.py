"""
description: 
author: zhangyan
date: 2021-04-07 16:57
"""

import pandas as pd
import numpy as np
import os
import cv2


def csv_to_val(csv_path):
    data = pd.read_csv(csv_path)
    data = data.iloc[:, [1, 3, 4, 5, 6, 7, 8, 9]]
    data = np.array(data)
    return data

def val_match(val1, val2):
    pass


if __name__ == '__main__':
    csv_path = r'C:\Users\Administrator\Desktop\test.csv'
    val1 = csv_to_val(csv_path=csv_path)
    print(val1)
    # val2 = csv_to_val(csv_path=None)
    # val = val_match(val1, val2)