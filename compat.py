

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
레거시 파일 구조 → 신규 구조 마이그레이션 도구

목표
- 예전 단일 파일 형태(예: `solving/1000 - A+B.py`, `00000/1000 - A+B.cpp` 등)를
  신규 디렉터리 구조(예: `solving/1000 - A+B/1000 - A+B.py`, `README.md`, `tests/`)로 변환.
- README.md 와 docs/boj/{id}.md 를 생성(부족 시). 네트워크 크롤링 사이에는 슬립을 둬서 속도 제한을 회피.
- 진행도와 ETA(예상 소요 시간)를 실시간으로 표시.

사용 예시
  $ python3 compat.py --sleep 1.2  # 각 문제의 원격 조회 사이에 1.2초 대기
  $ python3 compat.py --dry-run     # 실제 이동/생성 없이 무엇을 할지 출력만

주의
- 외부 라이브러리(tqdm 등)에 의존하지 않음.
- CMake 타겟 수정은 하지 않음(필요시 이후 `boj finish`/`boj delete`로 정리 권장).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# 같은 저장소의 boj.py 모듈을 활용하여 Markdown을 생성한다
# (RepoPaths, BOJHelper, ProblemFetcher 를 재사용)
try:
    from boj import RepoPaths, BOJHelper, ProblemFetcher, sanitize_filename, thousand_folder
except Exception as e:
    print("boj.py 모듈을 불러오지 못했습니다: ", e)
    sys.exit(1)


# ============================== 유틸리티 ===============================

def is_problem_file(p: Path) -> Optional[Tuple[int, str, str]]:
    """파일명이 "<id> - <이름>.<확장자>" 패턴인지 검사하고 매칭 결과를 반환한다.
    반환: (문제번호, 제목, 확장자) 또는 None
    """
    m = re.match(r"^(\d+)\s*-\s*(.+)\.(py|cpp)$", p.name)
    if not m:
        return None
    pid = int(m.group(1))
    title = m.group(2)
    ext = m.group(3)
    return pid, title, ext


def find_legacy_files(root: Path) -> List[Path]:
    """레거시 단일 파일 후보들을 찾는다.
    - solving/ 아래의 단일 파일
    - 천 단위 폴더(\d{5}/) 아래의 단일 파일
    - 그 외 하위 경로 중 패턴에 부합하는 단일 파일
    이미 디렉터리형 구조(같은 이름의 폴더 존재 등)는 제외한다.
    """
    candidates: List[Path] = []

    # solving/ 최상위의 *.py, *.cpp
    for p in (root / "solving").glob("*.py"):
        if is_problem_file(p):
            candidates.append(p)
    for p in (root / "solving").glob("*.cpp"):
        if is_problem_file(p):
            candidates.append(p)

    # 천 단위 폴더(00000, 01000, …)에도 단일 파일이 있을 수 있음
    for d in sorted(root.glob("[0-9][0-9][0-9][0-9][0-9]")):
        if not d.is_dir():
            continue
        for p in d.glob("*.py"):
            if is_problem_file(p):
                candidates.append(p)
        for p in d.glob("*.cpp"):
            if is_problem_file(p):
                candidates.append(p)

    # 기타 서브트리(안전상 너무 깊게는 안 감). 필요 시 확장 가능
    for p in root.glob("**/*.py"):
        if p.parent.name.startswith("."):
            continue
        if "solving" in p.parts or re.match(r"^[0-9]{5}$", p.parent.name):
            continue  # 위에서 이미 포함됨
        if is_problem_file(p):
            candidates.append(p)
    for p in root.glob("**/*.cpp"):
        if p.parent.name.startswith("."):
            continue
        if "solving" in p.parts or re.match(r"^[0-9]{5}$", p.parent.name):
            continue
        if is_problem_file(p):
            candidates.append(p)

    # 이미 신규 디렉터리 형태(같은 이름의 폴더/README 존재)인 경우 제외
    filtered: List[Path] = []
    for p in candidates:
        info = is_problem_file(p)
        if not info:
            continue
        pid, title, _ = info
        prob_dir = root / "solving" / f"{pid} - {sanitize_filename(title)}"
        # 같은 디렉터리 안에 이미 같은 이름의 파일이 있으면 마이그레이션 대상이 아닐 수 있음
        if p.parent == prob_dir:
            continue
        filtered.append(p)

    return filtered


# ============================== 진행 표시줄 ===============================

def fmt_time(sec: float) -> str:
    """초 단위를 사람이 읽기 쉬운 mm:ss 형태로 변환"""
    sec = max(0, int(sec))
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def progress_bar(i: int, n: int, start_ts: float) -> None:
    """단순 텍스트 진행 표시줄 + ETA. 같은 줄에서 갱신한다."""
    now = time.monotonic()
    elapsed = now - start_ts
    rate = (i / elapsed) if elapsed > 0 else 0.0
    remain = (n - i) / rate if rate > 0 else 0.0

    width = 28
    done = int(width * i / max(1, n))
    bar = "#" * done + "." * (width - done)
    pct = (100.0 * i / max(1, n))

    line = f"[{bar}] {pct:6.2f}%  {i:4d}/{n:<4d}  ETA {fmt_time(remain)}"
    sys.stdout.write("\r" + line)
    sys.stdout.flush()
    if i == n:
        sys.stdout.write("\n")


