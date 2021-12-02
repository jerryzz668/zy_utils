"""
@Description:
@Author     : zhangyan
@Time       : 2021/11/22 下午3:53
"""
from tqdm import tqdm


nn = [15, 16, 18000000]
def inteer(a):
    if a - int(a) == 0:
        return True
    else:
        return False

for n in nn:
    count = 0
    for j in tqdm(range(1, n // 2 + 1)):
        if n/(j+1)-j/2 > 0 and inteer(n/(j+1)-j/2):
            count += 1
    print(count)