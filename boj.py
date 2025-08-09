#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baekjoon workflow helper (start / finish)
- start: create source under `solving/` and APPEND it into add_executable(ps ...)
- finish: move the file to thousand-range folder, REMOVE it from add_executable(ps ...), and git commit/push

It also fetches the problem title from solved.ac (API v3):
  https://solved.ac/api/v3/problem/show?problemId={id}
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import ssl
import html
try:
    import certifi
    _CAFILE = certifi.where()
except Exception:
    _CAFILE = None

# ------------ repo paths ------------
ROOT = Path(__file__).resolve().parent
SOLVING = ROOT / "solving"
CMAKELISTS = ROOT / "CMakeLists.txt"
CONFIG_PATH = ROOT / "bjconfig.json"

# ------------ defaults --------------
DEFAULT_CFG = {
    "lang": "cpp",            # default language
    "run_dir": "${CMAKE_BINARY_DIR}/bin",  # not used when injecting into ps target
}

INVALID_FS = r"[\\/:*?\"<>|]"

CPP_TEMPLATE = """// BOJ {id} - {name}
#include <bits/stdc++.h>
#define endl "\\n"

using namespace std;
using ll = long long;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    return 0;
}}
"""

PY_TEMPLATE = """# BOJ {id} - {name}
import sys

def main():
    data = sys.stdin.read().strip().split()
    pass

if __name__ == "__main__":
    main()
"""

# ------------ utils -----------------

def load_cfg():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            return {**DEFAULT_CFG, **cfg}
        except Exception:
            return DEFAULT_CFG
    return DEFAULT_CFG


def sanitize_filename(s: str) -> str:
    s = re.sub(INVALID_FS, "_", s)
    return s.strip()


