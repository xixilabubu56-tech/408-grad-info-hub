import requests
from bs4 import BeautifulSoup
import sys
import os
import time

# 把 backend 目录加入到 Python 搜索路径中，以便我们能导入数据库模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from database import SessionLocal
from models import Institution

def save_to_db(institutions_data):
    """将爬取的数据保存到数据库"""
    db = SessionLocal()
    try:
        count = 0
        for data in institutions_data:
            # 检查学校是否已经存在
            existing = db.query(Institution).filter(Institution.name == data['name']).first()
            if not existing:
                new_inst = Institution(
                    name=data['name'],
                    province=data['province'],
                    # 研招网列表通常不直接提供 985/211 标签，这里为了演示效果，我们简单匹配一下顶尖名校
                    is_985=data['name'] in ["北京大学", "清华大学", "浙江大学", "复旦大学", "上海交通大学", "南京大学", "中国科学技术大学", "武汉大学", "华中科技大学", "中国人民大学"],
                    is_211=data['name'] in ["北京邮电大学", "西安电子科技大学", "北京交通大学", "南京航空航天大学"] or data['name'] in ["北京大学", "清华大学", "浙江大学", "复旦大学", "上海交通大学", "南京大学", "中国科学技术大学", "武汉大学", "华中科技大学", "中国人民大学"],
                    school_code="00000" # 演示用假代码
                )
                db.add(new_inst)
                count += 1
        
        db.commit()
        print(f"✅ 成功将 {count} 条新院校数据保存到 MySQL 数据库！")
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
                # 研招网的名字通常带有类似 "(10001)北京大学" 的格式，我们尝试把前面的括号及数字去掉
                if ')' in school_name:
                    school_name = school_name.split(')')[-1]
                    
                location = cols[1].text.strip()
                # 研招网的所在地通常带有类似 "(11)北京市" 的格式
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
