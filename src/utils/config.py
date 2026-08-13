"""
config.py
读取项目配置文件
"""

from pathlib import Path
import os
import yaml


class Config:
    """配置管理类"""

    def __init__(self):
        # 项目根目录
        self.project_root = Path(__file__).resolve().parents[2]

        # config.yaml路径
        self.config_path = self.project_root / "config" / "config.yaml"

        # 读取配置
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def get_database_config(self):
        database = dict(self.config["database"])
        environment_keys = {
            "host": "ER_DB_HOST",
            "port": "ER_DB_PORT",
            "user": "ER_DB_USER",
            "password": "ER_DB_PASSWORD",
            "database": "ER_DB_NAME",
            "charset": "ER_DB_CHARSET",
        }
        for field, environment_key in environment_keys.items():
            value = os.getenv(environment_key)
            if value:
                database[field] = value
        database["port"] = int(database["port"])
        return database

    def get_generator_config(self):
        return self.config["generator"]

    def get_output_config(self):
        return self.config["output"]

    def get_risk_config(self):
        return self.config["risk"]

    def get_logging_config(self):
        return self.config["logging"]


config = Config()
