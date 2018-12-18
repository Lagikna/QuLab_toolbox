import copy
import numpy as np
import matplotlib.pyplot as plt


class Wave(object):

    def __init__(self,domain=(0,1)):
        '''domain: 定义域，即采点的区域，不能是inf'''
        self.domain = domain
        self.Func = lambda x : 0
        self._shift = 0

    def _mask(self, x):
        mask = (x>self.domain[0])*(x<self.domain[1])
        return mask

    def _comb_domain(a_domain, b_domain):
        start = min(a_domain[0], b_domain[0])
        stop = max(a_domain[1], b_domain[1])
        domain = (start, stop)
        return domain

    def __pos__(self):
        return self

    def __neg__(self):
        w = copy.deepcopy(self)
        w.Func = lambda x : - self.Func(x)
        w.domain = self.domain
        return w

    def __rshift__(self, t):
        w = copy.deepcopy(self)
        w._shift = self._shift + t
        w.domain = (self.domain[0]+t, self.domain[1]+t)
        return w

    def __lshift__(self, t):
        return self >> (-t)

    def __or__(self, other):
        w = Wave((self.domain[0], self.domain[1]+other.len()))
        w.Func = lambda x: self.Func(x) * self._mask(x) + other.Func(x-self._domain[1]+other._domain[0]) * (x >= self._domain[1])
        return w
