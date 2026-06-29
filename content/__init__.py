# 경기도 출장마사지 — 전체 페이지 목록 집계
from . import pages, generated_pages

PAGES = (
    pages.static_pages()
    + generated_pages.region_pages()
    + generated_pages.city_pages()
)
