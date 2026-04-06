import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

# 读取 MySQL 连接地址
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost:3306/grad_info_408?charset=utf8mb4"
)

engine_kwargs = {
    "pool_pre_ping": True,
}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False, "timeout": 30}
else:
    engine_kwargs["pool_size"] = int(os.getenv("DB_POOL_SIZE", "10"))
    engine_kwargs["max_overflow"] = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    engine_kwargs["pool_recycle"] = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    engine_kwargs["pool_timeout"] = int(os.getenv("DB_POOL_TIMEOUT", "30"))

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

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
