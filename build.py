#!/usr/bin/env python3
"""간다GO 경기 출장마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 루트(/)는 경기 메인(/gyeonggi/)으로 리다이렉트
"""
import datetime
import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, NAV, PHONE, PHONE_DISPLAY,
                          TRADE_NAME, TELEGRAM_WEB, TELEGRAM_PARTNER,
                          BRAND_MARK, REGION_NAME, AREA_SERVED,
                          RATING_VALUE, RATING_COUNT, RATING_BEST, REVIEWS,
                          NAVER_VERIFY, GOOGLE_VERIFY, INDEXNOW_KEY)

BUILD_DATE = datetime.date.today().isoformat()


def verify_meta() -> str:
    """검색엔진 사이트 소유확인 메타 태그(값이 있으면 출력)."""
    tags = []
    if NAVER_VERIFY:
        tags.append(f'<meta name="naver-site-verification" content="{NAVER_VERIFY}">')
    if GOOGLE_VERIFY:
        tags.append(f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">')
    return "\n".join(tags)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def publish_path(path: str) -> str:
    """소스 경로(gyeonggi/…)에서 노출 경로(…)를 만든다.

    URL 에 'gyeonggi/' 프리픽스가 붙지 않도록 빌드 단계에서 제거한다.
    (예: 'gyeonggi/suwon/' → 'suwon/', 'gyeonggi/' → '')
    """
    return re.sub(r"^gyeonggi/?", "", path)


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    사이트 공통 블록(요금·참고링크·Who/How/Why·CTA·공통 안내)은 페이지 고유
    본문이 아니므로 측정에서 제외해, 2,000자 기준이 '고유 콘텐츠'에 적용되도록 한다."""
    text = re.sub(
        r'<section class="(?:pricing|references|whw|cta|shared)[^"]*">.*?</section>',
        " ", body_html, flags=re.S,
    )
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_reviews() -> str:
    """화면 노출용 이용 후기·평점 블록.

    구조화 데이터(AggregateRating/Review)와 같은 데이터를 화면에도 노출해야
    구글 정책상 평점 마크업이 유효하다. class="shared" 로 고유 글자수에서 제외.
    """
    full = int(float(RATING_VALUE))
    half = 1 if (float(RATING_VALUE) - full) >= 0.5 else 0
    stars = "★" * full + ("⯨" if half else "") + "☆" * (5 - full - half)
    cards = []
    for r in REVIEWS:
        rstars = "★" * r["rating"] + "☆" * (5 - r["rating"])
        cards.append(
            '<li class="review-card">'
            f'<p class="review-stars" aria-label="별점 {r["rating"]}점">{rstars}</p>'
            f'<p class="review-body">{html.escape(r["body"])}</p>'
            f'<p class="review-meta"><span class="review-author">{html.escape(r["author"])}</span>'
            f'<time datetime="{r["date"]}">{r["date"]}</time></p>'
            "</li>"
        )
    return (
        '<section class="shared reviews" aria-label="이용 후기">'
        '<h2>이용 후기</h2>'
        '<div class="review-summary">'
        f'<span class="review-score">{RATING_VALUE}</span>'
        f'<span class="review-stars-lg" aria-hidden="true">{stars}</span>'
        f'<span class="review-count">이용자 평점 · 후기 {RATING_COUNT}건</span>'
        "</div>"
        f'<ul class="review-list">{"".join(cards)}</ul>'
        '<p class="review-note">표시된 후기는 이용 경험을 바탕으로 한 대표 사례이며, '
        '실제 방문 가능 여부·조건은 예약 시 안내됩니다.</p>'
        "</section>"
    )


def _json_escape(s: str) -> str:
    """JSON-LD 문자열 값 이스케이프."""
    return (
        s.replace("\\", "\\\\").replace('"', '\\"')
        .replace("\n", " ").replace("\r", " ")
    )


def render_base_schema(page: dict, canonical: str) -> str:
    """모든 페이지 공통 구조화 데이터: WebPage + BreadcrumbList + Organization.

    페이지별 추가 스키마(FAQPage, Article 등)는 extra_head 로 별도 주입된다.
    실제 매장 주소가 없는 방문형 서비스이므로 LocalBusiness 는 사용하지 않는다.
    """
    base = BASE_URL.rstrip("/")
    title = _json_escape(page["title"])
    desc = _json_escape(page["desc"])
    og = f"{base}/assets/og-image.png"

    # BreadcrumbList — 홈 + 페이지 breadcrumb(있으면)
    crumbs = page.get("breadcrumb") or []
    items = [(BRAND, base + "/")]
    for label, href in crumbs:
        url = (base + href) if href else canonical
        items.append((label, url))
    if not crumbs:
        # 단독 페이지도 현재 페이지를 마지막 항목으로 추가
        items.append((_json_escape(page["h1"]), canonical))
    crumb_items = ",\n      ".join(
        '{{"@type":"ListItem","position":{i},"name":"{name}","item":"{url}"}}'.format(
            i=i + 1, name=_json_escape(label), url=url
        )
        for i, (label, url) in enumerate(items)
    )

    # Service + 평점·후기(대표 샘플) — 모든 페이지 공통.
    review_items = ",\n        ".join(
        '{{"@type":"Review","author":{{"@type":"Person","name":"{name}"}},'
        '"datePublished":"{date}","reviewRating":{{"@type":"Rating",'
        '"ratingValue":"{rating}","bestRating":"{best}","worstRating":"1"}},'
        '"reviewBody":"{body}"}}'.format(
            name=_json_escape(r["author"]), date=r["date"], rating=r["rating"],
            best=RATING_BEST, body=_json_escape(r["body"]),
        )
        for r in REVIEWS
    )
    service_block = f"""    {{
      "@type": "Service",
      "@id": "{base}/#service",
      "name": "{TRADE_NAME} {AREA_SERVED} 방문형 관리 안내",
      "serviceType": "방문형 관리·홈케어 안내",
      "provider": {{"@id": "{base}/#organization"}},
      "areaServed": {{"@type": "AdministrativeArea", "name": "{AREA_SERVED}"}},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "{RATING_VALUE}",
        "reviewCount": "{RATING_COUNT}",
        "bestRating": "{RATING_BEST}",
        "worstRating": "1"
      }},
      "review": [
        {review_items}
      ]
    }},
