#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baekjoon (BOJ) 워크플로 도우미
- start: 문제별 디렉터리(코드 + README) 생성
- finish: 천 단위 폴더로 이동하고(선택) git 커밋/푸시
- md: 문제 페이지를 크롤링하여 Markdown 생성
- run: 샘플을 가져와 풀이에 실행

solved.ac 를 활용해 제목/난이도를 보강하고, HTML 크롤링으로 최대한 복원합니다.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import ssl
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional
from typing import TypedDict
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class ProblemSubmitter:
    """acmicpc.net 제출기 (쿠키 필요).
    - 쿠키: env BOJ_COOKIE → bojconfig.json 'boj_cookie'
    - 언어 id: 제출 페이지에서 옵션 파싱으로 자동 결정
    - 소스: 문제 디렉터리에서 확장자 기준 자동 탐색 (또는 --file)
    """
    BASE = "https://www.acmicpc.net"

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.cookie = os.environ.get("BOJ_COOKIE") or (self.cfg.get("boj_cookie") or "").strip()
        if not self.cookie:
            print(f"{L.ERROR} BOJ cookie is required for submission.")
            print(f"{L.HINT} Set environment variable: export BOJ_COOKIE='your_cookie_string'")
            print(f"{L.HINT} Or create bojconfig.json: {{'boj_cookie': 'your_cookie_string'}}")
            print(f"{L.HINT} Get cookie from browser after logging in to acmicpc.net")
            print(f"{L.HINT} Copy all cookies from Developer Tools → Application → Cookies")
            raise SystemExit("BOJ_COOKIE not configured")

    def _ctx(self):
        try:
            if _CAFILE:
                return ssl.create_default_context(cafile=_CAFILE)
            else:
                ctx = ssl.create_default_context()
                # macOS에서 시스템 키체인 사용
                if hasattr(ssl, '_create_unverified_context'):
                    ctx = ssl._create_unverified_context()
                return ctx
        except Exception:
            # SSL 검증 비활성화 (보안상 권장되지 않지만 테스트용)
            return ssl._create_unverified_context()

    def _get(self, path: str, headers: dict | None = None) -> str:
        h = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            # gzip 압축을 비활성화
            # "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "Referer": self.BASE + "/",
            "Cookie": self.cookie,
        }
        if headers:
            h.update(headers)
        req = Request(self.BASE + path, headers=h)
        with urlopen(req, timeout=10, context=self._ctx()) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    def _post(self, path: str, data: dict, headers: dict | None = None) -> str:
        body = urlencode(data).encode()
        h = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            # gzip 압축을 비활성화
            # "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(len(body)),
            "DNT": "1",
            "Connection": "keep-alive",
            "Origin": self.BASE,
            "Referer": self.BASE + path,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cookie": self.cookie,
        }
        if headers:
            h.update(headers)
        req = Request(self.BASE + path, data=body, headers=h, method="POST")
        with urlopen(req, timeout=10, context=self._ctx()) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    def _parse_csrf_and_langs(self, html_text: str) -> tuple[str, dict[str, str]]:
        csrf = ""
        langs: dict[str, str] = {}
        
        # 디버그 모드일 때 추가 정보 출력
        debug = os.environ.get("BOJ_DEBUG")
        
        if BeautifulSoup is not None:
            soup = BeautifulSoup(html_text, 'html.parser')
            
            # CSRF 토큰 찾기 - 더 다양한 패턴 지원
            csrf_selectors = [
                "input[name='csrf_key']",
                "input[name='csrf_token']", 
                "input[name='_token']",
                "meta[name='csrf-token']",
                "input[type='hidden'][name*='csrf']",
                "input[type='hidden'][name*='token']"
            ]
            
            for selector in csrf_selectors:
                token = soup.select_one(selector)
                if token:
                    csrf = (token.get("value") or token.get("content") or "").strip()
                    if debug:
                        print(f"{L.INFO} Found CSRF token using selector: {selector}")
                    break
            
            if debug and not csrf:
                print(f"{L.WARN} No CSRF token found with BeautifulSoup selectors")
                # 모든 input 태그 검사
                inputs = soup.find_all("input")
                print(f"{L.INFO} Found {len(inputs)} input elements")
                for inp in inputs[:10]:  # 처음 10개만
                    name = inp.get('name', '')
                    if name:
                        print(f"  - input name='{name}' type='{inp.get('type', '')}' value='{(inp.get('value') or '')[:20]}...'")
            
            # 언어 선택 옵션 파싱
            selectors = ["select[name='language']", "select#language", "select[name*='lang']"]
            sel = None
            for selector in selectors:
                sel = soup.select_one(selector)
                if sel:
                    break
                    
            if sel:
                for opt in sel.find_all("option"):
                    val = (opt.get("value") or "").strip()
                    text = opt.get_text(" ", strip=True)
                    if val and text and val != "":  # 빈 값 제외
                        langs[text] = val
            elif debug:
                print(f"{L.WARN} No language select found")
                
        else:
            # BeautifulSoup 없을 때 정규식으로 fallback
            # CSRF 토큰 찾기 - 더 많은 패턴 시도
            patterns = [
                r'name=["\']csrf_key["\'][^>]*value=["\']([^"\']+)["\']',
                r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', 
                r'name=["\']_token["\'][^>]*value=["\']([^"\']+)["\']',
                r'<meta[^>]*name=["\']csrf-token["\'][^>]*content=["\']([^"\']+)["\']',
                r'value=["\']([^"\']+)["\'][^>]*name=["\']csrf_key["\']',
                r'value=["\']([^"\']+)["\'][^>]*name=["\']csrf_token["\']',
                r'<input[^>]*type=["\']hidden["\'][^>]*name=["\'][^"\']*csrf[^"\']*["\'][^>]*value=["\']([^"\']+)["\']',
                r'<input[^>]*type=["\']hidden["\'][^>]*name=["\'][^"\']*token[^"\']*["\'][^>]*value=["\']([^"\']+)["\']'
            ]
            
            for pattern in patterns:
                m = re.search(pattern, html_text, re.IGNORECASE)
                if m:
                    csrf = m.group(1).strip()
                    if debug:
                        print(f"{L.INFO} Found CSRF token using regex pattern")
                    break
            
            # 언어 옵션 찾기
            for m2 in re.finditer(r'<option[^>]*value=["\']([^"\']+)["\'][^>]*>([^<]+)</option>', html_text, re.IGNORECASE):
                val = m2.group(1).strip()
                text = html.unescape(m2.group(2)).strip()
                if val and text and val != "":
                    langs[text] = val
                    
        if debug:
            print(f"{L.INFO} CSRF token: {'Found' if csrf else 'Not found'} ({'*' * min(len(csrf), 8) if csrf else 'None'})")
            print(f"{L.INFO} Languages found: {len(langs)} ({', '.join(list(langs.keys())[:3])}{'...' if len(langs) > 3 else ''})")
                    
        return csrf, langs

    def _pick_language_id(self, langs_map: dict[str, str], prefer: str) -> str:
        prefer = (prefer or '').lower()
        items = list(langs_map.items())

        def find_contains(keys: list[str]):
            for label, val in items:
                low = label.lower()
                if any(k in low for k in keys):
                    return val
            return ""

        def find_exact(keys: list[str]):
            for label, val in items:
                low = label.lower()
                if any(low == k for k in keys):
                    return val
            return ""

        if prefer == 'cpp' or prefer == 'c++':
            # C++ 언어 우선순위: 최신 버전부터
            v = (find_exact(["c++23", "c++20", "c++17", "c++14", "c++11"]) or
                 find_contains(["gnu++23", "gnu++20", "gnu++17", "gnu++14", "gnu++11"]) or
                 find_contains(["c++23", "c++20", "c++17", "c++14", "c++11", "c++", "gnu++"]))
            if v:
                return v
        elif prefer == 'py' or prefer == 'python':
            # Python 언어 우선순위: PyPy3 > Python 3
            v = (find_contains(["pypy3"]) or
                 find_contains(["python 3", "python3"]) or
                 find_contains(["python"]))
            if v:
                return v
        elif prefer == 'java':
            v = find_contains(["java", "openjdk"])
            if v:
                return v
        elif prefer == 'js' or prefer == 'javascript':
            v = find_contains(["node.js", "javascript"])
            if v:
                return v
        
        # 찾지 못했으면 첫 번째 유효한 언어 반환
        return next(iter(langs_map.values()), "")

    def detect_source(self, repo: RepoPaths, pid: int, explicit: Optional[str]) -> Path:
        if explicit:
            p = (repo.root / explicit).resolve()
            if not p.exists():
                raise SystemExit(f"source file not found: {explicit}")
            return p
        globs = [
            repo.root.glob(f"solving/{pid} -*/*.cpp"),
            repo.root.glob(f"solving/{pid} -*/*.py"),
            repo.root.glob(f"**/{pid} -*/*.cpp"),
            repo.root.glob(f"**/{pid} -*/*.py"),
            repo.root.glob(f"solving/{pid} -*.cpp"),
            repo.root.glob(f"solving/{pid} -*.py"),
            repo.root.glob(f"**/{pid} -*.cpp"),
            repo.root.glob(f"**/{pid} -*.py"),
        ]
        for g in globs:
            for p in g:
                return p
        raise SystemExit(f"No source found for {pid}. Use --file to specify.")

    def submit(self, pid: int, repo: RepoPaths, prefer_lang_key: str, open_code: bool, file_path: Optional[str]) -> dict:
        try:
            # 1. 제출 페이지에서 CSRF 토큰과 언어 목록 가져오기
            print(f"{L.INFO} Fetching submit page for problem {pid}...")
            html_text = self._get(f"/submit/{pid}")
            
            # 디버그: HTML 응답 일부 출력
            if os.environ.get("BOJ_DEBUG"):
                print(f"{L.INFO} HTML response preview (first 500 chars):")
                print(html_text[:500])
                print(f"{L.INFO} Searching for login indicators...")
                if "로그인" in html_text or "login" in html_text.lower():
                    print(f"{L.WARN} Login page detected!")
            
            # 로그인 페이지인지 확인
            if "로그인" in html_text or "login" in html_text.lower() or "/login" in html_text:
                print(f"{L.ERROR} Redirected to login page. Your session has expired.")
                print(f"{L.HINT} Please login to acmicpc.net and update your cookie.")
                return {"ok": False, "error": "Session expired - login required"}
            
            csrf, langs = self._parse_csrf_and_langs(html_text)
            
            if not csrf:
                print(f"{L.ERROR} Failed to obtain CSRF token. Please check your BOJ_COOKIE.")
                print(f"{L.HINT} Make sure you're logged in to acmicpc.net and copy the cookie.")
                raise SystemExit("CSRF token not found")
                
            if not langs:
                print(f"{L.ERROR} Failed to parse language list from submit page.")
                raise SystemExit("Language options not found")
            
            print(f"{L.INFO} Available languages: {', '.join(langs.keys())}")
            
            # 2. 언어 ID 선택
            lang_id = self._pick_language_id(langs, prefer_lang_key)
            if not lang_id:
                print(f"{L.ERROR} Could not find suitable language for '{prefer_lang_key}'")
                print(f"{L.HINT} Available: {list(langs.keys())}")
                raise SystemExit("Language selection failed")
            
            # 선택된 언어 표시
            selected_lang = next((k for k, v in langs.items() if v == lang_id), lang_id)
            print(f"{L.OK} Selected language: {selected_lang} (ID: {lang_id})")
            
            # 3. 소스 코드 파일 찾기
            src_path = self.detect_source(repo, pid, file_path)
            print(f"{L.INFO} Source file: {src_path}")
            
            # 4. 소스 코드 읽기
            try:
                code = src_path.read_text(encoding='utf-8')
                if not code.strip():
                    raise SystemExit(f"Source file is empty: {src_path}")
                print(f"{L.INFO} Source code length: {len(code)} characters")
            except UnicodeDecodeError:
                print(f"{L.ERROR} Failed to read source file with UTF-8 encoding: {src_path}")
                raise SystemExit("Source file encoding error")
            
            # 5. 제출 데이터 준비
            data = {
                "problem_id": str(pid),
                "language": lang_id,
                "code_open": "open" if open_code else "close",
                "source": code,
                "csrf_key": csrf,
            }
            
            # 6. 제출 실행
            print(f"{L.INFO} Submitting solution...")
            result_html = self._post(f"/submit/{pid}", data)
            
            # 7. 제출 결과 확인
            success_indicators = [
                "제출되었습니다",
                "submitted successfully", 
                "/status?",
                "status.php",
                "내 제출",
                "My Submissions"
            ]
            
            error_indicators = [
                "로그인이 필요합니다",
                "login required",
                "제출에 실패했습니다",
                "submission failed",
                "잘못된 요청입니다",
                "invalid request"
            ]
            
            success = any(indicator in result_html for indicator in success_indicators)
            has_error = any(indicator in result_html for indicator in error_indicators)
            
            if has_error:
                print(f"{L.ERROR} Submission failed - please check your login status")
                if "로그인" in result_html or "login" in result_html:
                    print(f"{L.HINT} Your session may have expired. Please update BOJ_COOKIE")
                return {"ok": False, "error": "Login required or session expired"}
            
            if success:
                print(f"{L.OK} Solution submitted successfully!")
                print(f"{L.HINT} Check your submission status at: https://www.acmicpc.net/status?user_id=YOUR_ID&problem_id={pid}")
            else:
                print(f"{L.WARN} Submission may have failed - please check manually")
            
            return {
                "ok": success,
                "lang_id": lang_id,
                "language_name": selected_lang,
                "source_path": str(src_path),
                "csrf_token": csrf,
            }
            
        except HTTPError as e:
            if e.code == 403:
                print(f"{L.ERROR} Access forbidden (403) - check your login cookie")
            elif e.code == 404:
                print(f"{L.ERROR} Problem {pid} not found (404)")
            else:
                print(f"{L.ERROR} HTTP error {e.code}: {e.reason}")
            raise SystemExit(f"HTTP error: {e.code}")
            
        except URLError as e:
            print(f"{L.ERROR} Network error: {e.reason}")
            raise SystemExit("Network connection failed")
            
        except Exception as e:
            print(f"{L.ERROR} Unexpected error during submission: {e}")
            raise SystemExit("Submission failed")

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover
    BeautifulSoup = None  # type: ignore


