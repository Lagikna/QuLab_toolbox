import numpy as np
from scipy import interpolate
from scipy.signal import chirp,sweep_poly
from ._wavedata import Wavedata

__all__ = ['Sin', 'Cos', 'Exp', 'DC',
    'Blank', 'Noise_wgn', 'Triangle', 'Gaussian', 'Gaussian2', 'CosPulse', 
    'Sinc', 'Interpolation', 'Chirp', 'Sweep_poly', 'DRAGpulse', 'DRAG_wd',]

### 重要的wd函数
def Sin(w, phi=0, width=0, sRate=1e2):
    '''正弦波形

    Parameters:
        w: 角频率
        phi: 相位，弧度制
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例，数据为实数类型
    '''
    timeFunc = lambda t: np.sin(w*t+phi)
    domain=(0,width)
    return Wavedata.init(timeFunc,domain,sRate)

def Cos(w, phi=0, width=0, sRate=1e2):
    '''余弦波形

    Parameters:
        w: 角频率
        phi: 相位，弧度制
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例，数据为实数类型
    '''
    timeFunc = lambda t: np.cos(w*t+phi)
    domain=(0,width)
    return Wavedata.init(timeFunc,domain,sRate)

def Exp(w, phi=0, width=0, sRate=1e2):
    '''IQ类型 复数正弦信号

    Parameters:
        w: 角频率
        phi: 相位，弧度制
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例，数据为复数类型
    '''
    timeFunc = lambda t: np.exp(1j*(w*t+phi))
    domain=(0,width)
    return Wavedata.init(timeFunc,domain,sRate)

def DC(width=0, sRate=1e2, phi=0):
    '''方波，可以设相位参数，默认为0

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
        phi: 相位，弧度单位
    Return:
        Wavedata类实例
    '''
    # 这里确保phi=0时，数据值为实数而不是复数类型
    timeFunc = lambda x: 1 if phi==0 else np.exp(1j*phi)
    domain=(0, width)
    return Wavedata.init(timeFunc,domain,sRate)


### 非IQ类型
def Blank(width=0, sRate=1e2):
    '''空波形

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例
    '''
    timeFunc = lambda x: 0
    domain=(0, width)
    return Wavedata.init(timeFunc,domain,sRate)

def Noise_wgn(width=0, sRate=1e2):
    '''产生高斯白噪声序列，注意序列未归一化

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例'''
    size = np.around(width * sRate).astype(int)
    data = np.random.randn(size)
    return Wavedata(data,sRate)

def Triangle(width=1, sRate=1e2):
    '''三角波

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例'''
    timeFunc = lambda x: 0 if width==0 else 1-np.abs(2/width*x)
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def Gaussian(width=1, sRate=1e2):
    '''高斯波形

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例'''
    c = width/(4*np.sqrt(2*np.log(2)))
    timeFunc = lambda x: np.exp(-0.5*(x/c)**2)
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def Gaussian2(width=1,sRate=1e2,a=5):
    '''修正的高斯波形

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
        a: 波形宽度width和方差的比值
    Return:
        Wavedata类实例'''
    c = width/a # 方差
    # 减去由于截取造成的台阶, 使边缘为0, 并归一化
    y0 = np.exp(-0.5*(width/2/c)**2)
    timeFunc = lambda x: (np.exp(-0.5*(x/c)**2)-y0)/(1-y0)
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def CosPulse(width=1, sRate=1e2):
    '''余弦包络波形

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
    Return:
        Wavedata类实例'''
    timeFunc = lambda x: 0 if width==0 else (np.cos(2*np.pi/width*x)+1)/2
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def Sinc(width=1, sRate=1e2, a=1):
    '''Sinc函数波形

    Parameters:
        width: 波形宽度参数
        sRate: 采样率
        a: Sinc函数系数
    Return:
        Wavedata类实例'''
    timeFunc = lambda t: np.sinc(a*t)
    domain=(-0.5*width,0.5*width)
    return Wavedata.init(timeFunc,domain,sRate)

def Interpolation(x, y, sRate=1e2, kind='linear'):
    '''参考scipy.interpolate.interp1d 插值'''
    timeFunc = interpolate.interp1d(x, y, kind=kind)
    domain = (x[0], x[-1])
    return Wavedata.init(timeFunc,domain,sRate)

def Chirp(f0, f1, width, sRate=1e2, phi=0, method='linear'):
    '''参考scipy.signal.chirp 啁啾'''
    t1 = width # 结束点
    timeFunc = lambda t: chirp(t, f0, t1, f1, method=method, phi=phi, )
    domain = (0,t1)
    return Wavedata.init(timeFunc,domain,sRate)

def Sweep_poly(poly, width, sRate=1e2, phi=0):
    '''参考scipy.signal.sweep_poly 多项式频率'''
    timeFunc = lambda t: sweep_poly(t, poly, phi=0)
    domain = (0,width)
    return Wavedata.init(timeFunc,domain,sRate)


### IQ类型
def DRAGpulse(width=0, sRate=1e2, a=0.5, TYPE=CosPulse, **kw):
    '''IQ类型 DRAG波形,a为系数'''
    I = TYPE(width, sRate, **kw)
    Q = a*I.derivative()
    return I+1j*Q

def DRAG_wd(wd, a=0.5):
    '''IQ类型 DRAG给定的Wavedata类波形'''
    assert isinstance(wd, Wavedata)
    assert not wd.isIQ
    I = wd
    Q = a*I.derivative()
    return I+1j*Q
