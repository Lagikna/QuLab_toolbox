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
        
        调用一万次耗时 60~80 ms (2-4层字典)'''
        keys=keystr.split(splitsymbol)
        d=self.todict()
        for k in keys:
            d=d.get(k)
        return d

    def set(self,keystr,value,splitsymbol='.'):
        '''根据关键词连接的字符串，设置对应的值
        
        调用一万次耗时 110~160 ms (2-4层字典)'''
        keys=keystr.split(splitsymbol)
        for k in reversed(keys):
            value={k:value}
        d=self.todict()
        d.update(value)
        return d2c(d)