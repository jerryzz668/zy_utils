"""
@Description:
@Author     : zhangyan
@Time       : 2021/11/22 下午3:53
"""

a,b = 7,5


def gcd(a,b):
    if a%b==0:
        return b
    elif b%a==0:
        return a
    elif a>b:
        return gcd(a%b, b)
    elif b>a:
        return gcd(b%a, a)

for i in range(2, b+1):
    gcd_result = gcd(a,b)
    print(int(i/gcd_result))