# ---- 섹션 구조를 위한 TypedDicts ----
class SectionDict(TypedDict):
    id: str
    title: str
    content: str


# ============================ ANSI 색상 도우미 =============================

class Ansi:
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"
    BG_RED = "\x1b[41m"
    BG_GREEN = "\x1b[42m"
    BG_YELLOW = "\x1b[43m"
    BG_BLUE = "\x1b[44m"
    BG_MAGENTA = "\x1b[45m"
    BG_CYAN = "\x1b[46m"
    BG_WHITE = "\x1b[47m"

    @staticmethod
    def wrap(s: str, *codes: str) -> str:
        return "".join(codes) + s + Ansi.RESET


# TTY/NO_COLOR 환경에 따라 색상 출력 여부를 결정
def _colors_enabled() -> bool:
    try:
        if os.environ.get("NO_COLOR"):
            return False
        return os.isatty(1)
    except Exception:
        return True


Ansi.ENABLED = _colors_enabled()
Ansi._wrap_orig = Ansi.wrap


def _wrap_cond(s: str, *codes: str) -> str:
    if not Ansi.ENABLED:
        return s
    return Ansi._wrap_orig(s, *codes)


Ansi.wrap = staticmethod(_wrap_cond)


# 박스 그리기 문자 (환경 변수에 따라 ASCII 대체 지원)
class Box:
    if os.environ.get("ASCII_BOX"):
        H, V, TL, TR, BL, BR, T, B, L, R, X = "-", "|", "+", "+", "+", "+", "+", "+", "+", "+", "+"
    else:
        H, V = "─", "│"
        TL, TR, BL, BR = "┌", "┐", "└", "┘"
        T, B, L, R, X = "┬", "┴", "├", "┤", "┼"


class L:
    OK = Ansi.wrap("[ok]", Ansi.BOLD, Ansi.GREEN)
    WARN = Ansi.wrap("[warn]", Ansi.BOLD, Ansi.YELLOW)
    ERROR = Ansi.wrap("[error]", Ansi.BOLD, Ansi.RED)
    INFO = Ansi.wrap("[info]", Ansi.BOLD, Ansi.CYAN)
    HINT = Ansi.wrap("[hint]", Ansi.DIM, Ansi.CYAN)
    SKIP = Ansi.wrap("[skip]", Ansi.DIM, Ansi.BLUE)
    TITLE = Ansi.wrap("[boj]", Ansi.BOLD, Ansi.MAGENTA)


try:
    import certifi  # type: ignore

    _CAFILE = certifi.where()
except Exception:  # pragma: no cover
    _CAFILE = None

# ============================ 상수와 템플릿 ============================
INVALID_FS = r"[\\/:*?\"<>|]"

# C++ 문제 템플릿
CPP_TEMPLATE = """// BOJ {id} - {name}
#include <bits/stdc++.h>
#define endl "\\n"

using namespace std;
using ll = long long;
using ull = unsigned long long;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    return 0;
}}
"""

# 파이썬 문제 템플릿
PY_TEMPLATE = """# BOJ {id} - {name}
import sys
def input() -> str: return sys.stdin.readline()

data = input().split()
"""

DEFAULT_CFG = {
    "lang": "py",  # 기본 언어
    "run_dir": "${CMAKE_BINARY_DIR}/bin",  # ps 타겟에 직접 주입할 때는 사용하지 않음
}

SOLVEDAC_URL = "https://solved.ac/api/v3/problem/show?problemId={pid}"


# ================================= 유틸리티 함수 =================================

def sanitize_filename(s: str) -> str:
    # 파일 이름에 사용할 수 없는 문자를 _로 대체
    s = re.sub(INVALID_FS, "_", s)
    return s.strip()


