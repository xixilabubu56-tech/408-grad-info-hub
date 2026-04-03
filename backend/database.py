import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

# 读取 MySQL 连接地址
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost:3306/grad_info_408?charset=utf8mb4"
)

# 创建数据库引擎，开启 MySQL 专属的连接池优化
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

# 创建会话本地类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础映射类
Base = declarative_base()

def get_db():
    """FastAPI 依赖注入，用于获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
