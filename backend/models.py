from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DECIMAL, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Institution(Base):
    """院校表"""
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    school_code = Column(String(20), unique=True, index=True) # 院校代码
    name = Column(String(100), index=True)                   # 院校名称
    province = Column(String(50), index=True)                # 省份
    city = Column(String(50))                                # 城市
    is_985 = Column(Boolean, default=False)
    is_211 = Column(Boolean, default=False)
    is_double_first_class = Column(Boolean, default=False)
    ranking = Column(Integer, default=999)                   # 全国排名或学科排名，数字越小越靠前
    official_website = Column(String(255))
    grad_website = Column(String(255))
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # 关联关系
    majors = relationship("Major", back_populates="institution", cascade="all, delete")
    notices = relationship("OfficialNotice", back_populates="institution", cascade="all, delete")

class Major(Base):
    """专业表"""
    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"))
    college_name = Column(String(100))                       # 招生院系 (例如：计算机科学与技术学院, 软件与微电子学院)
    college_website = Column(String(255))                    # 该具体招生院系的官方网站
    major_code = Column(String(20), index=True)              # 专业代码
    major_name = Column(String(100))                         # 专业名称
    degree_type = Column(String(20))                         # academic / professional
    study_mode = Column(String(20), default="full_time")     # full_time / part_time
    exam_subjects = Column(String(255))                      # 考试科目
    created_at = Column(TIMESTAMP, server_default=func.now())

    # 反向关联
    institution = relationship("Institution", back_populates="majors")
    historical_data = relationship("HistoricalData", back_populates="major", cascade="all, delete")

class HistoricalData(Base):
    """历年分数线与录取数据表"""
    __tablename__ = "historical_data"
    
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id", ondelete="CASCADE"))
    year = Column(Integer, nullable=False)                   # 年份
    political_line = Column(Integer)                         # 政治单科线
    english_line = Column(Integer)                           # 英语单科线
    math_line = Column(Integer)                              # 数学单科线
    professional_line = Column(Integer)                      # 专业课(408)单科线
    total_score_line = Column(Integer)                       # 复试总分线/院线
    highest_score = Column(Integer)                          # 录取最高分
    lowest_score = Column(Integer)                           # 录取最低分
    average_score = Column(DECIMAL(5,2))                     # 录取平均分
    retest_count = Column(Integer)                           # 复试人数 (替换之前的报考人数)
    admitted_count = Column(Integer)                         # 录取人数
    retest_ratio = Column(String(20))                        # 复录比 (复试/录取)，如 "1.2:1"
    
    major = relationship("Major", back_populates="historical_data")

class OfficialNotice(Base):
    """官方通知公告表"""
    __tablename__ = "official_notices"
    
    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)              # 通知标题
    url = Column(String(500), nullable=False)                # 原文链接
    publish_date = Column(Date)                              # 发布日期
    category = Column(String(50))                            # 通知分类
    
    institution = relationship("Institution", back_populates="notices")
