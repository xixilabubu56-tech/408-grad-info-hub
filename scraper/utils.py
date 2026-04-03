import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

# 名校字典 (用于判断学校属性)
PROJECT_985 = {"北京大学", "清华大学", "中国人民大学", "北京航空航天大学", "北京理工大学", "中国农业大学", "北京师范大学", "中央民族大学", "南开大学", "天津大学", "大连理工大学", "吉林大学", "哈尔滨工业大学", "复旦大学", "同济大学", "上海交通大学", "华东师范大学", "南京大学", "东南大学", "浙江大学", "中国科学技术大学", "厦门大学", "山东大学", "武汉大学", "华中科技大学", "中南大学", "湖南大学", "中山大学", "国防科技大学", "四川大学", "华南理工大学", "重庆大学", "电子科技大学", "西安交通大学", "西北工业大学", "西北农林科技大学", "兰州大学", "东北大学", "中国海洋大学"}
PROJECT_211 = PROJECT_985.union({"北京交通大学", "北京工业大学", "北京科技大学", "北京化工大学", "北京邮电大学", "北京林业大学", "中国传媒大学", "中央音乐学院", "对外经济贸易大学", "北京中医药大学", "北京外国语大学", "中国政法大学", "中央财经大学", "华北电力大学", "北京体育大学", "中国地质大学", "上海外国语大学", "上海财经大学", "华东理工大学", "东华大学", "上海大学", "南京航空航天大学", "南京理工大学", "中国矿业大学", "河海大学", "江南大学", "南京农业大学", "中国药科大学", "南京师范大学", "苏州大学", "合肥工业大学", "福州大学", "南昌大学", "郑州大学", "暨南大学", "西南交通大学", "长安大学", "西安电子科技大学", "西北大学", "陕西师范大学"})
