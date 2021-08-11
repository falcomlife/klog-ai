import getopt
import sys
from common.config import config


class Runtime:
    # 单例
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
            cls._instance.init = True
        return cls._instance

    def __init__(self):
        if self.init:
            self.ENV = {}
            self.ARGS = {}
            self.env()
            self.config = config()
            self.config.read_config(self.ARGS['env'])
            self.options()
            self.ENV.update(self.ARGS)
            self.init = False

    # 配置文件参数读入
    def options(self):
        for section in self.config.cf.sections():
            self.config.cf.options(section)
            for key in self.config.cf.options(section):
                value = self.config.cf.get(section, key)
                self.ENV[section + "." + key] = value

    # 命令行参数读入
    def env(self):
        core_run_step = getopt.getopt(sys.argv[1:], None,
                                      ["core.run.step=", "core.train.type=", "data.prometheus.address=", "env="])
        for param in core_run_step[0]:
            key = str(param[0]).replace('--', '')
            value = param[1]
            self.ARGS[key] = value
