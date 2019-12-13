'''一些小工具的集合'''

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

    def get(self,keystr,splitsymbol='.'):
        '''根据关键词连接的字符串，获取对应的值
        
        Parameters:
            keystr: 使用符号串联key的字符串，比如'pulse.width.value'
            splitsymbol: 字符串的分割符号，默认为 '.'
        Return:
            返回键值串对应的值
        
        Note: 调用十万次耗时 ~90 ms (2-4层小型字典)'''
        keys=keystr.split(splitsymbol)
        value=self
        for k in keys:
            value=getattr(value,k)
        return value

    def set(self,keystr,value,splitsymbol='.'):
        '''根据关键词连接的字符串，设置对应的值
        
        Parameters:
            keystr: 使用符号串联key的字符串，比如'pulse.width.value'
            value: 待设入的值
            splitsymbol: 字符串的分割符号，默认为 '.'

        Note: 调用十万次耗时 ~100 ms (2-4层小型字典)'''
        keys=keystr.split(splitsymbol)
        ins=self
        for k in keys[:-1]:
            ins=getattr(ins,k)
        setattr(ins,keys[-1],value)


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