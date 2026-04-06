import os

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session, selectinload
import uvicorn
from dotenv import load_dotenv

from database import get_db
import models

load_dotenv()

cors_origins = os.getenv("CORS_ORIGINS", "*")
allow_origins = ["*"] if cors_origins.strip() == "*" else [
    origin.strip() for origin in cors_origins.split(",") if origin.strip()
]
allow_credentials = allow_origins != ["*"]

app = FastAPI(
    title="408 Grad Info Hub API",
    description="全国计算机统考408研究生招生信息查询系统后端接口",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_tags(inst: models.Institution) -> list[str]:
    tags: list[str] = []
    if inst.is_985:
        tags.append("985")
    if inst.is_211:
        tags.append("211")
    if inst.is_double_first_class:
        tags.append("双一流")
    if not tags:
        tags.append("普通本科")
    if inst.ranking:
        tags.append(f"全国排名 #{inst.ranking}")
    return tags


def build_institution_item(inst: models.Institution) -> dict:
    majors = inst.majors or []
    colleges = {major.college_name for major in majors if major.college_name}
    latest_year = max(
        (
            item.year
            for major in majors
            for item in (major.historical_data or [])
            if item.year
        ),
        default=None,
    )
    sample_majors = sorted({major.major_name for major in majors if major.major_name})[:4]
    return {
        "id": inst.id,
        "school_code": inst.school_code,
        "name": inst.name,
        "province": inst.province,
        "city": inst.city,
        "is985": inst.is_985,
        "is211": inst.is_211,
        "isDoubleFirstClass": inst.is_double_first_class,
        "ranking": inst.ranking,
        "majorCount": len(majors),
        "collegeCount": len(colleges),
        "noticeCount": len(inst.notices or []),
        "latestYear": latest_year,
        "sampleMajors": sample_majors,
        "tags": build_tags(inst),
    }


@app.get("/")
def read_root():
    return {"message": "Welcome to 408 Grad Info Hub API V2!"}


@app.get("/api/health")
def get_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    institution_count = db.query(func.count(models.Institution.id)).scalar() or 0
    return {
        "status": "ok",
        "database": "connected",
        "institutionCount": institution_count,
    }


@app.get("/api/summary")
def get_summary(db: Session = Depends(get_db)):
    institution_count = db.query(func.count(models.Institution.id)).scalar() or 0
    major_count = db.query(func.count(models.Major.id)).scalar() or 0
    notice_count = db.query(func.count(models.OfficialNotice.id)).scalar() or 0
    latest_year = db.query(func.max(models.HistoricalData.year)).scalar()
    college_names = db.query(models.Major.college_name).distinct().all()
    college_count = len([name for name, in college_names if name])
    province_count = db.query(models.Institution.province).distinct().count()
    latest_notice_date = db.query(func.max(models.OfficialNotice.publish_date)).scalar()
    top_institutions = (
        db.query(models.Institution)
        .order_by(models.Institution.ranking.asc())
        .limit(6)
        .all()
    )
    return {
        "institutionCount": institution_count,
        "majorCount": major_count,
        "collegeCount": college_count,
        "noticeCount": notice_count,
        "provinceCount": province_count,
        "latestYear": latest_year,
        "latestNoticeDate": latest_notice_date.strftime("%Y-%m-%d") if latest_notice_date else None,
        "topInstitutions": [
            {
                "id": inst.id,
                "name": inst.name,
                "ranking": inst.ranking,
            }
            for inst in top_institutions
        ],
    }


@app.get("/api/institutions/filters")
def get_institution_filters(db: Session = Depends(get_db)):
    provinces = [
        province
        for province, in (
            db.query(models.Institution.province)
            .distinct()
            .order_by(models.Institution.province.asc())
            .all()
        )
        if province
    ]
    return {
        "provinces": provinces,
        "schoolTypes": [
            {"label": "985 工程", "value": "985"},
            {"label": "211 工程", "value": "211"},
            {"label": "双一流", "value": "double_first_class"},
        ],
        "degreeTypes": [
            {"label": "学硕", "value": "academic"},
            {"label": "专硕", "value": "professional"},
        ],
    }


@app.get("/api/institutions")
def get_institutions(
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    province: str | None = None,
    school_type: str | None = Query(default=None, pattern="^(985|211|double_first_class)?$"),
    degree_type: str | None = Query(default=None, pattern="^(academic|professional)?$"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(models.Institution)
        .outerjoin(models.Major)
        .options(
            selectinload(models.Institution.majors).selectinload(models.Major.historical_data),
            selectinload(models.Institution.notices),
        )
    )

    if q:
        keyword = f"%{q.strip()}%"
        query = query.filter(
            or_(
                models.Institution.name.ilike(keyword),
                models.Institution.province.ilike(keyword),
                models.Institution.city.ilike(keyword),
                models.Major.major_name.ilike(keyword),
                models.Major.college_name.ilike(keyword),
                models.Major.major_code.ilike(keyword),
            )
        )

    if province:
        query = query.filter(models.Institution.province == province)

    if school_type == "985":
        query = query.filter(models.Institution.is_985.is_(True))
    elif school_type == "211":
        query = query.filter(models.Institution.is_211.is_(True))
    elif school_type == "double_first_class":
        query = query.filter(models.Institution.is_double_first_class.is_(True))

    if degree_type:
        query = query.filter(models.Major.degree_type == degree_type)

    institutions = (
        query.distinct()
        .order_by(models.Institution.ranking.asc())
        .offset(skip)
        .limit(min(limit, 200))
        .all()
    )
    return [build_institution_item(inst) for inst in institutions]


@app.get("/api/institutions/{inst_id}")
def get_institution_detail(inst_id: int, db: Session = Depends(get_db)):
    inst = (
        db.query(models.Institution)
        .options(
            selectinload(models.Institution.majors).selectinload(models.Major.historical_data),
            selectinload(models.Institution.notices),
        )
        .filter(models.Institution.id == inst_id)
        .first()
    )
    if not inst:
        raise HTTPException(status_code=404, detail="Institution not found")

    majors = sorted(
        inst.majors,
        key=lambda item: (
            item.college_name or "",
            item.degree_type or "",
            item.major_name or "",
        ),
    )
    colleges = sorted({major.college_name for major in majors if major.college_name})
    result = {
        "id": inst.id,
        "name": inst.name,
        "province": inst.province,
        "city": inst.city,
        "ranking": inst.ranking,
        "is985": inst.is_985,
        "is211": inst.is_211,
        "isDoubleFirstClass": inst.is_double_first_class,
        "official_website": inst.official_website,
        "grad_website": inst.grad_website,
        "description": inst.description,
        "latestYear": max((item.year for major in majors for item in major.historical_data), default=None),
        "lastNoticeDate": (
            max((notice.publish_date for notice in inst.notices if notice.publish_date), default=None)
        ),
        "stats": {
            "majorCount": len(majors),
            "collegeCount": len(colleges),
            "noticeCount": len(inst.notices),
        },
        "colleges": colleges,
        "majors": [],
        "notices": [],
    }

    for notice in sorted(
        inst.notices,
        key=lambda item: (item.publish_date is None, item.publish_date),
        reverse=True,
    ):
        result["notices"].append({
            "id": notice.id,
            "title": notice.title,
            "category": notice.category,
            "date": notice.publish_date.strftime("%Y-%m-%d") if notice.publish_date else None,
            "url": notice.url,
        })

    for major in majors:
        major_dict = {
            "id": major.id,
            "college_name": major.college_name,
            "college_website": major.college_website,
            "major_name": major.major_name,
            "degree_type": major.degree_type,
            "study_mode": major.study_mode,
            "exam_subjects": major.exam_subjects,
            "history": [],
        }
        for h in sorted(major.historical_data, key=lambda item: item.year, reverse=True):
            major_dict["history"].append({
                "year": h.year,
                "score_line": h.total_score_line,
                "highest": h.highest_score,
                "lowest": h.lowest_score,
                "average": float(h.average_score) if h.average_score else None,
                "retest_count": h.retest_count,
                "admitted": h.admitted_count,
                "retest_ratio": h.retest_ratio,
            })
        result["majors"].append(major_dict)

    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
