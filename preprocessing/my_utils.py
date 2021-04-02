"""
description: my dependent utils
author: zhangyan
date: 2021-04-02 17:42
"""

import os

def mkdir(save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
