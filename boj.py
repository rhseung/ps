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
            print(f"[warn] solved.ac HTTP {e.code}: {e.reason}")
        except URLError as e:
            print(f"[warn] solved.ac URL error: {e.reason}")
        except ssl.SSLError as e:
            print("[warn] SSL error when calling solved.ac:", e)
            print("[hint] Using fallback crawler for title…")
        except Exception as e:
            print(f"[warn] solved.ac parse error: {e}")

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
            print(f"[warn] crawl failed: {e}")

        return None

    def fetch_samples(self, pid: int) -> list[tuple[str, str]]:
        """Return list of (input, output) sample pairs from BOJ page.
        Strategy:
          1) Primary: <pre id="sample-input-N"> / <pre id="sample-output-N">
          2) Secondary: <section id="sampleinputN"> / <section id="sampleoutputN"> with <pre class="sampledata">
          3) Fallback: <h6>예제 입력 N</h6>/<h6>예제 출력 N</h6> followed by <pre>
        Cleans HTML spans (e.g., space-highlight) and preserves spaces/newlines.
        """
        try:
            html_text = self._request(
                f"https://www.acmicpc.net/problem/{pid}",
                {
                    "User-Agent": "ps-boj-helper/1.1 (+https://github.com/rhseung/ps)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                },
            )
        except Exception:
            return []

        def _clean_pre(fragment: str) -> str:
            # Replace explicit space markers
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

        # --- Primary by id attributes
        inputs: dict[int, str] = {}
        outputs: dict[int, str] = {}
        for m in re.finditer(r'<pre[^>]*id=\"sample-input-(\d+)\"[^>]*>(.*?)</pre>', html_text, re.DOTALL | re.IGNORECASE):
            idx = int(m.group(1))
            inputs[idx] = _clean_pre(m.group(2))
        for m in re.finditer(r'<pre[^>]*id=\"sample-output-(\d+)\"[^>]*>(.*?)</pre>', html_text, re.DOTALL | re.IGNORECASE):
            idx = int(m.group(1))
            outputs[idx] = _clean_pre(m.group(2))
        pairs: list[tuple[str, str]] = []
        for k in sorted(set(inputs) & set(outputs)):
            pairs.append((inputs[k], outputs[k]))
        if pairs:
            return pairs

        # --- Secondary: section ids sampleinputN / sampleoutputN
        inputs.clear();
        outputs.clear()
        for m in re.finditer(r'<section[^>]*id=\"sampleinput(\d+)\"[^>]*>.*?<pre[^>]*class=\"sampledata\"[^>]*>(.*?)</pre>', html_text,
                             re.DOTALL | re.IGNORECASE):
            inputs[int(m.group(1))] = _clean_pre(m.group(2))
        for m in re.finditer(r'<section[^>]*id=\"sampleoutput(\d+)\"[^>]*>.*?<pre[^>]*class=\"sampledata\"[^>]*>(.*?)</pre>', html_text,
                             re.DOTALL | re.IGNORECASE):
            outputs[int(m.group(1))] = _clean_pre(m.group(2))
        for k in sorted(set(inputs) & set(outputs)):
            pairs.append((inputs[k], outputs[k]))
        if pairs:
            return pairs

        # --- Fallback: headings <h6>예제 입력 N</h6> / <h6>예제 출력 N</h6>
        blocks: list[tuple[str, int, str]] = []
        for m in re.finditer(r'<h6[^>]*>\s*([^<]*?)\s*(\d+)\s*</h6>\s*<pre[^>]*>(.*?)</pre>', html_text, re.DOTALL | re.IGNORECASE):
            label_raw = html.unescape(m.group(1)).strip().lower()
            idx = int(m.group(2))
            txt = _clean_pre(m.group(3))
            if '입력' in label_raw or 'input' in label_raw:
                blocks.append(('input', idx, txt))
            elif '출력' in label_raw or 'output' in label_raw:
                blocks.append(('output', idx, txt))
        if blocks:
            in_map: dict[int, str] = {}
            out_map: dict[int, str] = {}
            for kind, idx, txt in blocks:
                (in_map if kind == 'input' else out_map)[idx] = txt
            res: list[tuple[str, str]] = []
            for k in sorted(set(in_map) & set(out_map)):
                res.append((in_map[k], out_map[k]))
            if res:
                return res

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
        run_dir = self.cfg.get("run_dir", "${CMAKE_BINARY_DIR}/bin")
        build_dir = self._guess_build_dir()
        run_dir = run_dir.replace("${CMAKE_BINARY_DIR}", str(build_dir))
        exe = "ps.exe" if os.name == "nt" else "ps"
        return Path(run_dir) / exe

    def run_cases(self, bin_path: Path, cases: list[tuple[str, str]]) -> list[dict]:
        results = []
        for i, (inp, expected) in enumerate(cases, 1):
            proc = subprocess.run([str(bin_path)], input=inp, text=True, capture_output=True)
            out = proc.stdout.rstrip("\n")
            exp = expected.rstrip("\n")
            ok = (proc.returncode == 0) and (out == exp)
            results.append({
                "idx": i,
                "ok": ok,
                "exit": proc.returncode,
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
                print(f"[ok] fetched title: {name}")
            else:
                name = f"BOJ {pid}"
                print("[warn] could not fetch title; using placeholder")

        fname = f"{pid} - {sanitize_filename(name)}.{lang}"
        dst = self.paths.solving / fname
        dst.parent.mkdir(parents=True, exist_ok=True)

        if not dst.exists():
            dst.write_text(self._lang_template(lang).format(id=pid, name=name), encoding="utf-8")
            print(f"[ok] created: {dst.relative_to(self.paths.root)}")
        else:
            print(f"[skip] exists: {dst.relative_to(self.paths.root)}")

        rel_src = self._rel(dst)
        self.cmake.add(rel_src)
        print(f"[ok] added to ps target: {rel_src}")

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
        self.cmake.remove(rel_src)
        print(f"[ok] removed from ps target: {rel_src}")

        dst_dir = self.paths.root / thousand_folder(pid)
        dst_dir.mkdir(exist_ok=True)
        dst = dst_dir / src.name
        shutil.move(str(src), str(dst))
        print(f"[ok] moved to: {dst.relative_to(self.paths.root)}")

        if not no_git:
            self.git.run("add", "-A")
            msg = f"solve: {pid} - {name}"
            self.git.run("commit", "-m", msg)
            print(f"[ok] committed: {msg}")
            if push:
                self.git.run("push")
                print("[ok] pushed")

    def run(self, pid: int, bin_override: Optional[str]) -> None:
        samples = self.fetcher.fetch_samples(pid)
        if not samples:
            print("[warn] No samples found on problem page.")
            return
        bin_path = Path(bin_override) if bin_override else self.runner.resolve_bin()
        if not bin_path.exists():
            print(f"[error] Binary not found: {bin_path}\n[hint] Build your project or override with --bin <path>.")
            return
        # Save samples locally
        base = self.paths.root / "tests" / "boj" / str(pid)
        base.mkdir(parents=True, exist_ok=True)
        for i, (inp, out) in enumerate(samples, 1):
            (base / f"sample-{i}.in").write_text(inp + "\n", encoding="utf-8")
            (base / f"sample-{i}.out").write_text(out + "\n", encoding="utf-8")
        results = self.runner.run_cases(bin_path, samples)
        for r in results:
            mark = "✅" if r["ok"] else "❌"
            print(f"[case {r['idx']}] {mark} exit={r['exit']}")
            if not r["ok"]:
                print("--- expected ---")
                print(r["expected"])
                print("--- actual ---")
                print(r["actual"])
                if r["stderr"].strip():
                    print("--- stderr ---")
                    print(r["stderr"])

                # ==================================== CLI ====================================


class CLI:
    def __init__(self, helper: BOJHelper):
        self.h = helper

    def run(self, argv: Optional[List[str]] = None) -> None:
        ap = argparse.ArgumentParser(prog="boj", description="Baekjoon workflow helper")
        sub = ap.add_subparsers(dest="cmd", required=True)

        sp = sub.add_parser("start", help="create file + add into ps target")
        sp.add_argument("id", type=int)
        sp.add_argument("name", nargs="?", default=None, help="(optional) problem title; fetched from solved.ac if omitted")
        sp.add_argument("--lang", choices=["cpp", "py"], default="cpp")

        fp = sub.add_parser("finish", help="move file + remove from ps target + git commit/push")
        fp.add_argument("id", type=int)
        fp.add_argument("name", nargs="?", default=None, help="(optional) title; auto-detect if omitted")
        fp.add_argument("--lang", choices=["cpp", "py"], default="cpp")
        fp.add_argument("--push", action="store_true")
        fp.add_argument("--no-git", action="store_true")

        rp = sub.add_parser("run", help="fetch samples and run them against the ps binary")
        rp.add_argument("id", type=int)
        rp.add_argument("--bin", dest="bin", default=None, help="override path to ps binary")

        args = ap.parse_args(argv)

        if args.cmd == "start":
            self.h.start(args.id, args.name, args.lang)
        elif args.cmd == "finish":
            self.h.finish(args.id, args.name, args.lang, args.push, args.no_git)
        elif args.cmd == "run":
            self.h.run(args.id, args.bin)


# ================================== Entrypoint ================================

def main() -> None:
    paths = RepoPaths(root=Path(__file__).resolve().parent)
    helper = BOJHelper(paths)
    CLI(helper).run()


if __name__ == "__main__":
    main()
