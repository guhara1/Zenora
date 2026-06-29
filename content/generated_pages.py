# 워크플로로 생성한 고유 본문(generated.json)을 읽어 31개 시군 + 8개 권역
# 페이지로 조립한다. FAQ 는 본문 표시 + FAQPage 구조화 데이터로 함께 출력한다.
import json
import os

from . import data
from .shared import assemble_city, assemble_region

_HERE = os.path.dirname(os.path.abspath(__file__))
_GEN_PATH = os.path.join(_HERE, "generated.json")


def _load():
    if not os.path.exists(_GEN_PATH):
        return {"cities": {}, "regions": {}}
    raw = json.load(open(_GEN_PATH, encoding="utf-8"))
    cities = {x["slug"]: x for x in raw.get("cities", [])}
    regions = {x["slug"]: x for x in raw.get("regions", [])}
    return {"cities": cities, "regions": regions}


_GEN = _load()


def _esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def faqpage_jsonld(faqs) -> str:
    if not faqs:
        return ""
    items = ",\n    ".join(
        '{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'.format(
            q=_esc(f["q"]), a=_esc(f["a"])
        )
        for f in faqs if f.get("q") and f.get("a")
    )
    if not items:
        return ""
    return (
        '<script type="application/ld+json">\n'
        '{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n'
        f'  "mainEntity": [\n    {items}\n  ]\n'
        '}\n</script>\n'
    )


def _clip(s: str, n: int = 80) -> str:
    return s if len(s) <= n else s[: n - 1].rstrip("·, ") + "…"


def _city_desc(slug: str) -> str:
    name = data.city_display(slug)
    life = data.CITIES[slug]["life"]
    lifestr = "·".join(life[:2]) if life else "주요 생활권"
    return _clip(f"{name} 출장마사지·홈타이 안내. {lifestr} 생활권과 방문 조건, 예약 전 확인사항을 정리했습니다.")


def _city_h1(slug: str) -> str:
    name = data.city_display(slug)
    if data.CITIES[slug]["districts"]:
        return f"{name} 출장마사지 · 행정구·행정동별 예약 안내"
    return f"{name} 출장마사지 · 대표 생활권별 예약 안내"


def _placeholder(name: str) -> str:
    return (
        f'<section><h2>{name} 지역 안내 준비 중</h2>'
        f'<p>{name} 상세 안내는 콘텐츠 품질 점검 후 공개됩니다.</p></section>'
    )


def city_pages():
    pages = []
    for slug in data.CITY_ORDER:
        c = data.CITIES[slug]
        name = data.city_display(slug)
        reg = c["region"]
        reg_name = data.REGIONS[reg]["name"]
        gen = _GEN["cities"].get(slug)
        unique = gen["body_html"] if gen else _placeholder(name)
        extra = faqpage_jsonld(gen["faqs"]) if gen else ""
        pages.append({
            "path": data.city_url(slug).strip("/") + "/",
            "title": f"{name} 출장마사지·홈타이 | {reg_name} 방문 관리 예약 안내",
            "desc": _city_desc(slug),
            "h1": _city_h1(slug),
            "body": assemble_city(slug, unique),
            "extra_head": extra,
            "breadcrumb": [("시군 안내", "/gyeonggi/cities/"), (name, None)],
        })
    return pages


def region_pages():
    pages = []
    for slug in data.REGION_ORDER:
        r = data.REGIONS[slug]
        gen = _GEN["regions"].get(slug)
        unique = gen["body_html"] if gen else _placeholder(r["name"])
        extra = faqpage_jsonld(gen["faqs"]) if gen else ""
        desc = _clip(f"{r['name']} 출장마사지·홈타이 안내. {r['subtitle']} 생활권과 예약 전 확인사항을 정리했습니다.")
        pages.append({
            "path": data.region_url(slug).strip("/") + "/",
            "title": f"{r['name']} 출장마사지 | {r['subtitle']} 지역 안내",
            "desc": desc,
            "h1": f"{r['name']} 출장마사지 · {r['subtitle']} 안내",
            "body": assemble_region(slug, unique),
            "extra_head": extra,
            "breadcrumb": [("권역 안내", "/gyeonggi/area/"), (r["name"], None)],
        })
    return pages
