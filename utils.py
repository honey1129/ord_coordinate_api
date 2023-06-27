# -*- coding:utf-8 -*-
"""
Author: honey1129
Created time:2023/6/27 17:30
"""


def array_diff(a: list, b: list) -> list:
    c = []
    for i in a:
        if i not in b:
            c.append(i)
    return c


# 调用方法，传入列表
array_diff([1, 2], [1])

if __name__ == '__main__':
    pass
