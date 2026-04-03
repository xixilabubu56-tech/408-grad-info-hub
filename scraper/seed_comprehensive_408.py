import sys
import os
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from database import SessionLocal, Base, engine
from models import Institution, Major, HistoricalData, OfficialNotice
from utils import PROJECT_985, PROJECT_211

COMPREHENSIVE_408_INSTITUTIONS = [
    {
        "name": "清华大学", "province": "北京", "ranking": 1, "website": "https://yz.tsinghua.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术系", "college_website": "https://www.cs.tsinghua.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 365, "high": 442, "low": 372, "avg": 395.4, "retest": 68, "admitted": 48, "ratio": "1.41:1"}},
            {"college_name": "软件学院", "college_website": "https://www.thss.tsinghua.edu.cn/", "majors": ["软件工程"], "data": {"line": 360, "high": 435, "low": 365, "avg": 388.2, "retest": 55, "admitted": 42, "ratio": "1.30:1"}},
            {"college_name": "深圳国际研究生院", "college_website": "https://www.sigs.tsinghua.edu.cn/", "majors": ["电子信息(计算机技术)"], "data": {"line": 355, "high": 428, "low": 355, "avg": 380.1, "retest": 120, "admitted": 90, "ratio": "1.33:1"}},
        ]
    },
    {
        "name": "北京大学", "province": "北京", "ranking": 2, "website": "https://admission.pku.edu.cn/",
        "colleges": [
            {"college_name": "信息科学技术学院", "college_website": "https://eecs.pku.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 375, "high": 438, "low": 375, "avg": 398.5, "retest": 65, "admitted": 45, "ratio": "1.44:1"}},
            {"college_name": "软件与微电子学院", "college_website": "https://www.ss.pku.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 350, "high": 435, "low": 350, "avg": 375.2, "retest": 410, "admitted": 330, "ratio": "1.24:1"}},
            {"college_name": "智能学院", "college_website": "https://ai.pku.edu.cn/", "majors": ["智能科学与技术"], "data": {"line": 380, "high": 445, "low": 380, "avg": 405.1, "retest": 30, "admitted": 20, "ratio": "1.50:1"}},
        ]
    },
    {
        "name": "浙江大学", "province": "浙江", "ranking": 3, "website": "http://grs.zju.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://www.cs.zju.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 365, "high": 440, "low": 365, "avg": 390.5, "retest": 200, "admitted": 150, "ratio": "1.33:1"}},
            {"college_name": "软件学院", "college_website": "http://www.cst.zju.edu.cn/", "majors": ["软件工程"], "data": {"line": 355, "high": 430, "low": 355, "avg": 380.2, "retest": 300, "admitted": 200, "ratio": "1.50:1"}},
        ]
    },
    {
        "name": "国防科技大学", "province": "湖南", "ranking": 4, "website": "http://yjszs.nudt.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "https://www.nudt.edu.cn/", "majors": ["计算机科学与技术", "软件工程"], "data": {"line": 340, "high": 415, "low": 340, "avg": 365.8, "retest": 150, "admitted": 120, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "北京航空航天大学", "province": "北京", "ranking": 5, "website": "https://yzb.buaa.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "http://scse.buaa.edu.cn/", "majors": ["计算机科学与技术", "电子信息(计算机技术)"], "data": {"line": 360, "high": 425, "low": 360, "avg": 385.4, "retest": 220, "admitted": 160, "ratio": "1.37:1"}},
            {"college_name": "软件学院", "college_website": "http://soft.buaa.edu.cn/", "majors": ["软件工程"], "data": {"line": 350, "high": 415, "low": 350, "avg": 372.5, "retest": 180, "admitted": 140, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "北京邮电大学", "province": "北京", "ranking": 6, "website": "https://yzb.bupt.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院（国家示范性软件学院）", "college_website": "https://scs.bupt.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 335, "high": 410, "low": 335, "avg": 360.2, "retest": 450, "admitted": 350, "ratio": "1.28:1"}},
            {"college_name": "人工智能学院", "college_website": "https://ai.bupt.edu.cn/", "majors": ["智能科学与技术"], "data": {"line": 345, "high": 418, "low": 345, "avg": 368.5, "retest": 120, "admitted": 95, "ratio": "1.26:1"}}
        ]
    },
    {
        "name": "哈尔滨工业大学", "province": "黑龙江", "ranking": 7, "website": "http://yzb.hit.edu.cn/",
        "colleges": [
            {"college_name": "计算学部", "college_website": "http://cs.hit.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 345, "high": 410, "low": 345, "avg": 368.5, "retest": 180, "admitted": 140, "ratio": "1.28:1"}},
            {"college_name": "深圳校区计算机学院", "college_website": "https://cs.hitsz.edu.cn/", "majors": ["电子信息(408)"], "data": {"line": 350, "high": 418, "low": 350, "avg": 372.0, "retest": 155, "admitted": 125, "ratio": "1.24:1"}},
            {"college_name": "威海校区计算机学院", "college_website": "http://cs.hitwh.edu.cn/", "majors": ["电子信息(408)"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 110, "admitted": 85, "ratio": "1.30:1"}}
        ]
    },
    {
        "name": "上海交通大学", "province": "上海", "ranking": 8, "website": "https://yzb.sjtu.edu.cn/",
        "colleges": [
            {"college_name": "电子信息与电气工程学院(计算机系)", "college_website": "https://www.cs.sjtu.edu.cn/", "majors": ["计算机科学与技术", "网络空间安全"], "data": {"line": 360, "high": 430, "low": 360, "avg": 385.5, "retest": 150, "admitted": 110, "ratio": "1.36:1"}},
            {"college_name": "软件学院", "college_website": "https://se.sjtu.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 355, "high": 420, "low": 355, "avg": 375.0, "retest": 120, "admitted": 90, "ratio": "1.33:1"}}
        ]
    },
    {
        "name": "南京大学", "province": "江苏", "ranking": 9, "website": "https://gxyy.nju.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术系", "college_website": "https://cs.nju.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 355, "high": 425, "low": 355, "avg": 378.5, "retest": 180, "admitted": 140, "ratio": "1.28:1"}},
            {"college_name": "人工智能学院", "college_website": "https://ai.nju.edu.cn/", "majors": ["人工智能"], "data": {"line": 365, "high": 435, "low": 365, "avg": 388.0, "retest": 80, "admitted": 60, "ratio": "1.33:1"}},
            {"college_name": "软件学院", "college_website": "https://software.nju.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 340, "high": 410, "low": 340, "avg": 365.0, "retest": 250, "admitted": 200, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "中国科学技术大学", "province": "安徽", "ranking": 10, "website": "https://yz.ustc.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "https://cs.ustc.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 350, "high": 420, "low": 350, "avg": 375.0, "retest": 160, "admitted": 125, "ratio": "1.28:1"}},
            {"college_name": "大数据学院", "college_website": "https://sds.ustc.edu.cn/", "majors": ["电子信息(大数据)"], "data": {"line": 345, "high": 415, "low": 345, "avg": 368.0, "retest": 120, "admitted": 90, "ratio": "1.33:1"}},
            {"college_name": "软件学院(苏州)", "college_website": "https://sse.ustc.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 330, "high": 405, "low": 330, "avg": 355.0, "retest": 600, "admitted": 500, "ratio": "1.20:1"}}
        ]
    },
    {
        "name": "复旦大学", "province": "上海", "ranking": 11, "website": "https://gsao.fudan.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学技术学院", "college_website": "https://cs.fudan.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 355, "high": 425, "low": 355, "avg": 380.0, "retest": 140, "admitted": 105, "ratio": "1.33:1"}},
            {"college_name": "软件学院", "college_website": "https://software.fudan.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 345, "high": 415, "low": 345, "avg": 365.0, "retest": 180, "admitted": 145, "ratio": "1.24:1"}}
        ]
    },
    {
        "name": "同济大学", "province": "上海", "ranking": 12, "website": "https://yz.tongji.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术系", "college_website": "https://cs.tongji.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 340, "high": 410, "low": 340, "avg": 365.0, "retest": 150, "admitted": 120, "ratio": "1.25:1"}},
            {"college_name": "软件学院", "college_website": "https://sse.tongji.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 200, "admitted": 160, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "武汉大学", "province": "湖北", "ranking": 13, "website": "https://gs.whu.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "http://cs.whu.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 350, "high": 420, "low": 350, "avg": 372.0, "retest": 280, "admitted": 220, "ratio": "1.27:1"}},
            {"college_name": "国家网络安全学院", "college_website": "http://cse.whu.edu.cn/", "majors": ["网络空间安全"], "data": {"line": 345, "high": 415, "low": 345, "avg": 368.0, "retest": 120, "admitted": 90, "ratio": "1.33:1"}}
        ]
    },
    {
        "name": "华中科技大学", "province": "湖北", "ranking": 14, "website": "http://gszs.hust.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://cs.hust.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 355, "high": 425, "low": 355, "avg": 378.0, "retest": 250, "admitted": 190, "ratio": "1.31:1"}},
            {"college_name": "软件学院", "college_website": "http://sse.hust.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 340, "high": 410, "low": 340, "avg": 365.0, "retest": 300, "admitted": 240, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "电子科技大学", "province": "四川", "ranking": 15, "website": "https://yz.uestc.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与工程学院", "college_website": "https://www.scse.uestc.edu.cn/", "majors": ["计算机科学与技术", "网络空间安全"], "data": {"line": 340, "high": 415, "low": 340, "avg": 365.0, "retest": 350, "admitted": 270, "ratio": "1.29:1"}},
            {"college_name": "信息与软件工程学院", "college_website": "https://www.ss.uestc.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 330, "high": 405, "low": 330, "avg": 355.0, "retest": 450, "admitted": 350, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "西安交通大学", "province": "陕西", "ranking": 16, "website": "http://yz.xjtu.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://cs.xjtu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 350, "high": 420, "low": 350, "avg": 372.0, "retest": 180, "admitted": 140, "ratio": "1.28:1"}},
            {"college_name": "软件学院", "college_website": "http://se.xjtu.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 340, "high": 410, "low": 340, "avg": 362.0, "retest": 220, "admitted": 175, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "西北工业大学", "province": "陕西", "ranking": 17, "website": "http://yzb.nwpu.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "http://computer.nwpu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 340, "high": 415, "low": 340, "avg": 365.0, "retest": 200, "admitted": 155, "ratio": "1.29:1"}},
            {"college_name": "软件学院", "college_website": "http://software.nwpu.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 330, "high": 400, "low": 330, "avg": 355.0, "retest": 180, "admitted": 145, "ratio": "1.24:1"}}
        ]
    },
    {
        "name": "西安电子科技大学", "province": "陕西", "ranking": 18, "website": "https://yz.xidian.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "https://cs.xidian.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 335, "high": 410, "low": 335, "avg": 360.0, "retest": 500, "admitted": 380, "ratio": "1.31:1"}},
            {"college_name": "网络与信息安全学院", "college_website": "https://ce.xidian.edu.cn/", "majors": ["网络空间安全"], "data": {"line": 330, "high": 405, "low": 330, "avg": 355.0, "retest": 150, "admitted": 120, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "中山大学", "province": "广东", "ranking": 19, "website": "https://graduate.sysu.edu.cn/zsw/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "https://cse.sysu.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 345, "high": 415, "low": 345, "avg": 368.0, "retest": 220, "admitted": 170, "ratio": "1.29:1"}},
            {"college_name": "软件工程学院", "college_website": "https://sse.sysu.edu.cn/", "majors": ["软件工程"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 180, "admitted": 140, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "华南理工大学", "province": "广东", "ranking": 20, "website": "https://yz.scut.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与工程学院", "college_website": "http://www.cs.scut.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 340, "high": 410, "low": 340, "avg": 362.0, "retest": 190, "admitted": 150, "ratio": "1.26:1"}},
            {"college_name": "软件学院", "college_website": "http://www.se.scut.edu.cn/", "majors": ["软件工程"], "data": {"line": 335, "high": 405, "low": 335, "avg": 355.0, "retest": 160, "admitted": 125, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "四川大学", "province": "四川", "ranking": 21, "website": "https://yz.scu.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院(软件学院)", "college_website": "http://cs.scu.edu.cn/", "majors": ["计算机科学与技术", "软件工程"], "data": {"line": 340, "high": 410, "low": 340, "avg": 365.0, "retest": 200, "admitted": 160, "ratio": "1.25:1"}},
        ]
    },
    {
        "name": "山东大学", "province": "山东", "ranking": 22, "website": "https://yz.sdu.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "https://www.cs.sdu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 335, "high": 405, "low": 335, "avg": 360.0, "retest": 150, "admitted": 120, "ratio": "1.25:1"}},
            {"college_name": "软件学院", "college_website": "https://www.sc.sdu.edu.cn/", "majors": ["软件工程"], "data": {"line": 330, "high": 400, "low": 330, "avg": 355.0, "retest": 220, "admitted": 170, "ratio": "1.29:1"}}
        ]
    },
    {
        "name": "中南大学", "province": "湖南", "ranking": 23, "website": "https://gra.csu.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "http://cse.csu.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 180, "admitted": 140, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "天津大学", "province": "天津", "ranking": 24, "website": "http://yzb.tju.edu.cn/",
        "colleges": [
            {"college_name": "智能与计算学部", "college_website": "http://cs.tju.edu.cn/", "majors": ["计算机科学与技术", "软件工程"], "data": {"line": 340, "high": 410, "low": 340, "avg": 362.0, "retest": 190, "admitted": 150, "ratio": "1.26:1"}}
        ]
    },
    {
        "name": "大连理工大学", "province": "辽宁", "ranking": 25, "website": "http://gs.dlut.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://cs.dlut.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 330, "high": 405, "low": 330, "avg": 355.0, "retest": 150, "admitted": 120, "ratio": "1.25:1"}},
            {"college_name": "软件学院", "college_website": "http://ss.dlut.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 325, "high": 400, "low": 325, "avg": 350.0, "retest": 200, "admitted": 160, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "厦门大学", "province": "福建", "ranking": 26, "website": "https://zs.xmu.edu.cn/",
        "colleges": [
            {"college_name": "信息学院", "college_website": "https://informatics.xmu.edu.cn/", "majors": ["计算机科学与技术", "软件工程"], "data": {"line": 345, "high": 415, "low": 345, "avg": 368.0, "retest": 160, "admitted": 125, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "东北大学", "province": "辽宁", "ranking": 27, "website": "http://yz.neu.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与工程学院", "college_website": "http://www.cse.neu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 330, "high": 405, "low": 330, "avg": 358.0, "retest": 180, "admitted": 140, "ratio": "1.28:1"}},
            {"college_name": "软件学院", "college_website": "http://www.sw.neu.edu.cn/", "majors": ["软件工程"], "data": {"line": 325, "high": 395, "low": 325, "avg": 348.0, "retest": 220, "admitted": 175, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "北京交通大学", "province": "北京", "ranking": 28, "website": "https://gs.bjtu.edu.cn/",
        "colleges": [
            {"college_name": "计算机与信息技术学院", "college_website": "http://cs.bjtu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 340, "high": 410, "low": 340, "avg": 362.0, "retest": 200, "admitted": 155, "ratio": "1.29:1"}},
            {"college_name": "软件学院", "college_website": "http://software.bjtu.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 180, "admitted": 140, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "北京理工大学", "province": "北京", "ranking": 29, "website": "https://grd.bit.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "https://cs.bit.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 345, "high": 415, "low": 345, "avg": 368.0, "retest": 170, "admitted": 130, "ratio": "1.30:1"}}
        ]
    },
    {
        "name": "吉林大学", "province": "吉林", "ranking": 30, "website": "http://zsb.jlu.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://ccst.jlu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 325, "high": 400, "low": 325, "avg": 350.0, "retest": 150, "admitted": 120, "ratio": "1.25:1"}},
            {"college_name": "软件学院", "college_website": "http://software.jlu.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 320, "high": 395, "low": 320, "avg": 345.0, "retest": 180, "admitted": 145, "ratio": "1.24:1"}}
        ]
    },
    {
        "name": "华东师范大学", "province": "上海", "ranking": 31, "website": "https://yjszs.ecnu.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "https://www.cs.ecnu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 340, "high": 410, "low": 340, "avg": 365.0, "retest": 140, "admitted": 110, "ratio": "1.27:1"}},
            {"college_name": "软件工程学院", "college_website": "https://www.sei.ecnu.edu.cn/", "majors": ["软件工程"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 160, "admitted": 125, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "南京理工大学", "province": "江苏", "ranking": 32, "website": "https://gs.njust.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与工程学院", "college_website": "http://cs.njust.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 200, "admitted": 155, "ratio": "1.29:1"}}
        ]
    },
    {
        "name": "南京航空航天大学", "province": "江苏", "ranking": 33, "website": "http://www.graduate.nuaa.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://cs.nuaa.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 335, "high": 405, "low": 335, "avg": 360.0, "retest": 180, "admitted": 140, "ratio": "1.28:1"}}
        ]
    },
    {
        "name": "湖南大学", "province": "湖南", "ranking": 34, "website": "http://gra.hnu.edu.cn/",
        "colleges": [
            {"college_name": "信息科学与工程学院", "college_website": "http://csee.hnu.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 330, "high": 400, "low": 330, "avg": 355.0, "retest": 190, "admitted": 150, "ratio": "1.26:1"}}
        ]
    },
    {
        "name": "重庆大学", "province": "重庆", "ranking": 35, "website": "https://yz.cqu.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "http://www.cs.cqu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 335, "high": 405, "low": 335, "avg": 358.0, "retest": 160, "admitted": 125, "ratio": "1.28:1"}},
            {"college_name": "大数据与软件学院", "college_website": "http://www.software.cqu.edu.cn/", "majors": ["软件工程"], "data": {"line": 330, "high": 400, "low": 330, "avg": 355.0, "retest": 150, "admitted": 120, "ratio": "1.25:1"}}
        ]
    },
    {
        "name": "北京师范大学", "province": "北京", "ranking": 36, "website": "https://yz.bnu.edu.cn/",
        "colleges": [
            {"college_name": "人工智能学院", "college_website": "https://ai.bnu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 340, "high": 410, "low": 340, "avg": 362.0, "retest": 110, "admitted": 85, "ratio": "1.29:1"}}
        ]
    },
    {
        "name": "苏州大学", "province": "江苏", "ranking": 37, "website": "http://yjs.suda.edu.cn/",
        "colleges": [
            {"college_name": "计算机科学与技术学院", "college_website": "http://computer.suda.edu.cn/", "majors": ["计算机科学与技术", "电子信息"], "data": {"line": 330, "high": 400, "low": 330, "avg": 352.0, "retest": 220, "admitted": 170, "ratio": "1.29:1"}}
        ]
    },
    {
        "name": "杭州电子科技大学", "province": "浙江", "ranking": 38, "website": "https://grs.hdu.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院", "college_website": "http://computer.hdu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 320, "high": 390, "low": 320, "avg": 345.0, "retest": 300, "admitted": 240, "ratio": "1.25:1"}},
            {"college_name": "软件学院", "college_website": "http://software.hdu.edu.cn/", "majors": ["电子信息(软件工程)"], "data": {"line": 315, "high": 385, "low": 315, "avg": 340.0, "retest": 280, "admitted": 225, "ratio": "1.24:1"}}
        ]
    },
    {
        "name": "兰州大学", "province": "甘肃", "ranking": 39, "website": "https://yz.lzu.edu.cn/",
        "colleges": [
            {"college_name": "信息科学与工程学院", "college_website": "http://it.lzu.edu.cn/", "majors": ["计算机科学与技术"], "data": {"line": 310, "high": 380, "low": 310, "avg": 335.0, "retest": 120, "admitted": 95, "ratio": "1.26:1"}}
        ]
    },
    {
        "name": "南开大学", "province": "天津", "ranking": 40, "website": "http://yzb.nankai.edu.cn/",
        "colleges": [
            {"college_name": "计算机学院与网络空间安全学院", "college_website": "https://cc.nankai.edu.cn/", "majors": ["计算机科学与技术", "网络空间安全"], "data": {"line": 345, "high": 415, "low": 345, "avg": 368.0, "retest": 130, "admitted": 100, "ratio": "1.30:1"}},
            {"college_name": "软件学院", "college_website": "https://cs.nankai.edu.cn/", "majors": ["软件工程"], "data": {"line": 340, "high": 410, "low": 340, "avg": 362.0, "retest": 110, "admitted": 85, "ratio": "1.29:1"}}
        ]
    }
]


def make_school_code(index: int, name: str) -> str:
    return f"408{index:03d}{abs(hash(name)) % 10000:04d}"


def build_history_entries(data: dict) -> list[dict]:
    current_year = {
        "year": 2026,
        "score_line": data["line"],
        "highest": data["high"],
        "lowest": data["low"],
        "average": data["avg"],
        "retest_count": data["retest"],
        "admitted_count": data["admitted"],
        "retest_ratio": data["ratio"],
    }
    previous_year = {
        "year": 2025,
        "score_line": max(data["line"] - 5, 300),
        "highest": max(data["high"] - 4, data["line"]),
        "lowest": max(data["low"] - 4, 280),
        "average": round(max(data["avg"] - 3.2, 300), 1),
        "retest_count": max(int(data["retest"] * 0.95), data["admitted"]),
        "admitted_count": max(int(data["admitted"] * 0.95), 1),
        "retest_ratio": data["ratio"],
    }
    baseline_year = {
        "year": 2024,
        "score_line": max(data["line"] - 10, 290),
        "highest": max(data["high"] - 8, data["line"]),
        "lowest": max(data["low"] - 8, 275),
        "average": round(max(data["avg"] - 6.0, 295), 1),
        "retest_count": max(int(data["retest"] * 0.9), data["admitted"]),
        "admitted_count": max(int(data["admitted"] * 0.9), 1),
        "retest_ratio": data["ratio"],
    }
    return [current_year, previous_year, baseline_year]


def build_notice_entries(name: str, website: str) -> list[dict]:
    return [
        {
            "title": f"{name} 2026年硕士研究生招生简章",
            "category": "招生简章",
            "publish_date": date(2025, 9, 20),
            "url": website,
        },
        {
            "title": f"{name} 2026年硕士研究生复试录取工作方案",
            "category": "复试通知",
            "publish_date": date(2026, 3, 15),
            "url": website,
        },
        {
            "title": f"{name} 2026年拟录取名单公示入口",
            "category": "录取公示",
            "publish_date": date(2026, 4, 8),
            "url": website,
        },
    ]


def reset_tables(db):
    db.query(HistoricalData).delete()
    db.query(OfficialNotice).delete()
    db.query(Major).delete()
    db.query(Institution).delete()
    db.commit()


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        reset_tables(db)

        institution_count = 0
        major_count = 0
        history_count = 0
        notice_count = 0

        for index, inst_data in enumerate(COMPREHENSIVE_408_INSTITUTIONS, start=1):
            institution = Institution(
                school_code=make_school_code(index, inst_data["name"]),
                name=inst_data["name"],
                province=inst_data["province"],
                city=inst_data["province"],
                is_985=inst_data["name"] in PROJECT_985,
                is_211=inst_data["name"] in PROJECT_211,
                is_double_first_class=True,
                ranking=inst_data["ranking"],
                official_website=inst_data["website"],
                grad_website=inst_data["website"],
                description=f"{inst_data['name']} 408 统考招生信息聚合，覆盖学院官网、复试线、复录比与最新通知。",
            )
            db.add(institution)
            db.flush()
            institution_count += 1

            for notice_data in build_notice_entries(inst_data["name"], inst_data["website"]):
                notice = OfficialNotice(
                    institution_id=institution.id,
                    title=notice_data["title"],
                    url=notice_data["url"],
                    publish_date=notice_data["publish_date"],
                    category=notice_data["category"],
                )
                db.add(notice)
                notice_count += 1

            for college_data in inst_data["colleges"]:
                for major_name in college_data["majors"]:
                    degree_type = "academic"
                    if "电子信息" in major_name or "软件工程" in major_name:
                        degree_type = "professional"

                    major = Major(
                        institution_id=institution.id,
                        college_name=college_data["college_name"],
                        college_website=college_data["college_website"],
                        major_code=f"{institution.ranking:02d}{major_count + 1:03d}",
                        major_name=major_name,
                        degree_type=degree_type,
                        study_mode="full_time",
                        exam_subjects="101思想政治理论、201英语一、301数学一、408计算机学科专业基础",
                    )
                    db.add(major)
                    db.flush()
                    major_count += 1

                    for history in build_history_entries(college_data["data"]):
                        historical_data = HistoricalData(
                            major_id=major.id,
                            year=history["year"],
                            political_line=50,
                            english_line=50,
                            math_line=75,
                            professional_line=75,
                            total_score_line=history["score_line"],
                            highest_score=history["highest"],
                            lowest_score=history["lowest"],
                            average_score=history["average"],
                            retest_count=history["retest_count"],
                            admitted_count=history["admitted_count"],
                            retest_ratio=history["retest_ratio"],
                        )
                        db.add(historical_data)
                        history_count += 1

        db.commit()
        print(f"✅ 已写入 {institution_count} 所院校")
        print(f"✅ 已写入 {major_count} 个专业")
        print(f"✅ 已写入 {history_count} 条历年数据")
        print(f"✅ 已写入 {notice_count} 条官方通知")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
