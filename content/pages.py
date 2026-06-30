# 정적 허브·안내 페이지 — 메인, 시군/권역/행정구/생활권/역세권 허브,
# 이용 장소, 예약 전 확인, 운영 기준, 문의하기.
# 상세(일반구·행정동·생활권·역세권 개별) 페이지는 단계적 확장 대상이다.
from .site import (PHONE, PHONE_DISPLAY, REFERENCES, WHO_HOW_WHY,
                   REGION_NAME, TELEGRAM_WEB, TELEGRAM_PARTNER, TRADE_NAME)
import json
import os

from .shared import CTA, CHECKLIST, _li
from .generated_pages import faqpage_jsonld
from . import data
from . import data_ext as E

_GEN3_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated3.json")


def _load_gen3():
    if not os.path.exists(_GEN3_PATH):
        return {"use": {}, "check": {}}
    raw = json.load(open(_GEN3_PATH, encoding="utf-8"))
    return {"use": {x["slug"]: x for x in raw.get("use", [])},
            "check": {x["slug"]: x for x in raw.get("check", [])}}


_GEN3 = _load_gen3()


def _topic_related(kind, slug):
    """이용 장소/예약 전 확인 상세 페이지 하단 관련 링크."""
    hub = "/gyeonggi/use/" if kind == "use" else "/gyeonggi/check/"
    lst = _USE if kind == "use" else _CHECK
    label = next((l for s, l, _ in lst if s == slug), "")
    head = "이용 장소 전체 보기" if kind == "use" else "예약 전 확인 전체 보기"
    items = [_li(hub, head)]
    for s, l, _ in lst:
        if s != slug:
            items.append(_li(f"{hub}{s}/", f"{l} 보기"))
    cross = ("/gyeonggi/check/", "예약 전 확인사항 모아보기") if kind == "use" \
        else ("/gyeonggi/use/", "이용 장소별 안내 보기")
    items.append(_li(*cross))
    items.append(_li("/gyeonggi/cities/", "경기 시군별 안내 보기"))
    items.append(_li("/gyeonggi/area/", "경기 권역별 안내 보기"))
    if kind == "use":
        intro = (f"{label}은(는) 경기도 방문형 관리에서 자주 확인되는 이용 장소 유형입니다. 같은 경기도라도 "
                 "수원 광교·영통, 성남 분당·판교, 고양 일산 같은 신도시와 역세권, 그리고 양평·가평·이천 같은 외곽 생활권은 "
                 "건물 출입과 주차, 이동 시간 조건이 서로 다릅니다. 아래에서 다른 이용 장소와 예약 전 확인 항목, "
                 "시군·권역별 안내를 함께 살펴보면 방문 전 준비에 도움이 됩니다.")
    else:
        intro = (f"{label}은(는) 경기도에서 예약 전에 미리 확인하면 좋은 항목입니다. 수원·성남·고양 등 시군과 "
                 "신도시·역세권·외곽 생활권마다 방문 환경이 달라 같은 항목이라도 확인 포인트가 조금씩 다릅니다. "
                 "아래에서 다른 예약 전 확인 항목과 이용 장소별 안내, 시군·권역 안내를 함께 살펴보시면 방문 준비가 수월합니다.")
    return ('<section class="related">\n<h2>관련 안내 함께 보기</h2>\n'
            f'<p>{intro}</p>\n'
            f'<ul class="ref-list">\n{chr(10).join(items)}\n</ul>\n</section>\n')


def _grid(items):
    lis = "\n".join(f'<li><a href="{h}">{lbl}</a></li>' for lbl, h in items)
    return f'<ul class="card-grid">\n{lis}\n</ul>'


# ── 경기 메인 (/gyeonggi/) ─────────────────────────────────
_REGION_CARDS = _grid([(data.REGIONS[s]["name"], data.region_url(s))
                       for s in data.REGION_ORDER])
_CITY_CARDS = _grid([(data.city_display(s), data.city_url(s))
                     for s in data.CITY_ORDER])

