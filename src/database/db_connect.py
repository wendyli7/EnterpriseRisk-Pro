"""
db_connect.py

企业风险项目数据库连接模块

功能：
1. 读取数据库配置
2. 创建SQLAlchemy连接池
3. 管理数据库Session
4. 测试数据库连接

Author: Wendy
Project: EnterpriseRisk-Pro
"""


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

from src.utils.config import config


class DatabaseManager:
    """
    数据库管理类
    """

    def __init__(self):

        # 获取数据库配置
        self.db_config = config.get_database_config()

        # 密码URL编码
        password = quote_plus(
            self.db_config["password"]
        )

        # 数据库连接地址
        self.connection_url = (
            f"mysql+pymysql://"
            f"{self.db_config['user']}:"
            f"{password}@"
            f"{self.db_config['host']}:"
            f"{self.db_config['port']}/"
            f"{self.db_config['database']}"
            f"?charset={self.db_config['charset']}"
        )


        # 创建数据库引擎
        self.engine = create_engine(

            self.connection_url,

            # 连接池配置
            pool_size=10,

            max_overflow=20,

            pool_recycle=3600,

            echo=False

        )


        # 创建Session
        self.SessionLocal = sessionmaker(
            bind=self.engine
        )



    def get_session(self):
        """
        获取数据库Session
        """

        return self.SessionLocal()



    def test_connection(self):
        """
        测试数据库连接
        """

        try:

            with self.engine.connect() as conn:

                result = conn.execute(
                    text("SELECT 1")
                )

                print(
                    "✅ MySQL数据库连接成功"
                )

                print(
                    "测试结果:",
                    result.fetchone()
                )


        except Exception as e:

            print(
                "❌ MySQL数据库连接失败"
            )

            print(e)



# 创建全局数据库对象

database = DatabaseManager()