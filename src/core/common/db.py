from common.args import Runtime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB:
    # 单例
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        host = Runtime().ENV['datasource.host']
        port = Runtime().ENV['datasource.port']
        user = Runtime().ENV['datasource.user']
        password = Runtime().ENV['datasource.password']
        # 初始化数据库连接:
        self.engine = create_engine(
            'mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/analy')
        # 创建DBSession类型:

    def get_session(self):
        return sessionmaker(bind=self.engine)
