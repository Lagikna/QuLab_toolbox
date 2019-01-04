import numpy as np
from ._waveform import *


class vIQmixer(object):
    '''virtual IQ mixer'''

    def __init__(self):
        self.LO_freq = None
        # _I, _Q 表示输入的I, Q
        self._I = None
        self._Q = None
        # __I, __Q 表示校准之后的I, Q
        self.__I = None
        self.__Q = None
        self._cali_amp_I = (1,0)
        self._cali_amp_Q = (1,0)
        self._cali_phi = (0,0) #弧度
        self.cali_array = None
        self._RF = None

    def set_IQ(self,I=0,Q=0):
        '''I/Q, at least one waveform class'''
        self._I = I
        self._Q = Q
        if I == 0:
            self._I = 0*Q
        elif Q == 0:
            self._Q = 0*I
        if isinstance(self._I,Waveform) and isinstance(self._Q,Waveform):
            return self
        else:
            raise TypeError("I/Q aren't Waveform ! ")

    def set_LO(self,LO_freq):
        self.LO_freq = LO_freq
        return self

    def set_Cali(self,cali_array=None,DEG=True):
        '''cali_array: 2x3 array ;
        两行分别代表I/Q的校准系数；
        三列分别代表I/Q的 振幅系数、振幅补偿、相位补偿(默认角度)'''
        if cali_array is not None:
            cali_array = np.array(cali_array)
            self.cali_array = cali_array
            self._cali_amp_I = cali_array[0,:2]
            self._cali_amp_Q = cali_array[1,:2]
            if DEG:
                self._cali_phi = cali_array[:,2]*np.pi/180  #转为弧度
            else:
                self._cali_phi = cali_array[:,2]

        return self

    def __Cali_IQ(self):
        scale_i, offset_i = self._cali_amp_I
        scale_q, offset_q = self._cali_amp_Q
        self.__I = scale_i * self._I + offset_i
        self.__Q = scale_q * self._Q + offset_q

    def _up_conversion(self):
        if isinstance(self._I,Waveform) and isinstance(self._Q,Waveform):
            self.__Cali_IQ()
            cali_phi_i, cali_phi_q = self._cali_phi
            rf_wf = self.__I * Sin(2*np.pi*self.LO_freq, cali_phi_i) + \
                    self.__Q * Cos(2*np.pi*self.LO_freq, cali_phi_q)
            # _timeFunc=lambda x : self.__I._timeFunc(x) * np.sin(2*np.pi*self.LO_freq*x+cali_phi_i) + \
            #                      self.__Q._timeFunc(x) * np.cos(2*np.pi*self.LO_freq*x+cali_phi_q)
            # rf_wf = Waveform()
            # rf_wf._domain = self.__I._domain
            # rf_wf._timeFunc=_timeFunc
            self._RF = rf_wf
        else:
            raise TypeError("I/Q aren't Waveform ! ")

    def up_conversion(self,LO_freq,I=0,Q=0,cali_array=None):
        '''快速配置并上变频'''
        self.set_LO(LO_freq).set_IQ(I,Q).set_Cali(cali_array)
        self._up_conversion()
        return self._RF
