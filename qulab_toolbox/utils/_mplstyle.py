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