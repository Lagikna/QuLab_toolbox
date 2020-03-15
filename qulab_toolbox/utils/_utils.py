import numpy as np

def flatten_dict(d,symbol='.'):
    '''将多层字典压平为一层
    Parameters:
        d: 待压平的字典
        symbol: 压平所用的连接符号
    Return:
        压平后的字典
    '''
    fd={}
    for k,v in d.items():
        if isinstance(v,dict) and bool(v): # v 非空字典
            fd1=flatten_dict(v,symbol)
            fd2=dict(zip((k+symbol+_k for _k in fd1.keys()),fd1.values()))
            fd.update(fd2)
        else:
            fd.update({k:v})
    return fd

def restore_dict(d,symbol='.'):
    '''上面 flatten_dict 函数的逆过程，将压平的字典还原'''
    rd={}
    for k,v in d.items():
        ks=k.split(symbol)
        _d=rd
        for _k in ks[:-1]:
            _d.setdefault(_k,{})
            _d=_d.get(_k)
        _d.update({ks[-1]:v})
    return rd

def norm(z,axis=1,mode='mean'):
    '''对序列z沿axis轴进行归一化
    Parameters:
        z: 待归一化的序列
        axis: 归一化的轴向
        mode: 模式，包括 mean、max、min
    Return:
        归一化的序列
    '''
    z=np.array(z)
    if mode in ['mean']:
        n=np.mean(np.abs(z),axis=axis)
    elif mode in ['max']:
        n=np.max(np.abs(z),axis=axis)
    elif mode in ['min']:
        n=np.min(np.abs(z),axis=axis)
    n_list=[n]*z.shape[axis]
    n_array=np.stack(n_list,axis=axis)
    z_norm=z/n_array
    return z_norm

def is_equal(v1,v2):
    '''深入地比较v1,v2是否相等'''
    try:
        assert_equal(v1,v2)
        return True
    except AssertionError:
        return False

def assert_equal(v1,v2):
    '''断言v1,v2相等'''
    try:
        if isinstance(v1,np.ndarray) or isinstance(v1,np.ndarray):
            assert np.all(v1==v2)
        else:
            assert v1==v2
    except ValueError: # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        if isinstance(v1,dict) and isinstance(v2,dict):
            assert not set(v1.keys())^set(v2.keys()),Exception('keys not equal !')
            for k in v1.keys():
                _v1,_v2=v1[k],v2[k]
                assert_equal(_v1,_v2)
        elif isinstance(v1,(list,tuple,set)) and isinstance(v2,(list,tuple,set)):
            for _v1,_v2 in zip(v1,v2):
                assert_equal(_v1,_v2)
        else:
            assert False