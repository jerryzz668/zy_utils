"""
description: my dependent utils
author: zhangyan
date: 2021-04-02 17:42
"""

import os
import json

def mkdir(save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)


def json_to_instance(json_file_path):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance
