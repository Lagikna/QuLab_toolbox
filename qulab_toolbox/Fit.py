import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

inf=np.inf

class BaseFit(object):
    """docstring for BaseFit."""
    def __init__(self, data,p0=None,bounds=(-inf, inf)):
        super(BaseFit, self).__init__()
        self.data=data
        self.p0=p0
        self.bounds=bounds
        self._Fitcurve()

    def _fitfunc(self, t, *params):
        '''params: paramters list'''
        A,B,T1 = params
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


class T1_Fit():
    '''Fit T1'''

    def __init__(self,data,p0=None,bounds=(-inf, inf)):
        self.data=data
        self._A=None
        self._B=None
        self._T1=None
        self.p0=p0
        self.bounds=bounds
        self._pcov=None
        self._error=None

    def _fitfunc(self,t,A,B,T1):
        y=A*np.exp(-t/T1)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc, t, y,
                                p0=self.p0, bounds=self.bounds, maxfev=100000)
        [A,B,T1]=p_est
        self._A=A
        self._B=B
        self._T1=T1
        self._pcov = err_est
        self._error = np.sqrt(np.diag(err_est))
        return p_est, err_est

    def Plot_Fit(self):
        t,y=self.data
        p_est, err_est=self._Fitcurve()
        plt.plot(t,y,'rx')
        plt.plot(t,self._fitfunc(t,*p_est),'k--')
        plt.show()

    @property
    def T1(self):
        self._Fitcurve()
        return self._T1

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        self._Fitcurve()
        return self._error


class Rabi_Fit():
    '''Fit rabi'''

    def __init__(self,data,p0=None,bounds=(-inf, inf)):
        self.data=data
        self._A=None
        self._B=None
        self._C=None
        self._lambda=None
        self._Tr=None
        self.p0=p0
        self.bounds=bounds
        self._pcov=None
        self._error=None

    def _fitfunc(self,t,A,B,C,lmda,Tr):
        # lmda: lambda,rabi's wavelength
        y=A*np.exp(-t/Tr)*np.cos(2*np.pi/lmda*t+B)+C
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc, t, y,
                                p0=self.p0, bounds=self.bounds, maxfev=100000)
        [A,B,C,lmda,Tr]=p_est
        self._A=A
        self._B=B
        self._C=C
        self._lambda=lmda
        self._Tr=Tr
        self._pcov = err_est
        self._error = np.sqrt(np.diag(err_est))
        return p_est, err_est

    def Plot_Fit(self):
        t,y=self.data
        p_est, err_est=self._Fitcurve()
        plt.plot(t,y,'rx')
        plt.plot(t,self._fitfunc(t,*p_est),'k--')
        plt.show()

    @property
    def Tr(self):
        self._Fitcurve()
        return self._Tr

    @property
    def rabi_freq(self):
        '''rabi frequency'''
        self._Fitcurve()
        # lambda 默认单位为us, 所以返回频率为MHz
        rabi_freq=np.abs(2*np.pi/self._lambda)
        return rabi_freq

    @property
    def PPlen(self):
        '''Pi Pulse Length, equal 1/2 lambda'''
        self._Fitcurve()
        _PPlen=np.abs(self._lambda/2)
        return _PPlen

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        self._Fitcurve()
        return self._error


class Ramsey_Fit():
    '''Fit Ramsey'''

    def __init__(self,data,T1,p0=None,bounds=(-inf, inf)):
        self.data=data
        self._T1=T1
        self._delta=None
        self._A=None
        self._B=None
        self._T_phi=None
        self.p0=p0
        self.bounds=bounds
        self._pcov=None
        self._error=None

    def _fitfunc(self,t,A,B,T_phi,delta):
        y=A*np.exp(-t/2/self._T1-np.square(t/T_phi))*np.cos(delta*t)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc, t, y,
                                p0=self.p0, bounds=self.bounds, maxfev=100000)
        [A,B,T_phi,delta]=p_est
        self._A=A
        self._B=B
        self._T_phi=T_phi
        self._delta=delta
        self._pcov = err_est
        self._error = np.sqrt(np.diag(err_est))
        return p_est, err_est

    def Plot_Fit(self):
        t,y=self.data
        p_est, err_est=self._Fitcurve()
        plt.plot(t,y,'rx')
        plt.plot(t,self._fitfunc(t,*p_est),'k--')
        plt.show()

    @property
    def T_phi(self):
        self._Fitcurve()
        return self._T_phi

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        self._Fitcurve()
        return self._error


class Spinecho_Fit():
    '''Fit spinecho
    '''

    def __init__(self,data,p0=None,bounds=(-inf, inf)):
        self.data=data
        self._A=None
        self._B=None
        self._T_2E=None
        self.p0=p0
        self.bounds=bounds
        self._pcov=None
        self._error=None

    def _fitfunc(self,t,A,B,T_2E):
        y=A*np.exp(-t/T_2E)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc, t, y,
                                p0=self.p0, bounds=self.bounds, maxfev=100000)
        [A,B,T_2E]=p_est
        self._A=A
        self._B=B
        self._T_2E=T_2E
        self._pcov = err_est
        self._error = np.sqrt(np.diag(err_est))
        return p_est, err_est

    def Plot_Fit(self):
        t,y=self.data
        p_est, err_est=self._Fitcurve()
        plt.plot(t,y,'rx')
        plt.plot(t,self._fitfunc(t,*p_est),'k--')
        plt.show()

    @property
    def T_2E(self):
        self._Fitcurve()
        return self._T_2E

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        self._Fitcurve()
        return self._error
