from ._waveform import *
from ._vIQmixer import vIQmixer


'''不再更新此模块！
waveform的缺点是波形本身是很多函数的堆叠，导致对特别长的波形序列运算效率比较低，耗费时间太长，
出现函数深度溢出的问题。后续使用wavedata模块产生波形，只保留data和sRate两个属性，效率较高。
'''
