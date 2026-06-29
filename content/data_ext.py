# 경기도 데이터 — 1차-B 확장: 일반구(20) · 생활권(22) · 역세권(34)
# data.py(시군·권역)와 분리. 순환 임포트를 피하기 위해 외부 의존을 두지 않는다.

# ── 일반구 (20) ─────────────────────────────────────────────
# slug(시-구) → city(상위 시군 slug), name, dongs(대표 행정동, 번호동 통합)
DISTRICTS = {
    "jangan-gu": dict(city="suwon", name="장안구", dongs=["정자동", "영화동", "송죽동", "조원동", "연무동"]),
    "gwonseon-gu": dict(city="suwon", name="권선구", dongs=["권선동", "세류동", "호매실동", "금곡동", "곡반정동"]),
    "paldal-gu": dict(city="suwon", name="팔달구", dongs=["인계동", "매산동", "우만동", "화서동", "행궁동"]),
    "yeongtong-gu": dict(city="suwon", name="영통구", dongs=["영통동", "매탄동", "광교동", "망포동", "원천동"]),
    "sujeong-gu": dict(city="seongnam", name="수정구", dongs=["신흥동", "태평동", "수진동", "위례동", "복정동"]),
    "jungwon-gu": dict(city="seongnam", name="중원구", dongs=["성남동", "중앙동", "금광동", "상대원동", "하대원동"]),
    "bundang-gu": dict(city="seongnam", name="분당구", dongs=["분당동", "정자동", "수내동", "서현동", "야탑동", "판교동", "백현동", "이매동", "구미동"]),
    "cheoin-gu": dict(city="yongin", name="처인구", dongs=["김량장동", "역북동", "포곡읍", "모현읍", "남사읍"]),
    "giheung-gu": dict(city="yongin", name="기흥구", dongs=["구갈동", "신갈동", "보정동", "동백동", "상갈동", "영덕동"]),
    "suji-gu": dict(city="yongin", name="수지구", dongs=["풍덕천동", "죽전동", "상현동", "동천동", "성복동", "신봉동"]),
    "deogyang-gu": dict(city="goyang", name="덕양구", dongs=["화정동", "행신동", "삼송동", "원흥동", "토당동"]),
    "ilsandong-gu": dict(city="goyang", name="일산동구", dongs=["마두동", "장항동", "백석동", "정발산동", "풍산동"]),
    "ilsanseo-gu": dict(city="goyang", name="일산서구", dongs=["일산동", "탄현동", "주엽동", "대화동", "덕이동"]),
    "wonmi-gu": dict(city="bucheon", name="원미구", dongs=["중동", "상동", "심곡동", "춘의동", "역곡동"]),
    "sosa-gu": dict(city="bucheon", name="소사구", dongs=["소사본동", "괴안동", "송내동", "범박동"]),
    "ojeong-gu": dict(city="bucheon", name="오정구", dongs=["원종동", "고강동", "오정동", "삼정동"]),
    "sangnok-gu": dict(city="ansan", name="상록구", dongs=["본오동", "사동", "월피동", "성포동", "이동"]),
    "danwon-gu": dict(city="ansan", name="단원구", dongs=["고잔동", "초지동", "선부동", "원곡동", "와동"]),
    "manan-gu": dict(city="anyang", name="만안구", dongs=["안양동", "석수동", "박달동"]),
    "dongan-gu": dict(city="anyang", name="동안구", dongs=["비산동", "관양동", "평촌동", "호계동", "범계동"]),
}
DISTRICT_ORDER = [
    "jangan-gu", "gwonseon-gu", "paldal-gu", "yeongtong-gu",
    "sujeong-gu", "jungwon-gu", "bundang-gu",
    "cheoin-gu", "giheung-gu", "suji-gu",
    "deogyang-gu", "ilsandong-gu", "ilsanseo-gu",
    "wonmi-gu", "sosa-gu", "ojeong-gu",
    "sangnok-gu", "danwon-gu", "manan-gu", "dongan-gu",
]

