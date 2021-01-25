# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os

import functools

class Person:
    def __setitem__(self, key, value):
        print(key, value)
    