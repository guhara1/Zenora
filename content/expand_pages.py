# 1차-B 상세 페이지: 일반구(20)·생활권(22)·역세권(34)
# 워크플로 생성 본문(generated2.json)을 읽어 조립한다.
import json
import os

from . import data
from . import data_ext as E
from .shared import assemble_district, assemble_life, assemble_station
from .generated_pages import faqpage_jsonld, _clip

_HERE = os.path.dirname(os.path.abspath(__file__))
_GEN2_PATH = os.path.join(_HERE, "generated2.json")


def _load():
    if not os.path.exists(_GEN2_PATH):
        return {"districts": {}, "life": {}, "stations": {}}
    raw = json.load(open(_GEN2_PATH, encoding="utf-8"))
    return {
        "districts": {x["slug"]: x for x in raw.get("districts", [])},
        "life": {x["slug"]: x for x in raw.get("life", [])},
        "stations": {x["slug"]: x for x in raw.get("stations", [])},
    }


_GEN = _load()


def _ph(name):
    return (f'<section><h2>{name} 안내 준비 중</h2>'
            f'<p>{name} 상세 안내는 콘텐츠 품질 점검 후 공개됩니다.</p></section>')


def district_pages():
    pages = []
    for slug in E.DISTRICT_ORDER:
        d = E.DISTRICTS[slug]
        city = d["city"]
        cname = data.city_display(city)
        reg = data.REGIONS[data.CITIES[city]["region"]]["name"]
        gen = _GEN["districts"].get(slug)
        unique = gen["body_html"] if gen else _ph(f"{cname} {d['name']}")
        extra = faqpage_jsonld(gen["faqs"]) if gen else ""
        dong = "·".join(d["dongs"][:3])
        pages.append({
            "path": f"gyeonggi/{city}/{slug}/",
            "title": f"{cname} {d['name']} 출장마사지·홈타이 | 행정동·생활권 안내",
            "desc": _clip(f"{cname} {d['name']} 출장마사지·홈타이 안내. {dong} 등 생활권과 예약 전 확인사항을 정리했습니다."),
            "h1": f"{cname} {d['name']} 출장마사지 · 행정동·생활권 안내",
            "body": assemble_district(slug, unique),
            "extra_head": extra,
            "breadcrumb": [("시군 안내", "/gyeonggi/cities/"),
                           (cname, data.city_url(city)), (d["name"], None)],
        })
    return pages


def life_pages():
    pages = []
    for slug in E.LIFE_ORDER:
        lf = E.LIFE[slug]
        cname = data.city_display(lf["city"])
        gen = _GEN["life"].get(slug)
        unique = gen["body_html"] if gen else _ph(f"{lf['name']} 생활권")
        extra = faqpage_jsonld(gen["faqs"]) if gen else ""
        pages.append({
            "path": f"gyeonggi/life/{slug}/",
            "title": f"{lf['name']} 출장마사지 생활권 안내 | 경기 {lf['kind']} 생활권",
            "desc": _clip(f"{lf['name']} 생활권 출장마사지·홈타이 안내. {cname} 중심 {lf['kind']}형 생활권의 방문 조건을 정리했습니다."),
            "h1": f"{lf['name']} 출장마사지 생활권 안내",
            "body": assemble_life(slug, unique),
            "extra_head": extra,
            "breadcrumb": [("생활권", "/gyeonggi/life/"), (lf["name"], None)],
        })
    return pages


def station_pages():
    pages = []
    for slug in E.STATION_ORDER:
        st = E.STATIONS[slug]
        cname = data.city_display(st["city"])
        gen = _GEN["stations"].get(slug)
        unique = gen["body_html"] if gen else _ph(f"{st['name']} 역세권")
        extra = faqpage_jsonld(gen["faqs"]) if gen else ""
        pages.append({
            "path": f"gyeonggi/station/{slug}/",
            "title": f"{st['name']} 출장마사지 역세권 안내 | {cname} 방문 관리",
            "desc": _clip(f"{st['name']} 인근 출장마사지·홈타이 안내. {cname} 역세권 생활권과 예약 전 확인사항을 정리했습니다."),
            "h1": f"{st['name']} 출장마사지 역세권 안내",
            "body": assemble_station(slug, unique),
            "extra_head": extra,
            "breadcrumb": [("지하철역", "/gyeonggi/station/"), (st["name"], None)],
        })
    return pages