def thousand_folder(pid: int) -> str:
    # 천 단위 폴더 이름 생성
    base = (pid // 1000) * 1000
    return f"{base:05d}"


# ================================== 경로 관련 ====================================
@dataclass(frozen=True)
class RepoPaths:
    root: Path

    @property
    def solving(self) -> Path:
        # 문제 풀이 디렉터리
        return self.root / "solving"

    @property
    def cmakelists(self) -> Path:
        # CMakeLists.txt 경로
        return self.root / "CMakeLists.txt"

    @property
    def config(self) -> Path:
        # 설정 파일 경로
        return self.root / "bojconfig.json"


# ================================== 설정 ===================================
class Config:
    def __init__(self, paths: RepoPaths):
        self.paths = paths
        self._cfg = DEFAULT_CFG | self._load()

    def _load(self) -> dict:
        # bojconfig.json을 읽어 설정을 불러옴
        if self.paths.config.exists():
            try:
                return json.loads(self.paths.config.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def get(self, key: str, default=None):
        return self._cfg.get(key, default)


# ================================ HTTP / 제목 조회 ===============================
class ProblemFetcher:
    # ---- HTML 표를 Markdown 표로 변환 ----
    def _table_to_markdown(self, table_el) -> str:
        if not table_el:
            return ''
        rows: list[list[str]] = []
        heads = table_el.select('thead tr') if hasattr(table_el, 'select') else []
        bodies = table_el.select('tbody tr') if hasattr(table_el, 'select') else []
        if heads:
            for tr in heads:
                rows.append([c.get_text(strip=True) for c in tr.find_all(['th', 'td'])])
        if bodies:
            for tr in bodies:
                rows.append([c.get_text(strip=True) for c in tr.find_all(['th', 'td'])])
        if not rows:
            for tr in table_el.find_all('tr'):
                cells = [c.get_text(strip=True) for c in tr.find_all(['th', 'td'])]
                if cells:
                    rows.append(cells)
        if not rows:
            return ''
        width = max(len(r) for r in rows)
        rows = [r + [''] * (width - len(r)) for r in rows]
        out = [
            '| ' + ' | '.join(rows[0]) + ' |',
            '| ' + ' | '.join(['---'] * width) + ' |',
        ]
        for r in rows[1:]:
            out.append('| ' + ' | '.join(r) + ' |')
        return "\n".join(out)

    # ---- 섹션 노드를 Markdown 텍스트로 변환 (.spoiler 포함) ----
    def _section_to_markdown(self, sec) -> str:
        include_nodes = []
        pt = sec.select_one('.problem-text')
        include_nodes.append(pt if pt else sec)
        include_nodes.extend(sec.select('.spoiler'))
        combined_html = ''.join(str(el) for el in include_nodes)
        if BeautifulSoup is not None:
            tmp = BeautifulSoup(combined_html, 'html.parser')
            for h in list(tmp.select('.headline h2')):
                h.decompose()
            for tbl in list(tmp.find_all('table')):
                md_tbl = self._table_to_markdown(tbl)
                from bs4 import NavigableString  # type: ignore
                tbl.replace_with(NavigableString('\n' + md_tbl + '\n') if md_tbl else NavigableString(''))
            combined_html = str(tmp)
        cleaned = self._clean_html_block(combined_html)
        if not cleaned.strip() and BeautifulSoup is not None:
            tmp2 = BeautifulSoup(combined_html, 'html.parser')
            items = [li.get_text(' ', strip=True) for li in tmp2.select('li')]
            items = [it for it in items if it]
            if items:
                return '\n' + '\n'.join(f'- {it}' for it in items) + '\n'
        return cleaned

    # === HTML → Markdown 보조 함수 (bs4 사용) ===
    def _bs4_convert_images(self, soup):
        for img in list(soup.find_all('img')):
            src = (img.get('src') or '').strip()
            alt = (img.get('alt') or '').strip() or 'image'
            if not src:
                img.decompose()
                continue
            if src.startswith('//'):
                src_abs = 'https:' + src
            elif src.startswith('/'):
                src_abs = 'https://www.acmicpc.net' + src
            else:
                src_abs = src
            md_img = f"\n![{alt}]({src_abs})\n"
            img.replace_with(md_img)

    def _bs4_convert_inline_marks(self, soup):
        for t in list(soup.find_all(['strong', 'b'])):
            t.replace_with(f"**{t.get_text(separator=' ', strip=True)}**")
        for t in list(soup.find_all(['em', 'i'])):
            t.replace_with(f"*{t.get_text(separator=' ', strip=True)}*")
        for t in list(soup.find_all(['s', 'del', 'strike'])):
            t.replace_with(f"~~{t.get_text(separator=' ', strip=True)}~~")

    def _bs4_convert_sup_sub(self, soup):
        for t in list(soup.find_all('sup')):
            t.replace_with(f"^{{{t.get_text(separator=' ', strip=True)}}}")
        for t in list(soup.find_all('sub')):
            t.replace_with(f"_{{{t.get_text(separator=' ', strip=True)}}}")

    def _bs4_convert_lists(self, soup):
        def _ul_to_md(ul):
            items = [f"- {li.get_text(separator=' ', strip=True)}" for li in ul.find_all('li', recursive=False)]
            return '\n' + '\n'.join(items) + '\n'

        def _ol_to_md(ol):
            items = [f"{i + 1}. {li.get_text(separator=' ', strip=True)}" for i, li in enumerate(ol.find_all('li', recursive=False))]
            return '\n' + '\n'.join(items) + '\n'

        for ul in list(soup.find_all('ul')):
            ul.replace_with(_ul_to_md(ul))
        for ol in list(soup.find_all('ol')):
            ol.replace_with(_ol_to_md(ol))
        # lone li (safety)
        for li in list(soup.find_all('li')):
            li.replace_with(f"- {li.get_text(separator=' ', strip=True)}")

    def _bs4_convert_pre(self, soup):
        for pre in list(soup.find_all('pre')):
            # pre 태그 내의 텍스트를 가져옴 (HTML 엔티티 디코딩 포함)
            import html
            code_text = html.unescape(pre.get_text())
            # 마크다운 코드 블록으로 변환
            md_code = f"\n```\n{code_text}\n```\n"
            pre.replace_with(md_code)

    def _finalize_text_common(self, text: str) -> str:
        import re as _re, html as _html
        text = _html.unescape(text).replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')
        text = _re.sub(r'([0-9A-Za-z]+)\s*\^\{([^}]+)\}', r'$\1^{\2}$', text)
        text = _re.sub(r'([0-9A-Za-z]+)\s*_\{([^}]+)\}', r'$\1_{\2}$', text)
        text = _re.sub(r'\n\s*([+*/=])', r' \1', text)
        text = _re.sub(r'([+*/=])\s*\n', r'\1 ', text)
        text = _re.sub(r'^(\s*)>(\s*)$', r'\1\\>\2', text, flags=_re.MULTILINE)
        text = _re.sub(r'^(\s*)>\s+(?=\S)', r'\1\\> ', text, flags=_re.MULTILINE)
        text = _re.sub(r'^[ \t]+', '', text, flags=_re.MULTILINE)
        text = _re.sub(r'\n{3,}', '\n\n', text)
        return text.strip('\n')

    # === HTML → Markdown 보조 함수 (정규식 폴백) ===
    def _fallback_clean(self, fragment: str) -> str:
        import re as _re, html as _html
        frag = _re.sub(r'<br\s*/?>', '\n', fragment, flags=_re.IGNORECASE)
        
        # <pre> 태그를 마크다운 코드 블록으로 변환
        def _pre_repl(m):
            code_content = _html.unescape(m.group(1))
            return f"\n```\n{code_content}\n```\n"
        frag = _re.sub(r'<pre[^>]*>(.*?)</pre>', _pre_repl, frag, flags=_re.IGNORECASE | _re.DOTALL)
        
        frag = _re.sub(r'</?\s*(strong|b)\s*>', '**', frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'</?\s*(em|i)\s*>', '*', frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'</?\s*(s|del|strike)\s*>', '~~', frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'<\s*sup\s*>', '^{', frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'<\s*/\s*sup\s*>', '}', frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'<\s*sub\s*>', '_{', frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'<\s*/\s*sub\s*>', '}', frag, flags=_re.IGNORECASE)

        def _img_repl(m):
            src = (m.group(1) or '').strip()
            alt = (m.group(2) or '').strip() or 'image'
            if src.startswith('//'):
                src_abs = 'https:' + src
            elif src.startswith('/'):
                src_abs = 'https://www.acmicpc.net' + src
            else:
                src_abs = src
            return f"\n![{alt}]({src_abs})\n"

        frag = _re.sub(r'<img[^>]*src\s*=\s*"([^"]+)"[^>]*alt\s*=\s*"([^"]*)"[^>]*>', _img_repl, frag, flags=_re.IGNORECASE)
        frag = _re.sub(r"<img[^>]*src\s*=\s*'([^']+)'[^>]*alt\s*=\s*'([^']*)'[^>]*>", _img_repl, frag, flags=_re.IGNORECASE)

        def _img_repl2(m):
            src = (m.group(1) or '').strip()
            alt = 'image'
            if src.startswith('//'):
                src_abs = 'https:' + src
            elif src.startswith('/'):
                src_abs = 'https://www.acmicpc.net' + src
            else:
                src_abs = src
            return f"\n![{alt}]({src_abs})\n"

        frag = _re.sub(r'<img[^>]*src\s*=\s*"([^"]+)"[^>]*>', _img_repl2, frag, flags=_re.IGNORECASE)
        frag = _re.sub(r"<img[^>]*src\s*=\s*'([^']+)'[^>]*>", _img_repl2, frag, flags=_re.IGNORECASE)
        frag = _re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f"- {m.group(1).strip()}\n", frag, flags=_re.IGNORECASE | _re.DOTALL)
        frag = _re.sub(r'<[^>]+>', '', frag)
        frag = _html.unescape(frag).replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')
        frag = _re.sub(r'([0-9A-Za-z]+)\s*\^\{([^}]+)\}', r'$\1^{\2}$', frag)
        frag = _re.sub(r'([0-9A-Za-z]+)\s*_\{([^}]+)\}', r'$\1_{\2}$', frag)
        frag = _re.sub(r'^[ \t]+', '', frag, flags=_re.MULTILINE)
        frag = _re.sub(r'\n{3,}', '\n\n', frag)
        frag = _re.sub(r'\n\s*([+*/=])', r' \1', frag)
        frag = _re.sub(r'([+*/=])\s*\n', r'\1 ', frag)
        frag = _re.sub(r'^(\s*)>(\s*)$', r'\\>\2', frag, flags=_re.MULTILINE)
        frag = _re.sub(r'^(\s*)>\s+(?=\S)', r'\1\\> ', frag, flags=_re.MULTILINE)
        return frag.strip('\n')

    def _clean_html_block(self, fragment: str) -> str:
        """HTML 조각을 읽기 쉬운 Markdown 형태로 변환합니다(bs4 우선 적용).
        - **굵게**, *기울임*, ~~취소선~~을 유지합니다.
        - <sup>/<sub>는 LaTeX 스타일로 변환: `$base^{exp}$`, `$base_{sub}$`
        - 줄바꿈을 보존하고 들여쓰기를 제거합니다.
        - 인라인 이미지는 절대 URL의 Markdown 이미지로 변환합니다.
        - <ul>/<ol>/<li>를 Markdown 리스트로 변환합니다.
        """
        if BeautifulSoup is None:
            return self._fallback_clean(fragment)

        soup = BeautifulSoup(fragment, 'html.parser')
        for el in soup.select('a.copy-button, a.show-spoiler, button'):
            el.decompose()
        for br in soup.find_all('br'):
            br.replace_with('\n')
        self._bs4_convert_images(soup)
        self._bs4_convert_inline_marks(soup)
        self._bs4_convert_sup_sub(soup)
        self._bs4_convert_lists(soup)
        self._bs4_convert_pre(soup)
        text = soup.get_text(separator='\n')
        return self._finalize_text_common(text)

    def _download_problem_html(self, pid: int) -> str:

        try:
            return self._request(
                f"https://www.acmicpc.net/problem/{pid}",
                {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                },
            )
        except Exception:
            return ""

    def _parse_title(self, soup, html_text: str) -> str:
        title = ''
        if soup:
            t = soup.select_one('#problem_title')
            if t:
                title = t.get_text(strip=True)
        if not title:
            mt = re.search(r'<title>(.*?)</title>', html_text, re.IGNORECASE | re.DOTALL)
            if mt:
                title_tag = html.unescape(mt.group(1)).strip()
                parts = re.split(r'[:\-]\s*', title_tag, maxsplit=1)
                title = (parts[-1] if parts else title_tag).strip()
        return title

    def _parse_tier_image(self, soup) -> str:

        tier_image = ''
        if soup:
            img = soup.select_one('img[src*="/tier/"]')
            if img and img.get('src'):
                tier_image = img['src']
        if tier_image:
            if tier_image.startswith('//'):
                tier_image = 'https:' + tier_image
            elif tier_image.startswith('/'):
                tier_image = 'https://www.acmicpc.net' + tier_image
        return tier_image

    def _parse_info_table(self, soup, html_text: str) -> tuple[str, str, str, str, str, str]:

        time_limit = memory_limit = submissions = accepted = solved = ratio = ''
        if soup:
            table = soup.select_one('#problem-info')
            if table:
                headers = [th.get_text(strip=True) for th in table.select('thead th')]
                values = [td.get_text(strip=True) for td in table.select('tbody td')]
                if headers and values and len(values) >= len(headers):
                    for i, label in enumerate(headers):
                        value = values[i] if i < len(values) else ''
                        if '시간 제한' in label:
                            time_limit = value
                        elif '메모리 제한' in label:
                            memory_limit = value
                        elif '제출' in label:
                            submissions = value
                        elif label.strip() == '정답':
                            accepted = value
                        elif '맞힌 사람' in label:
                            solved = value
                        elif '정답 비율' in label:
                            ratio = value
                else:
                    for tr in table.select('tr'):
                        th = tr.find(['th', 'td'])
                        tds = tr.find_all('td')
                        label = th.get_text(strip=True) if th else ''
                        val = tds[0].get_text(strip=True) if tds else ''
                        if not label:
                            continue
                        if '시간 제한' in label and not time_limit:
                            time_limit = val
                        elif '메모리 제한' in label and not memory_limit:
                            memory_limit = val
                        elif '제출' in label and not submissions:
                            submissions = val
                        elif label.strip() == '정답' and not accepted:
                            accepted = val
                        elif '맞힌 사람' in label and not solved:
                            solved = val
                        elif '정답 비율' in label and not ratio:
                            ratio = val
        if not time_limit:
            tl = re.search(r'시간\s*제한[^0-9]*([0-9][^<\n]*)', html_text, re.IGNORECASE)
            time_limit = html.unescape(tl.group(1)).strip() if tl else ''
        if not memory_limit:
            ml = re.search(r'메모리\s*제한[^0-9]*([0-9][^<\n]*)', html_text, re.IGNORECASE)
            memory_limit = html.unescape(ml.group(1)).strip() if ml else ''
        if not submissions:
            m = re.search(r'>\s*제출\s*<.*?>\s*([0-9,]+)\s*<', html_text, re.IGNORECASE | re.DOTALL)
            submissions = m.group(1).strip() if m else submissions
        if not accepted:
            m = re.search(r'>\s*정답\s*<.*?>\s*([0-9,]+)\s*<', html_text, re.IGNORECASE | re.DOTALL)
            accepted = m.group(1).strip() if m else accepted
        if not solved:
            m = re.search(r'>\s*맞힌\s*사람\s*<.*?>\s*([0-9,]+)\s*<', html_text, re.IGNORECASE | re.DOTALL)
            solved = m.group(1).strip() if m else solved
        if not ratio:
            m = re.search(r'>\s*정답\s*비율\s*<.*?>\s*([0-9.,%]+)\s*<', html_text, re.IGNORECASE | re.DOTALL)
            ratio = m.group(1).strip() if m else ratio
        return time_limit, memory_limit, submissions, accepted, solved, ratio

    def _collect_sections(self, soup, html_text: str) -> list[SectionDict]:
        # BOJ 문제 본문에서 모든 섹션을 수집하고, 필요한 경우 예제 섹션을 합성한다.

        if not soup:
            # minimal legacy fallback
            sections: list[SectionDict] = []

            def _extract_node_text(sel: str) -> str:
                m1 = re.search(rf'id\s*=\s*[\"\']{sel}[\"\'][^>]*>(.*?)</section>', html_text, re.IGNORECASE | re.DOTALL)
                if m1:
                    return self._clean_html_block(m1.group(1))
                m2 = re.search(rf'id\s*=\s*[\"\']{sel}[\"\'][^>]*>(.*?)</div>', html_text, re.IGNORECASE | re.DOTALL)
                return self._clean_html_block(m2.group(1)) if m2 else ''

            for sid, title_txt in (
                    ('problem_description', '문제'),
                    ('problem_input', '입력'),
                    ('problem_output', '출력'),
                    ('problem_note', '노트'),
            ):
                txt = _extract_node_text(sid)
                if txt:
                    sections.append({'id': sid, 'title': title_txt, 'content': txt})
            return sections

        # 샘플 맵(예제 입력/출력 수집)
        sample_inputs: dict[int, str] = {}
        sample_outputs: dict[int, str] = {}

        def _clean_pre_local(pre_el) -> str:
            frag = str(pre_el)
            frag = re.sub(r'<span[^>]*class=\"space-highlight\"[^>]*>\s*</span>', ' ', frag, flags=re.IGNORECASE)
            frag = re.sub(r'<br\s*/?>', '\n', frag, flags=re.IGNORECASE)
            frag = re.sub(r'<[^>]+>', '', frag)
            frag = html.unescape(frag).replace('\r\n', '\n').replace('\r', '\n')
            return frag.strip('\n')

        for pre in soup.select('pre[id^="sample-input-"]'):
            try:
                n = int((pre.get('id') or '').split('-')[-1])
            except Exception:
                continue
            sample_inputs[n] = _clean_pre_local(pre)
        for pre in soup.select('pre[id^="sample-output-"]'):
            try:
                n = int((pre.get('id') or '').split('-')[-1])
            except Exception:
                continue
            sample_outputs[n] = _clean_pre_local(pre)
        handled_samples: set[int] = set()

        sections: list[SectionDict] = []
        seen: set = set()
        sec_nodes: list = []
        body = soup.select_one('#problem-body')
        if body:
            sec_nodes += body.select('section')
        for s in soup.select('section'):
            if s not in sec_nodes:
                sec_nodes.append(s)
        for sec in sec_nodes:
            sid = sec.get('id', '')
            # 섹션 트리 내의 인라인 예제 블록을 처리
            m_in = re.match(r'^sampleinput(\d+)$', sid)
            m_out = re.match(r'^sampleoutput(\d+)$', sid)
            if m_in:
                n = int(m_in.group(1))
                if n not in handled_samples:
                    in_txt = sample_inputs.get(n, '')
                    out_txt = sample_outputs.get(n, '')
                    content_md = ''
                    if in_txt or out_txt:
                        block = []
                        block.append(f"### 예제 입력 {n}\n")
                        block.append("```\n" + (in_txt or '') + "\n```\n")
                        block.append(f"### 예제 출력 {n}\n")
                        block.append("```\n" + (out_txt or '') + "\n```\n")
                        content_md = "\n".join(block)
                    if content_md:
                        sections.append({'id': f'sample-{n}', 'title': '예제', 'content': content_md.rstrip()})
                        handled_samples.add(n)
                continue
            if m_out:
                n = int(m_out.group(1))
                if n in handled_samples:
                    continue
            # 메모/에디터 UI 및 display:none 섹션은 제외
            if sec.select_one('#problem-memo-view, #memo-content, .editor-toolbar'):
                continue
            style = (sec.get('style') or '').lower()
            if 'display:none' in style:
                continue
            h2 = sec.select_one('.headline h2')
            title_txt = h2.get_text(strip=True) if h2 else (sid or '섹션')
            content_md = self._section_to_markdown(sec).rstrip()
            key = (sid, title_txt, hash(content_md))
            if not content_md or key in seen:
                continue
            seen.add(key)
            sections.append({'id': sid, 'title': title_txt, 'content': content_md})
        return sections

    def _fetch_tags_and_level(self, pid: int) -> tuple[list[str], int]:
        tags: list[str] = []
        level = 0
        try:
            data = self._request(
                SOLVEDAC_URL.format(pid=pid),
                {
                    "User-Agent": "ps-boj-helper/1.1 (+https://github.com/rhseung/ps)",
                    "Accept": "application/json",
                },
            )
            obj = json.loads(data)
            # level
            try:
                level = int(obj.get("level", 0))
            except Exception:
                level = 0
            # tags: prefer Korean displayNames
            try:
                tag_objs = obj.get("tags") or []
                for t in tag_objs:
                    dn = t.get("displayNames") or []
                    # find Korean name first
                    ko = next((d.get("name") for d in dn if (d.get("language") == "ko" and d.get("name"))), None)
                    if ko:
                        tags.append(ko)
                        continue
                    # fallback to any non-empty display name
                    any_name = next((d.get("name") for d in dn if d.get("name")), None)
                    if any_name:
                        tags.append(any_name)
            except Exception:
                pass
        except Exception:
            pass
        # de-duplicate while preserving order
        seen = set()
        tags = [x for x in tags if not (x in seen or seen.add(x))]
        return tags, level

    def fetch_full_details(self, pid: int) -> dict:
        """BOJ 문제 페이지를 크롤링하여 구조화된 dict로 반환합니다.
        필드가 없을 경우 빈 문자열을 반환하며, 다양한 DOM 변형에도 최대한 견고하게 동작합니다."""
        html_text = self._download_problem_html(pid)
        soup = BeautifulSoup(html_text, 'html.parser') if BeautifulSoup else None
        title = self._parse_title(soup, html_text)
        tier_image = self._parse_tier_image(soup)
        time_limit, memory_limit, submissions, accepted, solved, ratio = self._parse_info_table(soup, html_text)
        sections = self._collect_sections(soup, html_text)
        tags, level = self._fetch_tags_and_level(pid)
        if not tier_image and level:
            tier_image = f"https://static.solved.ac/tier_small/{level}.svg"
        # samples kept for Runner/save; may be re-fetched by caller
        try:
            samples = self.fetch_samples(pid)
        except Exception:
            samples = []
        return {
            "title": title,
            "tier_image": tier_image,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "submissions": submissions,
            "accepted": accepted,
            "solved": solved,
            "ratio": ratio,
            "samples": samples,
            "tags": tags,
            "sections": sections,
        }

    def to_markdown(self, pid: int, details: dict) -> str:
        def esc(s: str) -> str:
            return s if s is not None else ""

        title = esc(details.get("title", "")).strip() or f"BOJ {pid}"
        tier_md = f'<img src="{details["tier_image"]}" width="20px" />' if details.get("tier_image") else ""
        md = []
        md.append(f"# {pid}. [{title}](https://www.acmicpc.net/problem/{pid})")
        md.append("")
        md.append("| 티어 | 시간 제한 | 메모리 제한 | 제출 | 정답 | 맞힌 사람 | 정답 비율 |\n|---|---|---|---:|---:|---:|---:|")
        md.append(
            f"| {tier_md} | {esc(details.get('time_limit', ''))} | {esc(details.get('memory_limit', ''))} | {esc(details.get('submissions', ''))} | {esc(details.get('accepted', ''))} | {esc(details.get('solved', ''))} | {esc(details.get('ratio', ''))} |")
        md.append("\n---\n")
        # Render sections: generic when available
        if details.get('sections'):
            for sec in details['sections']:
                title_txt = sec.get('title') or '섹션'
                content_md = sec.get('content') or ''
                md.append(f"## {title_txt}\n")
                md.append(content_md.rstrip() + "\n")
        else:
            # Legacy fallback (older cached results)
            if details.get('description'):
                md.append("## 문제\n")
                md.append(esc(details['description']).rstrip() + "\n")
            if details.get('input'):
                md.append("## 입력\n")
                md.append(esc(details['input']).rstrip() + "\n")
            if details.get('output'):
                md.append("## 출력\n")
                md.append(esc(details['output']).rstrip() + "\n")
            if details.get('notes'):
                md.append("## 노트\n")
                md.append(esc(details['notes']).rstrip() + "\n")
        # If crawling didn't include a tag section, but solved.ac provided tags, append them here
        has_tag_section = False
        for sec in details.get('sections') or []:
            sid = (sec.get('id') or '').lower()
            title_txt = (sec.get('title') or '')
            if sid.startswith('problem_tags') or '알고리즘 분류' in title_txt:
                has_tag_section = True
                break
        solvedac_tags = [t for t in details.get('tags') or [] if isinstance(t, str) and t.strip()]
        if (not has_tag_section) and solvedac_tags:
            md.append("## 알고리즘 분류\n")
            for t in solvedac_tags:
                md.append(f"- {t.strip()}")
            md.append("")
        # (Samples are now inlined as sections with title '예제', so do not render separately)
        # Tags: no special handling; rely on crawled sections (e.g., <section id="problem_tags">)
        return "\n".join(md)

    def __init__(self, cafile: Optional[str] = _CAFILE):
        self.cafile = cafile
        self.debug = bool(os.getenv("BOJ_DEBUG"))

    def _ctx(self):
        return ssl.create_default_context(cafile=self.cafile) if self.cafile else ssl.create_default_context()

    def _request(self, url: str, headers: dict) -> str:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=8, context=self._ctx()) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    def fetch(self, pid: int) -> Optional[str]:
        # 1) Try solved.ac
        try:
            data = self._request(
                SOLVEDAC_URL.format(pid=pid),
                {
                    "User-Agent": "ps-boj-helper/1.1 (+https://github.com/rhseung/ps)",
                    "Accept": "application/json",
                },
            )
            obj = json.loads(data)
            title = obj.get("titleKo") or obj.get("titleEn") or obj.get("title")
            if isinstance(title, str) and title.strip():
                return title.strip()
        except HTTPError as e:
            print(f"{L.WARN} solved.ac HTTP {e.code}: {e.reason}")
        except URLError as e:
            print(f"{L.WARN} solved.ac URL error: {e.reason}")
        except ssl.SSLError as e:
            print(f"{L.WARN} SSL error when calling solved.ac: {e}")
            print(f"{L.HINT} Using fallback crawler for title…")
        except Exception as e:
            print(f"{L.WARN} solved.ac parse error: {e}")

        # 2) Fallback: crawl acmicpc.net/problem/{pid}
        try:
            html_text = self._request(
                f"https://www.acmicpc.net/problem/{pid}",
                {
                    "User-Agent": "ps-boj-helper/1.1 (+https://github.com/rhseung/ps)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            m = re.search(r'id="problem_title"\s*>\s*(.*?)\s*<', html_text, re.IGNORECASE | re.DOTALL)
            if not m:
                mt = re.search(r"<title>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
                if mt:
                    title_tag = html.unescape(mt.group(1)).strip()
                    parts = re.split(r"[:\-]\s*", title_tag, maxsplit=1)
                    guess = parts[-1].strip() if parts else title_tag
                    return guess
            else:
                title = html.unescape(m.group(1)).strip()
                if title:
                    return title
        except Exception as e:
            print(f"{L.WARN} crawl failed: {e}")

        return None

    def fetch_samples(self, pid: int) -> list[tuple[str, str]]:

        def _log(msg: str) -> None:
            if getattr(self, "debug", False):
                print(f"[fetch_samples:{pid}] {msg}")

        try:
            _log("requesting problem page…")
            html_text = self._request(
                f"https://www.acmicpc.net/problem/{pid}",
                {
                    "User-Agent": "ps-boj-helper/1.1 (+https://github.com/rhseung/ps)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                },
            )
            _log(f"downloaded html: {len(html_text)} bytes")
        except HTTPError as e:
            if e.code == 403:
                _log("got 403 Forbidden. retrying with browser-like headers…")
                try:
                    html_text = self._request(
                        f"https://www.acmicpc.net/problem/{pid}",
                        {
                            # macOS Chrome UA (generic)
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
                            "Referer": "https://www.acmicpc.net/",
                            "Pragma": "no-cache",
                            "Cache-Control": "no-cache",
                            "Connection": "keep-alive",
                        },
                    )
                    _log(f"downloaded html (retry): {len(html_text)} bytes")
                except Exception as er:
                    if getattr(self, "debug", False):
                        print(f"[fetch_samples:{pid}] retry failed after 403: {er}")
                    return []
            else:
                if getattr(self, "debug", False):
                    print(f"[fetch_samples:{pid}] HTTP error: {e}")
                return []
        except Exception as e:
            if getattr(self, "debug", False):
                print(f"[fetch_samples:{pid}] request failed: {e}")
            return []

        soup = BeautifulSoup(html_text, 'html.parser') if BeautifulSoup else None

        def _clean_pre(fragment: str) -> str:
            # 시각화용 공백 마커(span.space-highlight)를 실제 공백으로 교체
            frag = re.sub(r'<span[^>]*class=\"space-highlight\"[^>]*>\s*</span>', ' ', fragment, flags=re.IGNORECASE)
            # <br>을 줄바꿈으로 치환
            frag = re.sub(r'<br\s*/?>', '\n', frag, flags=re.IGNORECASE)
            # 남은 태그 제거(텍스트만 유지)
            frag = re.sub(r'<[^>]+>', '', frag)
            # HTML 엔티티 해제
            frag = html.unescape(frag)
            # 개행 정규화; 내용은 유지하고 마지막 개행만 제거
            frag = frag.replace('\r\n', '\n').replace('\r', '\n')
            return frag.strip('\n')

        def _preview(s: str, n: int = 80) -> str:
            s = s.replace('\n', '\\n')
            return s[:n] + ('…' if len(s) > n else '')

        # 입력/출력 맵을 쌍 리스트로 병합하는 유틸
        def _pairs_from_maps(inp_map: dict[int, str], out_map: dict[int, str]) -> list[tuple[str, str]]:
            out: list[tuple[str, str]] = []
            for k in sorted(set(inp_map) & set(out_map)):
                out.append((inp_map[k], out_map[k]))
            return out

        inputs: dict[int, str] = {}
        outputs: dict[int, str] = {}
        if soup:
            for pre in soup.select('pre[id^="sample-input-"]'):
                try:
                    n = int((pre.get('id') or '').split('-')[-1])
                except Exception:
                    continue
                inputs[n] = _clean_pre(str(pre))
            for pre in soup.select('pre[id^="sample-output-"]'):
                try:
                    n = int((pre.get('id') or '').split('-')[-1])
                except Exception:
                    continue
                outputs[n] = _clean_pre(str(pre))
        else:
            for m in re.finditer(r'<pre[^>]*id\s*=\s*[\"\']sample-input-(\d+)[\"\'][^>]*>(.*?)</pre>', html_text,
                                 re.DOTALL | re.IGNORECASE):
                inputs[int(m.group(1))] = _clean_pre(m.group(2))
            for m in re.finditer(r'<pre[^>]*id\s*=\s*[\"\']sample-output-(\d+)[\"\'][^>]*>(.*?)</pre>', html_text,
                                 re.DOTALL | re.IGNORECASE):
                outputs[int(m.group(1))] = _clean_pre(m.group(2))
        _log(f"primary <pre> ids: inputs={len(inputs)}, outputs={len(outputs)}")  # 기본 <pre> 아이디
        pairs = _pairs_from_maps(inputs, outputs)
        if not pairs and getattr(self, "debug", False):
            # 디버그: sample-* 부근 HTML 일부를 덤프
            mm = re.search(r'sample-(?:input|output)-', html_text)
            if mm:
                s = max(0, mm.start() - 200)
                e = min(len(html_text), mm.end() + 240)
                print(f"[fetch_samples:{pid}] debug snippet (around sample-):\n" + html_text[s:e])
        if pairs:
            _log(f"기본 <pre> 매칭 완료: {len(pairs)} pair(s)")
            for i, (a, b) in enumerate(pairs, 1):
                _log(f"  sample #{i} in: '{_preview(a)}' | out: '{_preview(b)}'")
            return pairs
        inputs.clear()
        outputs.clear()
        if soup:
            for sec in soup.select('section[id^="sampleinput"]'):
                try:
                    n = int((sec.get('id') or '')[len('sampleinput'):])
                except Exception:
                    continue
                pre = sec.select_one('pre.sampledata') or sec.find('pre')
                if pre:
                    inputs[n] = _clean_pre(str(pre))
            for sec in soup.select('section[id^="sampleoutput"]'):
                try:
                    n = int((sec.get('id') or '')[len('sampleoutput'):])
                except Exception:
                    continue
                pre = sec.select_one('pre.sampledata') or sec.find('pre')
                if pre:
                    outputs[n] = _clean_pre(str(pre))
        else:
            for m in re.finditer(
                    r'<section[^>]*id\s*=\s*[\"\']sampleinput(\d+)[\"\'][^>]*>.*?<pre[^>]*class\s*=\s*[\"\'][^\"\']*\bsampledata\b[^\"\']*[\"\'][^>]*>(.*?)</pre>',
                    html_text, re.DOTALL | re.IGNORECASE):
                inputs[int(m.group(1))] = _clean_pre(m.group(2))
            for m in re.finditer(
                    r'<section[^>]*id\s*=\s*[\"\']sampleoutput(\d+)[\"\'][^>]*>.*?<pre[^>]*class\s*=\s*[\"\'][^\"\']*\bsampledata\b[^\"\']*[\"\'][^>]*>(.*?)</pre>',
                    html_text, re.DOTALL | re.IGNORECASE):
                outputs[int(m.group(1))] = _clean_pre(m.group(2))
        _log(f"레거시 섹션 패턴: inputs={len(inputs)}, outputs={len(outputs)}")
        pairs = _pairs_from_maps(inputs, outputs)
        if pairs:
            _log(f"레거시 섹션 매칭 완료: {len(pairs)} pair(s)")
            for i, (a, b) in enumerate(pairs, 1):
                _log(f"  sample #{i} in: '{_preview(a)}' | out: '{_preview(b)}'")
            return pairs
        blocks: list[tuple[str, int, str]] = []
        if soup:
            for h in soup.select('h1, h2, h3, h4, h5, h6'):
                txt = (h.get_text(" ", strip=True) or "").lower()
                m = re.search(r'(입력|input|출력|output)\s*(\d+)', txt)
                if not m:
                    continue
                kind_ko = m.group(1)
                idx = int(m.group(2))
                pre = h.find_next('pre')
                if not pre:
                    continue
                text = _clean_pre(str(pre))
                kind = 'input' if ('입력' in kind_ko or 'input' in kind_ko) else 'output'
                blocks.append((kind, idx, text))
        else:
            for m in re.finditer(r'<h[1-6][^>]*>\s*([^<]*?)\s*(\d+)\s*</h[1-6]>\s*<pre[^>]*>(.*?)</pre>', html_text,
                                 re.DOTALL | re.IGNORECASE):
                label_raw = html.unescape(m.group(1)).strip().lower()
                idx = int(m.group(2))
                txt = _clean_pre(m.group(3))
                if '입력' in label_raw or 'input' in label_raw:
                    blocks.append(('input', idx, txt))
                elif '출력' in label_raw or 'output' in label_raw:
                    blocks.append(('output', idx, txt))
        _log(f"폴백: 헤딩 기반 블록 수집: {len(blocks)}")
        if blocks:
            in_map: dict[int, str] = {}
            out_map: dict[int, str] = {}
            for kind, idx, txt in blocks:
                (in_map if kind == 'input' else out_map)[idx] = txt
            pairs = _pairs_from_maps(in_map, out_map)
            if pairs:
                _log(f"헤딩 폴백 매칭 완료: {len(pairs)} pair(s)")
                for i, (a, b) in enumerate(pairs, 1):
                    _log(f"  sample #{i} in: '{_preview(a)}' | out: '{_preview(b)}'")
                return pairs
        _log("모든 전략 실패: 샘플 쌍을 찾지 못함")
        return []


# ================================ CMake 편집기 ================================
class CMakePS:
    _PS_CALL_RE = re.compile(r"add_executable\s*\(\s*ps\b", re.IGNORECASE)

    def __init__(self, cmakelists: Path):
        self.path = cmakelists

    def _find_ps_block(self, text: str) -> tuple[int, int, str]:
        # add_executable(ps ...) 블록의 위치와 들여쓰기를 찾음
        m = self._PS_CALL_RE.search(text)
        if not m:
            raise SystemExit("add_executable(ps ...) not found in CMakeLists.txt")
        start = m.start()
        open_paren = text.find("(", m.start())
        if open_paren == -1:
            raise SystemExit("Malformed add_executable(ps ...): '(' not found")
        depth = 0
        i = open_paren
        while i < len(text):
            ch = text[i]
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    line_start = text.rfind('\n', 0, start) + 1
                    indent = text[line_start:start]
                    return start, end, indent
            i += 1
        raise SystemExit("Malformed add_executable(ps ...): closing ')' not found")

    @staticmethod
    def _parse_sources(inside: str) -> List[str]:
        # add_executable 블록 내부에서 소스 파일 목록을 파싱
        tokens = re.findall(r'"[^"\n]+"|[^\s\n]+', inside)
        if not tokens:
            return []
        if tokens[0].strip('"') != 'ps':
            try:
                idx = [t.strip('"') for t in tokens].index('ps')
                tokens = tokens[idx + 1:]
            except ValueError:
                pass
        else:
            tokens = tokens[1:]
        out: List[str] = []
        for t in tokens:
            t = t.strip()
            if t.endswith(')'):
                t = t[:-1]
            if t.startswith('"') and t.endswith('"'):
                t = t[1:-1]
            if t:
                out.append(t)
        return out

    @staticmethod
    def _rebuild(indent: str, sources: Iterable[str]) -> str:
        # add_executable 블록을 다시 만듦
        inner_indent = indent + "    "
        body = "\n".join(f"{inner_indent}\"{src}\"" for src in sources)
        return f"{indent}add_executable(ps\n{body}\n{indent})"

    def add(self, rel_src: str) -> None:
        text = self.path.read_text(encoding="utf-8")
        start, end, indent = self._find_ps_block(text)
        inside = text[start:end]
        open_idx = inside.find('(')
        close_idx = inside.rfind(')')
        content = inside[open_idx + 1: close_idx]

        sources = self._parse_sources(content)
        if rel_src not in sources:
            sources.append(rel_src)
        new_block = self._rebuild(indent, sources)
        new_text = text[:start] + new_block + text[end:]
        self.path.write_text(new_text, encoding="utf-8")

    def remove(self, rel_src: str) -> None:
        text = self.path.read_text(encoding="utf-8")
        start, end, indent = self._find_ps_block(text)
        inside = text[start:end]
        open_idx = inside.find('(')
        close_idx = inside.rfind(')')
        content = inside[open_idx + 1: close_idx]

        sources = self._parse_sources(content)
        new_sources = [s for s in sources if s != rel_src]
        new_block = self._rebuild(indent, new_sources)
        new_text = text[:start] + new_block + text[end:]
        self.path.write_text(new_text, encoding="utf-8")


# ================================== Git =======================================
class Git:
    def __init__(self, cwd: Path):
        self.cwd = cwd

    def run(self, *args: str) -> None:
        # 지정된 인자와 함께 git 명령어를 실행
        subprocess.check_call(["git", *args], cwd=self.cwd)


class Runner:
    def __init__(self, repo: RepoPaths, cfg: Config):
        self.repo = repo
        self.cfg = cfg

    def _guess_build_dir(self) -> Path:
        # 우선순위: ./build, 그 다음 cmake 빌드 디렉터리들
        candidates = [self.repo.root / "build"]
        candidates += sorted(self.repo.root.glob("cmake-build-*"))
        for c in candidates:
            if c.exists():
                return c
        return self.repo.root / "build"

    def resolve_bin(self) -> Path:
        # ps 바이너리(실행 파일) 경로를 추정
        build_dir = self._guess_build_dir()
        exe = "ps.exe" if os.name == "nt" else "ps"

        # 설정은 디렉터리 또는 전체 경로일 수 있음; ${CMAKE_BINARY_DIR}를 실제 경로로 치환
        run_dir_cfg = self.cfg.get("run_dir", "${CMAKE_BINARY_DIR}/bin")
        run_dir_resolved = run_dir_cfg.replace("${CMAKE_BINARY_DIR}", str(build_dir))

        candidates: list[Path] = []
        p_cfg = Path(run_dir_resolved)
        if p_cfg.suffix == "" and p_cfg.name != exe:
            # 디렉터리로 보이면 그 하위에 실행 파일을 붙임
            candidates.append(p_cfg / exe)
        else:
            # 이미 파일 경로로 보임
            candidates.append(p_cfg)

        # CMake의 일반적인 출력 경로들 추가
        candidates.append(build_dir / exe)  # 예: cmake-build-debug/ps
        candidates.append(build_dir / "bin" / exe)  # 예: build/bin/ps
        for sub in ("Debug", "Release", "RelWithDebInfo", "MinSizeRel"):
            candidates.append(build_dir / sub / exe)

        # 존재하는 첫 번째 경로 반환
        for c in candidates:
            if c.exists():
                return c

        # 없으면 첫 번째 후보 반환(오류 메시지용)
        return candidates[0]

    def run_cases(self, bin_path: Path, cases: list[tuple[str, str]]) -> list[dict]:
        # 바이너리에 대해 각 샘플 케이스를 실행
        results = []
        for i, (inp, expected) in enumerate(cases, 1):
            start = subprocess.time.time() if hasattr(subprocess, 'time') else __import__('time').time()
            proc = subprocess.run([str(bin_path)], input=inp, text=True, capture_output=True)
            dur_ms = int(((__import__('time').time() - start) * 1000))
            out = proc.stdout.rstrip("\n")
            exp = expected.rstrip("\n")
            ok = (proc.returncode == 0) and (out == exp)
            results.append({
                "idx": i,
                "ok": ok,
                "exit": proc.returncode,
                "ms": dur_ms,
                "expected": exp,
                "actual": out,
                "stderr": proc.stderr,
            })
        return results


# ================================== 코어 =====================================
class BOJHelper:
    def submit(self, pid: int, lang: Optional[str], file_path: Optional[str], open_code: bool) -> None:
        prefer = (lang or self.config.get("lang", "py")).lower()
        subm = ProblemSubmitter(self.config)
        res = subm.submit(pid, self.paths, prefer, open_code, file_path)
        # pretty box summary
        title = f" Submit BOJ {pid} "
        bar = Box.TL + Box.H * (len(title) + 2) + Box.TR
        print(Ansi.wrap(bar, Ansi.BOLD))
        print(Ansi.wrap(Box.V + " " + title + " " + Box.V, Ansi.BOLD, Ansi.MAGENTA))
        print(Ansi.wrap(Box.L + Box.H * (len(title) + 2) + Box.R, Ansi.DIM))
        kv = [
            ("Language Pref", prefer),
            ("Lang ID", res.get("lang_id", "?")),
            ("Source", res.get("source_path", "")),
            ("Visibility", "open" if open_code else "close"),
        ]
        for k, v in kv:
            line = f"  {k:12}: {v}"
            print(Box.V + line + Box.V)
        print(Ansi.wrap(Box.BL + Box.H * (len(title) + 2) + Box.BR, Ansi.DIM))
        if res.get("ok"):
            print(f"  {L.OK} submission request sent. Check status page for verdict.")
            print(Ansi.wrap("  Hint: https://www.acmicpc.net/status?user_id=<YOUR_ID>&problem_id=" + str(pid), Ansi.DIM))
        else:
            print(f"  {L.WARN} submission may not have been accepted. Re-check cookie or try again.")

    def markdown(self, pid: int, out_path: Optional[str]) -> Path:
        details = self.fetcher.fetch_full_details(pid)
        if not details.get("samples"):
            try:
                details["samples"] = self.fetcher.fetch_samples(pid)
            except Exception:
                details["samples"] = []
        md = self.fetcher.to_markdown(pid, details)
        # resolve output
        if out_path:
            outp = (self.paths.root / out_path).resolve()
        else:
            outp = (self.paths.root / "docs" / "boj" / f"{pid}.md").resolve()
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(md + "\n", encoding="utf-8")
        print(f"{L.OK} markdown written: {outp.relative_to(self.paths.root)}")
        return outp

    def __init__(self, paths: RepoPaths):
        self.paths = paths
        self.config = Config(paths)
        self.fetcher = ProblemFetcher()
        self.cmake = CMakePS(paths.cmakelists)
        self.git = Git(paths.root)
        self.runner = Runner(paths, self.config)

    def _lang_template(self, lang: str) -> str:
        return CPP_TEMPLATE if lang == "cpp" else PY_TEMPLATE

    def _rel(self, p: Path) -> str:
        return str(p.relative_to(self.paths.root)).replace(os.sep, "/")

    # ----------------------------- start command -----------------------------
    def start(self, pid: int, name: Optional[str], lang: Optional[str]) -> None:
        lang = (lang or self.config.get("lang", "py")).lower()

        # Resolve title if not provided
        if not name:
            fetched = self.fetcher.fetch(pid)
            if fetched:
                name = fetched
                print(f"{L.OK} fetched title: {name}")
            else:
                name = f"BOJ {pid}"
                print(f"{L.WARN} could not fetch title; using placeholder")

        # Create per-problem directory under solving/: "<pid> - <name>/"
        dir_name = f"{pid} - {sanitize_filename(name)}"
        prob_dir = self.paths.solving / dir_name
        prob_dir.mkdir(parents=True, exist_ok=True)

        # Create source file inside the directory
        src_fname = f"{dir_name}.{lang}"
        src_path = prob_dir / src_fname
        if not src_path.exists():
            src_path.write_text(self._lang_template(lang).format(id=pid, name=name), encoding="utf-8")
            print(f"{L.OK} created: {src_path.relative_to(self.paths.root)}")
        else:
            print(f"{L.SKIP} exists: {src_path.relative_to(self.paths.root)}")

        # Generate Markdown inside the same directory as README.md
        try:
            details = self.fetcher.fetch_full_details(pid)
            if not details.get("samples"):
                try:
                    details["samples"] = self.fetcher.fetch_samples(pid)
                except Exception:
                    details["samples"] = []
            md_text = self.fetcher.to_markdown(pid, details)
            md_path = prob_dir / "README.md"
            md_path.write_text(md_text + "\n", encoding="utf-8")
            print(f"{L.OK} markdown written: {md_path.relative_to(self.paths.root)}")
        except Exception as e:
            print(f"{L.WARN} failed to write markdown: {e}")

        # Add C++ source into CMake target if cpp
        rel_src = self._rel(src_path)
        if lang == "cpp":
            self.cmake.add(rel_src)
            print(f"{L.OK} added to ps target: {rel_src}")
        else:
            print(f"{L.HINT} python source created; not added to CMake target: {rel_src}")

        # Change current working directory to the new problem directory
        try:
            os.chdir(prob_dir)
            print(f"{L.HINT} Changed working directory to: {prob_dir}")
        except Exception as e:
            print(f"{L.WARN} Failed to change working directory: {e}")

    # ---------------------------- finish command -----------------------------
    def finish(self, pid: int, name: Optional[str], lang: Optional[str], push: bool, no_git: bool) -> None:
        lang = (lang or self.config.get("lang", "py")).lower()

        # Locate per-problem directory under solving/
        prob_dir: Optional[Path] = None
        if name:
            candidate = self.paths.solving / f"{pid} - {sanitize_filename(name)}"
            if candidate.exists() and candidate.is_dir():
                prob_dir = candidate
        if prob_dir is None:
            cand = sorted(self.paths.solving.glob(f"{pid} -*"))
            if cand:
                prob_dir = next((p for p in cand if p.is_dir()), None)

        if prob_dir is None:
            # Fallback: try to infer from a source file (legacy layout)
            if not name:
                name = self.fetcher.fetch(pid) or f"BOJ {pid}"
            legacy_src = self.paths.solving / f"{pid} - {sanitize_filename(name)}.{lang}"
            if legacy_src.exists():
                # Promote legacy file into a dir for consistency
                prob_dir = self.paths.solving / f"{pid} - {sanitize_filename(name)}"
                prob_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(legacy_src), str(prob_dir / legacy_src.name))
                print(f"{L.HINT} migrated legacy file into directory: {prob_dir.relative_to(self.paths.root)}")

        if prob_dir is None:
            raise SystemExit(f"Problem directory not found for id={pid}. Try providing a name or ensure it exists under solving/")

        # Determine the primary source file path for CMake removal (cpp only)
        src_path = None
        if lang == "cpp":
            # pick the first .cpp in the directory whose basename contains "<pid} -"
            cpp_list = sorted(prob_dir.glob("*.cpp"))
            if cpp_list:
                # Prefer file named "<pid> - <name>.cpp"
                prefer = f"{pid} - "
                src_path = next((p for p in cpp_list if p.name.startswith(prefer)), cpp_list[0])

        # Remove from CMake if needed
        if lang == "cpp" and src_path is not None:
            rel_src = self._rel(src_path)
            self.cmake.remove(rel_src)
            print(f"{L.OK} removed from ps target: {rel_src}")
        elif lang == "cpp":
            print(f"{L.WARN} no .cpp found under: {prob_dir.relative_to(self.paths.root)}")

        # Move the entire problem directory into the thousand-range folder
        dst_dir = self.paths.root / thousand_folder(pid)
        dst_dir.mkdir(exist_ok=True)
        dst = dst_dir / prob_dir.name
        if dst.exists():
            # If target exists, move contents over (simple merge)
            for item in prob_dir.iterdir():
                shutil.move(str(item), str(dst / item.name))
            shutil.rmtree(prob_dir)
        else:
            shutil.move(str(prob_dir), str(dst))
        print(f"{L.OK} moved to: {dst.relative_to(self.paths.root)}")

        if not no_git:
            self.git.run("add", "-A")
            msg = f"solve: {pid} - {name or prob_dir.name.split(' - ', 1)[-1]}"
            self.git.run("commit", "-m", msg)
            print(f"{L.OK} committed: {msg}")
            if push:
                self.git.run("push")
                print(f"{L.OK} pushed")

    # ---------------------------- delete command -----------------------------
    def delete(self, pid: int, name: Optional[str], lang: Optional[str]) -> None:
        lang = (lang or self.config.get("lang", "py")).lower()

        # Try to locate the problem directory (prefer solving/)
        prob_dir: Optional[Path] = None
        if name:
            candidate = self.paths.solving / f"{pid} - {sanitize_filename(name)}"
            if candidate.exists() and candidate.is_dir():
                prob_dir = candidate
        if prob_dir is None:
            cand_solving = sorted(self.paths.solving.glob(f"{pid} -*"))
            prob_dir = next((p for p in cand_solving if p.is_dir()), None)
        if prob_dir is None:
            # As a fallback, search repo (shallow) for any match directory
            cand_any = sorted(self.paths.root.glob(f"**/{pid} -*"))
            prob_dir = next((p for p in cand_any if p.is_dir()), None)
        if prob_dir is None:
            raise SystemExit(f"Problem directory not found for id={pid}. Try providing a name or --lang.")

        # If C++: remove file from CMake target
        if lang == "cpp":
            cpp_list = sorted(prob_dir.glob("*.cpp"))
            if cpp_list:
                prefer = f"{pid} - "
                src_path = next((p for p in cpp_list if p.name.startswith(prefer)), cpp_list[0])
                rel_src = self._rel(src_path)
                self.cmake.remove(rel_src)
                print(f"{L.OK} removed from ps target: {rel_src}")
            else:
                print(f"{L.HINT} no .cpp under: {prob_dir.relative_to(self.paths.root)} (nothing to remove)")

        print(f"{L.HINT} kept code and files under: {prob_dir.relative_to(self.paths.root)}")

    def run_cases_argv(self, argv: List[str], cases: list[tuple[str, str]]) -> list[dict]:
        results = []
        for i, (inp, expected) in enumerate(cases, 1):
            start = __import__('time').time()
            proc = subprocess.run(argv, input=inp, text=True, capture_output=True)
            dur_ms = int(((__import__('time').time() - start) * 1000))
            out = proc.stdout.rstrip("\n")
            exp = expected.rstrip("\n")
            ok = (proc.returncode == 0) and (out == exp)
            results.append({
                "idx": i,
                "ok": ok,
                "exit": proc.returncode,
                "ms": dur_ms,
                "expected": exp,
                "actual": out,
                "stderr": proc.stderr,
            })
        return results

    def run(self, pid: int, bin_override: Optional[str]) -> None:
        samples = self.fetcher.fetch_samples(pid)
        print(f"{L.TITLE} Running samples for BOJ {pid}")
        if not samples:
            print(f"{L.WARN} No samples found on problem page.")
            return

        # 파이썬 풀이 우선 자동 탐지
        py_src = None
        # 신규 레이아웃: "<pid> - */*.py"
        cand_solving = list(self.paths.solving.glob(f"{pid} -*/**/*.py")) + list(self.paths.solving.glob(f"{pid} -*/*.py"))
        if cand_solving:
            py_src = cand_solving[0]
        else:
            # 레거시 단일 파일/천 단위 폴더도 지원
            legacy_flat = list(self.paths.solving.glob(f"{pid} -*.py"))
            if legacy_flat:
                py_src = legacy_flat[0]
            else:
                py_glob = list(self.paths.root.glob(f"**/{pid} -*/**/*.py")) + list(self.paths.root.glob(f"**/{pid} -*/*.py")) + list(
                    self.paths.root.glob(f"**/{pid} -*.py"))
                if py_glob:
                    py_src = py_glob[0]

        if py_src is not None:
            # 파이썬 인터프리터로 실행
            import sys as _sys
            argv = [_sys.executable, str(py_src)]
            results = self.run_cases_argv(argv, samples)
            bin_display = py_src.name
        else:
            # 컴파일된 C++ 바이너리로 폴백
            bin_path = Path(bin_override) if bin_override else self.runner.resolve_bin()
            if not bin_path.exists():
                # 후보 목록을 다시 계산해 힌트를 제공
                build_dir = self.runner._guess_build_dir()
                exe = "ps.exe" if os.name == "nt" else "ps"
                run_dir_cfg = self.config.get("run_dir", "${CMAKE_BINARY_DIR}/bin")
                run_dir_resolved = run_dir_cfg.replace("${CMAKE_BINARY_DIR}", str(build_dir))
                p_cfg = Path(run_dir_resolved)
                candidates = []
                candidates.append(p_cfg / exe if (p_cfg.suffix == "" and p_cfg.name != exe) else p_cfg)
                candidates += [
                    build_dir / exe,
                    build_dir / "bin" / exe,
                    build_dir / "Debug" / exe,
                    build_dir / "Release" / exe,
                    build_dir / "RelWithDebInfo" / exe,
                    build_dir / "MinSizeRel" / exe,
                ]
                pretty = "\n  - " + "\n  - ".join(str(c) for c in candidates)
                print(
                    f"{L.ERROR} Binary not found: {bin_path}\n{L.HINT} Tried: {pretty}\n{L.HINT} Build your project or override with --bin <path>.")
                return
            results = self.runner.run_cases(bin_path, samples)
            bin_display = bin_path.name
        # 샘플을 각 문제 디렉터리의 tests/로 저장
        prob_dir = None
        cand = sorted(self.paths.solving.glob(f"{pid} -*"))
        if cand:
            prob_dir = next((p for p in cand if p.is_dir()), None)
        if not prob_dir:
            cand_any = sorted(self.paths.root.glob(f"**/{pid} -*"))
            prob_dir = next((p for p in cand_any if p.is_dir()), None)
        if prob_dir:
            base = prob_dir / "tests"
        else:
            base = self.paths.root / "tests" / "boj" / str(pid)
        base.mkdir(parents=True, exist_ok=True)
        for i, (inp, out) in enumerate(samples, 1):
            (base / f"sample-{i}.in").write_text(inp + "\n", encoding="utf-8")
            (base / f"sample-{i}.out").write_text(out + "\n", encoding="utf-8")

        # 단순 텍스트 출력(박스 없음)
        ok_sym = "✓"
        fail_sym = "✗"
        pass_cnt = 0
        for r in results:
            status = Ansi.wrap(f"{ok_sym} OK", Ansi.BOLD, Ansi.GREEN) if r["ok"] else Ansi.wrap(f"{fail_sym} FAIL", Ansi.BOLD, Ansi.RED)
            exit_col = Ansi.wrap(str(r['exit']), Ansi.DIM)
            time_col = Ansi.wrap(f"{r['ms']}ms", Ansi.DIM)
            print(f"  {r['idx']:>2}. {status}   exit={exit_col}   time={time_col}")
            if not r["ok"]:
                # Detail blocks
                branch_mid = "    ├─ "
                branch_end = "    └─ "
                pipe = "    │  "

                # expected
                print(Ansi.wrap(branch_mid + "expected:", Ansi.BOLD, Ansi.YELLOW))
                exp_lines = r["expected"].splitlines() or [""]
                for line in exp_lines:
                    print(pipe + line)

                # actual
                print(Ansi.wrap(branch_mid + "actual:", Ansi.BOLD, Ansi.CYAN))
                act_lines = r["actual"].splitlines() or [""]
                for line in act_lines:
                    print(pipe + line)

                # stderr (optional)
                if r["stderr"].strip():
                    print(Ansi.wrap(branch_end + "stderr:", Ansi.BOLD, Ansi.MAGENTA))
                    for line in r["stderr"].splitlines():
                        print(pipe + line)
            else:
                pass_cnt += 1

        # 요약 라인
        total = len(results)
        summ = f"Passed {pass_cnt}/{total}  |  Binary: {bin_display}"
        print(Ansi.wrap(summ, Ansi.BOLD))

        # ==================================== CLI ====================================


class CLI:
    def __init__(self, helper: BOJHelper):
        self.h = helper

    def _build_parser(self) -> argparse.ArgumentParser:
        ap = argparse.ArgumentParser(
            prog="boj",
            description="Baekjoon workflow helper",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        sub = ap.add_subparsers(dest="cmd", required=True, metavar="command")

        # start
        sp = sub.add_parser("start", aliases=["s", "st"], help="create file + add into ps target")
        sp.set_defaults(cmd="start")
        sp.add_argument("id", type=int, nargs="?", help="problem id (optional; inferred from directory if omitted)")
        sp.add_argument("name", nargs="?", default=None, help="(optional) problem title; fetched from solved.ac if omitted")
        sp.add_argument("-l", "--lang", choices=["cpp", "py"], default="py")

        # finish
        fp = sub.add_parser("finish", aliases=["f", "fin"], help="move file + remove from ps target + git commit/push")
        fp.set_defaults(cmd="finish")
        fp.add_argument("id", type=int, nargs="?", help="problem id (optional; inferred from directory if omitted)")
        fp.add_argument("name", nargs="?", default=None, help="(optional) title; auto-detect if omitted")
        fp.add_argument("-l", "--lang", choices=["cpp", "py"], default="py")
        fp.add_argument("-p", "--push", action="store_true")
        fp.add_argument("-n", "--no-git", action="store_true")

        # delete
        dp = sub.add_parser("delete", aliases=["d", "del"], help="remove file from ps target (code is kept; no git)")
        dp.set_defaults(cmd="delete")
        dp.add_argument("id", type=int, nargs="?", help="problem id (optional; inferred from directory if omitted)")
        dp.add_argument("name", nargs="?", default=None, help="(optional) title to help locate the file")
        dp.add_argument("-l", "--lang", choices=["cpp", "py"], default="py")

        # run
        rp = sub.add_parser("run", aliases=["r"], help="fetch samples and run them against the ps binary")
        rp.set_defaults(cmd="run")
        rp.add_argument("id", type=int, nargs="?", help="problem id (optional; inferred from directory if omitted)")
        rp.add_argument("-b", "--bin", dest="bin", default=None, help="override path to ps binary")

        # submit
        spb = sub.add_parser("submit", aliases=["sb"], help="submit code to acmicpc.net (requires BOJ_COOKIE)")
        spb.set_defaults(cmd="submit")
        spb.add_argument("id", type=int, nargs="?", help="problem id (optional; inferred from directory if omitted)")
        spb.add_argument("-l", "--lang", choices=["cpp", "py"], default='py', help="preferred language family")
        spb.add_argument("-f", "--file", dest="file", default=None, help="explicit path to source file")
        spb.add_argument("--open", dest="open", action="store_true", help="make code public (default: private)")

        # help
        hp = sub.add_parser("help", aliases=["h"], help="show help (optionally for a specific command)")
        hp.set_defaults(cmd="help")
        hp.add_argument("topic", nargs="?", help="command to show help for (start|finish|delete|run)")

        ap.epilog = (
            "\ncommands:\n"
            "  start  (s, st)   create file and add into ps target\n"
            "  finish (f, fin)  move file, remove from ps target, and optionally git commit/push\n"
            "  delete (d, del)  remove from ps target only (code kept, no git)\n"
            "  run    (r)       fetch samples and run them against the ps binary\n"
            "  submit (sb)     submit code to acmicpc.net using your login cookie\n"
            "  help   (h)       show this help or per-command usage\n"
        )
        return ap

    def run(self, argv: Optional[List[str]] = None) -> None:
        import re
        ap = self._build_parser()
        args = ap.parse_args(argv)

        # For commands that require an id, make it optional and infer from directory if not provided
        commands_with_id = {"start", "finish", "delete", "run", "submit"}
        if args.cmd in commands_with_id:
            # Only infer if id is None
            if getattr(args, "id", None) is None:
                cwd = Path.cwd()
                # Try to extract leading integer from directory name, which starts with number + space or dash
                m = re.match(r"^(\d+)[\s-]", cwd.name)
                if m:
                    try:
                        args.id = int(m.group(1))
                    except Exception:
                        pass
                else:
                    raise SystemExit("Problem ID not provided and current directory is not a problem directory.")

        if args.cmd == "start":
            self.h.start(args.id, args.name, args.lang)
        elif args.cmd == "finish":
            self.h.finish(args.id, args.name, args.lang, args.push, args.no_git)
        elif args.cmd == "delete":
            self.h.delete(args.id, args.name, args.lang)
        elif args.cmd == "run":
            self.h.run(args.id, args.bin)
        elif args.cmd == "submit":
            self.h.submit(args.id, args.lang, args.file, args.open)
        elif args.cmd == "help":
            # Rebuild parsers to print the right help if a topic is provided
            if args.topic is None:
                ap.print_help()
            else:
                topic = args.topic.lower()
                # Map aliases to canonical
                alias_map = {
                    "s": "start", "st": "start", "start": "start",
                    "f": "finish", "fin": "finish", "finish": "finish",
                    "d": "delete", "del": "delete", "delete": "delete",
                    "r": "run", "run": "run",
                }
                canonical = alias_map.get(topic)
                if not canonical:
                    print(f"{L.WARN} Unknown command: {args.topic}")
                    return
                # Show minimal per-command help text
                if canonical == "start":
                    print("usage: boj start|s|st <id> [name] [-l {cpp,py}]")
                elif canonical == "finish":
                    print("usage: boj finish|f|fin <id> [name] [-l {cpp,py}] [-p] [-n]")
                elif canonical == "delete":
                    print("usage: boj delete|d|del <id> [name] [-l {cpp,py}]")
                elif canonical == "run":
                    print("usage: boj run|r <id> [-b <path-to-ps>]")
                elif canonical == "submit":
                    print("usage: boj submit|sb <id> [-l {cpp,py}] [-f <file>] [--open]\nRequires env BOJ_COOKIE or 'boj_cookie' in bojconfig.json")


# ================================== 엔트리포인트 ================================

def main() -> None:
    paths = RepoPaths(root=Path(__file__).resolve().parent)
    helper = BOJHelper(paths)
    CLI(helper).run()


if __name__ == "__main__":
    main()
