import numpy as np

def f_ge(I, args):
    '''
    基态和第一激发态能级间距与磁通偏置电流的关系

    f_ge：基态和第一激发态能级间距
    I：偏置电流大小
    args：参数字典，如下
        {
            'f_c': 裸腔频率，
            'g': 谐振腔与量子比特的耦合常量，
            'Period': 对应一个磁通量子的电流周期，
            'I_SS': 频率最高点对应的电流大小，
            'f_ge_max': 最高点频率，
            'd': SQUID双结的不对称度参数，完全对称为0，完全不对称为1,
        }
    '''
    f_ge_max = args['f_ge_max']
    I_SS = args['I_SS']
    Period = args['Period']
    d = args['d']
    phi = np.pi * (I - I_SS) / Period
    y = f_ge_max * (np.cos(phi)**2 + d * d * np.sin(phi)**2)**0.25
    return y


def f_r(I, args):
    '''
    色散区域的谐振腔频率与磁通偏置电流的关系

    f_r：谐振腔频率
    I：偏置电流大小
    args：参数字典，如下
        {
            'f_c': 裸腔频率，
            'g': 谐振腔与量子比特的耦合常量，
            'Period': 对应一个磁通量子的电流周期，
            'I_SS': 频率最高点对应的电流大小，
            'f_ge_max': 最高点频率，
            'd': SQUID双结的不对称度参数，完全对称为0，完全不对称为1,
        }
    '''
    f_c = args['f_c']
    g = args['g']
    f_ge_i=f_ge(I, args)
    term1 = (f_c + f_ge_i)/2
    term2 = np.sqrt(g * g + (f_ge_i - f_c)**2 / 4)
    a=np.where(f_c>f_ge_i,1,-1)
    y=term1 + term2*a
    return y