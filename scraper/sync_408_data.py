import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from database import Base, engine, SessionLocal
from models import Institution, Major, HistoricalData, OfficialNotice
from seed_comprehensive_408 import seed_database
from fetch_and_save import fetch_and_save
from fetch_408_details import fetch_408_details


def print_counts():
    db = SessionLocal()
    try:
        print(f"院校数: {db.query(Institution).count()}")
        print(f"专业数: {db.query(Major).count()}")
        print(f"历年数据数: {db.query(HistoricalData).count()}")
        print(f"通知数: {db.query(OfficialNotice).count()}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="先清空核心表，再重建 408 数据")
    parser.add_argument("--with-yzw-list", action="store_true", help="额外执行研招网院校列表同步")
    parser.add_argument("--with-detail-demo", action="store_true", help="额外执行 408 详情样例同步")
    args = parser.parse_args()

    print("🚀 开始同步 408 数据")
    Base.metadata.create_all(bind=engine)
    seed_database(reset=args.reset)

    if args.with_yzw_list:
        print("📚 开始同步研招网院校列表")
        fetch_and_save()

    if args.with_detail_demo:
        print("🧠 开始同步 408 详情样例")
        fetch_408_details()

    print("📊 同步后的数据库统计")
    print_counts()
    print("✅ 408 数据同步流程完成")


if __name__ == "__main__":
    main()