# ============================== 마이그레이션 본체 ===============================

def migrate(root: Path, sleep_sec: float, dry_run: bool, only_markdown: bool) -> None:
    paths = RepoPaths(root=root)
    helper = BOJHelper(paths)
    fetcher: ProblemFetcher = helper.fetcher

    # 레거시 단일 파일 수집 및 문제 ID 묶음 만들기
    files = find_legacy_files(root)

    # 같은 문제 번호가 여러 위치에 있을 수 있으므로, ID 기준으로 그룹핑
    grouped: Dict[int, List[Path]] = {}
    for f in files:
        info = is_problem_file(f)
        if not info:
            continue
        pid, title, ext = info
        grouped.setdefault(pid, []).append(f)

    # 또, 이미 신규 구조로 존재하지만 README.md/docs가 없는 경우를 위해 solving/* 디렉터리도 훑는다
    for d in sorted((root / "solving").glob("* - *")):
        if not d.is_dir():
            continue
        try:
            pid = int(d.name.split(" - ", 1)[0])
        except Exception:
            continue
        grouped.setdefault(pid, [])  # 항목만 만들어 둠

    ids = sorted(grouped.keys())
    total = len(ids)
    if total == 0:
        print("이동/보정할 항목이 없습니다.")
        return

    print(f"대상 문제 수: {total} (sleep={sleep_sec}s, dry_run={dry_run}, only_markdown={only_markdown})")

    start_ts = time.monotonic()

    for idx, pid in enumerate(ids, 1):
        # 진행 표시줄 갱신
        progress_bar(idx - 1, total, start_ts)

        # 대상 디렉터리 경로 결정(제목은 첫 파일에서 가져오거나, 없으면 원격에서 가져옴)
        # 우선 파일 이름에 있는 제목을 우선, 없으면 원격에서 확인
        title: Optional[str] = None
        for f in grouped.get(pid, []):
            info = is_problem_file(f)
            if info:
                _, t, _ = info
                title = t
                break
        if not title:
            if dry_run:
                title = f"BOJ {pid}"
            else:
                t = helper.fetcher.fetch(pid)
                title = t or f"BOJ {pid}"

        dest_base = paths.root / thousand_folder(pid)
        prob_dir = dest_base / f"{pid} - {sanitize_filename(title)}"

        # 1) 디렉터리 구조 만들기
        if not only_markdown:
            if dry_run:
                print(f"\n[DRY] mkdir -p {prob_dir}")
            else:
                prob_dir.mkdir(parents=True, exist_ok=True)

            # 2) 해당 ID의 단일 파일들을 새 디렉터리로 이동(이름 보존)
            for f in grouped.get(pid, []):
                target = prob_dir / f.name
                if dry_run:
                    print(f"[DRY] move {f} -> {target}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if not target.exists():
                        shutil.move(str(f), str(target))

            # 3) tests/ 이동(기존 tests/boj/{id} → 새 디렉터리 tests/)
            old_tests = root / "tests" / "boj" / str(pid)
            new_tests = prob_dir / "tests"
            if old_tests.exists() and old_tests.is_dir():
                if dry_run:
                    print(f"[DRY] move {old_tests} -> {new_tests}")
                else:
                    new_tests.mkdir(parents=True, exist_ok=True)
                    for item in old_tests.iterdir():
                        shutil.move(str(item), str(new_tests / item.name))
                    # 비워졌으면 폴더 삭제 시도
                    try:
                        old_tests.rmdir()
                    except Exception:
                        pass

        # 4) README.md 및 docs/boj/{id}.md 생성(이미 있으면 건너뜀)
        readme_path = prob_dir / "README.md"
        docs_path = paths.root / "docs" / "boj" / f"{pid}.md"
        need_network = False
        if not readme_path.exists() or not docs_path.exists():
            need_network = True

        if need_network:
            if dry_run:
                print(f"[DRY] fetch & write markdown for {pid}")
            else:
                details = fetcher.fetch_full_details(pid)
                md = fetcher.to_markdown(pid, details)

                # README.md
                prob_dir.mkdir(parents=True, exist_ok=True)
                if not readme_path.exists():
                    readme_path.write_text(md + "\n", encoding="utf-8")

                # docs/boj/{id}.md
                docs_path.parent.mkdir(parents=True, exist_ok=True)
                if not docs_path.exists():
                    docs_path.write_text(md + "\n", encoding="utf-8")

                # 슬립으로 레이트 리밋 회피
                if sleep_sec > 0:
                    time.sleep(sleep_sec)

        # 루프 끝에서 진행률 1증가 출력
        progress_bar(idx, total, start_ts)

    print("완료")


# ============================== 엔트리 포인트 ===============================

def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="BOJ 레거시 파일 구조를 신규 구조로 변환")
    parser.add_argument("--sleep", type=float, default=1.0, help="원격 조회 사이 대기 시간(초)")
    parser.add_argument("--dry-run", action="store_true", help="파일 이동/생성 없이 시뮬레이션만 수행")
    parser.add_argument("--only-markdown", action="store_true", help="파일 이동은 건너뛰고 README/docs 생성만 수행")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parent
    migrate(root=root, sleep_sec=args.sleep, dry_run=args.dry_run, only_markdown=args.only_markdown)


if __name__ == "__main__":
    main()