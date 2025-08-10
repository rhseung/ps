#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baekjoon workflow helper (start / finish)
Refactored: modular classes + clearer structure, same CLI and behavior
- start: create source under `solving/` and APPEND it into add_executable(ps ...)
- finish: move the file to thousand-range folder, REMOVE it from add_executable(ps ...), and git commit/push

It fetches the problem title from solved.ac (API v3) with crawler fallback.
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
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# ============================ ANSI Color Helpers =============================

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


# Runtime color toggle based on TTY/NO_COLOR
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


# Box drawing characters (ASCII fallback)
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

# ============================ Constants & Templates ============================
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

DEFAULT_CFG = {
    "lang": "cpp",  # default language
    "run_dir": "${CMAKE_BINARY_DIR}/bin",  # not used when injecting into ps target
}

SOLVEDAC_URL = "https://solved.ac/api/v3/problem/show?problemId={pid}"


# ================================= Utilities =================================

def sanitize_filename(s: str) -> str:
    s = re.sub(INVALID_FS, "_", s)
    return s.strip()


def thousand_folder(pid: int) -> str:
    base = (pid // 1000) * 1000
    return f"{base:05d}"


# ================================== Paths ====================================
@dataclass(frozen=True)
class RepoPaths:
    root: Path

    @property
    def solving(self) -> Path:
        return self.root / "solving"

    @property
    def cmakelists(self) -> Path:
        return self.root / "CMakeLists.txt"

    @property
    def config(self) -> Path:
        return self.root / "bojconfig.json"


# ================================== Config ===================================
class Config:
    def __init__(self, paths: RepoPaths):
        self.paths = paths
        self._cfg = DEFAULT_CFG | self._load()

    def _load(self) -> dict:
        if self.paths.config.exists():
            try:
                return json.loads(self.paths.config.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def get(self, key: str, default=None):
        return self._cfg.get(key, default)


# ================================ HTTP / Titles ===============================
class ProblemFetcher:
    """Fetch problem metadata (title + sample I/O) via solved.ac (v3) with acmicpc.net fallback."""

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
        """Return list of (input, output) sample pairs from BOJ page.
        Strategy (handle as many DOM variants as possible):
          A) Primary: <pre id="sample-input-N"> / <pre id="sample-output-N">
          B) Variants: allow <div> instead of <pre> and any order of attributes
          C) Legacy: <section id="sampleinputN"> / <section id="sampleoutputN"> with <pre class="sampledata">
          D) Fallback: headings <h[1-6]>예제 입력 N</h[1-6]> followed by <pre>
        Cleans HTML spans (e.g., space-highlight), converts <br> to newlines, preserves spaces/newlines.
        """

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

        def _clean_pre(fragment: str) -> str:
            # Replace explicit space markers (e.g., used to visualize spaces)
            frag = re.sub(r'<span[^>]*class=\"space-highlight\"[^>]*>\s*</span>', ' ', fragment, flags=re.IGNORECASE)
            # Convert <br> to newlines
            frag = re.sub(r'<br\s*/?>', '\n', frag, flags=re.IGNORECASE)
            # Drop remaining tags but keep text
            frag = re.sub(r'<[^>]+>', '', frag)
            # Unescape HTML entities
            frag = html.unescape(frag)
            # Normalise newlines; keep trailing spaces, trim only trailing newlines
            frag = frag.replace('\r\n', '\n').replace('\r', '\n')
            return frag.strip('\n')

        def _preview(s: str, n: int = 80) -> str:
            s = s.replace('\n', '\\n')
            return (s[:n] + ('…' if len(s) > n else ''))

        # Collector util that merges input/output maps into ordered pairs
        def _pairs_from_maps(inp_map: dict[int, str], out_map: dict[int, str]) -> list[tuple[str, str]]:
            out: list[tuple[str, str]] = []
            for k in sorted(set(inp_map) & set(out_map)):
                out.append((inp_map[k], out_map[k]))
            return out

        # --- Primary: strictly <pre id="sample-input-N"> / <pre id="sample-output-N">
        inputs: dict[int, str] = {}
        outputs: dict[int, str] = {}
        for m in re.finditer(r'<pre[^>]*id\s*=\s*[\"\']sample-input-(\d+)[\"\'][^>]*>(.*?)</pre>', html_text, re.DOTALL | re.IGNORECASE):
            inputs[int(m.group(1))] = _clean_pre(m.group(2))
        for m in re.finditer(r'<pre[^>]*id\s*=\s*[\"\']sample-output-(\d+)[\"\'][^>]*>(.*?)</pre>', html_text, re.DOTALL | re.IGNORECASE):
            outputs[int(m.group(1))] = _clean_pre(m.group(2))
        _log(f"primary <pre> ids: inputs={len(inputs)}, outputs={len(outputs)}")
        pairs = _pairs_from_maps(inputs, outputs)
        if not pairs and getattr(self, "debug", False):
            # Dump a tiny snippet around the first occurrence of 'sample-input' to help debug
            mm = re.search(r'sample-(?:input|output)-', html_text)
            if mm:
                s = max(0, mm.start() - 200)
                e = min(len(html_text), mm.end() + 240)
                print(f"[fetch_samples:{pid}] debug snippet (around sample-):\n" + html_text[s:e])
        if pairs:
            _log(f"matched primary <pre>: {len(pairs)} pair(s)")
            for i, (a, b) in enumerate(pairs, 1):
                _log(f"  sample #{i} in: '{_preview(a)}' | out: '{_preview(b)}'")
            return pairs

        # --- C) Legacy section ids sampleinputN / sampleoutputN with <pre class="sampledata">
        inputs.clear()
        outputs.clear()
        for m in re.finditer(
                r'<section[^>]*id\s*=\s*[\"\']sampleinput(\d+)[\"\'][^>]*>.*?<pre[^>]*class\s*=\s*[\"\'][^\"\']*\bsampledata\b[^\"\']*[\"\'][^>]*>(.*?)</pre>',
                html_text, re.DOTALL | re.IGNORECASE):
            inputs[int(m.group(1))] = _clean_pre(m.group(2))
        for m in re.finditer(
                r'<section[^>]*id\s*=\s*[\"\']sampleoutput(\d+)[\"\'][^>]*>.*?<pre[^>]*class\s*=\s*[\"\'][^\"\']*\bsampledata\b[^\"\']*[\"\'][^>]*>(.*?)</pre>',
                html_text, re.DOTALL | re.IGNORECASE):
            outputs[int(m.group(1))] = _clean_pre(m.group(2))
        _log(f"legacy sections: inputs={len(inputs)}, outputs={len(outputs)}")
        pairs = _pairs_from_maps(inputs, outputs)
        if pairs:
            _log(f"matched legacy sections: {len(pairs)} pair(s)")
            for i, (a, b) in enumerate(pairs, 1):
                _log(f"  sample #{i} in: '{_preview(a)}' | out: '{_preview(b)}'")
            return pairs

        # --- D) Fallback: headings 예제 입력/출력 N with arbitrary heading level and following <pre>
        blocks: list[tuple[str, int, str]] = []
        for m in re.finditer(r'<h[1-6][^>]*>\s*([^<]*?)\s*(\d+)\s*<\/h[1-6]>\s*<pre[^>]*>(.*?)<\/pre>', html_text,
                             re.DOTALL | re.IGNORECASE):
            label_raw = html.unescape(m.group(1)).strip().lower()
            idx = int(m.group(2))
            txt = _clean_pre(m.group(3))
            if '입력' in label_raw or 'input' in label_raw:
                blocks.append(('input', idx, txt))
            elif '출력' in label_raw or 'output' in label_raw:
                blocks.append(('output', idx, txt))
        _log(f"fallback headings blocks collected: {len(blocks)}")
        if blocks:
            in_map: dict[int, str] = {}
            out_map: dict[int, str] = {}
            for kind, idx, txt in blocks:
                (in_map if kind == 'input' else out_map)[idx] = txt
            pairs = _pairs_from_maps(in_map, out_map)
            if pairs:
                _log(f"matched heading fallback: {len(pairs)} pair(s)")
                for i, (a, b) in enumerate(pairs, 1):
                    _log(f"  sample #{i} in: '{_preview(a)}' | out: '{_preview(b)}'")
                return pairs

        _log("no sample pairs found after all strategies")
        return []


# ================================ CMake editor ================================
class CMakePS:
    _PS_CALL_RE = re.compile(r"add_executable\s*\(\s*ps\b", re.IGNORECASE)

    def __init__(self, cmakelists: Path):
        self.path = cmakelists

    def _find_ps_block(self, text: str) -> tuple[int, int, str]:
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
        subprocess.check_call(["git", *args], cwd=self.cwd)


class Runner:
    def __init__(self, repo: RepoPaths, cfg: Config):
        self.repo = repo
        self.cfg = cfg

    def _guess_build_dir(self) -> Path:
        # prefer ./build then common cmake dirs
        candidates = [self.repo.root / "build"]
        candidates += sorted(self.repo.root.glob("cmake-build-*"))
        for c in candidates:
            if c.exists():
                return c
        return self.repo.root / "build"

    def resolve_bin(self) -> Path:
        build_dir = self._guess_build_dir()
        exe = "ps.exe" if os.name == "nt" else "ps"

        # Config may be a dir or a full path; resolve ${CMAKE_BINARY_DIR}
        run_dir_cfg = self.cfg.get("run_dir", "${CMAKE_BINARY_DIR}/bin")
        run_dir_resolved = run_dir_cfg.replace("${CMAKE_BINARY_DIR}", str(build_dir))

        candidates: list[Path] = []
        p_cfg = Path(run_dir_resolved)
        if p_cfg.suffix == "" and p_cfg.name != exe:
            # looks like a directory; append exe under it
            candidates.append(p_cfg / exe)
        else:
            # looks like a file path already
            candidates.append(p_cfg)

        # Common CMake output patterns
        candidates.append(build_dir / exe)  # e.g., cmake-build-debug/ps (user case)
        candidates.append(build_dir / "bin" / exe)  # e.g., build/bin/ps
        for sub in ("Debug", "Release", "RelWithDebInfo", "MinSizeRel"):
            candidates.append(build_dir / sub / exe)

        # First existing wins
        for c in candidates:
            if c.exists():
                return c

        # Fallback to the first candidate even if missing (for helpful error path)
        return candidates[0]

    def run_cases(self, bin_path: Path, cases: list[tuple[str, str]]) -> list[dict]:
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


# ================================== Core =====================================
class BOJHelper:
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
        lang = (lang or self.config.get("lang", "cpp")).lower()

        if not name:
            fetched = self.fetcher.fetch(pid)
            if fetched:
                name = fetched
                print(f"{L.OK} fetched title: {name}")
            else:
                name = f"BOJ {pid}"
                print(f"{L.WARN} could not fetch title; using placeholder")

        fname = f"{pid} - {sanitize_filename(name)}.{lang}"
        dst = self.paths.solving / fname
        dst.parent.mkdir(parents=True, exist_ok=True)

        if not dst.exists():
            dst.write_text(self._lang_template(lang).format(id=pid, name=name), encoding="utf-8")
            print(f"{L.OK} created: {dst.relative_to(self.paths.root)}")
        else:
            print(f"{L.SKIP} exists: {dst.relative_to(self.paths.root)}")

        rel_src = self._rel(dst)
        if lang == "cpp":
            self.cmake.add(rel_src)
            print(f"{L.OK} added to ps target: {rel_src}")
        else:
            print(f"{L.HINT} python source created; not added to CMake target: {rel_src}")

    # ---------------------------- finish command -----------------------------
    def finish(self, pid: int, name: Optional[str], lang: Optional[str], push: bool, no_git: bool) -> None:
        lang = (lang or self.config.get("lang", "cpp")).lower()

        # locate source in solving/
        src: Optional[Path] = None
        if name:
            candidate = self.paths.solving / f"{pid} - {sanitize_filename(name)}.{lang}"
            if candidate.exists():
                src = candidate
        if src is None:
            cand = sorted(self.paths.solving.glob(f"{pid} -*.{lang}"))
            if cand:
                src = cand[0]
                if not name:
                    try:
                        name = src.stem.split(" - ", 1)[1]
                    except Exception:
                        pass
        if src is None:
            if not name:
                name = self.fetcher.fetch(pid) or f"BOJ {pid}"
            src = self.paths.solving / f"{pid} - {sanitize_filename(name)}.{lang}"
            if not src.exists():
                raise SystemExit(f"Source not found: {src}")

        if not name:
            # last-ditch best-effort name
            try:
                name = src.stem.split(" - ", 1)[1]
            except Exception:
                name = self.fetcher.fetch(pid) or f"BOJ {pid}"

        rel_src = self._rel(src)
        if lang == "cpp":
            self.cmake.remove(rel_src)
            print(f"{L.OK} removed from ps target: {rel_src}")
        else:
            print(f"{L.HINT} python source; nothing to remove from CMake: {rel_src}")

        dst_dir = self.paths.root / thousand_folder(pid)
        dst_dir.mkdir(exist_ok=True)
        dst = dst_dir / src.name
        shutil.move(str(src), str(dst))
        print(f"{L.OK} moved to: {dst.relative_to(self.paths.root)}")

        if not no_git:
            self.git.run("add", "-A")
            msg = f"solve: {pid} - {name}"
            self.git.run("commit", "-m", msg)
            print(f"{L.OK} committed: {msg}")
            if push:
                self.git.run("push")
                print(f"{L.OK} pushed")

    # ---------------------------- delete command -----------------------------
    def delete(self, pid: int, name: Optional[str], lang: Optional[str]) -> None:
        """Remove the file from the ps target **without** deleting the code or committing.
        - If `name` is omitted, try to resolve it similarly to `finish`.
        - Prefer files under `solving/`, but fall back to the first match anywhere if needed.
        """
        lang = (lang or self.config.get("lang", "cpp")).lower()

        # Try to locate the source file (prefer solving/)
        src: Optional[Path] = None
        if name:
            candidate = self.paths.solving / f"{pid} - {sanitize_filename(name)}.{lang}"
            if candidate.exists():
                src = candidate
        if src is None:
            # Prefer solving/ if possible
            cand_solving = sorted(self.paths.solving.glob(f"{pid} -*.{lang}"))
            if cand_solving:
                src = cand_solving[0]
        if src is None:
            # As a fallback, search repo (shallow) for any match
            cand_any = sorted(self.paths.root.glob(f"**/{pid} -*.{lang}"))
            if cand_any:
                src = cand_any[0]
        if src is None:
            # If still unknown and name was omitted, best-effort name fetch
            if not name:
                fetched = self.fetcher.fetch(pid)
                if fetched:
                    name = fetched
                    candidate = self.paths.solving / f"{pid} - {sanitize_filename(name)}.{lang}"
                    if candidate.exists():
                        src = candidate
        if src is None:
            raise SystemExit(f"Source not found for id={pid}. Try providing a name or --lang.")

        rel_src = self._rel(src)
        if lang == "cpp":
            self.cmake.remove(rel_src)
            print(f"{L.OK} removed from ps target: {rel_src}")
        else:
            print(f"{L.HINT} python source; nothing to remove from CMake: {rel_src}")
        print(f"{L.HINT} code file kept: {src.relative_to(self.paths.root)}")

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

        # Auto-detect python solution first (preferred when exists)
        py_src = None
        cand_solving = sorted(self.paths.solving.glob(f"{pid} -*.py"))
        if cand_solving:
            py_src = cand_solving[0]
        else:
            # also allow thousand folder (e.g., 02000/xxxx.py)
            py_glob = list(self.paths.root.glob(f"**/{pid} -*.py"))
            if py_glob:
                py_src = py_glob[0]

        if py_src is not None:
            # Run with python interpreter
            import sys as _sys
            argv = [_sys.executable, str(py_src)]
            results = self.runner.run_cases_argv(argv, samples)
            bin_display = py_src.name
        else:
            # Fall back to compiled C++ binary
            bin_path = Path(bin_override) if bin_override else self.runner.resolve_bin()
            if not bin_path.exists():
                # Recompute candidate list to show helpful hint
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
        # Save samples locally
        base = self.paths.root / "tests" / "boj" / str(pid)
        base.mkdir(parents=True, exist_ok=True)
        for i, (inp, out) in enumerate(samples, 1):
            (base / f"sample-{i}.in").write_text(inp + "\n", encoding="utf-8")
            (base / f"sample-{i}.out").write_text(out + "\n", encoding="utf-8")

        # Pretty, simple text output (no boxes)
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

        # Summary line
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
        sp.add_argument("id", type=int)
        sp.add_argument("name", nargs="?", default=None, help="(optional) problem title; fetched from solved.ac if omitted")
        sp.add_argument("-l", "--lang", choices=["cpp", "py"], default="cpp")

        # finish
        fp = sub.add_parser("finish", aliases=["f", "fin"], help="move file + remove from ps target + git commit/push")
        fp.set_defaults(cmd="finish")
        fp.add_argument("id", type=int)
        fp.add_argument("name", nargs="?", default=None, help="(optional) title; auto-detect if omitted")
        fp.add_argument("-l", "--lang", choices=["cpp", "py"], default="cpp")
        fp.add_argument("-p", "--push", action="store_true")
        fp.add_argument("-n", "--no-git", action="store_true")

        # delete
        dp = sub.add_parser("delete", aliases=["d", "del"], help="remove file from ps target (code is kept; no git)")
        dp.set_defaults(cmd="delete")
        dp.add_argument("id", type=int)
        dp.add_argument("name", nargs="?", default=None, help="(optional) title to help locate the file")
        dp.add_argument("-l", "--lang", choices=["cpp", "py"], default="cpp")

        # run
        rp = sub.add_parser("run", aliases=["r"], help="fetch samples and run them against the ps binary")
        rp.set_defaults(cmd="run")
        rp.add_argument("id", type=int)
        rp.add_argument("-b", "--bin", dest="bin", default=None, help="override path to ps binary")

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
            "  help   (h)       show this help or per-command usage\n"
        )
        return ap

    def run(self, argv: Optional[List[str]] = None) -> None:
        ap = self._build_parser()
        args = ap.parse_args(argv)

        if args.cmd == "start":
            self.h.start(args.id, args.name, args.lang)
        elif args.cmd == "finish":
            self.h.finish(args.id, args.name, args.lang, args.push, args.no_git)
        elif args.cmd == "delete":
            self.h.delete(args.id, args.name, args.lang)
        elif args.cmd == "run":
            self.h.run(args.id, args.bin)
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


# ================================== Entrypoint ================================

def main() -> None:
    paths = RepoPaths(root=Path(__file__).resolve().parent)
    helper = BOJHelper(paths)
    CLI(helper).run()


if __name__ == "__main__":
    main()