_MAIN_BODY = f"""
<section id="intro">
<h2>경기도는 시군·행정구·행정동 구조가 중요합니다</h2>
<p>경기도 출장마사지·홈타이는 시군 이름만으로 판단하기 어렵습니다. 경기도는 서울보다 지역 범위가 훨씬 넓고, 같은 도시 안에서도 일반구와 행정동, 생활권, 지하철역, 차량 이동 기준이 서로 다릅니다. 수원은 장안구·권선구·팔달구·영통구로 나뉘고, 같은 수원이라도 팔달구 인계동, 영통구 광교·영통, 권선구 호매실은 이용 환경이 다릅니다. 성남도 분당·판교, 수정·위례, 중원·모란의 생활권이 다르고, 용인은 수지·기흥·처인 권역의 이동 기준이 다릅니다. 그래서 이 사이트는 지역명만 반복하는 대신 시군 → 일반구 → 행정동 → 생활권 → 역세권을 연결해, 방문형 서비스를 찾는 분이 자신의 실제 위치와 이용 장소를 정확히 확인하도록 돕습니다.</p>
</section>

<section id="regions">
<h2>경기도 권역별로 빠르게 찾기</h2>
<p>먼저 큰 권역으로 위치를 좁혀 보세요. 경기남부는 수원·성남·용인을 축으로 한 최대 인구 밀집권이고, 경기북부는 고양 일산권과 의정부 역세권이 거점입니다. 경기서부는 부천·안산·시흥 등 서울·인천과 맞닿은 도시들이 모여 있고, 경기동부는 하남·남양주 신도시권과 동부 외곽 이동권이 함께 묶입니다. 경기외곽은 이천·안성·여주처럼 차량 이동과 사전 예약이 기본이 되는 권역입니다. 여기에 광교·판교·동탄·일산·운정·미사를 묶은 신도시 생활권, 판교·광교·안산·평택 중심의 산업·업무지구, 광명·하남·구리·과천 같은 서울 인접권을 더해 모두 여덟 개 권역으로 안내합니다.</p>
{_REGION_CARDS}
</section>

<section id="cities">
<h2>경기도 31개 시군 안내</h2>
<p>거주하시거나 머무시는 시군을 선택하면 일반구·대표 행정동·생활권·가까운 역세권과 이용 장소별 예약 전 확인사항을 이어서 볼 수 있습니다. 일반구가 있는 도시는 시 → 일반구 → 행정동 구조로, 일반구가 없는 도시는 시 → 대표 생활권 구조로 안내합니다. 일반구가 있는 도시는 수원(4구), 성남·용인·고양·부천(각 3구), 안산·안양(각 2구) 일곱 곳으로 모두 스무 개 구입니다. 각 시군 페이지에는 대표 일반구 또는 대표 생활권, 대표 역, 자택·호텔·오피스텔·업무지구 등 이용 장소 기준을 함께 정리했습니다.</p>
{_CITY_CARDS}
<p><a href="/gyeonggi/cities/">시군 전체 목록</a>에서 권역별로 한눈에 확인할 수 있습니다.</p>
</section>

<section id="districts">
<h2>일반구가 있는 도시를 먼저 확인하세요</h2>
<p>일반구가 있는 도시는 같은 시 안에서도 이동 기준이 크게 달라집니다. 수원은 장안·권선·팔달·영통구, 성남은 수정·중원·분당구, 용인은 처인·기흥·수지구, 고양은 덕양·일산동·일산서구, 부천은 원미·소사·오정구, 안산은 상록·단원구, 안양은 만안·동안구로 나뉩니다. 각 일반구는 상위 시군과 대표 행정동, 대표 생활권으로 연결되며, 자세한 구조는 <a href="/gyeonggi/districts/">행정구 안내</a>에서 확인할 수 있습니다.</p>
</section>

<section id="safety">
<h2>안내 기준과 안전 운영 원칙</h2>
<p>이 사이트는 실제 매장 주소가 없는 방문형 안내 사이트입니다. 그래서 과장된 가격 문구나 검색 순위만을 위한 지역명 반복 페이지는 만들지 않으며, 이용 후기는 실제 이용 경험을 바탕으로 한 대표 사례로 정리합니다. 방문 가능 여부는 행정구역 경계가 아니라 실제 주소와 예약 시간을 기준으로 확인하며, 외곽 지역은 차량 이동과 추가 이동비를 사전에 안내합니다. 양평·가평·연천·포천·안성·여주처럼 지하철이 닿지 않는 지역은 사전 예약과 방문 가능 여부 확인이 특히 중요합니다. 모든 안내는 안내된 관리 범위 안에서만 운영하며, 불법·선정적 서비스는 제공하거나 안내하지 않습니다. 예약 정보는 예약 확인과 연락에 필요한 최소한의 범위에서만 사용합니다.</p>
</section>

<section id="structure">
<h2>생활권·역세권과 이용 안내</h2>
<p>광교·영통, 분당·판교, 동탄신도시, 일산·킨텍스, 운정신도시, 하남·미사처럼 신도시형 생활권과 수원역·인계동, 부천역·상동, 안양·범계·평촌 같은 역세권형 생활권은 <a href="/gyeonggi/life/">생활권 안내</a>와 <a href="/gyeonggi/station/">지하철역 안내</a>에서 정리합니다. 출구별 페이지나 환승역 노선별 페이지는 만들지 않고, 한 역은 하나의 안내로 운영합니다. 자택·호텔·오피스텔·업무지구·신도시·외곽 등 장소별 기준은 <a href="/gyeonggi/use/">이용 장소</a>, 방문 주소·건물 출입·추가 이동비·예약 시간·개인정보 기준은 <a href="/gyeonggi/check/">예약 전 확인</a>에 정리되어 있습니다.</p>
</section>

<section id="topics" class="topic-links">
<h2>자주 찾는 주제별 안내 바로가기</h2>
<p>지역과 이용 장소, 예약 전 확인 항목을 조합해 자주 찾는 안내를 모았습니다. 원하는 주제를 고르면 해당 지역·장소의 확인사항으로 바로 이동합니다.</p>
<div class="topic-cols">
<div class="topic-col">
<h3>시군별 출장마사지·홈타이 안내</h3>
<ul class="ref-list">
<li><a href="/gyeonggi/suwon/">수원 출장마사지 — 광교·영통·인계동 생활권 방문 안내</a></li>
<li><a href="/gyeonggi/seongnam/">성남 출장마사지 — 분당·판교·위례 신도시 방문 안내</a></li>
<li><a href="/gyeonggi/yongin/">용인 출장마사지 — 수지·기흥·처인 권역 방문 안내</a></li>
<li><a href="/gyeonggi/goyang/">고양 출장마사지 — 일산·킨텍스 역세권 방문 안내</a></li>
<li><a href="/gyeonggi/hwaseong/">화성 출장마사지 — 동탄신도시 방문 안내</a></li>
<li><a href="/gyeonggi/bucheon/">부천 출장마사지 — 부천역·상동 역세권 방문 안내</a></li>
</ul>
</div>
<div class="topic-col">
<h3>이용 장소별 예약 전 확인</h3>
<ul class="ref-list">
<li><a href="/gyeonggi/use/home/">자택 방문 마사지 — 공동현관·동호수·주차 확인 안내</a></li>
<li><a href="/gyeonggi/use/hotel/">호텔·숙소 방문 마사지 — 객실 출입·프런트 정책 확인</a></li>
<li><a href="/gyeonggi/use/officetel/">오피스텔 방문 마사지 — 공동현관·엘리베이터 확인</a></li>
<li><a href="/gyeonggi/use/business-district/">업무지구 방문 마사지 — 판교·광교 건물 출입 확인</a></li>
<li><a href="/gyeonggi/use/night/">야간 출장마사지 — 늦은 시간 예약·위치 확인 안내</a></li>
<li><a href="/gyeonggi/use/outer-area/">외곽 지역 방문 마사지 — 차량 이동·추가 이동비 안내</a></li>
</ul>
</div>
<div class="topic-col">
<h3>생활권·역세권·확인 항목</h3>
<ul class="ref-list">
<li><a href="/gyeonggi/life/">경기 신도시·역세권 생활권별 방문 조건 안내</a></li>
<li><a href="/gyeonggi/station/">수원역·판교역·동탄역 등 역세권 인근 방문 안내</a></li>
<li><a href="/gyeonggi/check/address/">방문 주소·동호수 정확히 확인하는 방법</a></li>
<li><a href="/gyeonggi/check/travel-fee/">경기 외곽 추가 이동비 기준 안내</a></li>
<li><a href="/gyeonggi/check/time/">예약 가능 시간대 확인 안내</a></li>
<li><a href="/gyeonggi/cities/">경기 31개 시군 전체 지역 안내 보기</a></li>
</ul>
</div>
</div>
</section>
"""