"""

    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Organization",
      "@id": "{base}/#organization",
      "name": "{TRADE_NAME}",
      "alternateName": "{BRAND}",
      "url": "{base}/",
      "image": "{og}",
      "logo": "{og}",
      "telephone": "{PHONE}",
      "areaServed": {{"@type": "AdministrativeArea", "name": "{AREA_SERVED}"}},
      "contactPoint": {{
        "@type": "ContactPoint",
        "telephone": "{PHONE}",
        "contactType": "reservations",
        "availableLanguage": "ko"
      }}
    }},
{service_block}    {{
      "@type": "WebSite",
      "@id": "{base}/#website",
      "url": "{base}/",
      "name": "{BRAND}",
      "publisher": {{"@id": "{base}/#organization"}},
      "inLanguage": "ko"
    }},
    {{
      "@type": "WebPage",
      "@id": "{canonical}#webpage",
      "url": "{canonical}",
      "name": "{title}",
      "description": "{desc}",
      "isPartOf": {{"@id": "{base}/#website"}},
      "primaryImageOfPage": {{"@type": "ImageObject", "url": "{og}"}},
      "inLanguage": "ko"
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{canonical}#breadcrumb",
      "itemListElement": [
      {crumb_items}
      ]
    }}
  ]
}}
</script>
"""


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow,max-image-preview:large,'
             'max-snippet:-1,max-video-preview:-1">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path
    base_schema = render_base_schema(page, canonical)

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    reviews_html = render_reviews()
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    html_out = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{verify_meta()}
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="alternate" type="application/rss+xml" title="{BRAND} 최신 안내" href="{BASE_URL.rstrip('/')}/rss.xml">
<link rel="sitemap" type="application/xml" href="{BASE_URL.rstrip('/')}/sitemap.xml">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#05080f">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{base_schema}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/gyeonggi/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> {REGION_NAME} 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
      {reviews_html}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">{REGION_NAME} 전지역 방문형 관리 안내 사이트입니다. 시군·일반구·행정동·생활권·역세권별 예약 전 확인사항을 안내하며, 안내된 관리 범위 안에서만 운영합니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">상　　호</span> {TRADE_NAME}</span>
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> {REGION_NAME} 전지역</span>
      </address>
      <div class="footer-cta">
        <a class="footer-cta-btn" href="{TELEGRAM_WEB}" target="_blank" rel="noopener nofollow">
          <span class="footer-cta-ic" aria-hidden="true">✦</span> 웹사이트 제작문의
        </a>
        <a class="footer-cta-btn" href="{TELEGRAM_PARTNER}" target="_blank" rel="noopener nofollow">
          <span class="footer-cta-ic" aria-hidden="true">✦</span> 제휴문의
        </a>
      </div>
    </div>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>
        <li><a href="/gyeonggi/">경기 홈</a></li>
        <li><a href="/gyeonggi/area/">권역 안내</a></li>
        <li><a href="/gyeonggi/cities/">시군 안내</a></li>
        <li><a href="/gyeonggi/districts/">행정구 안내</a></li>
        <li><a href="/gyeonggi/life/">생활권 안내</a></li>
        <li><a href="/gyeonggi/station/">지하철역 안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/gyeonggi/use/">이용 장소</a></li>
        <li><a href="/gyeonggi/check/">예약 전 확인</a></li>
        <li><a href="/gyeonggi/check/time/">예약 가능 시간</a></li>
        <li><a href="/gyeonggi/check/travel-fee/">추가 이동비 기준</a></li>
        <li><a href="/gyeonggi/contact/">문의하기</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="운영 기준">
      <p class="footer-title">운영 기준</p>
      <ul>
        <li><a href="/gyeonggi/policy/service-standard/">콘텐츠·운영 기준</a></li>
        <li><a href="/gyeonggi/policy/authors/">작성자·검수자 안내</a></li>
        <li><a href="/gyeonggi/policy/privacy/">개인정보 처리방침</a></li>
        <li><a href="/gyeonggi/check/privacy/">개인정보 처리 기준</a></li>
        <li><a href="/gyeonggi/check/service-policy/">불법·선정적 서비스 불가</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND} · 상호 {TRADE_NAME}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""
    # URL 에서 'gyeonggi/' 프리픽스를 제거한다(내부 링크·canonical·schema 일괄).
    return html_out.replace("/gyeonggi/", "/")


