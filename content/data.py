# 경기도 출장마사지 사이트 — 지역 데이터 모델
# 지시서(섹션 9·10·12) 기준. 행정동/생활권/역세권 상세 페이지는 단계적 확장 대상이며
# 본 데이터는 1차(메인·권역·31시군) 생성에 필요한 필드만 정규화해 담는다.

# ── 권역 (8) ───────────────────────────────────────────────
# slug, name(메뉴/표기), 부제, 포함 시군 slug 목록, 권역 성격
REGIONS = {
    "south": {
        "name": "경기남부",
        "subtitle": "수원·성남·용인 생활권",
        "cities": ["suwon", "seongnam", "yongin", "hwaseong", "osan",
                   "pyeongtaek", "anyang", "gunpo", "uiwang", "gwacheon"],
        "focus": "수원·성남·용인을 축으로 한 경기 최대 인구 밀집권. 일반구와 신도시 생활권이 촘촘해 같은 시 안에서도 이동 기준이 갈린다.",
    },
    "north": {
        "name": "경기북부",
        "subtitle": "고양·파주·의정부 생활권",
        "cities": ["goyang", "paju", "uijeongbu", "yangju", "dongducheon",
                   "pocheon", "yeoncheon"],
        "focus": "고양 일산권과 파주 운정·의정부 역세권이 거점. 북부로 갈수록 외곽 이동과 사전 예약 비중이 커진다.",
    },
    "west": {
        "name": "경기서부",
        "subtitle": "부천·안산·시흥 생활권",
        "cities": ["bucheon", "ansan", "siheung", "gimpo", "gwangmyeong"],
        "focus": "서울·인천과 맞닿은 도시들이 모인 권역. 부천 역세권, 안산 산업·주거 혼합, 김포 한강신도시 등 성격이 다양하다.",
    },
    "east": {
        "name": "경기동부",
        "subtitle": "하남·남양주·구리 생활권",
        "cities": ["hanam", "namyangju", "guri", "gwangju-si", "yangpyeong", "gapyeong"],
        "focus": "서울 동측과 이어지는 미사·다산 신도시권과 동부 외곽 이동권이 함께 묶인 권역.",
    },
    "outer": {
        "name": "경기외곽",
        "subtitle": "이천·안성·여주 이동권",
        "cities": ["icheon", "anseong", "yeoju", "yangpyeong", "gapyeong",
                   "yeoncheon", "pocheon"],
        "focus": "차량 이동과 사전 예약이 기본이 되는 외곽 권역. 추가 이동비와 방문 가능 여부 확인이 가장 중요하다.",
    },
    "newtown": {
        "name": "신도시 생활권",
        "subtitle": "광교·판교·동탄·일산·운정·미사",
        "cities": ["suwon", "seongnam", "hwaseong", "goyang", "paju",
                   "hanam", "namyangju", "gimpo"],
        "focus": "광교·판교·동탄·일산·운정·미사·다산·별내·김포한강 등 경기 주요 신도시 생활권을 한 번에 안내한다.",
    },
    "business-industrial": {
        "name": "산업·업무지구",
        "subtitle": "판교·광교·동탄·안산·평택",
        "cities": ["seongnam", "suwon", "hwaseong", "ansan", "siheung",
                   "pyeongtaek", "gimpo"],
        "focus": "판교 테크노밸리, 광교·동탄 업무지구, 안산·시흥 산업단지, 평택 고덕 등 업무·산업 거점 생활권.",
    },
    "seoul": {
        "name": "서울 인접권",
        "subtitle": "광명·하남·구리·과천·부천",
        "cities": ["gwangmyeong", "hanam", "guri", "gwacheon", "bucheon",
                   "gimpo", "anyang", "uiwang"],
        "focus": "서울 경계와 맞닿아 이동이 빠른 도시들. 서울 생활권과 사실상 하나로 묶이는 구간이 많다.",
    },
}

# 권역 페이지 출력 순서
REGION_ORDER = ["south", "north", "west", "east", "outer",
                "newtown", "business-industrial", "seoul"]


