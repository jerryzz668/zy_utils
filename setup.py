"""
@Description:
@Author     : zhangyan
@Time       : 2021/7/1 下午5:25
"""
import os.path

from setuptools import setup, find_packages
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

setup(
    name="utils",
    version="1.0",
    author="jerry",
    author_email="jerryzz668@163.com",
    description="Stay true  -->公众号：Codejerry",

    # 项目主页
    url="https://gitee.com/jerry/zy_utils",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)