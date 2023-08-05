from distutils.core import setup
setup(
    name='xiao11', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='xiaoy', # 作者
    author_email='1355833051@qq.com',
    py_modules=['xiao.cfb99','xiao.circles'] # 要发布的模块
)