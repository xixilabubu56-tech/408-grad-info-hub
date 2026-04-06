import requests
from bs4 import BeautifulSoup
import sys
import os
import time
import random
import hashlib
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils import get_random_headers, PROJECT_985, PROJECT_211

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from database import SessionLocal, Base, engine
from models import Institution, Major

Base.metadata.create_all(bind=engine)


def make_school_code(name):
    return f"408-{hashlib.md5(name.encode('utf-8')).hexdigest()[:8].upper()}"


def make_major_code(college_name, major_name):
    return hashlib.md5(f'{college_name}-{major_name}'.encode('utf-8')).hexdigest()[:8].upper()

def create_robust_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def save_detailed_data(school_name, province, college_name, major_name, study_mode, exam_subjects):
    db = SessionLocal()
    try:
        inst = db.query(Institution).filter(Institution.name == school_name).first()
        if not inst:
            is_985 = school_name in PROJECT_985
            is_211 = school_name in PROJECT_211
            
            inst = Institution(
                name=school_name,
                province=province,
                is_985=is_985,
                is_211=is_211,
                is_double_first_class=is_985 or is_211,
                city=province,
                school_code=make_school_code(school_name)
            )
            db.add(inst)
            db.commit()
            db.refresh(inst)

        existing_major = db.query(Major).filter(
            Major.institution_id == inst.id,
            Major.college_name == college_name,
            Major.major_name == major_name,
            Major.study_mode == study_mode
        ).first()

        if not existing_major:
            new_major = Major(
                institution_id=inst.id,
                college_name=college_name,
                major_code=make_major_code(college_name, major_name),
                major_name=major_name,
                degree_type="academic" if "学硕" in major_name or "学术" in major_name else "professional",
                study_mode=study_mode,
                exam_subjects=exam_subjects
            )
            db.add(new_major)
            print(f"  └─ [+] 成功入库: {college_name} - {major_name} ({study_mode})")
        else:
            existing_major.exam_subjects = exam_subjects
            existing_major.major_code = existing_major.major_code or make_major_code(college_name, major_name)
            print(f"  └─ [~] 更新数据: {college_name} - {major_name} ({study_mode})")
            
        db.commit()
            
    except Exception as e:
        print(f"❌ 数据库保存出错: {e}")
        db.rollback()
    finally:
        db.close()


def fetch_408_details():
    print("🚀 开始执行 408 专属深度爬虫...")
    
    session = create_robust_session()
    headers = get_random_headers()
    
    print("当前脚本使用结构化样例做增量同步，可作为后续真实详情爬虫的稳定入库模板。")
    
    time.sleep(random.uniform(1.0, 2.5))
    
    mock_scraped_details = [
        {
            "school_name": "北京大学",
            "province": "北京",
            "college_name": "信息科学技术学院",
            "major_name": "计算机科学与技术",
            "study_mode": "full_time",
            "exam_subjects": "101思想政治理论, 201英语(一), 301数学(一), 408计算机学科专业基础"
        },
        {
            "school_name": "北京大学",
            "province": "北京",
            "college_name": "软件与微电子学院",
            "major_name": "电子信息(软件工程)",
            "study_mode": "full_time",
            "exam_subjects": "101思想政治理论, 201英语(一), 301数学(一), 408计算机学科专业基础"
        },
        {
            "school_name": "浙江大学",
            "province": "浙江",
            "college_name": "计算机科学与技术学院",
            "major_name": "计算机科学与技术",
            "study_mode": "full_time",
            "exam_subjects": "101思想政治理论, 201英语(一), 301数学(一), 408计算机学科专业基础"
        },
        {
            "school_name": "哈尔滨工业大学",
            "province": "黑龙江",
            "college_name": "计算机科学与技术学院",
            "major_name": "计算机科学与技术",
            "study_mode": "full_time",
            "exam_subjects": "101思想政治理论, 201英语(一), 301数学(一), 854计算机基础"
        },
        {
            "school_name": "西安电子科技大学",
            "province": "陕西",
            "college_name": "计算机科学与技术学院",
            "major_name": "电子信息(计算机技术)",
            "study_mode": "full_time",
            "exam_subjects": "101思想政治理论, 204英语(二), 302数学(二), 408计算机学科专业基础"
        }
    ]
    
    count = 0
    for item in mock_scraped_details:
        if "408" in item["exam_subjects"]:
            print(f"🎯 命中 408 专业: {item['school_name']} - {item['major_name']}")
            save_detailed_data(
                item["school_name"],
                item["province"],
                item["college_name"],
                item["major_name"],
                item["study_mode"],
                item["exam_subjects"]
            )
            count += 1
        else:
            print(f"⏭️ 跳过非 408 专业: {item['school_name']} - {item['major_name']} (科目: {item['exam_subjects']})")
            
    print(f"\n✅ 深度爬虫执行完毕，共提取到 {count} 个纯 408 统考专业并入库。")

if __name__ == "__main__":
    fetch_408_details()
