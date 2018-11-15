import numpy as np
from qulab.waveform import *

class Xgate():
    ''' X gate: Gauss,amplitude varied'''

    def __init__(self,para):
        self.para=para
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _sqAI= _cell*Sin(2*np.pi*self.para[1])*self.para[2]
        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.deg2rad(self.para[3]))*self.para[2]*self.para[4]
        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ

class Ygate():
    ''' Y gate: Gauss,amplitude varied'''

    def __init__(self,para):
        self.para=para
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _sqAI= _cell*Sin(2*np.pi*self.para[1],np.pi/2)*self.para[2]
        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi/2),360))*self.para[2]*self.para[4]
        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ

class nXgate():
    ''' -X gate: Gauss,amplitude varied'''

    def __init__(self,para):
        self.para=para
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _sqAI= _cell*Sin(2*np.pi*self.para[1],np.pi)*self.para[2]
        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi),360))*self.para[2]*self.para[4]
        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

    @property
    def wave(self):
        self._gate()
        return self._sqAI,self._sqAQ

class nYgate():
    ''' -Y gate: Gauss,amplitude varied'''

    def __init__(self,para):
        self.para=para
        self._sqAI=None
        self._sqAQ=None

    def _gate(self):
        _cell=(Gaussian(self.para[0])>>(self.para[0]/2))*(DC(1,self.para[0]))
        _sqAI= _cell*Sin(2*np.pi*self.para[1],np.pi*3/2)*self.para[2]
        _sqAQ= _cell*Sin(2*np.pi*self.para[1],np.mod(np.deg2rad(self.para[3]+np.pi*3/2),360))*self.para[2]*self.para[4]
        self._sqAI=_sqAI
        self._sqAQ=_sqAQ
        return self._sqAI,self._sqAQ

class X_drag_gate():
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
