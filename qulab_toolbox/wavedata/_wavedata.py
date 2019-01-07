import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft

__all__ = ['Wavedata', 'Blank', 'DC', 'Gaussian', 'CosPulse', 'Sin', 'Cos',]

class Wavedata(object):

    def __init__(self, data = [], sRate = 1):
        self.data = np.array(data)
        self.sRate = sRate

    @staticmethod
    def generateData(timeFunc, domain=(0,1), sRate=1e2):
        length = int(np.around(abs(domain[1]-domain[0]) * sRate)) / sRate
        _domain = min(domain), (min(domain)+length)
        dt=1/sRate
        _timeFunc = lambda x: timeFunc(x) * (x > _domain[0]) * ( x < _domain[1])
        x = np.arange(_domain[0]+dt/2, _domain[1], dt)
        data = np.array(_timeFunc(x))
        return data

    @classmethod
    def init(cls, timeFunc, domain=(0,1), sRate=1e2):
        data = cls.generateData(timeFunc,domain,sRate)
        return cls(data,sRate)

    def _blank(self,length=0):
        n = int(np.around(abs(length)*self.sRate))
        data = np.zeros(n)
        return data

    @property
    def x(self):
        dt=1/self.sRate
        x = np.arange(dt/2, self.len, dt)
        return x

    @property
    def len(self):
        length = self.size/self.sRate
        return length

    @property
    def size(self):
        size = len(self.data)
        return size

    def setLen(self,length):
        n = int(np.around(abs(length)*self.sRate))
        return self.setSize(n)

    def setSize(self,size):
        n = int(np.around(size))
        s = self.size
        if n > s:
            append_data=np.zeros(n-s)
            self.data = np.append(self.data, append_data)
        else:
            self.data = self.data[:n]
        return self

    def __pos__(self):
        return self

    def __neg__(self):
        w = Wavedata()
        w.sRate = self.sRate
        w.data = -self.data
        return w

    def __abs__(self):
        w = Wavedata()
        w.sRate = self.sRate
        w.data = np.abs(self.data)
        return w

    def __rshift__(self, t):
        if abs(t)>self.len:
            raise Error('shift is too large !')
        w = Wavedata()
        w.sRate = self.sRate
        shift_data=self._blank(abs(t))
        left_n = self.size-len(shift_data)
        if t>0:
            w.data = np.append(shift_data, self.data[:left_n])
        else:
            w.data = np.append(self.data[-left_n:], shift_data)
        return w

    def __lshift__(self, t):
        return self >> (-t)

    def __or__(self, other):
        if not isinstance(other,Wavedata):
            raise TypeError('not Wavedata class !')
        elif not self.sRate == other.sRate:
            raise Error('sRate not equal !')
        else:
            w = Wavedata()
            w.sRate = self.sRate
            w.data = np.append(self.data,other.data)
            return w

    def __add__(self, other):
        if isinstance(other,Wavedata):
            if not self.sRate == other.sRate:
                raise Error('sRate not equal !')
            else:
                w = Wavedata()
                w.sRate = self.sRate
                size = max(self.size, other.size)
                self.setSize(size)
                other.setSize(size)
                w.data = self.data + other.data
                return w
        else:
            return other + self

    def __radd__(self, v):
        w = Wavedata()
        w.sRate = self.sRate
        w.data = self.data +v
        return w

    def __sub__(self, other):
        return self + (- other)

    def __rsub__(self, v):
        return v + (-self)

    def __mul__(self, other):
        if isinstance(other,Wavedata):
            if not self.sRate == other.sRate:
                raise Error('sRate not equal !')
            else:
                w = Wavedata()
                w.sRate = self.sRate
                size = max(self.size, other.size)
                self.setSize(size)
                other.setSize(size)
                w.data = self.data * other.data
                return w
        else:
            return other * self

    def __rmul__(self, v):
        w = Wavedata()
        w.sRate = self.sRate
        w.data = self.data * v
        return w

    def __truediv__(self, other):
        if isinstance(other,Wavedata):
            if not self.sRate == other.sRate:
                raise Error('sRate not equal !')
            else:
                w = Wavedata()
                w.sRate = self.sRate
                size = max(self.size, other.size)
                self.setSize(size)
                other.setSize(size)
                w.data = self.data / other.data
                return w
        else:
            return (1/other) * self

    def __rtruediv__(self, v):
        w = Wavedata()
        w.sRate = self.sRate
        w.data = v / self.data
        return w

    def convolve(self, other, mode='same'):
        '''mode: full, same, valid'''
        if isinstance(other,Wavedata):
            _kernal = other.data
        elif isinstance(other,(np.ndarray,list)):
            _kernal = np.array(other)
        k_sum = sum(_kernal)
        kernal = _kernal / k_sum
        w = Wavedata()
        w.sRate = self.sRate
        w.data = np.convolve(self.data,kernal,mode)
        return w

    def FFT(self, mode='amp'):
        w = Wavedata()
        w.sRate = self.size/self.sRate
        if mode == 'amp':
            w.data =np.abs(fft(self.data))
        elif mode == 'phase':
            w.data =np.angle(fft(self.data),deg=True)
        elif mode == 'real':
            w.data =np.real(fft(self.data))
        elif mode == 'imag':
            w.data =np.imag(fft(self.data))
        elif mode == 'complex':
            w.data =fft(self.data)
        return w

    def plot(self, *arg, fft=False, **kw):
        ax = plt.gca()
        # 对于FFT变换后的波形数据，使用fft=True会去除了x的偏移，画出的频谱更准确
        if fft:
            dt=1/self.sRate
            x = np.arange(0, self.len-dt/2, dt)
            ax.plot(x, self.data, *arg, **kw)
        else:
            ax.plot(self.x, self.data, *arg, **kw)


def Blank(width=0, sRate=1e2):
    timeFunc = lambda x: 0
    domain=(0, width)
    return Wavedata.init(timeFunc,domain,sRate)

def DC(width=0, sRate=1e2):
    timeFunc = lambda x: 1
    domain=(0, width)
    return Wavedata.init(timeFunc,domain,sRate)

def Gaussian(width=1, sRate=1e2):
    c = width/(4*np.sqrt(2*np.log(2)))
    timeFunc = lambda x: np.exp(-0.5*(x/c)**2)
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def CosPulse(width=1, sRate=1e2):
    timeFunc = lambda x: (np.cos(2*np.pi/width*x)+1)/2
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def Sin(w, phi=0, width=0, sRate=1e2):
    timeFunc = lambda t: np.sin(w*t+phi)
    domain=(0,width)
    return Wavedata.init(timeFunc,domain,sRate)

def Cos(w, phi=0, width=0, sRate=1e2):
    timeFunc = lambda t: np.cos(w*t+phi)
    domain=(0,width)
    return Wavedata.init(timeFunc,domain,sRate)


if __name__ == "__main__":
    a=Sin(w=1, width=10, phi=0, sRate=1000)
    b=Gaussian(2,sRate=1000)
    c=Blank(1,sRate=1000)

    m=(0.5*a|c|b|c|b+1|c|a+0.5).setLen(20)>>5
    n=m.convolve(b)
    m.plot()
    n.plot()
    plt.show()