def _main_page():
    return {
        "path": "gyeonggi/",
        "title": "경기도 출장마사지｜수원·성남·용인·고양·화성 홈타이 지역 안내",
        "desc": "경기도 출장마사지·홈타이 안내. 수원·성남·용인·고양·화성 등 31개 시군과 권역·생활권·역세권별 예약 전 확인사항을 정리했습니다.",
        "h1": "경기도 출장마사지 · 시군·행정구·행정동별 지역 안내",
        "body": _MAIN_BODY + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA,
        "breadcrumb": [],
        "hero": _HERO,
    }


_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">경기도 전지역 방문형 관리 · 시군·행정구·행정동 안내</p>
    <h1>경기도 출장마사지·홈타이<br>지역 안내</h1>
    <p class="hero-lead">수원·성남·용인·고양·화성·부천·안산·평택 등 31개 시군과 권역·생활권·역세권별<br>예약 전 확인사항을 한곳에서 확인하세요.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/gyeonggi/cities/">시군 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>31개</strong><span>시군</span></li>
      <li><strong>8개</strong><span>권역</span></li>
      <li><strong>20개</strong><span>일반구</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""


# ── 시군 허브 (/gyeonggi/cities/) ──────────────────────────
def _cities_hub():
    by_region = []
    for rslug in data.REGION_ORDER[:5]:  # 지리 권역 5개로 묶어 표시
        members = [s for s in data.CITY_ORDER if data.CITIES[s]["region"] == rslug]
        if not members:
            continue
        cards = _grid([(data.city_display(s), data.city_url(s)) for s in members])
        by_region.append(
            f'<section><h2>{data.REGIONS[rslug]["name"]} 시군</h2>'
            f'<p>{data.REGIONS[rslug]["focus"]}</p>{cards}</section>'
        )
    body = (
        '<p class="lead">경기도 31개 시군을 권역별로 정리했습니다. 시군을 고르면 일반구·대표 행정동·생활권·가까운 역세권과 이용 장소별 예약 전 확인사항을 볼 수 있습니다.</p>\n'
        + "\n".join(by_region)
        + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA
    )
    return {
        "path": "gyeonggi/cities/",
        "title": "경기도 시군 안내｜31개 시군 출장마사지 지역 안내",
        "desc": "경기도 31개 시군을 권역별로 정리했습니다. 수원·성남·용인 등 시군별 방문 가능 지역과 예약 전 확인사항을 확인하세요.",
        "h1": "경기도 시군별 안내",
        "body": body,
        "breadcrumb": [("시군 안내", None)],
    }


# ── 권역 허브 (/gyeonggi/area/) ────────────────────────────
def _area_hub():
    cards = _grid([(f'{data.REGIONS[s]["name"]} · {data.REGIONS[s]["subtitle"]}',
                    data.region_url(s)) for s in data.REGION_ORDER])
    body = (
        '<p class="lead">경기도를 큰 권역으로 먼저 좁혀 보세요. 지리 권역(남부·북부·서부·동부·외곽)과 성격 권역(신도시·산업업무·서울 인접권)으로 나누어 안내합니다.</p>\n'
        f'<section><h2>경기도 권역 안내</h2>{cards}</section>'
        + REFERENCES + WHO_HOW_WHY + CTA
    )
    return {
        "path": "gyeonggi/area/",
        "title": "경기도 권역 안내｜남부·북부·서부·동부·외곽·신도시 지역 안내",
        "desc": "경기도를 권역별로 안내합니다. 경기남부·북부·서부·동부·외곽과 신도시·산업업무·서울 인접권 생활권을 확인하세요.",
        "h1": "경기도 권역별 안내",
        "body": body,
        "breadcrumb": [("권역 안내", None)],
    }


# ── 단순 안내(허브) 페이지 빌더 ────────────────────────────
def _simple(path, title, desc, h1, body_inner, crumbs, with_checklist=True):
    body = body_inner
    if with_checklist:
        body += CHECKLIST
    body += REFERENCES + WHO_HOW_WHY + CTA
    return {"path": path, "title": title, "desc": desc, "h1": h1,
            "body": body, "breadcrumb": crumbs}


def _districts_hub():
    rows = []
    for s in data.CITY_ORDER:
        gus = E.city_districts(s)
        if not gus:
            continue
        cname = data.city_display(s)
        gu_cards = _grid([(E.DISTRICTS[g]["name"], E.district_url(g)) for g in gus])
        rows.append(
            f'<section><h2>{cname} {len(gus)}개 구</h2>'
            f'<p>{data.CITIES[s]["focus"]} 각 구를 선택하면 대표 행정동·생활권·가까운 역세권 안내로 이어집니다. '
            f'시 전체는 <a href="{data.city_url(s)}">{cname} 지역 안내</a>에서 확인하세요.</p>{gu_cards}</section>'
        )
    inner = (
        '<p class="lead">경기도에서 일반구(행정구)가 있는 도시는 수원·성남·용인·고양·부천·안산·안양 7곳, 모두 20개 구입니다. 일반구가 있는 도시는 같은 시 안에서도 이동 기준이 달라 시·일반구·행정동을 함께 확인하는 것이 좋습니다.</p>\n'
        + "\n".join(rows)
    )
    return _simple(
        "gyeonggi/districts/",
        "경기도 행정구 안내｜수원·성남·용인·고양·부천·안산·안양 일반구",
        "경기도 일반구(행정구) 안내. 수원 4구, 성남·용인·고양·부천 3구, 안산·안양 2구 등 20개 구의 생활권을 확인하세요.",
        "경기도 행정구(일반구) 안내",
        inner, [("행정구 안내", None)], with_checklist=False,
    )


def _life_hub():
    kinds = [("신도시", "신도시 생활권"), ("역세권", "역세권·상권 생활권"), ("외곽", "외곽 이동 생활권")]
    secs = []
    for kind, title in kinds:
        slugs = [s for s in E.LIFE_ORDER if E.LIFE[s]["kind"] == kind]
        cards = _grid([(E.LIFE[s]["name"], E.life_url(s)) for s in slugs])
        secs.append(f'<section><h2>{title}</h2><p>{title}은(는) 방문 동선과 확인사항이 비슷한 지역을 묶은 단위입니다. 생활권을 선택하면 포함 지역·가까운 역·이용 장소별 확인사항을 볼 수 있습니다.</p>{cards}</section>')
    inner = (
        '<p class="lead">경기도는 신도시·역세권·외곽 이동권에 따라 방문 조건이 다릅니다. 생활권 단위로 묶어 안내하며, 각 생활권은 중심 시군·가까운 역세권과 연결됩니다.</p>\n'
        + "\n".join(secs)
    )
    return _simple(
        "gyeonggi/life/",
        "경기도 생활권 안내｜신도시·역세권·외곽 이동 생활권",
        "경기도 생활권 안내. 광교·판교·동탄·일산 등 신도시와 역세권·외곽 이동 생활권별 방문 조건을 정리합니다.",
        "경기도 생활권 안내",
        inner, [("생활권", None)], with_checklist=False,
    )


def _station_hub():
    cards = _grid([(E.STATIONS[s]["name"], E.station_url(s)) for s in E.STATION_ORDER])
    inner = (
        '<p class="lead">경기도를 지나는 1·4·수인분당·신분당·경의중앙·경춘선 등 주요 역세권을 기준으로 안내합니다. 출구별 페이지나 환승역 노선별 페이지는 만들지 않으며, 한 역은 하나의 안내로 운영합니다.</p>\n'
        f'<section><h2>경기 주요 역세권</h2><p>역을 선택하면 상위 시군·인근 생활권·이용 장소별 확인사항으로 이어집니다.</p>{cards}</section>'
        '<section><h2>역세권 이용 기준</h2><p>역과의 거리는 방문 가능 여부와 직접적인 관련이 없습니다. 경기도 전지역이 방문 범위이며, 역 안내는 위치 설명을 돕는 기준일 뿐입니다. 정확한 가능 여부는 예약 시 실제 주소와 시간으로 확인합니다.</p></section>'
    )
    return _simple(
        "gyeonggi/station/",
        "경기도 지하철역 안내｜수원역·판교역·동탄역 역세권 안내",
        "경기도 지하철역 인근 방문 관리 안내. 수원역·판교역·동탄역 등 주요 역세권 기준으로 확인하세요.",
        "경기도 지하철역별 안내",
        inner, [("지하철역", None)], with_checklist=False,
    )


# ── 이용 장소 (허브 + 8) ───────────────────────────────────
_USE = [
    ("home", "자택 이용", "자택 방문 시 공동현관·동호수·주차·조용한 공간 확보를 미리 확인합니다."),
    ("hotel", "호텔·숙소 이용", "숙소·객실 출입 가능 여부와 프런트 정책을 먼저 확인해야 합니다."),
    ("officetel", "오피스텔 이용", "공동현관·엘리베이터·관리 규정과 방문 가능 시간대를 확인합니다."),
    ("business-district", "업무지구 이용", "판교·광교·동탄 등 업무지구 방문 시 건물 출입과 시간대를 확인합니다."),
    ("night", "야간 예약", "야간 시간대는 문의가 몰릴 수 있어 사전 예약과 위치 확인이 중요합니다."),
    ("newtown", "신도시 이용", "광교·판교·동탄·일산·미사 등 신도시는 단지·동선 기준을 함께 확인합니다."),
    ("outer-area", "외곽 지역 이용", "양평·가평·연천·포천·안성·여주 등 외곽은 차량 이동·추가 이동비를 확인합니다."),
    ("station-area", "역세권 이용", "역 인근 방문도 실제 주소 기준으로 가능 여부를 확인합니다."),
]


def _use_pages():
    pages = []
    cards = _grid([(lbl, f"/gyeonggi/use/{slug}/") for slug, lbl, _ in _USE])
    hub_inner = (
        '<p class="lead">경기도에서는 같은 시군이라도 방문 장소에 따라 확인사항이 다릅니다. 자택·호텔·오피스텔·업무지구·신도시·외곽 등 장소별 예약 전 확인 포인트를 정리했습니다.</p>\n'
        f'<section><h2>이용 장소별 안내</h2>{cards}</section>'
    )
    pages.append(_simple(
        "gyeonggi/use/",
        "경기도 이용 장소 안내｜자택·호텔·오피스텔·업무지구 방문 안내",
        "경기도 방문형 관리 이용 장소 안내. 자택·호텔·오피스텔·업무지구·신도시·외곽 등 장소별 확인사항을 정리했습니다.",
        "경기도 이용 장소별 안내",
        hub_inner, [("이용 장소", None)], with_checklist=False,
    ))
    for slug, lbl, line in _USE:
        gen = _GEN3["use"].get(slug)
        if gen:
            body = (gen["body_html"] + _topic_related("use", slug)
                    + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA)
            extra = faqpage_jsonld(gen["faqs"])
        else:
            body = (
                f'<section><h2>{lbl} 안내</h2><p>{line} 경기도 전지역에서 {lbl.replace(" 이용","")} 방문은 실제 주소와 예약 시간을 기준으로 가능 여부를 확인합니다. 안내된 관리 범위 안에서만 운영하며, 불법·선정적 서비스는 제공하거나 안내하지 않습니다.</p></section>'
                + REFERENCES + WHO_HOW_WHY + CTA
            )
            extra = ""
        pages.append({
            "path": f"gyeonggi/use/{slug}/",
            "title": f"경기도 {lbl} 안내｜방문형 관리 이용 장소",
            "desc": f"경기도 {lbl} 안내. {line}"[:80],
            "h1": f"경기도 {lbl} 안내",
            "body": body, "extra_head": extra,
            "breadcrumb": [("이용 장소", "/gyeonggi/use/"), (lbl, None)],
        })
    return pages


# ── 예약 전 확인 (허브 + 6) ────────────────────────────────
_CHECK = [
    ("address", "방문 주소 확인", "도로명 주소와 동·호수를 정확히 확인하면 방문이 매끄럽습니다."),
    ("building-access", "건물 출입 방식", "공동현관 비밀번호·호출 방식·출입 절차를 미리 확인합니다."),
    ("travel-fee", "추가 이동비 기준", "외곽·장거리 방문은 추가 이동비가 필요할 수 있어 사전 확인이 필요합니다."),
    ("time", "예약 가능 시간", "저녁·주말·야간은 문의가 몰릴 수 있어 여유 있게 예약하는 것이 좋습니다."),
    ("privacy", "개인정보 처리 기준", "예약 확인·연락에 필요한 최소 정보만 사용하며 관리 목적 외로 쓰지 않습니다."),
    ("service-policy", "불법·선정적 서비스 불가 안내", "불법·선정적 서비스는 제공하거나 안내하지 않습니다."),
]


def _check_pages():
    pages = []
    cards = _grid([(lbl, f"/gyeonggi/check/{slug}/") for slug, lbl, _ in _CHECK])
    hub_inner = (
        '<p class="lead">예약 전에 확인하면 좋은 항목을 모았습니다. 방문 주소·건물 출입·추가 이동비·예약 시간·개인정보 처리·서비스 기준을 미리 확인해 주세요.</p>\n'
        f'<section><h2>예약 전 확인 항목</h2>{cards}</section>'
    )
    pages.append(_simple(
        "gyeonggi/check/",
        "경기도 예약 전 확인｜방문 주소·건물 출입·이동비·시간 안내",
        "경기도 출장마사지 예약 전 확인 안내. 방문 주소·건물 출입·추가 이동비·예약 시간·개인정보 기준을 정리했습니다.",
        "경기도 예약 전 확인사항",
        hub_inner, [("예약 전 확인", None)], with_checklist=False,
    ))
    for slug, lbl, line in _CHECK:
        gen = _GEN3["check"].get(slug)
        if gen:
            body = (gen["body_html"] + _topic_related("check", slug)
                    + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA)
            extra = faqpage_jsonld(gen["faqs"])
        else:
            body = (
                f'<section><h2>{lbl}</h2><p>{line} 경기도는 시군·일반구·행정동·생활권에 따라 방문 환경이 다르므로, {lbl} 항목을 예약 단계에서 함께 확인하면 방문이 한층 매끄럽습니다.</p></section>'
                + REFERENCES + WHO_HOW_WHY + CTA
            )
            extra = ""
        pages.append({
            "path": f"gyeonggi/check/{slug}/",
            "title": f"경기도 {lbl}｜예약 전 확인",
            "desc": f"경기도 출장마사지 {lbl}. {line}"[:80],
            "h1": f"경기도 출장마사지 {lbl}",
            "body": body, "extra_head": extra,
            "breadcrumb": [("예약 전 확인", "/gyeonggi/check/"), (lbl, None)],
        })
    return pages


