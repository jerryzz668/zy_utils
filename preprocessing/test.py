# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os

train_path = '/Users/zhangyan/Desktop/a件_0830damian/0830img/train/imgs'
PR_path = '/Users/zhangyan/Desktop/a件_0830damian/0830img/train/imgs/PR'

train_files = os.listdir(train_path)
PR_files = os.listdir(PR_path)

tra = []
PR = []

for file in train_files:
    tra.append(file)
for file in PR_files:
    PR.append(file)

result = [d for d in tra if d not in PR]
print(result)