def thousand_folder(pid: int) -> str:
    base = (pid // 1000) * 1000
    return f"{base:05d}"


# ------------ solved.ac -------------
SOLVEDAC_URL = "https://solved.ac/api/v3/problem/show?problemId={pid}"


def fetch_problem_title(pid: int) -> str | None:
    """Get problem title by ID.
    Order: solved.ac API -> crawl acmicpc.net/problem/{pid}
    """
    # 1) Try solved.ac API
    url = SOLVEDAC_URL.format(pid=pid)
    try:
        req = Request(url, headers={
            "User-Agent": "ps-bj-helper/1.0 (+https://github.com/rhseung/ps)",
            "Accept": "application/json",
        })
        ctx = ssl.create_default_context(cafile=_CAFILE) if _CAFILE else ssl.create_default_context()
        with urlopen(req, timeout=6, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            title = data.get("titleKo") or data.get("titleEn") or data.get("title")
            if isinstance(title, str) and title.strip():
                return title.strip()
    except HTTPError as e:
        print(f"[warn] solved.ac HTTP {e.code}: {e.reason}")
    except URLError as e:
        print(f"[warn] solved.ac URL error: {e.reason}")
    except ssl.SSLError as e:
        print("[warn] SSL error when calling solved.ac:", e)
        print("[hint] Using fallback crawler for title…")
    except Exception as e:
        print(f"[warn] solved.ac parse error: {e}")

    # 2) Fallback: crawl acmicpc.net
    try:
        bj_url = f"https://www.acmicpc.net/problem/{pid}"
        req = Request(bj_url, headers={
            "User-Agent": "ps-bj-helper/1.0 (+https://github.com/rhseung/ps)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        ctx = ssl.create_default_context(cafile=_CAFILE) if _CAFILE else ssl.create_default_context()
        with urlopen(req, timeout=8, context=ctx) as resp:
            raw = resp.read()
            # Try UTF-8 first; Baekjoon uses UTF-8
            html_text = raw.decode("utf-8", errors="ignore")
            # Prefer id="problem_title"
            m = re.search(r'id="problem_title"\s*>\s*(.*?)\s*<', html_text, re.IGNORECASE | re.DOTALL)
            if not m:
                # Fallback to <title> tag
                mt = re.search(r"<title>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
                if mt:
                    title_tag = html.unescape(mt.group(1)).strip()
                    # Known pattern example: "1000번: A+B" or "A+B - 백준"; normalize to part after colon if exists
                    parts = re.split(r"[:\-]\s*", title_tag, maxsplit=1)
                    guess = parts[-1].strip() if parts else title_tag
                    return guess
            else:
                title = html.unescape(m.group(1)).strip()
                if title:
                    return title
    except Exception as e:
        print(f"[warn] crawl failed: {e}")

    return None


# ------------ CMake helpers ---------
_PS_CALL_RE = re.compile(r"add_executable\s*\(\s*ps\b", re.IGNORECASE)


def _find_ps_block(text: str):
    """Find the add_executable(ps ...) block and return (start_idx, end_idx, indent).
    end_idx is the index AFTER the closing ')'.
    """
    m = _PS_CALL_RE.search(text)
    if not m:
        raise SystemExit("add_executable(ps ...) not found in CMakeLists.txt")
    start = m.start()
    # find opening '(' from this call
    open_paren = text.find('(', m.start())
    if open_paren == -1:
        raise SystemExit("Malformed add_executable(ps ...): '(' not found")
    # Walk to matching ')'
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
                # indentation = whitespace at line start of the call
                line_start = text.rfind('\n', 0, start) + 1
                indent = text[line_start:start]
                return start, end, indent
        i += 1
    raise SystemExit("Malformed add_executable(ps ...): closing ')' not found")


def _parse_ps_sources(inside: str) -> list[str]:
    """Parse tokens inside add_executable(ps ...). Keeps order.
    Accepts quoted tokens (with spaces) and unquoted tokens.
    First token should be 'ps'. Returns the list of sources (without the 'ps').
    """
    # Remove newlines for tokenization but keep spaces inside quotes
    tokens = re.findall(r'"[^"\n]+"|[^\s\n]+', inside)
    if not tokens:
        return []
    if tokens[0].strip('"') != 'ps':
        # Some odd formatting; try to find 'ps' token index
        try:
            idx = [t.strip('"') for t in tokens].index('ps')
            tokens = tokens[idx+1:]
        except ValueError:
            # fallback: treat all as sources
            pass
    else:
        tokens = tokens[1:]
    # Normalize: strip surrounding quotes
    out = []
    for t in tokens:
        t = t.strip()
        if t.endswith(')'):
            t = t[:-1]
        if t.startswith('"') and t.endswith('"'):
            t = t[1:-1]
        if t:
            out.append(t)
    return out


def _rebuild_ps_block(indent: str, sources: list[str]) -> str:
    """Build a pretty multi-line add_executable(ps ...) block.
    We quote every source to safely allow spaces.
    """
    inner_indent = indent + "    "
    body = "\n".join(f"{inner_indent}\"{src}\"" for src in sources)
    return f"{indent}add_executable(ps\n{body}\n{indent})"


def add_source_to_ps(rel_src: str):
    text = CMAKELISTS.read_text(encoding="utf-8")
    start, end, indent = _find_ps_block(text)
    inside = text[start:end]
    # content between '(' and ')'
    open_idx = inside.find('(')
    close_idx = inside.rfind(')')
    content = inside[open_idx+1:close_idx]

    sources = _parse_ps_sources(content)
    if rel_src not in sources:
        sources.append(rel_src)
    new_block = _rebuild_ps_block(indent, sources)
    new_text = text[:start] + new_block + text[end:]
    CMAKELISTS.write_text(new_text, encoding="utf-8")


def remove_source_from_ps(rel_src: str):
    text = CMAKELISTS.read_text(encoding="utf-8")
    start, end, indent = _find_ps_block(text)
    inside = text[start:end]
    open_idx = inside.find('(')
    close_idx = inside.rfind(')')
    content = inside[open_idx+1:close_idx]

    sources = _parse_ps_sources(content)
    new_sources = [s for s in sources if s != rel_src]
    new_block = _rebuild_ps_block(indent, new_sources)
    new_text = text[:start] + new_block + text[end:]
    CMAKELISTS.write_text(new_text, encoding="utf-8")


# ------------ git helper ------------

def git(*args):
    subprocess.check_call(["git", *args], cwd=ROOT)


# ------------ commands --------------

def cmd_start(pid: int, name: str | None, lang: str | None):
    cfg = load_cfg()
    lang = lang or cfg["lang"]

    if not name:
        fetched = fetch_problem_title(pid)
        if fetched:
            name = fetched
            print(f"[ok] fetched title: {name}")
        else:
            name = f"BOJ {pid}"
            print("[warn] could not fetch title; using placeholder")

    fname = f"{pid} - {sanitize_filename(name)}.{lang}"
    dst = SOLVING / fname
    dst.parent.mkdir(parents=True, exist_ok=True)

    if not dst.exists():
        template = CPP_TEMPLATE if lang == "cpp" else PY_TEMPLATE
        dst.write_text(template.format(id=pid, name=name), encoding="utf-8")
        print(f"[ok] created: {dst.relative_to(ROOT)}")
    else:
        print(f"[skip] exists: {dst.relative_to(ROOT)}")

    rel_src = str(dst.relative_to(ROOT)).replace(os.sep, "/")
    add_source_to_ps(rel_src)
    print(f"[ok] added to ps target: {rel_src}")


def cmd_finish(pid: int, name: str | None, lang: str | None, push: bool, no_git: bool):
    cfg = load_cfg()
    lang = lang or cfg["lang"]

    # locate source in solving/
    src = None
    if name:
        candidate = SOLVING / f"{pid} - {sanitize_filename(name)}.{lang}"
        if candidate.exists():
            src = candidate
    if src is None:
        # fallback by id only
        cand = sorted(SOLVING.glob(f"{pid} -*.{lang}"))
        if cand:
            src = cand[0]
            if not name:
                try:
                    name = src.stem.split(" - ", 1)[1]
                except Exception:
                    pass
    if src is None:
        # last resort: fetch to know the filename to look for
        if not name:
            name = fetch_problem_title(pid) or f"BOJ {pid}"
        src = SOLVING / f"{pid} - {sanitize_filename(name)}.{lang}"
        if not src.exists():
            raise SystemExit(f"Source not found: {src}")

    if not name:
        name = fetch_problem_title(pid) or src.stem.split(" - ", 1)[1]

    rel_src = str(src.relative_to(ROOT)).replace(os.sep, "/")
    remove_source_from_ps(rel_src)
    print(f"[ok] removed from ps target: {rel_src}")

    dst_dir = ROOT / thousand_folder(pid)
    dst_dir.mkdir(exist_ok=True)
    dst = dst_dir / src.name
    shutil.move(str(src), str(dst))
    print(f"[ok] moved to: {dst.relative_to(ROOT)}")

    if not no_git:
        git("add", "-A")
        msg = f"solve: {pid} - {name}"
        git("commit", "-m", msg)
        print(f"[ok] committed: {msg}")
        if push:
            git("push")
            print("[ok] pushed")


# ------------ CLI -------------------

def main():
    """
    시작 (제목 자동 조회: solved.ac API)
    >>> python boj.py start 1562 --lang cpp

    완료 (커밋/푸시까지)
    >>> python boj.py finish 1562 --push
    """
  
    ap = argparse.ArgumentParser(prog="boj", description="Baekjoon workflow helper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("start", help="create file + add into ps target")
    sp.add_argument("id", type=int)
    sp.add_argument("name", nargs="?", default=None, help="(optional) problem title; fetched from solved.ac if omitted")
    sp.add_argument("--lang", choices=["cpp", "py"], default='cpp')

    fp = sub.add_parser("finish", help="move file + remove from ps target + git commit/push")
    fp.add_argument("id", type=int)
    fp.add_argument("name", nargs="?", default=None, help="(optional) title; auto-detect if omitted")
    fp.add_argument("--lang", choices=["cpp", "py"], default='cpp')
    fp.add_argument("--push", action="store_true")
    fp.add_argument("--no-git", action="store_true")

    args = ap.parse_args()

    if args.cmd == "start":
        cmd_start(args.id, args.name, args.lang)
    elif args.cmd == "finish":
        cmd_finish(args.id, args.name, args.lang, args.push, args.no_git)


if __name__ == "__main__":
    main()