# ── 31개 시군 ──────────────────────────────────────────────
# region = 1차(지리) 상위 권역 slug · districts = 일반구(없으면 [])
# life = 대표 생활권 · stations = 대표 역(없으면 []) · focus = 콘텐츠 방향
CITIES = {
    "suwon": dict(name="수원", region="south",
        districts=["장안구", "권선구", "팔달구", "영통구"],
        life=["수원역·인계동", "광교·영통"],
        stations=["수원역", "광교중앙역", "영통역"],
        focus="일반구 내부링크 강화. 팔달구 인계동, 영통구 광교·영통 생활권 연결이 핵심."),
    "seongnam": dict(name="성남", region="south",
        districts=["수정구", "중원구", "분당구"],
        life=["분당·판교", "야탑·서현", "수정·위례"],
        stations=["판교역", "서현역", "야탑역", "정자역"],
        focus="분당구·판교 업무지구, 수정구 위례, 중원구 모란 생활권을 분리해 설명."),
    "yongin": dict(name="용인", region="south",
        districts=["처인구", "기흥구", "수지구"],
        life=["죽전·수지", "기흥·동백", "처인·역북"],
        stations=["죽전역", "기흥역", "보정역"],
        focus="수지·기흥·처인 권역의 이동 기준을 서로 다르게 작성."),
    "hwaseong": dict(name="화성", region="south",
        districts=[],
        life=["동탄신도시", "병점·봉담", "향남"],
        stations=["동탄역", "병점역"],
        focus="동탄신도시 중심, 봉담·향남 등 외곽 이동 기준 병행."),
    "osan": dict(name="오산", region="south",
        districts=[],
        life=["오산역", "세교", "원동"],
        stations=["오산역"],
        focus="세교 신도시와 남부권 차량 이동 기준."),
    "pyeongtaek": dict(name="평택", region="south",
        districts=[],
        life=["평택역·소사벌", "고덕", "송탄"],
        stations=["평택역", "서정리역"],
        focus="고덕 국제신도시·산업단지와 외곽 이동이 섞인 혼합형."),
    "anyang": dict(name="안양", region="south",
        districts=["만안구", "동안구"],
        life=["안양·범계·평촌"],
        stations=["안양역", "범계역", "평촌역"],
        focus="만안구·동안구 내부링크 강화, 범계·평촌 생활권 분리."),
    "gunpo": dict(name="군포", region="south",
        districts=[],
        life=["산본", "금정", "당동"],
        stations=["산본역", "금정역"],
        focus="산본 생활권 중심, 환승역은 노선별로 나누지 않는 원칙 적용."),
    "uiwang": dict(name="의왕", region="south",
        districts=[],
        life=["내손", "오전", "의왕역"],
        stations=["의왕역"],
        focus="안양·군포와 이어지는 인접권, 차량 이동 기준."),
    "gwacheon": dict(name="과천", region="south",
        districts=[],
        life=["정부청사", "별양", "중앙"],
        stations=["정부과천청사역"],
        focus="서울 강남권 인접, 정부청사 행정업무지구 중심."),
    "goyang": dict(name="고양", region="north",
        districts=["덕양구", "일산동구", "일산서구"],
        life=["일산·킨텍스", "화정·삼송", "백석·마두"],
        stations=["대화역", "정발산역", "화정역", "삼송역"],
        focus="일산권(일산동·서구)과 덕양권을 분리해 설명."),
    "paju": dict(name="파주", region="north",
        districts=[],
        life=["운정", "금촌", "문산"],
        stations=["운정역", "금촌역", "문산역"],
        focus="운정신도시와 북부 외곽(문산)을 분리."),
    "uijeongbu": dict(name="의정부", region="north",
        districts=[],
        life=["의정부역·민락", "신곡", "호원"],
        stations=["의정부역", "회룡역"],
        focus="북부 거점, 의정부역·민락 역세권 중심."),
    "yangju": dict(name="양주", region="north",
        districts=[],
        life=["옥정", "덕정", "고읍"],
        stations=["덕정역"],
        focus="옥정신도시 중심, 북부 외곽 이동 기준 병행."),
    "dongducheon": dict(name="동두천", region="north",
        districts=[],
        life=["지행", "동두천중앙", "생연"],
        stations=["지행역", "동두천중앙역"],
        focus="북부 역세권과 외곽 이동이 섞인 구간."),
    "pocheon": dict(name="포천", region="north",
        districts=[],
        life=["포천", "소흘", "송우"],
        stations=[],
        focus="지하철이 닿지 않는 북부 외곽. 사전 예약·차량 이동 중심."),
    "yeoncheon": dict(name="연천", region="north",
        districts=[],
        life=["연천", "전곡"],
        stations=["전곡역"],
        focus="북부 최외곽. 방문 가능 여부 사전 확인이 우선."),
    "bucheon": dict(name="부천", region="west",
        districts=["원미구", "소사구", "오정구"],
        life=["부천역·상동", "중동", "소사"],
        stations=["부천역", "상동역", "신중동역"],
        focus="원미·소사·오정 일반구 내부링크와 역세권 연결 강화."),
    "ansan": dict(name="안산", region="west",
        districts=["상록구", "단원구"],
        life=["안산중앙·초지", "고잔", "상록수"],
        stations=["중앙역", "초지역", "상록수역"],
        focus="상록구·단원구 분리, 산업권과 주거지 성격을 함께 반영."),
    "siheung": dict(name="시흥", region="west",
        districts=[],
        life=["배곧", "정왕", "은계", "시흥능곡"],
        stations=["시흥능곡역", "정왕역"],
        focus="배곧·정왕 대표동 묶음, 산업·주거 혼합."),
    "gimpo": dict(name="김포", region="west",
        districts=[],
        life=["구래", "장기", "풍무", "김포공항 인접권"],
        stations=["구래역", "장기역", "풍무역"],
        focus="김포한강신도시 중심, 서울·인천 인접권."),
    "gwangmyeong": dict(name="광명", region="west",
        districts=[],
        life=["광명·철산", "소하", "KTX광명"],
        stations=["광명역", "철산역"],
        focus="서울 인접권, KTX 광명역 역세권."),
    "hanam": dict(name="하남", region="east",
        districts=[],
        life=["미사", "감일", "하남시청"],
        stations=["하남검단산역", "미사역"],
        focus="미사 신도시와 서울 인접권."),
    "namyangju": dict(name="남양주", region="east",
        districts=[],
        life=["다산", "별내", "평내호평", "진접"],
        stations=["별내역", "평내호평역"],
        focus="다산·별내 신도시권과 동부 외곽 이동권."),
    "guri": dict(name="구리", region="east",
        districts=[],
        life=["구리·갈매", "인창", "수택"],
        stations=["구리역", "갈매역"],
        focus="동부 서울 인접권."),
    "gwangju-si": dict(name="광주", region="east",
        districts=[],
        life=["경기광주", "태전", "오포"],
        stations=["경기광주역"],
        focus="동부권, 차량 이동 기준 중심.", display="경기광주"),
    "yangpyeong": dict(name="양평", region="east",
        districts=[],
        life=["양평", "용문", "양서"],
        stations=["양평역", "용문역"],
        focus="외곽·관광지, 차량 이동 기준."),
    "gapyeong": dict(name="가평", region="east",
        districts=[],
        life=["가평", "청평", "설악"],
        stations=["가평역", "청평역"],
        focus="관광·외곽 이동, 사전 예약 중심."),
    "icheon": dict(name="이천", region="outer",
        districts=[],
        life=["이천", "부발", "마장"],
        stations=["이천역", "부발역"],
        focus="산업권과 외곽 이동 기준."),
    "anseong": dict(name="안성", region="outer",
        districts=[],
        life=["안성", "공도", "대덕"],
        stations=[],
        focus="지하철 없는 외곽. 차량 이동·사전 예약 기준."),
    "yeoju": dict(name="여주", region="outer",
        districts=[],
        life=["여주", "오학", "가남"],
        stations=["여주역"],
        focus="동남부 외곽, 차량 이동 기준."),
}

CITY_ORDER = [
    "suwon", "seongnam", "yongin", "goyang", "hwaseong", "bucheon", "ansan",
    "pyeongtaek", "anyang", "siheung", "gimpo", "namyangju", "paju", "uijeongbu",
    "hanam", "gwangmyeong", "guri", "gunpo", "osan", "uiwang", "gwacheon",
    "gwangju-si", "icheon", "anseong", "yeoju", "yangpyeong", "yangju",
    "pocheon", "dongducheon", "gapyeong", "yeoncheon",
]

assert len(CITIES) == 31, len(CITIES)
assert set(CITIES) == set(CITY_ORDER), set(CITIES) ^ set(CITY_ORDER)


def city_display(slug: str) -> str:
    c = CITIES[slug]
    return c.get("display", c["name"])


def city_url(slug: str) -> str:
    return f"/gyeonggi/{slug}/"


def region_url(slug: str) -> str:
    return f"/gyeonggi/area/{slug}/"


def neighbors(slug: str, k: int = 4):
    """같은 1차 권역의 다른 시군 slug (최대 k개)."""
    reg = CITIES[slug]["region"]
    same = [s for s in CITY_ORDER if CITIES[s]["region"] == reg and s != slug]
    return same[:k]
