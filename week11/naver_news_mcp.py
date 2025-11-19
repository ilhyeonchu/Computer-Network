# naver-news-mcp.py
import csv
import os
import re
import sys
import time
from typing import Any, List, Tuple

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

DEFAULT_SECTION_URLS: list[str] = [f"https://news.naver.com/section/{i}" for i in range(100,106)]
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ko-KR,ko;q=0.9",
}


def clean_text(s: str) -> str:
    """줄바꿈/연속 공백 제거."""
    s = re.sub(r"\s+", " ", s or "").strip()
    return s

def get_soup(url: str, timeout: int = 50) -> BeautifulSoup | None:
    try:
        res = requests.get(url, headers=HEADERS, timeout=timeout)
        res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"[ERROR] GET {url} failed: {e}", file=sys.stderr)
        return None


def fetch_news_texts(url: str | list[str] = DEFAULT_SECTION_URLS) -> list[str]:
    """
    섹션 첫 페이지에서 기사 제목 텍스트를 수집합니다.
    (네이버 섹션 페이지의 a.sa_text 선택자를 사용 – 스크린샷과 동일)
    """
    urls = [url] if isinstance(url, str) else list(url)
    all_titles: list[str] = []

    for u in urls:
        soup = get_soup(u)
        if not soup:
            continue

        # 섹션 페이지의 제목 링크는 보통 .sa_text 에 들어있습니다.
        titles = [clean_text(tag.get_text(strip=True)) for tag in soup.select(".sa_text")]
        all_titles.extend(t for t in titles if t)

        time.sleep(0.3)

    seen = set()
    deduped = []
    for t in all_titles:
        if t not in seen:
            seen.add(t)
            deduped.append(t)

    print(f"[DEBUG] 추출된 텍스트 개수: {len(deduped)}", file=sys.stderr)
    return deduped

def fetch_news_with_links(url: str | list[str] = DEFAULT_SECTION_URLS) -> list[Tuple[str, str]]:
    """
    제목과 링크를 함께 가져옵니다.
    """
    urls = [url] if isinstance(url, str) else list(url)
    items: list[Tuple[str, str]] = []

    for u in urls:
        soup = get_soup(u)
        if not soup:
            continue

        for a in soup.select("a.sa_text"):
            title = clean_text(a.get_text(strip=True))
            href = a.get("href") or ""
            #if title and href:
                # 절대경로 보정(대부분 절대 URL이지만 혹시 몰라서)
                #if href.startswith("/"):
                #    href = f"https://news.naver.com{href}"
                #items.append((title, href))
        
        time.sleep(0.3)

    print(f"[DEBUG] 추출된 (제목,링크) 개수: {len(items)}", file=sys.stderr)
    return items


mcp = FastMCP("naver_news")

SECTION_LABELS = {
        "100": "정치", "101": "경제", "102": "사회", "103": "생활/문화", "104": "세계", "105": "IT/과학",
        }

@mcp.tool()
async def fetch_it_news(max_count: int = 50) -> str:
    per_section = max(1, max_count // len(DEFAULT_SECTION_URLS))
    lines: list[str] = []
    for url in DEFAULT_SECTION_URLS:
        section_id = url.rsplit("/", 1)[-1]
        section_name = SECTION_LABELS.get(section_id, section_id)
        titles = fetch_news_texts(url)[:per_section]

        if not titles:
            continue
        
        lines.append(f"[{section_name}]")
        lines.extend(f"- {title}" for title in titles)
    return "\n".join(lines) if lines else "⚠️ 뉴스 텍스트를 찾지 못했습니다."

###############################################################################
# CLI로도 사용 가능
###############################################################################

def main_cli():
    import argparse
    p = argparse.ArgumentParser(description="Naver 뉴스 크롤러")
    p.add_argument("--mode", choices=["print", "csv", "wc"], default="print",
                   help="print: 제목 출력, csv: CSV 저장, wc: 워드클라우드")
    p.add_argument("--url", default=DEFAULT_SECTION_URLS,
                   help="대상 섹션 URL (기본: IT/과학 105)")
    p.add_argument("--out", default="naver_it_news.csv", help="CSV/PNG 출력 파일명")
    p.add_argument("--max", type=int, default=100, help="최대 개수")
    args = p.parse_args()

    if args.mode == "print":
        for t in fetch_news_texts(args.url)[:args.max]:
            print(t)
            
if __name__ == "__main__":
    mcp.run()
