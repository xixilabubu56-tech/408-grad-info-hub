import os
from sqlalchemy import create_engine
from database import Base, engine
import models  # 导入所有模型以便 SQLAlchemy 识别

print("🚀 开始在数据库中创建表结构...")
try:
    # 这一步会根据 models.py 中的类在数据库中生成对应的表
    # 注意：如果表已经存在，它不会修改或重建。如果需要修改表结构，需要用到 Alembic 这样的迁移工具，这里我们简化处理。
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表结构创建成功！")
except Exception as e:
    print(f"❌ 数据库连接或创建表失败: {e}")
    print("👉 请确保你本地的 MySQL 已经启动，并且在 backend/.env 中配置了正确的账号密码和数据库名。")
