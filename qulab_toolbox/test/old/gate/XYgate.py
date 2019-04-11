import numpy as np
from qulab_toolbox.wavedata import *

def gen_XY_by_index(index, pi_len, half_pi_len, pi_factor, half_pi_factor, sRate, TYPE=Gaussian):
    '''通过给定的参数和索引，产生相应的波形脉冲；
    index : I/X/Y/X2p/X2n/Y2p/Y2n
    TYPE : 为由 width，sRate 两个参数决定的Wavedata类波形，现支持 DC,Gaussian,CosPulse
    '''
    if len(index)==1:
            if index=='I':
                pulse_wd_I=Blank(pi_len,sRate)
                pulse_wd_Q=Blank(pi_len,sRate)
            elif index=='X':
                pulse_wd_I=pi_factor*TYPE(pi_len,sRate)
                pulse_wd_Q=Blank(pi_len,sRate)
            elif index=='Y':
                pulse_wd_I=Blank(pi_len,sRate)
                pulse_wd_Q=pi_factor*TYPE(pi_len,sRate)
    else:
            if index[0]=='X':
                if index[2]=='p':
                    pulse_wd_I=half_pi_factor*TYPE(half_pi_len,sRate)
                    pulse_wd_Q=Blank(half_pi_len,sRate)
                else:
                    pulse_wd_I=-half_pi_factor*TYPE(half_pi_len,sRate)
                    pulse_wd_Q=Blank(half_pi_len,sRate)
            elif index[0]=='Y':
                if index[2]=='p':
                    pulse_wd_I=Blank(half_pi_len,sRate)
                    pulse_wd_Q=half_pi_factor*TYPE(half_pi_len,sRate)
                else:
                    pulse_wd_I=Blank(half_pi_len,sRate)
                    pulse_wd_Q=-half_pi_factor*TYPE(half_pi_len,sRate)
    return pulse_wd_I, pulse_wd_Q
