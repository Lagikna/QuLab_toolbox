import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class T1_Fit():
    '''Fit T1'''

    def __init__(self,data):
        self.data=data
        self._A=None
        self._B=None
        self._T1=None

    def _fitfunc(self,t,A,B,T1):
        y=A*np.exp(-t/T1)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc,t,y,maxfev=100000)
        [A,B,T1]=p_est
        self._A=A
        self._B=B
        self._T1=T1
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

class Rabi_Fit():
    '''Fit rabi'''

    def __init__(self,data):
        self.data=data
        self._A=None
        self._B=None
        self._C=None
        self._D=None
        self._Tr=None

    def _fitfunc(self,t,A,B,C,D,Tr):
        y=A*np.exp(-t/Tr)*np.cos(B*t+C)+D
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc,t,y,maxfev=100000)
        [A,B,C,D,Tr]=p_est
        self._A=A
        self._B=B
        self._C=C
        self._D=D
        self._Tr=Tr
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
    def PPlen(self):
        self._Fitcurve()
        _PPlen=1/self._B
        return _PPlen

class Ramsey_Fit():
    '''Fit Ramsey'''

    def __init__(self,data,T1):
        self.data=data
        self._T1=T1
        self._delta=None
        self._A=None
        self._B=None
        self._T_phi=None

    def _fitfunc(self,t,A,B,T_phi,delta):
        y=A*np.exp(-t/2/self._T1-np.square(t/T_phi))*np.cos(delta*t)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc,t,y,maxfev=100000)
        [A,B,T_phi,delta]=p_est
        self._A=A
        self._B=B
        self._T_phi=T_phi
        self._delta=delta
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

class Spinecho_Fit():
    '''Fit spinecho
    '''

    def __init__(self,data):
        self.data=data
        self._A=None
        self._B=None
        self._T_2E=None

    def _fitfunc(self,t,A,B,T_2E):
        y=A*np.exp(-t/T_2E)+B
        return y

    def _Fitcurve(self):
        t,y=self.data
        p_est, err_est=curve_fit(self._fitfunc,t,y,maxfev=100000)
        [A,B,T_2E]=p_est
        self._A=A
        self._B=B
        self._T_2E=T_2E
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
