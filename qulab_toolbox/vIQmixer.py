import numpy as np
from .waveform import *


class vIQmixer(object):
    '''virtual IQ mixer'''

    def __init__(self,LO_freq,I,Q=0,cali_I=(1,0),cali_Q=(1,0)):
        self.LO_freq = LO_freq
        # _I, _Q 表示输入的I, Q
        self.set_IQ(I,Q)
        # __I, __Q 表示校准之后的I, Q
        self.Calibrate(cali_I,cali_Q)
        self._RF = None

    def set_IQ(self,I,Q=0):
        self._I = I
        if Q == 0:
            self._Q = 0*I
        else:
            self._Q = Q

    def Calibrate(self,cali_I=(1,0),cali_Q=(1,0)):
        self.cali_params_I = scale_i, offset_i = cali_I
        self.cali_params_Q = scale_q, offset_q = cali_Q
        self.__I = scale_i * self._I + offset_i
        self.__Q = scale_q * self._Q + offset_q


    def RF(self):
        if not isinstance((self._I,self._Q),Waveform):
            raise TypeError("I/Q aren't Waveform ! ")
        rf_wf = self.__I * Sin(2*np.pi*self.LO_freq) + \
                self.__Q * Cos(2*np.pi*self.LO_freq)
        return rf_wf
