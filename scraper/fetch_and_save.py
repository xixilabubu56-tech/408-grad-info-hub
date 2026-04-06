import requests
from bs4 import BeautifulSoup
import sys
import os
import hashlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from database import SessionLocal
from models import Institution
from utils import PROJECT_985, PROJECT_211


def make_school_code(name):
    return f"YZW-{hashlib.md5(name.encode('utf-8')).hexdigest()[:8].upper()}"

def save_to_db(institutions_data):
    db = SessionLocal()
    try:
        created = 0
        updated = 0
        for data in institutions_data:
            existing = db.query(Institution).filter(Institution.name == data['name']).first()
            if not existing:
                new_inst = Institution(
                    name=data['name'],
                    province=data['province'],
                    city=data['province'],
                    is_985=data['name'] in PROJECT_985,
                    is_211=data['name'] in PROJECT_211,
                    is_double_first_class=data['name'] in PROJECT_985 or data['name'] in PROJECT_211,
                    school_code=make_school_code(data['name'])
                )
                db.add(new_inst)
                created += 1
            else:
                existing.province = data['province']
                existing.city = data['province']
                existing.is_985 = data['name'] in PROJECT_985
                existing.is_211 = data['name'] in PROJECT_211
                existing.is_double_first_class = data['name'] in PROJECT_985 or data['name'] in PROJECT_211
                existing.school_code = existing.school_code or make_school_code(data['name'])
                updated += 1
        
        db.commit()
        print(f"✅ 新增 {created} 所院校，更新 {updated} 所院校")
    except Exception as e:
        print(f"❌ 保存到数据库失败: {e}")
        db.rollback()
    finally:
        db.close()

def fetch_and_save():
    url = "https://yz.chsi.com.cn/zsml/queryAction.do"
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    print("🚀 开始向研招网发送请求抓取数据...")
    try:
        session.get("https://yz.chsi.com.cn/zsml/zyfx_search.jsp", headers=headers)
        
        params = {
            "ssdm": "",       
            "dwmc": "",       
            "mldm": "zyxw",   
            "yjxkdm": "0812", 
            "zymc": "",       
            "xxfs": "1"       
        }
        
        response = session.post("https://yz.chsi.com.cn/zsml/queryAction.do", headers=headers, data=params, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='ch-table')
        
        if not table:
            print("❌ 未找到数据表格。")
            return
            
        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else []
        
        if not rows:
            print("⚠️ 查询结果为空。")
            return
            
        parsed_data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                school_name = cols[0].text.strip()
                if ')' in school_name:
                    school_name = school_name.split(')')[-1]
                    
                location = cols[1].text.strip()
                if ')' in location:
                    location = location.split(')')[-1]
                    
                parsed_data.append({
                    "name": school_name,
                    "province": location
                })
        
        print(f"📊 成功抓取到 {len(parsed_data)} 所院校的数据，准备存入数据库...")
        save_to_db(parsed_data)
        
    except Exception as e:
        print(f"❌ 请求发生错误: {e}")

if __name__ == "__main__":
    fetch_and_save()
