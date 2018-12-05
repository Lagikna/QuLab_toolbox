import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class BaseFit(object):
    """BaseFit class"""
    def __init__(self, data, **kw):
        super(BaseFit, self).__init__()
        self.data=data
        self._Fitcurve(**kw)

    def _fitfunc(self, t, A, B, T1):
        '''this an example: T1 fit function '''
        y=A*np.exp(-t/T1)+B
        return y

    def _Fitcurve(self, **kw):
        t,y=self.data
        popt, pcov=curve_fit(self._fitfunc, t, y, maxfev=100000, **kw)
        self._popt = popt
        self._pcov = pcov
        self._error = np.sqrt(np.diag(pcov))

    def plot(self, fmt1='rx', fmt2='k--', opt1={}, opt2={}):
        t,y=self.data
        plt.plot(t, y, fmt1, **opt1)
        plt.plot(t, self._fitfunc(t,*self._popt), fmt2, **opt2)
        plt.show()

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        return self._error

class Cauchy_Fit(BaseFit):
    '''Fit peak'''

    def _fitfunc(self,t,A,t0,FWHM):
        y=A*FWHM/((t-t0)**2+FWHM**2)/np.pi
        return y

    @property
    def t0(self):
        A,t0,FWHM=self._popt
        return t0

    @property
    def t0_error(self):
        A_e,t0_e,FWHM_e=self._error
        return t0_e

    @property
    def FWHM(self):
        A,t0,FWHM=self._popt
        return FWHM

    @property
    def FWHM_error(self):
        A_e,t0_e,FWHM_e=self._error
        return FWHM_e

class T1_Fit(BaseFit):
    '''Fit T1'''

    def _fitfunc(self,t,A,B,T1):
        y=A*np.exp(-t/T1)+B
        return y

    @property
    def T1(self):
        A,B,T1=self._popt
        return T1

    @property
    def T1_error(self):
        A_e,B_e,T1_e=self._error
        return T1_e


class Rabi_Fit(BaseFit):
    '''Fit rabi'''

    def _fitfunc(self,t,A,B,C,lmda,Tr):
        # lmda: lambda,rabi's wavelength
        y=A*np.exp(-t/Tr)*np.cos(2*np.pi/lmda*t+B)+C
        return y

    @property
    def Tr(self):
        A,B,C,lmda,Tr = self._popt
        return Tr

    @property
    def rabi_freq(self):
        '''rabi frequency'''
        A,B,C,lmda,Tr = self._popt
        # lambda 默认单位为us, 所以返回频率为MHz
        rabi_freq=np.abs(2*np.pi/lmda)
        return rabi_freq

    @property
    def rabi_freq_error(self):
        '''rabi frequency error'''
        A,B,C,lmda,Tr = self._popt
        A_e,B_e,C_e,lmda_e,Tr_e = self._error
        rabi_freq_e=np.abs(2*np.pi/(lmda**2))*lmda_e
        return rabi_freq_e

    @property
    def PPlen(self):
        '''Pi Pulse Length, equal 1/2 lambda'''
        A,B,C,lmda,Tr = self._popt
        _PPlen=np.abs(lmda/2)
        return _PPlen


class Ramsey_Fit(BaseFit):
    '''Fit Ramsey'''

    def __init__(self,data,T1,**kw):
        self._T1=T1
        super(Ramsey_Fit, self).__init__(data=data,**kw)

    def _fitfunc(self,t,A,B,Tphi,delta):
        y=A*np.exp(-t/2/self._T1-np.square(t/Tphi))*np.cos(delta*t)+B
        return y

    @property
    def Tphi(self):
        A,B,Tphi,delta = self._popt
        return Tphi

    @property
    def Tphi_error(self):
        A_e,B_e,Tphi_e,delta_e=self._error
        return Tphi_e


class Spinecho_Fit(BaseFit):
    '''Fit spinecho'''

    def _fitfunc(self,t,A,B,T2E):
        y=A*np.exp(-t/T2E)+B
        return y

    @property
    def T2E(self):
        A,B,T2E = self._popt
        return T_2E

    @property
    def T2E_error(self):
        A_e,B_e,T2E_e=self._error
        return T2E_e
