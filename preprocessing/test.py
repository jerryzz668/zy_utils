# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


class Test:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.plus(a, b)
        self.minus(b, c)
    def plus(self, f, g):
        print(f+g)
    def minus(self, d, e):
        print(d-e)

Test(1,2,3)