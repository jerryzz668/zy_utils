# -*- coding: utf-8 -*-
# author：Xu
# datetime： 2020/9/19 8:19 
# ide：PyCharm

import numpy as np

def select_sort(Array, K):
    '''
        Time complexity: O(n^2)
    '''
    Array = Array.flatten()
    array = Array.copy().astype(float)
    l = []
    print('before sort:{}'.format(array))
    min_loc = 0
    for i in range(K):
        for j in range(0, len(array)):
            if array[j] < array[min_loc]:
                min_loc = j
        l.append(array[min_loc] )
        array[min_loc] = float('inf')
    print('K:{}'.format(l))
    # print('position:{}'.format(min_loc))
    print(min_loc)

array = np.random.randint(low=1,high=20,size=(3,3))
select_sort(array,3)

