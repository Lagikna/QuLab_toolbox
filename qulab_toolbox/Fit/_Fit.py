import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import interpolate

_CONFIG={
    'scatter':{
        'marker':'p',
        'color':'g',
        'edgecolors':'',
        's':15,
    },
    'plot':{

    }
}

def config(scatter={},plot={}):
    '''设置BaseFit默认的画图格式
    
    Parameters:
        scatter: 散点图的设置字典
        plot: 折线图的设置字典
    '''
    _CONFIG['scatter'].update(scatter)
    _CONFIG['plot'].update(plot)

def getconfig():
    return _CONFIG


class BaseFit(object):
    """BaseFit class, based on scipy.optimiz.curve_fit """
    def __init__(self, data, fitfunc=None, **kw):
        super(BaseFit, self).__init__()
        x,y=data
        self.x=np.array(x)
        self.y=np.array(y)
        self.fitfunc=self._fitfunc if fitfunc is None else fitfunc

        popt, pcov=curve_fit(self.fitfunc, self.x, self.y, maxfev=100000, **kw)
        self._popt = popt
        self._pcov = pcov
        self._error = np.sqrt(np.diag(pcov))

    def _fitfunc(self, t, A, B, T1):
        '''this an example: T1 fit function '''
        y=A*np.exp(-t/T1)+B
        return y

    def func(self,t):
        '''拟合后的函数'''
        return self.fitfunc(t,*self._popt)

    def plotscript(self,ax=None):
        pass

    def plot(self, fmt='r-', show='both', times=10):
        '''画图
        
        Parameters:
            fmt: plot curve format
            show: both/plot/scatter, 根据选择画图
            times: 插值的倍率(整数)，重新对x轴数据插值使画出的拟合曲线更平滑
        '''
        ax = plt.gca()
        self.plotscript(ax=ax)
        t,y=self.x,self.y
        if show in ['both','scatter']:
            scatter_kw=_CONFIG['scatter']
            ax.scatter(t, y, **scatter_kw)
        if show in ['both','plot']:
            plot_kw=_CONFIG['plot']
            size=len(t)
            t_func=interpolate.interp1d(np.array(range(size))*times,t,kind='linear')
            _t=t_func(np.array(range((size-1)*times+1)))
            ax.plot(_t, self.func(_t), fmt, **plot_kw)

    @property
    def error(self):
        '''standard deviation errors on the parameters '''
        return self._error

    @property
    def params(self):
        '''optimized parameters '''
        return self._popt


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


class Linear_Fit(BaseFit):
    '''Simple Linear Fit'''

    def _fitfunc(self,t,A,B):
        y= A * t + B
        return y

    @property
    def A(self):
        A,B=self._popt
        return A

    @property
    def B(self):
        A,B=self._popt
        return B


class Sin_Fit(BaseFit):

    def _fitfunc(self, t, A, B, w, phi):
        y=A*np.sin(w*t+phi)+B
        return y


class RBM_Fit(BaseFit):
    '''Randomized Benchmarking Fit'''

    def __init__(self,data, d=2, **kw):
        '''d: d-dimensional system, for the Clifford group, d=2'''
        super(RBM_Fit, self).__init__(data=data,**kw)
        self.d = d

    def _fitfunc(self,t,A,B,p):
        y=A*p**t+B
        return y

    @property
    def p(self):
        A,B,p=self._popt
        return p

    @property
    def p_error(self):
        A_e,B_e,p_e=self._error
        return p_e

    @property
    def F(self):
        '''Fidelity '''
        d = self.d
        A,B,p=self._popt
        F=1-(1-p)*(d-1)/d
        return F

    @property
    def F_error(self):
        d = self.d
        A_e,B_e,p_e=self._error
        F_e=p_e*(1-d)/d
        return F_e


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

    def plotscript(self,ax=None):
        ax = plt.gca() if ax is None else ax
        ax.set_xlabel(r'Time ($\mu$s)')
        ax.set_ylabel('Population')
        ax.set_title('Energy Relaxation')
        plt.text(0.95, 0.95, r'$T_1 = %.1f^{%.2f}_{%.2f} \mu$s'%(self.T1,self.T1_error,self.T1_error), 
                horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)

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
        rabi_freq=np.abs(1/lmda)
        return rabi_freq

    @property
    def rabi_freq_error(self):
        '''rabi frequency error'''
        A,B,C,lmda,Tr = self._popt
        A_e,B_e,C_e,lmda_e,Tr_e = self._error
        rabi_freq_e=np.abs(1/(lmda**2))*lmda_e
        return rabi_freq_e

    @property
    def PPlen(self):
        '''Pi Pulse Length, equal 1/2 lambda'''
        A,B,C,lmda,Tr = self._popt
        _PPlen=np.abs(lmda/2)
        return _PPlen

    def plotscript(self,ax=None):
        ax = plt.gca() if ax is None else ax
        ax.set_xlabel(r'Time ($\mu$s)')
        ax.set_ylabel('Population')
        ax.set_title('Rabi')
        plt.text(0.95, 0.95, r'$T_r = %.1f \mu$s'%(self.Tr), 
                horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)

class Ramsey_Fit(BaseFit):
    '''Fit Ramsey'''

    def __init__(self,data,T1,**kw):
        self._T1=T1
        super(Ramsey_Fit, self).__init__(data=data,**kw)

    def _fitfunc(self,t,A,B,C,Tphi,w):
        y=A*np.exp(-t/2/self._T1-np.square(t/Tphi))*np.cos(w*t+C)+B
        return y

    @property
    def Tphi(self):
        A,B,C,Tphi,delta = self._popt
        return Tphi

    @property
    def Tphi_error(self):
        A_e,B_e,C_e,Tphi_e,delta_e=self._error
        return Tphi_e

    @property
    def detuning(self):
        A,B,C,Tphi,w = self._popt
        return w/2/np.pi

    def plotscript(self,ax=None):
        ax = plt.gca() if ax is None else ax
        ax.set_xlabel(r'Time ($\mu$s)')
        ax.set_ylabel('Population')
        ax.set_title('Ramsey')
        plt.text(0.95, 0.95, '$T_{\phi} = %.1f^{%.2f}_{%.2f} \mu$s\n$\Delta = %.4f$ MHz'%(
                            self.Tphi,self.Tphi_error,self.Tphi_error,self.detuning), 
                horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)

from .function import f_ge,f_r
class Fge_Fit(BaseFit):
    '''Simple Fit'''

    def _fitfunc(self,I,f_ge_max,I_SS,Period,d):
        args=dict(f_ge_max=f_ge_max,
                  I_SS=I_SS,
                  Period=Period,
                  d=d)
        return f_ge(I,args)

class Fr_Fit(BaseFit):
    '''Simple Fit'''

    def _fitfunc(self,I,f_ge_max,I_SS,Period,d,f_c,g):
        args=dict(f_ge_max=f_ge_max,
                  I_SS=I_SS,
                  Period=Period,
                  d=d,
                  f_c=f_c,
                  g=g)
        return f_r(I,args)