import configparser
import os


class config:
    # 单例
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
            cls._instance.init = True
        return cls._instance

    def __init__(self):
        if self.init:
            self.env_dist = os.environ
            self.HOME = self.env_dist.get('ANALY_HOME')
            self.cf = configparser.ConfigParser()
            self.init = False
            # 读取配置文件，如果写文件的绝对路径，就可以不用os模块

    def read_config(self, env):
        self.cf.read(self.HOME + "/src/options-" + str(env) + ".ini")

    # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，每个section由[]包裹，即[section])，并以列表的形式返回
    def read_sections(self):
        return self.cf.sections()

    # 获取某个section名为key所对应的键
    def read_section(self, section):
        options = self.cf.options(section)

    # 获取section名为key所对应的全部键值对
    def read_items(self, section):
        return self.cf.items(section)

    # 获取[section]中key对应的值
    def read(self, section, key):
        return self.cf.get(section, key)
