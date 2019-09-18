'''一些小工具的集合'''

class d2c(object):
    '''dict to class
    
    将字典的调用方式转化为类属性的调用方式；
    字典的关键字须符合类属性的规范，可以赋值'''

    def __init__(self,d):
        assert isinstance(d,dict)
        for k,v in d.items():
            _v=d2c(v) if isinstance(v,dict) else v           
            self.__dict__.update({k:_v})
            
    def todict(self):
        '''重新转化为字典'''
        d={}
        for k,v in self.__dict__.items():
            _v=v.todict() if isinstance(v,d2c) else v
            d.update({k:_v})
        return d