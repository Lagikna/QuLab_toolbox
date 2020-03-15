from blinker import Signal
import numpy as np

from ._utils import is_equal

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

class cons_d2c(object):
    '''包含约束的d2c类'''

    def __init__(self,d,constrains,init=True):
        '''
        Parameters:
            d: 一个字典
            constrains: 约束条目，每个元素都为一个三元元组（deps, func, target），例如，
                (
                    (('k1.k11','k1.k12'),   (lambda v1,v2:v1+v2),   'k2'       ),
                    (('k3','k4'),           (lambda v1,v2:(v1,v2)), ('k5','k6')),
                )
            init: bool, 是否使用约束条件初始化传入的字典
        '''
        self.__d2c_instance=d2c(d)
        self.sig=Signal()
        self.constrains=constrains
        self.subscribers=self.__init_cons(constrains,init=init)

    def __init_cons(self,constrains,init=True):
        subscribers=[]
        for deps,func,target in constrains:
            subs=_subscrib(deps,func,target,self)
            subscribers.append(subs)
            for _k in deps:
                self.sig.connect(subs,sender=_k)    
        if init:
            deps_set=set()
            for deps,func,target in constrains:
                deps_set.update(deps)
            for dep in deps_set:
                self.sig.send(dep)
        return subscribers
        
    def set(self,k,v,check=True):
        _changed=self.__d2c_instance.set(k,v,check=check)
        if _changed:
            self.sig.send(k)
        return _changed
            
    def get(self,k):
        return self.__d2c_instance.get(k)
    
    def update(self,d,check=True):
        k_changed=[]
        for k,v in d.items():
            _changed=self.__d2c_instance.set(k,v,check=check)
            if _changed:
                k_changed.append(k)
        for _k in k_changed:
            self.sig.send(_k)
    
    def __getattr__(self,item):
        return getattr(self.__d2c_instance,item)

def _subscrib(deps, func, target, cons_d2c_ins):
    '''根据需要的参量产生一个订阅函数
    Parameters:
        deps,func,target: 分别为 依赖的key[列表或元组]、约束函数、目标[单key(字符串)，或者多key(列表/元组)]，
            比如 (('k1','k2'), lambda v1,v2:v1+v2, 'k3'), func的返回值应与target数目一致
        cons_d2c_ins: 上面cons_d2c的一个实例
    Return:
        返回一个订阅函数
    '''
    if isinstance(target,str):
        def subscriber(send):
            arg = [cons_d2c_ins.get(k_dep) for k_dep in deps]
            value=func(*arg)
            cons_d2c_ins.set(target,value)
    else:
        def subscriber(send):
            arg = [cons_d2c_ins.get(k_dep) for k_dep in deps]
            value=func(*arg)
            d=dict(zip(target,value))
            cons_d2c_ins.update(d)
    return subscriber