def build() -> None:
    report = []
    sitemap_urls = []
    feed_items = []  # (url, title, desc) — RSS 용 색인 페이지

    for page in PAGES:
        pub = publish_path(page["path"])  # 노출 경로(gyeonggi/ 프리픽스 제거)
        out_dir = os.path.join(ROOT, pub)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            url = BASE_URL.rstrip("/") + "/" + pub
            sitemap_urls.append(url)
            feed_items.append((url, page["title"], page["desc"]))
        report.append((pub or "/", chars, "noindex" if noindex else "index"))

    base = BASE_URL.rstrip("/")

    # sitemap.xml — lastmod 포함(색인 신선도 신호)
    urls = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{BUILD_DATE}</lastmod>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if u == base + '/' else '0.7'}</priority></url>"
        for u in sitemap_urls
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 구글·네이버가 신규/변경 URL 을 빠르게 발견하도록 RSS 2.0 피드 생성
    rfc822 = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")
    items = "\n".join(
        "    <item>\n"
        f"      <title>{html.escape(t)}</title>\n"
        f"      <link>{u}</link>\n"
        f"      <guid isPermaLink=\"true\">{u}</guid>\n"
        f"      <description>{html.escape(d)}</description>\n"
        f"      <pubDate>{rfc822}</pubDate>\n"
        "    </item>"
        for u, t, d in feed_items
    )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} 출장마사지 지역 안내</title>\n"
            f"    <link>{base}/</link>\n"
            f'    <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            f"    <description>{html.escape(REGION_NAME)} 시군·생활권·역세권별 방문형 관리 안내</description>\n"
            "    <language>ko</language>\n"
            f"    <lastBuildDate>{rfc822}</lastBuildDate>\n"
            f"{items}\n"
            "  </channel>\n</rss>\n"
        )

    # robots.txt — 모든 봇 허용 + 네이버(Yeti)·구글·Bing 명시 + sitemap·rss 안내
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"          # 네이버 검색로봇
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Bingbot\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — 네이버·Bing 즉시 색인 제출(POST)에 사용
    if INDEXNOW_KEY:
        with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
            f.write(INDEXNOW_KEY + "\n")

    # 구 URL(/gyeonggi/*) → 신 URL(/*) 301 리다이렉트 (Netlify).
    # 기존에 색인된 /gyeonggi/ 경로의 SEO 가치를 새 루트 경로로 넘긴다.
    with open(os.path.join(ROOT, "_redirects"), "w", encoding="utf-8") as f:
        f.write(
            "# 구 경로 호환 — gyeonggi/ 프리픽스 제거(영구 이동)\n"
            "/gyeonggi/*    /:splat    301!\n"
            "/gyeonggi      /          301!\n"
        )

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
