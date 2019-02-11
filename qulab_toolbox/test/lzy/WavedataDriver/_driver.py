import numpy as np
import matplotlib.pyplot as plt

from qulab_toolbox.wavedata import *
from .BaseDriver import BaseDriver, QInteger, QOption, QReal, QString, QVector


class Driver(BaseDriver):
    """docstring for Driver."""

    support_models = ['Wavedata']

    quants = [
        QVector('data'),
        QReal('sRate', unit='Sa/s'),
        QReal('Length', unit='s'),
        QInteger('Size', unit='point'),
        QReal('FFT50M', unit='V'),
    ]

    def __init__(self, addr=None, **kw):
        super(Driver, self).__init__(addr=addr, **kw)

    def performOpen(self):
        self.handle = Wavedata(sRate=1e9)

    def performSetValue(self, quant, value, **kw):
        if quant.name == 'data':
            self.handle.data = value
        elif quant.name == 'sRate':
            self.handle.sRate = value
        elif quant.name == 'Length':
            self.handle.setLen(value)
        elif quant.name == 'Size':
            self.handle.setSize(value)
        else:
            pass

    def performGetValue(self, quant, **kw):
        if quant.name == 'data':
            return self.handle.data
        elif quant.name == 'sRate':
            return self.handle.sRate
        elif quant.name == 'Length':
            return self.handle.len
        elif quant.name == 'Size':
            return self.handle.size
        elif quant.name == 'FFT50M':
            return self.handle.getFFT(50e6,mode='complex',**kw)
        else:
            pass

    def renewData(self,data):
        self.handle.data = data
