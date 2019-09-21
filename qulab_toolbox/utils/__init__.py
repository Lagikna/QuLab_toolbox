'''一些小工具的集合'''

class d2c(object):
    '''dict to class
    
    将字典的调用方式转化为类属性的调用方式；
    字典的关键字须符合类属性的规范，可以赋值'''

    def __init__(self,d):
        '''传入一个字典或者d2c类的实例，构造一个d2c实例'''
        if isinstance(d,d2c):
            d=d.todict()
        assert isinstance(d,dict)
        for k,v in d.items():
            _v=d2c(v) if isinstance(v,dict) else v           
            self.__dict__.update({k:_v})
            
    def todict(self):
        '''从d2c实例提取出字典'''
        d={}
        for k,v in self.__dict__.items():
            _v=v.todict() if isinstance(v,d2c) else v
            d.update({k:_v})
        return d