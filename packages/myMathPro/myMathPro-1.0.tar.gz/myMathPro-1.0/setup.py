from distutils.core import setup

setup(
    name='myMathPro',  # 对外发布模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦',  #描述
    author='admin', # 作者
    author_email='admin@163.com',
    py_modules=['mathPro.addPro','mathPro.multiPro'] # 要发布的模块
)
