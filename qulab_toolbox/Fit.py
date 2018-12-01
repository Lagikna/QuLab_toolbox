import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inf=np.inf

class BaseFit(object):
    """BaseFit class"""
    def __init__(self, data,p0=None,bounds=(-inf, inf)):
        super(BaseFit, self).__init__()
        self.data=data
        self.p0=p0
        self.bounds=bounds
        self._Fitcurve()

    def _fitfunc(self, t, A ,B ,T1):
        '''this an example: T1 fit function '''
        y=A*np.exp(-t/T1)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc, t, y,
                                p0=self.p0, bounds=self.bounds, maxfev=100000)
        self._popt = p_est
        self._pcov = err_est
        self._error = np.sqrt(np.diag(err_est))

    def Plot_Fit(self):
        t,y=self.data
        plt.plot(t,y,'rx')
        plt.plot(t,self._fitfunc(t,*self._popt),'k--')
        plt.show()

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        return self._error


class T1_Fit(BaseFit):
    '''Fit T1'''

    def _fitfunc(self,t,A,B,T1):
        y=A*np.exp(-t/T1)+B
        return y

    @property
    def T1(self):
        A,B,T1=self._popt
        return T1


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
    def PPlen(self):
        '''Pi Pulse Length, equal 1/2 lambda'''
        A,B,C,lmda,Tr = self._popt
        _PPlen=np.abs(lmda/2)
        return _PPlen


class Ramsey_Fit(BaseFit):
    '''Fit Ramsey'''

    def __init__(self,data,T1,p0=None,bounds=(-inf, inf)):
        self._T1=T1
        super(Ramsey_Fit, self).__init__(data=data,p0=p0,bounds=bounds)

    def _fitfunc(self,t,A,B,T_phi,delta):
        y=A*np.exp(-t/2/self._T1-np.square(t/T_phi))*np.cos(delta*t)+B
        return y

    @property
    def T_phi(self):
        A,B,T_phi,delta = self._popt
        return T_phi


class Spinecho_Fit():
    '''Fit spinecho
    '''

    def _fitfunc(self,t,A,B,T_2E):
        y=A*np.exp(-t/T_2E)+B
        return y

    @property
    def T_2E(self):
        A,B,T_2E = self._popt
        return T_2E
