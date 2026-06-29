# 공통 콘텐츠 블록 — 모든 시군·권역 페이지에서 재사용한다.
# 고유 본문(워크플로 생성)은 measure 대상이고, 아래 블록은 class 로 제외된다.
from .site import PHONE, PHONE_DISPLAY, REFERENCES, WHO_HOW_WHY, REGION_NAME
from . import data
from . import data_ext as E

CTA = f"""
<section class="cta">
<h2>예약문의</h2>
<p>방문 지역과 이용 장소, 희망 시간을 알려주시면 방문 가능 여부를 바로 확인해 드립니다. 상호 간다GO, 연중무휴 24시간 상담.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

# 예약 전 체크리스트 — 모든 주요 페이지 공통(지시서 §8·§16)
CHECKLIST = """
<section class="shared checklist">
<h2>예약 전 체크리스트</h2>
<ul class="check-list">
<li>방문 주소(도로명)와 동·호수를 정확히 확인했나요?</li>
<li>공동현관 또는 건물 출입 방식이 있나요?</li>
<li>시군·일반구·행정동이 정확한가요?</li>
<li>가까운 생활권이나 지하철역을 확인했나요?</li>
<li>호텔·숙소·오피스텔 이용 시 출입·관리 규정을 확인했나요?</li>
<li>외곽 지역은 추가 이동비가 필요한지 확인했나요?</li>
<li>예약 가능 시간대와 개인정보 처리 기준을 확인했나요?</li>
</ul>
<p class="check-policy">예약 정보는 예약 확인·연락 목적의 최소 정보만 사용합니다. 자세한 내용은 <a href="/gyeonggi/check/privacy/">개인정보 처리 기준</a>과 <a href="/gyeonggi/check/service-policy/">불법·선정적 서비스 불가 안내</a>를 확인해 주세요. 불법·선정적 서비스는 제공하거나 안내하지 않습니다.</p>
</section>
"""


def _li(href, label):
    return f'<li><a href="{href}">{label}</a></li>'


def related_section(slug: str) -> str:
    """시군 페이지 하단 관련 지역 내부링크(상위 권역·인접 시군·구조 허브)."""
    c = data.CITIES[slug]
    name = data.city_display(slug)
    reg = c["region"]
    reg_name = data.REGIONS[reg]["name"]
    life = "·".join(c["life"]) if c["life"] else "주요 생활권"
    intro = f"{name}의 대표 생활권은 {life}"
    if c["stations"]:
        intro += f", 가까운 역은 {'·'.join(c['stations'])}"
    else:
        intro += ", 지하철 미연결 지역으로 차량 이동이 기본"
    intro += f"입니다. {reg_name} 권역에 속하며 아래에서 인접 시군과 확인사항을 이어서 볼 수 있습니다."
    items = [_li(data.region_url(reg), f"{reg_name} 권역에서 인접 시군 함께 보기")]
    for n in data.neighbors(slug, 4):
        items.append(_li(data.city_url(n), f"{data.city_display(n)} 지역 안내 보기"))
    # 일반구 상세 페이지로 직접 연결(있는 경우)
    for g in E.city_districts(slug):
        items.append(_li(E.district_url(g),
                         f"{name} {E.DISTRICTS[g]['name']} 행정동·생활권 안내"))
    # 생활권 상세 페이지로 직접 연결
    for lf in E.city_life(slug):
        items.append(_li(E.life_url(lf), f"{E.LIFE[lf]['name']} 생활권 안내 보기"))
    # 역세권 상세 페이지로 직접 연결
    for st in E.city_stations(slug):
        items.append(_li(E.station_url(st), f"{E.STATIONS[st]['name']} 역세권 안내 보기"))
    items.append(_li("/gyeonggi/use/", "이용 장소별(자택·호텔·오피스텔) 확인사항"))
    items.append(_li("/gyeonggi/check/", "예약 전 확인사항 모아보기"))
    return (
        '<section class="related">\n<h2>관련 지역·확인사항 함께 보기</h2>\n'
        f'<p>{intro}</p>\n'
        f'<ul class="ref-list">\n{chr(10).join(items)}\n</ul>\n</section>\n'
    )


def assemble_city(slug: str, unique_html: str) -> str:
    """고유 본문 + 관련 링크 + 공통 블록(체크리스트·참고·Who/How/Why·CTA)."""
    return (
        unique_html
        + related_section(slug)
        + CHECKLIST
        + REFERENCES
        + WHO_HOW_WHY
        + CTA
    )


def assemble_region(slug: str, unique_html: str) -> str:
    """권역 페이지: 고유 본문 + 포함 시군 링크 + 공통 블록."""
    r = data.REGIONS[slug]
    members_list = [s for s in r["cities"] if s in data.CITIES]
    city_links = "\n".join(
        _li(data.city_url(s),
            f"{data.city_display(s)} — {'·'.join(data.CITIES[s]['life'][:2])} 생활권 안내")
        for s in members_list
    )
    summary = ", ".join(
        f"{data.city_display(s)}({'·'.join(data.CITIES[s]['life'][:1])})"
        for s in members_list
    )
    members = (
        '<section class="related">\n<h2>이 권역의 시군 안내</h2>\n'
        f'<p>{r["name"]} 권역에서 안내하는 시군과 대표 생활권은 다음과 같습니다 — {summary}. '
        '시군을 고르면 일반구·대표 행정동·생활권·가까운 역세권과 이용 장소별 예약 전 확인사항을 이어서 볼 수 있습니다.</p>\n'
        f'<ul class="ref-list">\n{city_links}\n</ul>\n</section>\n'
    )
    return unique_html + members + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA


# ── 1차-B 상세 페이지 조립(일반구·생활권·역세권) ───────────
def _district_related(slug: str) -> str:
    d = E.DISTRICTS[slug]
    city = d["city"]
    cname = data.city_display(city)
    items = [_li(data.city_url(city), f"{cname} 시 전체 지역 안내 보기")]
    for g in E.city_districts(city):
        if g == slug:
            continue
        items.append(_li(E.district_url(g), f"{cname} {E.DISTRICTS[g]['name']} 안내 보기"))
    for lf in E.city_life(city):
        items.append(_li(E.life_url(lf), f"{E.LIFE[lf]['name']} 생활권 안내 보기"))
    for st in E.city_stations(city):
        items.append(_li(E.station_url(st), f"{E.STATIONS[st]['name']} 역세권 안내 보기"))
    items.append(_li("/gyeonggi/use/", "이용 장소별 확인사항 보기"))
    items.append(_li("/gyeonggi/check/", "예약 전 확인사항 모아보기"))
    dong = "·".join(d["dongs"][:6])
    reg = data.REGIONS[data.CITIES[city]["region"]]["name"]
    lifes = "·".join(E.LIFE[x]["name"] for x in E.city_life(city)) or "주요 생활권"
    stns = "·".join(E.STATIONS[x]["name"] for x in E.city_stations(city)) \
        or "·".join(data.CITIES[city]["stations"]) or "차량 이동 중심"
    intro = (
        f"{cname} {d['name']}은(는) {reg}에 속한 {cname}의 일반구로, 대표 행정동은 {dong} 등입니다. "
        f"{cname}의 대표 생활권은 {lifes}이고 가까운 역으로는 {stns}이 있습니다. "
        f"같은 시의 다른 일반구와 생활권·역세권을 함께 보면 동선을 잡기 쉽고, "
        f"실제 방문 가능 여부는 예약 시 정확한 위치와 시간을 기준으로 확인합니다."
    )
    return (
        '<section class="related">\n<h2>관련 지역·확인사항 함께 보기</h2>\n'
        f'<p>{intro}</p>\n<ul class="ref-list">\n{chr(10).join(items)}\n</ul>\n</section>\n'
    )


def assemble_district(slug: str, unique_html: str) -> str:
    return unique_html + _district_related(slug) + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA


def _life_related(slug: str) -> str:
    lf = E.LIFE[slug]
    city = lf["city"]
    cname = data.city_display(city)
    items = [_li(data.city_url(city), f"{cname} 시 전체 지역 안내 보기")]
    for g in E.city_districts(city):
        items.append(_li(E.district_url(g), f"{cname} {E.DISTRICTS[g]['name']} 안내 보기"))
    for st in E.city_stations(city):
        items.append(_li(E.station_url(st), f"{E.STATIONS[st]['name']} 역세권 안내 보기"))
    items.append(_li("/gyeonggi/life/", "다른 생활권 안내 보기"))
    items.append(_li("/gyeonggi/use/", "이용 장소별 확인사항 보기"))
    items.append(_li("/gyeonggi/check/", "예약 전 확인사항 모아보기"))
    reg = data.REGIONS[data.CITIES[city]["region"]]["name"]
    stns = "·".join(E.STATIONS[x]["name"] for x in E.city_stations(city)) \
        or "·".join(data.CITIES[city]["stations"]) or "차량 이동 중심"
    intro = (
        f"{lf['name']} 생활권은 {reg} {cname}을 중심으로 한 {lf['kind']}형 생활권입니다. "
        f"{cname}의 가까운 역으로는 {stns}이 있고, 인접 생활권·행정구와 이동 동선이 이어집니다. "
        f"생활권은 방문 동선과 확인사항이 비슷한 지역을 묶은 단위이며, 자택·호텔·오피스텔·업무지구 등 "
        f"이용 장소별 확인사항과 함께 보시면 준비가 수월합니다. 실제 방문 가능 여부는 예약 시 위치와 시간 기준으로 확인합니다."
    )
    return (
        '<section class="related">\n<h2>관련 지역·확인사항 함께 보기</h2>\n'
        f'<p>{intro}</p>\n'
        f'<ul class="ref-list">\n{chr(10).join(items)}\n</ul>\n</section>\n'
    )


def assemble_life(slug: str, unique_html: str) -> str:
    return unique_html + _life_related(slug) + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA


def _station_related(slug: str) -> str:
    st = E.STATIONS[slug]
    city = st["city"]
    cname = data.city_display(city)
    items = [_li(data.city_url(city), f"{cname} 시 전체 지역 안내 보기")]
    for lf in E.city_life(city):
        items.append(_li(E.life_url(lf), f"{E.LIFE[lf]['name']} 생활권 안내 보기"))
    for g in E.city_districts(city):
        items.append(_li(E.district_url(g), f"{cname} {E.DISTRICTS[g]['name']} 안내 보기"))
    items.append(_li("/gyeonggi/station/", "다른 역세권 안내 보기"))
    items.append(_li("/gyeonggi/use/", "이용 장소별 확인사항 보기"))
    items.append(_li("/gyeonggi/check/", "예약 전 확인사항 모아보기"))
    reg = data.REGIONS[data.CITIES[city]["region"]]["name"]
    lifes = "·".join(E.LIFE[x]["name"] for x in E.city_life(city)) or f"{cname} 주요 생활권"
    others = "·".join(E.STATIONS[x]["name"] for x in E.city_stations(city) if x != slug)
    intro = (
        f"{st['name']}은(는) {reg} {cname}의 역세권입니다. {cname}의 대표 생활권은 {lifes}이며"
        + (f", 같은 {cname}의 다른 역으로는 {others}이 있습니다" if others else "")
        + ". 출구별로 페이지를 나누지 않고 한 역을 하나의 안내로 다루며, 환승역이라도 노선별로 구역을 쪼개지 않습니다. "
        f"{cname}은(는) {data.CITIES[city]['focus']} 이런 특성을 고려해 방문 동선을 잡으며, "
        f"자택·호텔·오피스텔 등 머무시는 장소에 따라 출입 방식이 다르므로 예약 시 건물 형태를 함께 알려주시면 좋습니다. "
        f"방문 위치는 역 자체가 아니라 실제 도착지 주소와 예약 시간을 기준으로 확인합니다."
    )
    return (
        '<section class="related">\n<h2>관련 지역·확인사항 함께 보기</h2>\n'
        f'<p>{intro}</p>\n'
        f'<ul class="ref-list">\n{chr(10).join(items)}\n</ul>\n</section>\n'
    )


def assemble_station(slug: str, unique_html: str) -> str:
    return unique_html + _station_related(slug) + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA
