# from hashlib import sha256
# import random
# l = 'wcncc'.encode()
# salt = 'asd'.encode()
# sha = sha256(l+salt)
# print(sha.hexdigest())
# sha.hexdigest()
# # print(random.randint(1,9))
# print(int('市',16))
# v=1
# a=1
# print(v is a)
# l=['a','b','c']
# s=['a','b','c']
# print(l is s)
# print(l[5:])
# a= 'asdasd'
# for i in a:
#     print(i)
# print(a.__next__())
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class A(object):
    a = 1

    def __init__(self, x=0):
        self.x = x


a1 = A(2)
a2 = A(3)
print(a1)