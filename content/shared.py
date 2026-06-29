# 공통 콘텐츠 블록 — 모든 시군·권역 페이지에서 재사용한다.
# 고유 본문(워크플로 생성)은 measure 대상이고, 아래 블록은 class 로 제외된다.
from .site import PHONE, PHONE_DISPLAY, REFERENCES, WHO_HOW_WHY, REGION_NAME
from . import data

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
    items = [_li(data.region_url(reg), f"{reg_name} 권역에서 인접 시군 함께 보기")]
    for n in data.neighbors(slug, 4):
        items.append(_li(data.city_url(n), f"{data.city_display(n)} 지역 안내 보기"))
    if c["districts"]:
        gu = "·".join(c["districts"])
        items.append(_li("/gyeonggi/districts/", f"{name} 일반구({gu}) 행정구 안내"))
    items.append(_li("/gyeonggi/life/", f"{name} 주변 생활권 안내 보기"))
    items.append(_li("/gyeonggi/station/", f"{name} 인근 역세권 안내 보기"))
    items.append(_li("/gyeonggi/use/", "이용 장소별(자택·호텔·오피스텔) 확인사항"))
    items.append(_li("/gyeonggi/check/", "예약 전 확인사항 모아보기"))
    return (
        '<section class="related">\n<h2>관련 지역·확인사항 함께 보기</h2>\n'
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
    city_links = "\n".join(
        _li(data.city_url(s), f"{data.city_display(s)} 지역 안내 보기")
        for s in r["cities"] if s in data.CITIES
    )
    members = (
        '<section class="related">\n<h2>이 권역의 시군 안내</h2>\n'
        f'<ul class="ref-list">\n{city_links}\n</ul>\n'
        '<p>시군을 고르면 일반구·대표 행정동·생활권·가까운 역세권과 이용 장소별 예약 전 확인사항을 이어서 볼 수 있습니다.</p>\n</section>\n'
    )
    return unique_html + members + CHECKLIST + REFERENCES + WHO_HOW_WHY + CTA
