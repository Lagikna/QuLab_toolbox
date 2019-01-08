import numpy as np
from qulab.waveform import *

#Created by hanzhikun
#Email: zkhan@foxmail.com
#Created date:2018.11.22

#Data Input:
#1.para         :Gaussian width,awg_freq,amplitude,IM_phas,IM_amp
#Attention the right side of the waveform is at time 0.
#3.theta        :phase angle for different rotation angle
#4.range        :generate data from range(detail in qulab.waveform)
#5.samplerate   :generate data same as the awg samplerate
#Data Output:
#Waveform data For IQ mixer.

class xy_gauss():
    ''' XY gate: Gauss;with DRAG'''

    def __init__(self,para,delay,theta=0,alpha=0,range=[0,50.0],samplerate=2.0e9):
        self.para=para
        self.delay=delay
        self.range=range
        self.theta=theta
        self.alpha=alpha
        self.samplerate=samplerate/1.0e6

        self._sqAI=None
        self._sqAQ=None
        self._I=None
        self._Q=None
        self.len=None

    def _gate(self):
        #create basic gauss waveform & DRAG_gauss
        _cell=(Gaussian(self.para[0])<<(self.para[0]/2))
        self.len=self.para[0]/(4*np.sqrt(2*np.log(2)))
        _drag_gauss=(Drag_gauss(self.para[0],self.samplerate)<<(self.para[0]/2))

        #mutiply with Sin wave(differ phase for differ gate) and gauss DRAG.(alpha modify the drag parameter)
        _sqAI= (((_cell>>self.delay)*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.theta),360.0))*self.para[2])+\
        ((_drag_gauss>>self.delay)*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.theta)+90.0,360.0))*self.para[2]*self.alpha))*\
        (DC(1,self.para[0])>>(self.delay-self.para[0]))

        _sqAQ= (((_cell>>self.delay)*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+self.theta),360.0))*self.para[2]*self.para[4])+\
        ((_drag_gauss>>self.delay)*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+self.theta)+90.0,360.0))*self.para[2]*self.para[4]*self.alpha))*\
        (DC(1,self.para[0])>>(self.delay-self.para[0]))

        #generate gate (detail see qulab.waveform)
        _I=_sqAI.set_range(self.range[0],self.range[1]).generateData(sampleRate=(self.samplerate))
        _Q=_sqAQ.set_range(self.range[0],self.range[1]).generateData(sampleRate=(self.samplerate))
        self._sqAI=_I
        self._sqAQ=_Q
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ
# class xy_gauss():
#     ''' XY gate: Gauss;with DRAG'''
#
#     def __init__(self,para,theta=0,alpha=0,samplerate=2.0e9):
#         self.para=para
#         self.theta=theta
#         self.alpha=alpha
#         self.samplerate=samplerate/1.0e6
#
#         self._sqAI=None
#         self._sqAQ=None
#         self._I=None
#         self._Q=None
#         self.len=None
#
#     def _gate(self):
#         #create basic gauss waveform & DRAG_gauss
#         _cell=(Gaussian(self.para[0])<<(self.para[0]/2))
#         self.len=self.para[0]/(4*np.sqrt(2*np.log(2)))
#         _drag_gauss=(Drag_gauss(self.para[0],self.samplerate)<<(self.para[0]/2))
#
#         #mutiply with Sin wave(differ phase for differ gate) and gauss DRAG.(alpha modify the drag parameter)
#         self._sqAI= (((_cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.theta),360.0))*self.para[2])+\
#         (_drag_gauss*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.theta)+90.0,360.0))*self.para[2]*self.alpha))*\
#         (DC(1,self.para[0])<<self.para[0]))
#
#         self._sqAQ= (((_cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+self.theta),360.0))*self.para[2]*self.para[4])+\
#         (_drag_gauss*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+self.theta)+90.0,360.0))*self.para[2]*self.para[4]*self.alpha))*\
#         (DC(1,self.para[0])<<self.para[0]))
#
#     @property
#     def wave(self):
#         self._gate()
#         return self._sqAI,self._sqAQ
#
# class xy_pts():
#     ''' generate IQ dual channel waveform datat points'''
#     def __init__(self,sqA,sqB,start=0,stop=50.0,samplerate=2.0e9):
#         self.start=start
#         self.stop=stop
#         self.samplerate=samplerate/1.0e6
#         self._I=sqA
#         self._Q=sqB
#         self._sqAI=None
#         self._sqAQ=None
#
#     def _pts(self):
#         self._sqAI=self._I.set_range(self.start,self.stop).generateData(sampleRate=(self.samplerate))
#         self._sqAQ=self._Q.set_range(self.start,self.stop).generateData(sampleRate=(self.samplerate))
#
#     @property
#     def pts(self):
#         self._pts()
#         return self._sqAI,self._sqAQ

class z_square():
    ''' DC gate:'''

    def __init__(self,len,amp,delay,range=[0,50.0],samplerate=2.0e9):
        self.len=len
        self.amp=amp
        self.delay=delay
        self.range=range
        self.samplerate=samplerate/1.0e6
        self._sqA=None
        self._I=None

    def _gate(self):
        _sqA=(DC(1,self.len)>>(self.delay-self.len))*self.amp
        self._I=_sqA.set_range(self.range[0],self.range[1]).generateData(sampleRate=self.samplerate)
        self._sqA=self._I

    @property
    def wave(self):
        self._gate()
        return self._sqA

class xy_drag_gate():
    ''' X gate with DRAG calibration'''

    def __init__(self,para,beta):
        self.para=para
        self.beta=beta
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _cell1=(DRAG(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))

        _sqAI= _cell*Sin(2*np.pi*self.para[1])*self.para[2]+\
        _cell1*Sin(2*np.pi*self.para[1],np.pi/2)*self.para[2]*self.beta

        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.deg2rad(self.para[3]))*self.para[2]*self.para[4]+\
        _cell1*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi/2),360))*self.para[2]*self.para[4]*self.beta

        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ

class Y_drag_gate():
    '''Y gate with DRAG calibration'''

    def __init__(self,para,beta):
        self.para=para
        self.beta=beta
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _cell1=(DRAG(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))


        _sqAI= _cell*Sin(2*np.pi*self.para[1],np.pi/2)*self.para[2]+\
        _cell1*Sin(2*np.pi*self.para[1],np.pi)*self.para[2]*self.beta

        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi/2),360))*self.para[2]*self.para[4]+\
        _cell1*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi),360))*self.para[2]*self.para[4]*self.beta

        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ

class nX_drag_gate():
    '''-X gate with DRAG calibration'''

    def __init__(self,para,beta):
        self.para=para
        self.beta=beta
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _cell1=(DRAG(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))


        _sqAI= _cell*Sin(2*np.pi*self.para[1],np.pi)*self.para[2]+\
        _cell1*Sin(2*np.pi*self.para[1],np.pi*3/2)*self.para[2]*self.beta

        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi),360))*self.para[2]*self.para[4]+\
        _cell1*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi*3/2),360))*self.para[2]*self.para[4]*self.beta

        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ

class nY_drag_gate():
    '''-Y gate with DRAG calibration'''

    def __init__(self,para,beta):
        self.para=para
        self.beta=beta
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _cell1=(DRAG(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))


        _sqAI= _cell*Sin(2*np.pi*self.para[1],np.pi*3/2)*self.para[2]+\
        _cell1*Sin(2*np.pi*self.para[1])*self.para[2]*self.beta

        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi*3/2),360))*self.para[2]*self.para[4]+\
        _cell1*Sin(2*np.pi*self.para[1],np.deg2rad(self.para[3]))*self.para[2]*self.para[4]*self.beta

        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ
