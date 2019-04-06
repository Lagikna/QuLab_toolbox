import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.fftpack import fft,ifft
from scipy.signal import chirp,sweep_poly

from ._wavedata import Wavedata



class WavedataIQ(Wavedata):
    """基于wavedata类，属性data为复数，实部为I分量，虚部为Q分量，并做了相应改进"""
    def __init__(self, data = [], sRate = 1):
        super(WavedataIQ, self).__init__(data, sRate)

    ###### 以下为不支持复数的属性和方法，对它们进行覆盖，没有列出的为直接继承
    def timeFunc(self,kind='cubic'):  # 不支持复数
        return None

    @property
    def f(self): # 不支持复数
        return None

    def convolve(self, other, mode='same', norm=True): # 未定是否支持复数
        return None

    def FFT(self, mode='amp',half=True,**kw): # 未定是否支持复数
        return None

    def getFFT(self,freq,mode='complex',**kw): # 未定是否支持复数
        return None

    def high_resample(self,sRate,kind='nearest'): # 不支持复数
        return None

    def low_resample(self,sRate,kind='linear'): # 不支持复数
        return None

    def resample(self,sRate): # 不支持复数
        return None

    def normalize(self): # 不支持复数
        pass

    def plot(self, *arg, isfft=False, **kw): # 不支持复数
        pass

    def plt(self,mode='psd', r=False, **kw): # 未定是否支持复数
        pass

    ###### 以下为WavedataIQ专有的属性和方法
    @property
    def real(self):
        '''实部 返回Wavedata类'''
        w = Wavedata(np.real(self.data), self.sRate)
        return w

    @property
    def imag(self):
        '''虚部 返回Wavedata类'''
        w = Wavedata(np.imag(self.data), self.sRate)
        return w