# ── 운영 기준 (3) + 문의 ───────────────────────────────────
def _policy_pages():
    std = (
        '<section><h2>콘텐츠 작성 기준</h2><p>이 사이트의 모든 지역 안내는 경기도 행정구역(시군·일반구·행정동), 주요 생활권, 가까운 지하철역, 이용 장소별 예약 전 확인사항을 기준으로 작성합니다. 지역명만 바꾼 본문, 가짜 후기, 허위 평점, 과장된 가격 문구, 검색 순위 조작을 위한 대량 저가치 페이지는 만들지 않습니다.</p></section>'
        '<section><h2>업데이트 기준</h2><p>행정구역 변경, 생활권 변화, 지하철역 변화, 신도시 개발, 사용자 문의 흐름, 콘텐츠 품질 점검 결과를 반영해 수정합니다. 본문 분량과 검색 수요가 확보된 페이지부터 단계적으로 공개합니다.</p></section>'
        '<section><h2>서비스 운영 원칙</h2><p>실제 매장 주소가 없는 방문형 안내이므로 LocalBusiness 구조화 데이터와 허위 후기·평점은 사용하지 않습니다. 불법·선정적 서비스는 제공하거나 안내하지 않으며, 안내된 관리 범위 안에서만 운영합니다.</p></section>'
    )
    authors = (
        '<section><h2>작성자</h2><p>경기도 지역 안내 콘텐츠 담당자가 시군·일반구·행정동·생활권·역세권 구조와 이용 장소별 확인사항을 기준으로 작성합니다.</p></section>'
        '<section><h2>검수자</h2><p>운영 책임자 또는 콘텐츠 품질 검수 담당자가 사실관계와 표현 기준을 검수합니다. AI 도구를 사용하더라도 책임 저자와 검수 절차를 명시하며, 결과물의 정확성과 가치를 기준으로 관리합니다.</p></section>'
        '<section><h2>연락</h2><p>콘텐츠 오류 신고나 제휴 문의는 <a href="/gyeonggi/contact/">문의하기</a>를 이용해 주세요.</p></section>'
    )
    privacy = (
        '<section><h2>수집 항목과 목적</h2><p>예약 확인과 연락에 필요한 최소한의 정보(연락처, 방문 지역·시간)만 사용합니다. 수집한 정보는 예약 안내 목적 외로 사용하지 않습니다.</p></section>'
        '<section><h2>보관과 파기</h2><p>예약 목적이 끝나면 관련 정보를 지체 없이 파기하며, 제3자에게 무단으로 제공하지 않습니다.</p></section>'
        '<section><h2>이용자 권리</h2><p>본인 정보의 열람·정정·삭제를 요청할 수 있으며, 요청 시 관련 안내를 따릅니다.</p></section>'
    )
    pages = [
        _simple("gyeonggi/policy/service-standard/",
                "경기도 사이트 콘텐츠·운영 기준 안내",
                "경기도 출장마사지 사이트의 콘텐츠 작성·업데이트·운영 원칙을 공개합니다.",
                "콘텐츠·운영 기준", std, [("운영 기준", None)], with_checklist=False),
        _simple("gyeonggi/policy/authors/",
                "작성자·검수자 안내｜경기도 지역 안내",
                "경기도 지역 안내 콘텐츠의 작성자와 검수 방식, 책임 기준을 공개합니다.",
                "작성자·검수자 안내", authors, [("운영 기준", "/gyeonggi/policy/service-standard/"), ("작성자·검수자", None)], with_checklist=False),
        _simple("gyeonggi/policy/privacy/",
                "개인정보 처리방침｜경기도 지역 안내",
                "경기도 지역 안내 사이트의 개인정보 수집·이용·보관·파기 기준을 안내합니다.",
                "개인정보 처리방침", privacy, [("운영 기준", "/gyeonggi/policy/service-standard/"), ("개인정보 처리방침", None)], with_checklist=False),
    ]
    return pages


def _contact_page():
    inner = (
        f'<section><h2>예약·상담 문의</h2><p>방문 지역과 이용 장소, 희망 시간을 알려주시면 방문 가능 여부를 바로 확인해 드립니다. 상호 {TRADE_NAME}, 연중무휴 24시간 상담.</p><p class="contact-phone"><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></p></section>'
        f'<section><h2>제휴·웹사이트 제작 문의</h2><p>제휴 문의와 웹사이트 제작 문의는 텔레그램으로 받습니다. 아래 버튼으로 연결해 주세요.</p>'
        f'<p class="contact-cta"><a class="footer-cta-btn" href="{TELEGRAM_WEB}" target="_blank" rel="noopener nofollow">✦ 웹사이트 제작문의</a> '
        f'<a class="footer-cta-btn" href="{TELEGRAM_PARTNER}" target="_blank" rel="noopener nofollow">✦ 제휴문의</a></p></section>'
        '<section><h2>콘텐츠 오류 신고</h2><p>지역 정보 오류나 수정이 필요한 내용을 발견하시면 알려주세요. 확인 후 반영합니다.</p></section>'
    )
    return _simple(
        "gyeonggi/contact/",
        "문의하기｜경기도 출장마사지 지역 안내",
        "경기도 출장마사지 예약·상담, 제휴·웹사이트 제작 문의 안내입니다. 상호 간다GO, 전화 0508-202-4719.",
        "문의하기",
        inner, [("문의하기", None)], with_checklist=False,
    )


def static_pages():
    pages = [_main_page(), _cities_hub(), _area_hub(),
             _districts_hub(), _life_hub(), _station_hub()]
    pages += _use_pages()
    pages += _check_pages()
    pages += _policy_pages()
    pages.append(_contact_page())
    return pages
