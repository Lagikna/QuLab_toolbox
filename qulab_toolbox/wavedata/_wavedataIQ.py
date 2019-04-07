import numpy as np
import matplotlib.pyplot as plt
# from scipy import interpolate
# from scipy.fftpack import fft,ifft
# from scipy.signal import chirp,sweep_poly

from ._wavedata import *

class WavedataIQ(Wavedata):
    """基于wavedata类，针对复数做了相应改进，属性data的实部为I分量，虚部为Q分量"""

    def __init__(self, data = [], sRate = 1):
        super(WavedataIQ, self).__init__(data, sRate)

    ###### 以下为wavedata不支持复数的属性和方法，对它们进行覆盖，没有列出的为直接继承
    def timeFunc(self,kind='cubic'):  # 改进后支持复数
        '''对实部和虚部分别插值，得到复数的时间函数，默认cubic插值'''
        _timeFuncI = self.real().timeFunc(kind=kind)
        _timeFuncQ = self.imag().timeFunc(kind=kind)
        _timeFunc = lambda x: _timeFuncI(x) + 1j*_timeFuncQ(x)
        return _timeFunc

    def FFT(self,mode='amp',**kw): # 支持复数，更改默认行为
        return super(WavedataIQ, self).FFT(self,mode=mode,half=False,**kw)

    def getFFT(self,freq,mode='complex',**kw): # 支持复数，更改默认行为
        return super(WavedataIQ, self).getFFT(self,freq,mode=mode,half=False,**kw)

    def normalize(self): # 改进后支持复数
        '''归一化 取实部和虚部绝对值的最大值进行归一'''
        v_max = max(abs(np.append(np.real(self.data),np.imag(self.data))))
        self.data = self.data/v_max
        return self

    def plot(self, *arg, mode='both', isfft=False, **kw): # 改进后支持复数
        '''画图'''
        ax = plt.gca()
        if isfft:
            dt=1/self.sRate
            x = np.arange(0, self.len-dt/2, dt)
        else:
            x = self.x
        if mode == 'both':
            ax.plot(x, np.real(self.data), *arg, label='real', **kw)
            ax.plot(x, np.imag(self.data), *arg, label='imag', **kw)
        else:
            if mode == 'abs':
                data = np.abs(self.data)
            elif mode == 'angle':
                data = np.angle(self.data,deg=True)
            elif mode == 'real':
                data = np.real(self.data)
            elif mode == 'imag':
                data = np.imag(self.data)
            ax.plot(x, data, *arg, label=mode, **kw)
        plt.legend(loc = 'best')

    ###### 以下为WavedataIQ专有的属性和方法
    @property
    def I(self):
        '''I分量 即data实部'''
        return np.real(self.data)

    @property
    def Q(self):
        '''Q分量 即data虚部'''
        return np.imag(self.data)

    def real(self):
        '''实部 返回Wavedata类'''
        w = Wavedata(np.real(self.data), self.sRate)
        return w

    def imag(self):
        '''虚部 返回Wavedata类'''
        w = Wavedata(np.imag(self.data), self.sRate)
        return w

    @classmethod
    def trans(cls, wdI, wdQ=None):
        '''转化 将一个或两个Wavedata实例转化为WavedataIQ实例'''
        assert isinstance(wdI, Wavedata)
        if wdQ is None:
            _wdIQ = wdI
        else:
            assert isinstance(wdQ, Wavedata)
            _wdIQ = wdI + 1j*wdQ
        return cls(_wdIQ.data, _wdIQ.sRate)

    def itrans(self, mode='direct'):
        '''反转化 将实例自身反转化为Wavedata实例，需注意mode'''
        if mode == 'IQ':
            dataI = np.real(self.data)
            dataQ = np.imag(self.data)
            wdI = Wavedata(dataI, self.sRate)
            wdQ = Wavedata(dataQ, self.sRate)
            return wdI, wdQ
        else:
            if mode == 'abs':
                data = np.abs(self.data)
            elif mode == 'angle':
                data = np.angle(self.data,deg=True)
            elif mode == 'real':
                data = np.real(self.data)
            elif mode == 'imag':
                data = np.imag(self.data)
            elif mode == 'direct':
                data = self.data
            return Wavedata(data, self.sRate)


def DRAGpulse(width=0, sRate=1e2, a=0.5, TYPE=Gaussian2, **kw):
    '''DRAG波形 a为系数'''
    I = TYPE(width, sRate, **kw)
    Q = a*I.derivative()
    return WavedataIQ.trans(I,Q)

def DRAG_wd(wd, a=0.5):
    '''DRAG给定的Wavedata类波形'''
    assert isinstance(wd, Wavedata)
    I = wd
    Q = a*I.derivative()
    return WavedataIQ.trans(I,Q)

def Exp(w, phi=0, width=0, sRate=1e2):
    timeFunc = lambda t: np.exp(1j*(w*t+phi))
    domain=(0,width)
    return WavedataIQ.init(timeFunc,domain,sRate)
