import numpy as np
from ._wavedata import Wavedata,Sin,Cos

'''Wavedata 虚拟IQ混频器模块'''

class vIQmixer(object):
    '''virtual IQ mixer'''

    def __init__(self):
        self.LO_freq = None
        # _IQ 表示输入的IQ
        self._IQ = None
        # __IQ 表示校准之后的IQ
        self.__IQ = None
        self._cali_amp_I = (1,0)
        self._cali_amp_Q = (1,0)
        self._cali_phi = (0,0) #弧度
        self._cali_rf = (1,0)
        self._RF = None

    def set_IQ(self,I=0,Q=0,IQ=None):
        '''I/Q至少一个是Wavedata类，或者传入IQ波形'''
        if IQ is None:
            IQ=I+1j*Q
        assert isinstance(IQ,Wavedata)
        self._IQ = IQ
        self.len = IQ.len
        self.sRate = IQ.sRate
        return self

    def set_LO(self,LO_freq):
        self.LO_freq = LO_freq
        return self

    def set_Cali(self,cali_array=None,DEG=True):
        '''cali_array: 2x3 array ;
        两行分别代表I/Q的校准系数；
        三列分别代表I/Q的 振幅系数、振幅补偿、相位补偿(默认角度)'''
        if cali_array is None:
            cali_array = [[1,0,0],
                          [1,0,0]]
        _cali_array = np.array(cali_array)
        self._cali_amp_I = _cali_array[0,:2]
        self._cali_amp_Q = _cali_array[1,:2]
        if DEG:
            self._cali_phi = _cali_array[:,2]*np.pi/180  #转为弧度
        else:
            self._cali_phi = _cali_array[:,2]
        self.__Cali_IQ()
        return self

    def __Cali_IQ(self):
        scale_i, offset_i = self._cali_amp_I
        scale_q, offset_q = self._cali_amp_Q
        __I = scale_i * self._IQ.I() + offset_i
        __Q = scale_q * self._IQ.Q() + offset_q
        self.__IQ = __I + 1j*__Q

    def UpConversion(self):
        '''需要先 set_IQ, set_LO, set_Cali, 再使用此方法'''
        cali_phi_i, cali_phi_q = self._cali_phi
        rf_wd = self.__IQ.I() * Sin(2*np.pi*self.LO_freq,cali_phi_i,self.len,self.sRate) + \
                self.__IQ.Q() * Cos(2*np.pi*self.LO_freq,cali_phi_q,self.len,self.sRate)
        self._RF = rf_wd
        return self

    def set_CaliRF(self, cali_rf=None):
        '''对输出的RF做最后的线性校准；
        cali_rf: 1*2的数组或序列，为RF的scale和offset'''
        if cali_rf is None:
            cali_rf=[1,0]
        self._cali_rf=np.array(cali_rf)
        scale_rf, offset_rf = self._cali_rf
        self._RF = scale_rf * self._RF + offset_rf
        return self

    @classmethod
    def up_conversion(cls,LO_freq,I=0,Q=0,IQ=None,cali_array=None,cali_rf=None):
        '''快速配置并上变频'''
        vIQ=cls().set_LO(LO_freq).set_IQ(I,Q,IQ).set_Cali(cali_array).UpConversion()
        if cali_rf is not None:
            vIQ.set_CaliRF(cali_rf)
        return vIQ._RF

    @classmethod
    def carry_wave(cls,carry_freq,I=0,Q=0,IQ=None,carry_cali=None,DEG=True):
        '''将I/Q分别加载某个频率的载波，
        carry_cali对应实体IQ混频器的校准矩阵，与上面cali_array格式相同'''
        if carry_cali is None:
            carry_cali = [[1,0,0],
                          [1,0,0]]
        _carry_cali = np.array(carry_cali)
        _scale_I, _offset_I = _carry_cali[0,:2]
        _scale_Q, _offset_Q = _carry_cali[1,:2]
        if DEG:
            _phi_I, _phi_Q = _carry_cali[:,2]*np.pi/180  #转为弧度
        else:
            _phi_I, _phi_Q = _carry_cali[:,2]

        if IQ is None:
            IQ=I+1j*Q

        carry_I = IQ.I()*Sin(2*np.pi*carry_freq,_phi_I,IQ.len,IQ.sRate)*_scale_I+_offset_I
        carry_Q = IQ.Q()*Cos(2*np.pi*carry_freq,_phi_Q,IQ.len,IQ.sRate)*_scale_Q+_offset_Q

        carry_wd=carry_I+1j*carry_Q
        return carry_wd