# ── 생활권 (22) ─────────────────────────────────────────────
LIFE = {
    "gwanggyo-yeongtong": dict(name="광교·영통", city="suwon", kind="신도시"),
    "bundang-pangyo": dict(name="분당·판교", city="seongnam", kind="신도시"),
    "dongtan-newtown": dict(name="동탄신도시", city="hwaseong", kind="신도시"),
    "ilsan-kintex": dict(name="일산·킨텍스", city="goyang", kind="신도시"),
    "paju-unjeong": dict(name="운정신도시", city="paju", kind="신도시"),
    "hanam-misa": dict(name="하남·미사", city="hanam", kind="신도시"),
    "gimpo-gurae": dict(name="김포·구래", city="gimpo", kind="신도시"),
    "namyangju-dasan": dict(name="남양주·다산", city="namyangju", kind="신도시"),
    "suwon-station-ingye": dict(name="수원역·인계동", city="suwon", kind="역세권"),
    "yatap-seohyeon": dict(name="야탑·서현", city="seongnam", kind="역세권"),
    "bucheon-station-sangdong": dict(name="부천역·상동", city="bucheon", kind="역세권"),
    "anyang-beomgye-pyeongchon": dict(name="안양·범계·평촌", city="anyang", kind="역세권"),
    "ansan-jungang-choji": dict(name="안산중앙·초지", city="ansan", kind="역세권"),
    "uijeongbu-station-minrak": dict(name="의정부역·민락", city="uijeongbu", kind="역세권"),
    "gwangmyeong-cheolsan": dict(name="광명·철산", city="gwangmyeong", kind="역세권"),
    "gunpo-sanbon": dict(name="군포·산본", city="gunpo", kind="역세권"),
    "yangpyeong-yongmun": dict(name="양평·용문", city="yangpyeong", kind="외곽"),
    "gapyeong-cheongpyeong": dict(name="가평·청평", city="gapyeong", kind="외곽"),
    "pocheon-songu": dict(name="포천·송우", city="pocheon", kind="외곽"),
    "yeoncheon-jeongok": dict(name="연천·전곡", city="yeoncheon", kind="외곽"),
    "anseong-gongdo": dict(name="안성·공도", city="anseong", kind="외곽"),
    "yeoju-ohak": dict(name="여주·오학", city="yeoju", kind="외곽"),
}
LIFE_ORDER = list(LIFE.keys())

# ── 역세권 (34) ─────────────────────────────────────────────
STATIONS = {
    "suwon-station": dict(name="수원역", city="suwon"),
    "gwanggyo-jungang-station": dict(name="광교중앙역", city="suwon"),
    "yeongtong-station": dict(name="영통역", city="suwon"),
    "pangyo-station": dict(name="판교역", city="seongnam"),
    "jeongja-station": dict(name="정자역", city="seongnam"),
    "seohyeon-station": dict(name="서현역", city="seongnam"),
    "yatap-station": dict(name="야탑역", city="seongnam"),
    "jukjeon-station": dict(name="죽전역", city="yongin"),
    "giheung-station": dict(name="기흥역", city="yongin"),
    "dongtan-station": dict(name="동탄역", city="hwaseong"),
    "pyeongtaek-station": dict(name="평택역", city="pyeongtaek"),
    "bucheon-station": dict(name="부천역", city="bucheon"),
    "sangdong-station": dict(name="상동역", city="bucheon"),
    "beomgye-station": dict(name="범계역", city="anyang"),
    "pyeongchon-station": dict(name="평촌역", city="anyang"),
    "jungang-station": dict(name="중앙역", city="ansan"),
    "choji-station": dict(name="초지역", city="ansan"),
    "jeongwang-station": dict(name="정왕역", city="siheung"),
    "gurae-station": dict(name="구래역", city="gimpo"),
    "daehwa-station": dict(name="대화역", city="goyang"),
    "jeongbalsan-station": dict(name="정발산역", city="goyang"),
    "hwajeong-station": dict(name="화정역", city="goyang"),
    "samsong-station": dict(name="삼송역", city="goyang"),
    "uijeongbu-station": dict(name="의정부역", city="uijeongbu"),
    "misa-station": dict(name="미사역", city="hanam"),
    "gwangmyeong-station": dict(name="광명역", city="gwangmyeong"),
    "cheolsan-station": dict(name="철산역", city="gwangmyeong"),
    "guri-station": dict(name="구리역", city="guri"),
    "sanbon-station": dict(name="산본역", city="gunpo"),
    "osan-station": dict(name="오산역", city="osan"),
    "gwacheon-government-complex-station": dict(name="정부과천청사역", city="gwacheon"),
    "gyeonggi-gwangju-station": dict(name="경기광주역", city="gwangju-si"),
    "icheon-station": dict(name="이천역", city="icheon"),
    "yangpyeong-station": dict(name="양평역", city="yangpyeong"),
}
STATION_ORDER = list(STATIONS.keys())

assert len(DISTRICTS) == 20 and len(DISTRICT_ORDER) == 20
assert len(LIFE) == 22 and len(STATIONS) == 34


def district_url(slug):
    return f"/gyeonggi/{DISTRICTS[slug]['city']}/{slug}/"


def life_url(slug):
    return f"/gyeonggi/life/{slug}/"


def station_url(slug):
    return f"/gyeonggi/station/{slug}/"


def city_districts(city_slug):
    return [d for d in DISTRICT_ORDER if DISTRICTS[d]["city"] == city_slug]


def city_life(city_slug):
    return [s for s in LIFE_ORDER if LIFE[s]["city"] == city_slug]


def city_stations(city_slug):
    return [s for s in STATION_ORDER if STATIONS[s]["city"] == city_slug]
