# 경기도 출장마사지 — 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://www.gyeonggi-massage.example.com"

BRAND = "간다GO 경기"            # 헤더 표기 브랜드
BRAND_FULL = "간다GO 경기 출장마사지 안내"
TRADE_NAME = "간다GO"            # 상호 (운영 주체)
BRAND_MARK = "G"                 # 헤더 로고 마크
REGION_NAME = "경기도"           # 서비스 광역 지역명
AREA_SERVED = "경기도"           # 스키마 areaServed
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 텔레그램 문의 채널 — 실제 운영 채널로 교체하세요.
TELEGRAM_WEB = "https://t.me/googleseolab"      # 웹사이트 제작문의
TELEGRAM_PARTNER = "https://t.me/googleseolab"  # 제휴문의

# 상단 메뉴 — 메뉴명에는 "출장마사지"를 반복하지 않고 지역·구분명만 노출한다(지시서 §4).
NAV = [
    ("경기 홈", "/gyeonggi/", []),
    ("권역 안내", "/gyeonggi/area/", [
        ("경기남부", "/gyeonggi/area/south/"),
        ("경기북부", "/gyeonggi/area/north/"),
        ("경기서부", "/gyeonggi/area/west/"),
        ("경기동부", "/gyeonggi/area/east/"),
        ("경기외곽", "/gyeonggi/area/outer/"),
        ("신도시 생활권", "/gyeonggi/area/newtown/"),
        ("산업·업무지구", "/gyeonggi/area/business-industrial/"),
        ("서울 인접권", "/gyeonggi/area/seoul/"),
    ]),
    ("시군 안내", "/gyeonggi/cities/", [
        ("시군 전체", "/gyeonggi/cities/"),
        ("수원", "/gyeonggi/suwon/"),
        ("성남", "/gyeonggi/seongnam/"),
        ("용인", "/gyeonggi/yongin/"),
        ("고양", "/gyeonggi/goyang/"),
        ("화성", "/gyeonggi/hwaseong/"),
        ("부천", "/gyeonggi/bucheon/"),
        ("안산", "/gyeonggi/ansan/"),
        ("평택", "/gyeonggi/pyeongtaek/"),
        ("안양", "/gyeonggi/anyang/"),
        ("남양주", "/gyeonggi/namyangju/"),
        ("의정부", "/gyeonggi/uijeongbu/"),
        ("김포·시흥", "/gyeonggi/gimpo/"),
    ]),
    ("행정구 안내", "/gyeonggi/districts/", [
        ("일반구 전체", "/gyeonggi/districts/"),
        ("수원 4개 구", "/gyeonggi/suwon/"),
        ("성남 3개 구", "/gyeonggi/seongnam/"),
        ("용인 3개 구", "/gyeonggi/yongin/"),
        ("고양 3개 구", "/gyeonggi/goyang/"),
        ("부천 3개 구", "/gyeonggi/bucheon/"),
        ("안산 2개 구", "/gyeonggi/ansan/"),
        ("안양 2개 구", "/gyeonggi/anyang/"),
    ]),
    ("생활권", "/gyeonggi/life/", []),
    ("지하철역", "/gyeonggi/station/", []),
    ("이용 장소", "/gyeonggi/use/", [
        ("이용 장소 전체", "/gyeonggi/use/"),
        ("자택 이용", "/gyeonggi/use/home/"),
        ("호텔·숙소 이용", "/gyeonggi/use/hotel/"),
        ("오피스텔 이용", "/gyeonggi/use/officetel/"),
        ("업무지구 이용", "/gyeonggi/use/business-district/"),
        ("야간 예약", "/gyeonggi/use/night/"),
        ("신도시 이용", "/gyeonggi/use/newtown/"),
        ("외곽 지역 이용", "/gyeonggi/use/outer-area/"),
    ]),
    ("예약 전 확인", "/gyeonggi/check/", [
        ("예약 전 확인 전체", "/gyeonggi/check/"),
        ("방문 주소 확인", "/gyeonggi/check/address/"),
        ("건물 출입 방식", "/gyeonggi/check/building-access/"),
        ("추가 이동비 기준", "/gyeonggi/check/travel-fee/"),
        ("예약 가능 시간", "/gyeonggi/check/time/"),
        ("개인정보 처리 기준", "/gyeonggi/check/privacy/"),
        ("불법·선정적 서비스 불가", "/gyeonggi/check/service-policy/"),
    ]),
    ("운영 기준", "/gyeonggi/policy/service-standard/", [
        ("콘텐츠·운영 기준", "/gyeonggi/policy/service-standard/"),
        ("작성자·검수자 안내", "/gyeonggi/policy/authors/"),
        ("개인정보 처리방침", "/gyeonggi/policy/privacy/"),
    ]),
    ("문의하기", "/gyeonggi/contact/", []),
]

# 공신력 있는 외부 참고 링크 블록 — 메인·권역·시군 페이지 하단에 공통 삽입한다.
# 설명형(롱테일) 앵커텍스트를 사용하고, 키워드 반복·과장 표현은 넣지 않는다(지시서 §16).
REFERENCES = """
<section class="references">
<h2>함께 참고하면 좋은 공신력 있는 정보</h2>
<p>방문형 관리를 안전하게 이용하시려면 신뢰할 수 있는 공공기관의 지역·건강 정보를 함께 확인하시는 것이 좋습니다. 아래는 경기도 생활정보와 근골격계 건강관리에 도움이 되는 공식 자료입니다.</p>
<ul class="ref-list">
<li><a href="https://www.gg.go.kr/" target="_blank" rel="noopener noreferrer">경기도청 누리집에서 경기도 행정구역·생활 정보 확인하기</a></li>
<li><a href="https://health.kdca.go.kr/" target="_blank" rel="noopener noreferrer">질병관리청 국가건강정보포털에서 근육·관절 건강관리 정보 살펴보기</a></li>
<li><a href="https://www.mohw.go.kr/" target="_blank" rel="noopener noreferrer">보건복지부에서 건강·의료 생활정보 공식 안내 보기</a></li>
<li><a href="https://www.data.go.kr/" target="_blank" rel="noopener noreferrer">공공데이터포털에서 경기도 행정동·교통 공공데이터 확인하기</a></li>
</ul>
</section>
"""

# Who/How/Why + 작성자·검수자 — 모든 주요 페이지 하단 공통(E-E-A-T, 지시서 §3)
WHO_HOW_WHY = """
<section class="whw">
<h2>Who · How · Why</h2>
<p class="whw-row"><strong>Who</strong> · 이 페이지는 경기도 지역 방문형 관리 안내 콘텐츠 담당자가 작성하고 운영 책임자가 검수합니다.</p>
<p class="whw-row"><strong>How</strong> · 경기도 행정구역, 시군·일반구·행정동 구조, 주요 생활권, 가까운 지하철역, 이용 장소별 예약 전 확인사항을 기준으로 구성했습니다.</p>
<p class="whw-row"><strong>Why</strong> · 경기도에서 방문형 서비스를 찾는 분이 자신의 지역과 이용 장소를 안전하게 확인할 수 있도록 돕기 위해 작성했습니다.</p>
<p class="whw-byline">작성: 경기 지역 안내 콘텐츠 담당자 · 검수: 운영 책임자 · 기준일: 2026년 · <a href="/gyeonggi/policy/authors/">작성자·검수자 안내</a></p>
</section>
"""
