import numpy as np
from ..wavedata import *

AWG_AMP=0.5

def generate_pulse_by_index(self, index, gate_len, pi_factor, half_pi_factor,sRate):
        if len(index)==1:
            if index=='I':
                pulse_wf_I=Blank(gate_len,sRate)
                pulse_wf_Q=Blank(gate_len,sRate)
            elif index=='X':
                pulse_wf_I=pi_factor*Gaussian(gate_len,sRate)
                pulse_wf_Q=Blank(gate_len,sRate)
            elif index=='Y':
                pulse_wf_I=Blank(gate_len,sRate)
                pulse_wf_Q=pi_factor*Gaussian(gate_len,sRate)
        else:
            if index[0]=='X':
                if index[2]=='p':
                    pulse_wf_I=half_pi_factor*Gaussian(gate_len/2,sRate)
                    pulse_wf_Q=Blank(gate_len/2,sRate)
                else:
                    pulse_wf_I=-half_pi_factor*Gaussian(gate_len/2,sRate)
                    pulse_wf_Q=Blank(gate_len/2,sRate)
            elif index[0]=='Y':
                if index[2]=='p':
                    pulse_wf_I=Blank(gate_len/2,sRate)
                    pulse_wf_Q=half_pi_factor*Gaussian(gate_len/2,sRate)
                else:
                    pulse_wf_I=Blank(gate_len/2,sRate)
                    pulse_wf_Q=-half_pi_factor*Gaussian(gate_len/2,sRate)
        return pulse_wf_I, pulse_wf_Q
