import requests
from bs4 import BeautifulSoup
import time

def fetch_cs_institutions():
    # 更新研招网最新专业目录查询地址
    url = "https://yz.chsi.com.cn/zsml/queryAction.do"
    
    session = requests.Session()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    print("🚀 开始向研招网发送请求，查询 [0812]计算机科学与技术 (全日制) 院校列表...")
    
    try:
        # 1. 研招网需要从入口获取cookie并跟随重定向
        session.get("https://yz.chsi.com.cn/zsml/zyfx_search.jsp", headers=headers)
        
        # 2. 修改表单发送 GET 请求
        params = {
            "ssdm": "",       
            "dwmc": "",       
            "mldm": "zyxw",   
            "yjxkdm": "0812", 
            "zymc": "",       
            "xxfs": "1"       
        }
        
        # 目前多数情况是 POST，但有时也是 GET。如果是404可能接口变成了 GET 或者需要其他路径
        response = session.post("https://yz.chsi.com.cn/zsml/queryAction.do", headers=headers, data=params, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='ch-table')
        
        if not table:
            print("❌ 未找到数据表格，研招网可能需要验证码拦截或数据为空。")
            return
            
        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else []
        
        if not rows:
            print("⚠️ 查询结果为空。")
            return
            
        print(f"\n✅ 成功获取到当前页数据，共 {len(rows)} 所院校！(以下展示前 10 所)\n")
        print(f"{'招生单位':<30} | {'所在地':<15}")
        print("-" * 50)
        
        for row in rows[:10]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                # 处理带有链接和括号的学校名称
                school_name = cols[0].text.strip()
                location = cols[1].text.strip()
                print(f"{school_name:<30} | {location:<15}")
                
    except Exception as e:
        print(f"❌ 请求发生错误: {e}")

if __name__ == "__main__":
    fetch_cs_institutions()
