import numpy as np
from ._wavedata import *

# def WGN(w, snr):
#     '''White Gaussian Noise: 向波形w中添加一个信噪比为 snr dB 的高斯白噪声；
#     返回添加噪声后的波形，Wavedata类'''
#     assert isinstance(w,Wavedata)
#     x=w.data
#     snr = 10**(snr/10.0)
#     xpower = np.sum(x**2)/len(x)
#     npower = xpower / snr
#     n = np.random.randn(len(x)) * np.sqrt(npower)
#     data = x + n
#     return Wavedata(data,w.sRate)

class Filter(object):
    """docstring for Filter."""
    def __init__(self):
        super(Filter, self).__init__()

    def process(self,data,sRate):
        return data,sRate

    def filt(self,w):
        assert isinstance(w,Wavedata)
        data,sRate = self.process(w.data,w.sRate)
        return Wavedata(data,sRate)


class WGN(Filter):
    '''White Gaussian Noise adder: 向波形w中添加一个信噪比为 snr dB 的高斯白噪声'''
    def __init__(self, snr):
        super(WGN, self).__init__()
        self.snr = snr

    def process(self,data,sRate):
        x=data
        snr = 10**(self.snr/10.0)
        xpower = np.sum(x**2)/len(x)
        npower = xpower / snr
        n = np.random.randn(len(x)) * np.sqrt(npower)
        _data = x + n
        return _data,sRate
