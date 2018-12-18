import numpy as np
from ..waveform import *

AWG_AMP=0.5

def pi_pulse(amp, length):
    factor = amp/AWG_AMP
    pulse = factor * Gaussian(length)
    return pulse
