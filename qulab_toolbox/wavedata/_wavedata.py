import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.fftpack import fft,ifft

__all__ = ['Wavedata', 'WavedataN']

class Wavedata(object):

    def __init__(self, data = [], sRate = 1):
        '''给定序列和采样率，构造Wavedata'''
        self.__data = np.asarray(data)#.flatten()
        # assert self.__data.ndim==1
        self.__sRate = sRate

    @property
    def data(self):
        '''只读'''
        return self.__data

    @property
    def sRate(self):
        '''只读'''
        return self.__sRate

    @staticmethod
    def generateData(timeFunc, domain=(0,1), sRate=1e2):
        '''给定函数、定义域、采样率，生成data序列'''
        length = np.around(abs(domain[1]-domain[0]) * sRate).astype(int) / sRate
        _domain = min(domain), (min(domain)+length)
        dt = 1/sRate
        _timeFunc = lambda x: timeFunc(x) * (x > _domain[0]) * ( x < _domain[1])
        x = np.arange(_domain[0]+dt/2, _domain[1], dt)
        data = np.array(_timeFunc(x))
        return data

    @classmethod
    def init(cls, timeFunc, domain=(0,1), sRate=1e2):
        '''给定函数、定义域、采样率，生成Wavedata类'''
        data = cls.generateData(timeFunc,domain,sRate)
        return cls(data,sRate)

    @property
    def isIQ(self):
        '''是否为IQ类型 即data是否包含复数'''
        return np.any(np.iscomplex(self.data))

    @property
    def x(self):
        '''返回波形的时间列表'''
        dt=1/self.sRate
        x = np.arange(dt/2, self.len, dt)
        return x

    @property
    def f(self): # 支持复数与timeFunc一致
        '''返回根据属性data进行cubic类型插值得到的时间函数'''
        f = self.timeFunc(kind='cubic')
        return f

    @property
    def len(self):
        '''返回波形长度'''
        length = self.size/self.sRate
        return length

    def __getattr__(self,item):
        if item in ['real','imag','size']: # ndarray attribute
            return getattr(self.data,item)
        elif item in ['max','min','argmax','argmin','clip',
            'conj','mean','ptp','round','std','sum']: # ndarray method
            return getattr(self.data,item)
        else:
            raise AttributeError('No such attribute!')

    def I(self):
        '''I波形 返回Wavedata类'''
        wd = self.__class__(np.real(self.data), self.sRate)
        return wd

    def Q(self):
        '''Q波形 返回Wavedata类'''
        wd = self.__class__(np.imag(self.data), self.sRate)
        return wd

    def trans(self,mode='self'):
        '''对于IQ波形转化成其他几种格式'''
        if mode == 'self':
            data = self.data
        elif mode in ['amp','abs']: #振幅或绝对值
            data = np.abs(self.data)
        elif mode in ['phase','angle']: #相位或辐角
            data = np.angle(self.data,deg=True)
        elif mode == 'real': #实部
            data = np.real(self.data)
        elif mode == 'imag': #虚部
            data = np.imag(self.data)
        elif mode == 'conj': #复共轭
            data = np.conj(self.data)
        elif mode == 'exchange': #交换实部和虚部
            data = 1j*np.conj(self.data)
        wd = self.__class__(data, self.sRate)
        return wd

    def timeFunc(self,kind='cubic'):
        '''返回波形插值得到的时间函数，默认cubic插值'''
        #为了更好地插值，在插值序列x/y前后各加一个点，增大插值范围
        dt = 1/self.sRate
        x = np.arange(-dt/2, self.len+dt, dt)
        _y = np.append(0,self.data)
        y = np.append(_y,0)
        if self.isIQ:
            _timeFuncI = interpolate.interp1d(x,np.real(y),kind=kind,
                            bounds_error=False,fill_value=(0,0))
            _timeFuncQ = interpolate.interp1d(x,np.imag(y),kind=kind,
                            bounds_error=False,fill_value=(0,0))
            _timeFunc = lambda x: _timeFuncI(x) + 1j*_timeFuncQ(x)
        else:
            _timeFunc = interpolate.interp1d(x,y,kind=kind,
                            bounds_error=False,fill_value=(0,0))
        return _timeFunc

    def append(self,left=0,right=0):
        '''在data左右两侧补相应数量的0

        Parameters:
            left: 左侧补零数量
            right: 右侧补零数量
        Return:
            一个新的Wavedata类实例'''
        left = np.around(left).astype(int)
        append_left=np.zeros(left)
        _data = np.append(append_left, self.data)
        right = np.around(right).astype(int)
        append_right=np.zeros(right)
        data = np.append(_data, append_right)
        wd = self.__class__(data, self.sRate)
        return wd

    def appendLen(self,left=0,right=0):
        '''在data左右两侧补相应时间长度数量的0

        Parameters:
            left: 左侧补零长度
            right: 右侧补零长度
        Return:
            一个新的Wavedata类实例'''
        left = np.around(left*self.sRate).astype(int)
        right = np.around(right*self.sRate).astype(int)
        return self.append(left,right)

    def setRange(self,a,b):
        '''设置波形点数范围，与切片规则一致'''
        a = np.around(a).astype(int)
        b = np.around(b).astype(int)
        data=self.data[a:b]
        wd = self.__class__(data, self.sRate)
        return wd

    def setRangeLen(self,a,b):
        '''设置波形长度范围，'''
        a = np.around(a*self.sRate).astype(int)
        b = np.around(b*self.sRate).astype(int)
        return self.setRange(a,b)

    def setSize(self,size):
        '''绝对值表示设置点数，增多补0，减少截取，正负号表示设置方向

        Parameters:
            size: 大小表示设置的点数，正负号表示方向，即负数表示从末尾开始，沿负方向计算点数
        '''
        pos_dirction=True if size>=0 else False
        size=np.around(np.abs(size)).astype(int)
        if size<=self.size:
            if pos_dirction:
                return self.setRange(0,size)
            else:
                return self.setRange(self.size-size,self.size)
        else:
            if pos_dirction:
                return self.append(0,size-self.size)
            else:
                return self.append(size-self.size,0)

    def setLen(self,length):
        '''绝对值表示设置长度，增大补0，减小截取，正负号表示设置方向
        
        Parameters:
            length: 设置的长度，正负号表示设置方向
        '''
        size = np.around(length*self.sRate).astype(int)
        return self.setSize(size)

    def __len__(self):
        '''len(wd) 返回点数'''
        return self.size

    def __call__(self, t):
        '''wd(t) 返回某个时间点的最近邻值'''
        dt = 1/self.sRate
        idx = np.around(t/dt-0.5).astype(int)
        return self.data[idx]

    def __pos__(self):
        '''正 +wd'''
        return self

    def __neg__(self):
        '''负 -wd'''
        wd = self.__class__(-self.data, self.sRate)
        return wd

    def __abs__(self):
        '''绝对值 abs(wd)'''
        wd = self.__class__(np.abs(self.data), self.sRate)
        return wd

    def __rshift__(self, t):
        '''右移 wd>>t 长度不变'''
        t=float(t)
        if abs(t)>self.len:
            raise TypeError('shift is too large !')
        n = np.around(abs(t)*self.sRate).astype(int)
        shift_data = np.zeros(n)
        left_n = self.size-n
        if t>0:
            data = np.append(shift_data, self.data[:left_n])
        else:
            data = np.append(self.data[-left_n:], shift_data)
        wd = self.__class__(data, self.sRate)
        return wd

    def __lshift__(self, t):
        '''左移 wd<<t 长度不变'''
        t=float(t)
        return self >> (-t)

    def __or__(self, other):
        '''或 wd|o 串联波形'''
        assert isinstance(other,Wavedata)
        assert self.sRate == other.sRate
        data = np.append(self.data,other.data)
        wd = self.__class__(data, self.sRate)
        return wd

    def __xor__(self, n):
        '''异或 wd^n 串联n个波形，n<=0时输出空波形'''
        n = np.around(n).astype(int)
        if n <= 0:
            data=[]
        else:
            data = list(self.data)*n
        wd = self.__class__(data, self.sRate)
        return wd

    def __pow__(self, v):
        '''幂 wd**v 波形值的v次幂'''
        data = self.data ** v
        wd = self.__class__(data, self.sRate)
        return wd

    def __add__(self, other):
        '''加 wd+o 波形值相加
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        if isinstance(other,Wavedata):
            assert self.sRate == other.sRate
            size = max(self.size, other.size)
            data_self = np.append(self.data, np.zeros(size-self.size))
            data_other = np.append(other.data, np.zeros(size-other.size))
            data = data_self + data_other
            wd = self.__class__(data, self.sRate)
            return wd
        else:
            return other + self

    def __radd__(self, v):
        '''加 v+wd 波形值加v
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        data = self.data + v
        wd = self.__class__(data, self.sRate)
        return wd

    def __sub__(self, other):
        '''减 wd-o 波形值相减
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        return self + (- other)

    def __rsub__(self, v):
        '''减 v-wd 波形值相减
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        return v + (-self)

    def __mul__(self, other):
        '''乘 wd*o 波形值相乘
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        if isinstance(other,Wavedata):
            assert self.sRate == other.sRate
            size = max(self.size, other.size)
            data_self = np.append(self.data, np.zeros(size-self.size))
            data_other = np.append(other.data, np.zeros(size-other.size))
            data = data_self * data_other
            wd = self.__class__(data, self.sRate)
            return wd
        else:
            return other * self

    def __rmul__(self, v):
        '''乘 v*wd 波形值相乘
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        data = self.data * v
        wd = self.__class__(data, self.sRate)
        return wd

    def __truediv__(self, other):
        '''除 wd/o 波形值相除
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        if isinstance(other,Wavedata):
            assert self.sRate == other.sRate
            size = max(self.size, other.size)
            data_self = np.append(self.data, np.zeros(size-self.size))
            data_other = np.append(other.data, np.zeros(size-other.size))
            data = data_self / data_other
            wd = self.__class__(data, self.sRate)
            return wd
        else:
            return (1/other) * self

    def __rtruediv__(self, v):
        '''除 v/wd 波形值相除
        Parameters:
            other/v: 可以为Wavedata类或者数值；如果为np.ndarray，则会造成另一种行为
        '''
        data = v / self.data
        wd = self.__class__(data, self.sRate)
        return wd

    def convolve(self, other, mode='same', norm=True):
        '''卷积
        Parameters:
            mode: full, same, valid
        '''
        if isinstance(other,Wavedata):
            _kernal = other.data
        elif isinstance(other,(np.ndarray,list)):
            _kernal = np.array(other)
        if norm:
            k_sum = sum(_kernal)
            kernal = _kernal / k_sum   #归一化kernal，使卷积后的波形总幅度不变
        else:
            kernal = _kernal
        data = np.convolve(self.data,kernal,mode)
        wd = self.__class__(data, self.sRate)
        return wd

    def FFT(self, mode='complex', half=False, **kw): # 支持复数，需做调整
        '''FFT, 默认形式为直接FFT变换；
        data为实数序列, 可以只取一半结果, 为实际物理频谱'''
        sRate = self.size/self.sRate
        # 对于实数序列的FFT，正负频率的分量是相同的
        # 对于双边谱，即包含负频率成分的，除以size N 得到实际振幅
        # 对于单边谱，即不包含负频成分，实际振幅是正负频振幅的和，
        # 所以除了0频成分其他需要再乘以2
        fft_data = fft(self.data,**kw)/self.size
        if mode in ['amp','abs']:
            data = np.abs(fft_data)
        elif mode in ['phase','angle']:
            data = np.angle(fft_data,deg=True)
        elif mode == 'real':
            data = np.real(fft_data)
        elif mode == 'imag':
            data = np.imag(fft_data)
        elif mode == 'complex':
            data = fft_data
        if half:
            #size N为偶数时，取N/2；为奇数时，取(N+1)/2
            index = int((len(data)+1)/2)-1
            data = data[:index]
            data[1:] = data[1:]*2 #非0频成分乘2
        wd = self.__class__(data, sRate)
        return wd

    def getFFT(self,freq,mode='complex',half=False,**kw):
        ''' 获取指定频率的FFT分量；
        freq: 为一个频率值或者频率的列表，
        返回值: 是对应mode的一个值或列表'''
        freq_array=np.array(freq)
        fft_wd = self.FFT(mode=mode,half=half,**kw)
        index_freq = np.around(freq_array*fft_wd.sRate).astype(int)
        res_array = fft_wd.data[index_freq]
        return res_array

    def high_resample(self,sRate,kind='nearest'): # 复数支持与timeFunc一致
        '''提高采样率重新采样'''
        assert sRate > self.sRate
        timeFunc = self.timeFunc(kind=kind)
        domain = (0,self.len)
        wd = self.init(timeFunc,domain,sRate)
        return wd

    def low_resample(self,sRate,kind='linear'): # 复数支持与timeFunc一致
        '''降低采样率重新采样'''
        assert sRate < self.sRate
        timeFunc = self.timeFunc(kind=kind)
        domain = (0,self.len)
        wd = self.init(timeFunc,domain,sRate)
        return wd

    def resample(self,sRate): # 复数支持与timeFunc一致
        '''改变采样率重新采样'''
        if sRate == self.sRate:
            return self
        elif sRate > self.sRate:
            return self.high_resample(sRate)
        elif sRate < self.sRate:
            return self.low_resample(sRate)

    def normalize(self):
        '''归一化 取实部和虚部绝对值的最大值进行归一，使分布在(-1,+1)'''
        v_max = max(abs(np.append(np.real(self.data),np.imag(self.data))))
        data = self.data/v_max
        wd = self.__class__(data, self.sRate)
        return wd

    def derivative(self):
        '''求导，点数不变'''
        y1=np.append(0,self.data[:-1])
        y2=np.append(self.data[1:],0)
        diff_data = (y2-y1)/2 #差分数据，间隔1个点做差分
        data = diff_data*self.sRate #导数，差分值除以 dt
        wd = self.__class__(data,self.sRate)
        return wd

    def integrate(self):
        '''求积分，点数不变'''
        cumsum_data = np.cumsum(self.data) #累积
        data = cumsum_data/self.sRate #积分，累积值乘以 dt
        wd = self.__class__(data,self.sRate)
        return wd

    def process(self,func,**kw): # 根据具体情况确定是否支持复数
        '''处理，传入一个处理函数func, 输入输出都是(data,sRate)格式'''
        data,sRate = func(self.data,self.sRate,**kw) # 接受额外的参数传递给func
        return self.__class__(data,sRate)

    def filter(self,filter): # 根据具体情况确定是否支持复数
        '''调用filter的process函数处理；
        一般filter是本模块里的Filter类'''
        assert hasattr(filter,'process')
        wd = self.process(filter.process)
        return wd

    def plot(self, fmt1='', fmt2='--', isfft=False, ax=None, **kw):
        '''对于FFT变换后的波形数据，包含0频成分，x从0开始；
        使用isfft=True会去除了x的偏移，画出的频谱更准确'''
        if ax is None:
            ax = plt.gca()
        if isfft:
            dt=1/self.sRate
            x = np.arange(0, self.len-dt/2, dt)
        else:
            x = self.x
        if self.isIQ:
            # ax.set_title('Wavedata-IQ')
            line1, = ax.plot(x, self.real, fmt1, label='real', **kw)
            line2, = ax.plot(x, self.imag, fmt2, label='imag', **kw)
            # plt.legend(loc = 'best')
            return [line1, line2]
        else:
            # ax.set_title('Wavedata')
            line1, = ax.plot(x, self.real, fmt1, **kw)
            return [line1, ]

    def plt(self, mode='psd', r=False, **kw): # 支持复数，需要具体了解
        '''调用pyplot里与频谱相关的函数画图
        mode 可以为 psd,specgram,magnitude_spectrum,angle_spectrum,
        phase_spectrum等5个(cohere,csd需要两列数据，这里不支持)'''
        _ = plt.gca()
        plt_func = getattr(plt,mode)
        res = plt_func(x=self.data,Fs=self.sRate,**kw)
        if r:
            return res


class WavedataN(object):
    """docstring for WavedataN."""

    def __init__(self, array=None):
        _array = np.array(array)
        # 对传入的序列进行处理，使所有元素都是Wavedata类
        __array=np.where(np.frompyfunc(isinstance,2,1)(_array,Wavedata),_array,Wavedata())
        self.__array = __array

    @property
    def array(self):
        return self.__array

    def vectorize(self,pyfunc,**kw):
        return np.vectorize(pyfunc,**kw)(self.array)

    def __getattr__(self,item):
        if item in ['sRate','isIQ','f','len','size',]:
            pyfunc=lambda wd: getattr(wd,item)
            return self.vectorize(pyfunc)
        elif item in ['data','x','real','imag']:
            pyfunc=lambda wd: getattr(wd,item)
            return self.vectorize(pyfunc,otypes=[object])
        elif item in ['shape','ndim','dtype','flat',
            'size','itemsize',]: # ndarray attribute
            return getattr(self.array,item)
        else:
            raise AttributeError('No such attribute!')

    @classmethod
    def init(cls,dataN,sRateN):
        dN=np.array(dataN)
        srN=np.array(sRateN)
        wd_gen=lambda d,sr: Wavedata(d,sr)
        if dN.ndim-1==srN.ndim: # 每个序列的点数相同
            signature='(n),()->()'
        elif dN.ndim==srN.ndim: # 各个序列的点数不同
            signature='(),()->()'
        vec_wd_gen=np.vectorize(wd_gen,signature=signature)
        array=vec_wd_gen(dN,srN)
        return cls(array)

    def __pos__(self):
        return self

    def __neg__(self):
        array = -self.array
        return self.__class__(array)

    def __abs__(self):
        array=np.abs(self.array)
        return self.__class__(array)

    def __rshift__(self, t):
        array=self.array>>t
        return self.__class__(array)

    def __lshift__(self, t):
        array=self.array<<t
        return self.__class__(array)

    def __or__(self, other):
        assert isinstance(other,WavedataN)
        assert self.shape == other.shape
        array=self.array|other.array
        return self.__class__(array)

    def __xor__(self, n):
        n = np.around(n).astype(int)
        array=self.array^n
        return self.__class__(array)

    def __pow__(self, v):
        array=self.array**v
        return self.__class__(array)

    def __add__(self, other):
        if isinstance(other,WavedataN):
            assert self.shape == other.shape
            array = self.array + other.array
            return self.__class__(array)
        else:
            return other + self

    def __radd__(self, v):
        array = self.array + v
        return self.__class__(array)

    def __sub__(self, other):
        return self + (- other)

    def __rsub__(self, v):
        return v + (-self)

    def __mul__(self, other):
        if isinstance(other,WavedataN):
            assert self.shape == other.shape
            array = self.array * other.array
            return self.__class__(array)
        else:
            return other * self

    def __rmul__(self, v):
        array = self.array * v
        return self.__class__(array)

    def __truediv__(self, other):
        if isinstance(other,WavedataN):
            assert self.shape == other.shape
            array = self.array / other.array
            return self.__class__(array)
        else:
            return (1/other) * self

    def __rtruediv__(self, v):
        array = v / self.array
        return self.__class__(array)

    def plot(self,**kw):
        array = self.array.flatten()
        row, = array.shape
        fig,ax = plt.subplots(row,1,figsize=(10,row),sharex=True)
        plt.subplots_adjust(hspace=0)
        for i in range(row):
            array[i].plot(ax=ax[i])
        return fig,ax
