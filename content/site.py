# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://www.nowon-black.example.com"

BRAND = "노원 블랙 마사지"
TRADE_NAME = "간다GO"          # 상호 (운영 주체)
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 텔레그램 문의 채널 — 실제 운영 채널로 교체하세요.
TELEGRAM_WEB = "https://t.me/googleseolab"      # 웹사이트 제작문의
TELEGRAM_PARTNER = "https://t.me/googleseolab"  # 제휴문의

# 공신력 있는 외부 참고 링크 블록 — 메인·지역·역세권 페이지 하단에 공통 삽입한다.
# 설명형(롱테일) 앵커텍스트를 사용하고, 키워드 반복·과장 표현은 넣지 않는다.
REFERENCES = """
<section class="references">
<h2>함께 참고하면 좋은 공신력 있는 정보</h2>
<p>방문 관리를 안전하게 이용하시려면 신뢰할 수 있는 공공기관의 지역·건강 정보를 함께 확인하시는 것이 좋습니다. 아래는 노원구 생활정보와 근골격계 건강관리에 도움이 되는 공식 자료입니다.</p>
<ul class="ref-list">
<li><a href="https://www.nowon.kr/" target="_blank" rel="noopener noreferrer">노원구청 공식 홈페이지에서 노원구 생활·복지 정보 확인하기</a></li>
<li><a href="https://health.kdca.go.kr/" target="_blank" rel="noopener noreferrer">질병관리청 국가건강정보포털에서 근육·관절 건강관리 정보 살펴보기</a></li>
<li><a href="https://www.mohw.go.kr/" target="_blank" rel="noopener noreferrer">보건복지부에서 건강·의료 생활정보 공식 안내 보기</a></li>
<li><a href="https://www.seoul.go.kr/" target="_blank" rel="noopener noreferrer">서울특별시 누리집에서 노원구 포함 생활·교통 정보 확인하기</a></li>
</ul>
</section>
"""

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("노원 출장마사지", "/massage/", [
        ("출장마사지 안내", "/massage/#service"),
        ("홈타이 안내", "/massage/#hometai"),
        ("전지역 방문 안내", "/massage/#coverage"),
        ("지하철역 인근 안내", "/massage/#stations"),
        ("예약 가능 시간", "/massage/#hours"),
        ("코스 선택 안내", "/massage/#course"),
        ("이용 전 확인사항", "/massage/#check"),
        ("위생·안전 안내", "/massage/#safety"),
        ("자주 묻는 질문", "/massage/#faq"),
    ]),
    ("지역별 안내", "/nowon-gu/", [
        ("노원구 전체", "/nowon-gu/"),
        ("월계동", "/nowon-gu/wolgye-dong/"),
        ("공릉동", "/nowon-gu/gongneung-dong/"),
        ("하계동", "/nowon-gu/hagye-dong/"),
        ("중계동", "/nowon-gu/junggye-dong/"),
        ("상계동", "/nowon-gu/sanggye-dong/"),
    ]),
    ("지하철역별 안내", "/nowon-gu/stations/", [
        ("역 전체", "/nowon-gu/stations/"),
        ("노원역", "/nowon-gu/stations/nowon-station/"),
        ("상계역", "/nowon-gu/stations/sanggye-station/"),
        ("불암산역", "/nowon-gu/stations/buramsan-station/"),
        ("수락산역", "/nowon-gu/stations/suraksan-station/"),
        ("마들역", "/nowon-gu/stations/madeul-station/"),
        ("중계역", "/nowon-gu/stations/junggye-station/"),
        ("하계역", "/nowon-gu/stations/hagye-station/"),
        ("공릉역", "/nowon-gu/stations/gongneung-station/"),
        ("태릉입구역", "/nowon-gu/stations/taereung-station/"),
        ("석계역", "/nowon-gu/stations/seokgye-station/"),
        ("광운대역", "/nowon-gu/stations/kwangwoon-univ-station/"),
        ("월계역", "/nowon-gu/stations/wolgye-station/"),
        ("화랑대역", "/nowon-gu/stations/hwarangdae-station/"),
    ]),
    ("테마별 안내", "/themes/", [
        ("전체 테마", "/themes/"),
        ("스웨디시", "/themes/swedish/"),
        ("로미로미", "/themes/lomilomi/"),
        ("타이마사지", "/themes/thai/"),
        ("중국마사지", "/themes/chinese/"),
        ("아로마테라피", "/themes/aroma/"),
        ("홈케어", "/themes/homecare/"),
        ("호텔식마사지", "/themes/hotel-style/"),
        ("발마사지", "/themes/foot/"),
        ("스포츠·경락", "/themes/sports/"),
        ("스킨케어", "/themes/skincare/"),
        ("왁싱", "/themes/waxing/"),
        ("커플 관리", "/themes/couple/"),
        ("24시간", "/themes/24hours/"),
        ("수면 가능", "/themes/overnight/"),
    ]),
    ("코스안내", "/courses/", [
        ("전체 코스", "/courses/"),
        ("피로 회복 관리", "/courses/#recovery"),
        ("아로마 관리", "/courses/#aroma"),
        ("스포츠 관리", "/courses/#sports"),
        ("홈타이 코스", "/courses/#hometai"),
        ("커플·가족 방문 관리", "/courses/#couple"),
        ("기업·단체 방문 관리", "/courses/#group"),
        ("가격 안내", "/courses/#price"),
        ("코스 선택 가이드", "/courses/#guide"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("방문 전 준비사항", "/guide/#prepare"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
        ("이용 FAQ", "/guide/#faq"),
    ]),
    ("매거진", "/magazine/", [
        ("전체 글", "/magazine/"),
        ("마사지 비교 가이드", "/magazine/swedish-vs-thai/"),
        ("처음 이용 가이드", "/magazine/first-time-guide/"),
        ("수면과 마사지", "/magazine/sleep-and-massage/"),
        ("운동 후 회복", "/magazine/post-workout-timing/"),
        ("어깨·목 결림 관리", "/magazine/neck-shoulder-care/"),
        ("부모님 선물 가이드", "/magazine/parents-gift/"),
    ]),
    ("후기", "/reviews/", [
        ("전체 후기", "/reviews/"),
        ("지역별 후기", "/reviews/#area"),
        ("역세권 후기", "/reviews/#station"),
        ("후기 작성 안내", "/reviews/#write"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("제휴·기업 문의", "/support/#biz"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
