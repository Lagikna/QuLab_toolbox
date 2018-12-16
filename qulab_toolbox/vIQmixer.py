import numpy as np
from .waveform import *


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
        self.cali_params_I = None
        self.cali_params_Q = None
        self._RF = None

    def set_IQ(self,I,Q=0):
        self._I = I
        if Q == 0:
            self._Q = 0*I
        else:
            self._Q = Q

    def set_LO(self,LO_freq):
        self.LO_freq = LO_freq

    def Cali_IQ(self,cali_I=(1,0),cali_Q=(1,0)):
        self.cali_params_I = scale_i, offset_i = cali_I
        self.cali_params_Q = scale_q, offset_q = cali_Q
        self.__I = scale_i * self._I + offset_i
        self.__Q = scale_q * self._Q + offset_q


    def _up_coversion(self):
        if isinstance(self.__I,Waveform) and \
            isinstance(self.__Q,Waveform):
            rf_wf = self.__I * Sin(2*np.pi*self.LO_freq) + \
                    self.__Q * Cos(2*np.pi*self.LO_freq)
            self._RF = rf_wf
        else:
            raise TypeError("I/Q aren't Waveform ! ")

    def up_coversion(self,LO_freq,I,Q=0,cali_I=(1,0),cali_Q=(1,0)):
        self.set_LO(LO_freq)
        self.set_IQ(I,Q)
        self.Cali_IQ(cali_I,cali_Q)
        self._up_coversion()
        return self._RF
