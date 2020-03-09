'''一些小工具的集合'''
import numpy as np

class d2c(object):
    '''dict to class
    
    将字典的调用方式转化为类属性的调用方式；
    字典的关键字须符合类属性命名的规范，可以赋值
    '''
    
    def __init__(self,d):
        '''传入一个字典或者d2c类的实例，构造一个d2c实例'''
        if isinstance(d,d2c):
            d=d.todict()
        assert isinstance(d,dict)
        for k,v in d.items():
            _v=d2c(v) if isinstance(v,dict) else v           
            self.__dict__.update({k:_v})
            
    def todict(self):
        '''从d2c实例提取出原字典'''
        d={}
        for k,v in self.__dict__.items():
            _v=v.todict() if isinstance(v,d2c) else v
            d.update({k:_v})
        return d

    def get(self,keys,splitsymbol='.'):
        '''根据关键词连接的字符串或者列表，获取对应的值
        
        Parameters:
            keys: 使用符号串联key的字符串，比如'pulse.width.value';
                或者key顺序列表，比如['pulse','width','value']
            splitsymbol: 字符串的分割符号，默认为 '.'
        Return:
            返回键值串对应的值
        '''
        keys=keys.split(splitsymbol) if isinstance(keys,str) else keys
        value=self
        for k in keys:
            value=getattr(value,k)
        ##
        # value=getattr(self,keys.pop(0))
        # if keys:
        #     value=value.get(keys) #递归
        return value

    def set(self,keys,value,check=False,splitsymbol='.'):
        '''根据关键词连接的字符串或者列表，设置对应的值
        
        Parameters:
            keys: 使用符号串联key的字符串，比如'pulse.width.value';
                或者key顺序列表，比如['pulse','width','value']
            value: 待设入的值
            check: bool, 是否检查设入值与原值相等
            splitsymbol: 字符串的分割符号，默认为 '.'
        Return:
            bool, True 表示value改变并且已设置，False 表示未变
        '''
        if check:
            if is_equal(value,self.get(keys)):
                return False
        keys=keys.split(splitsymbol) if isinstance(keys,str) else keys
        ins=self
        for k in keys[:-1]:
            ins=getattr(ins,k)
        assert hasattr(ins,keys[-1]),f'关键词 {keys[-1]} 不存在!'
        setattr(ins,keys[-1],value)
        ## 
        # if len(keys)>1:
        #     getattr(self,keys.pop(0)).set(keys,value) ##递归
        # else:
        #     assert hasattr(self,keys[0]) ##必须是字典中已有的关键词
        #     setattr(self,keys[0],value)
        return True

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


import os.path

def get_mplstyle_path(name='qulab'):
    '''
    返回本目录下自定义的一个matplotlib的画图风格文件的路径

    调用方法：
        plt.style.use(qulab_mplstyle)
        或
        with plt.style.context(qulab_mplstyle)：
            ....
    '''
    filepath = os.path.abspath(__file__)
    mplstyle_path=os.path.dirname(filepath)+'\\'+f'{name}.mplstyle'
    return mplstyle_path

qulab_mplstyle=get_mplstyle_path('qulab')