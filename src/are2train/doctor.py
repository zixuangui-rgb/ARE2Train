"""Environment checks for ARE2Train."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_DIRS = (
    "configs",
    "configs/eval",
    "docs/tutorial",
    "docs/process-log",
    "docs/paper",
    "experiments",
    "scripts",
    "src/are2train",
    "tests",
)

EVAL_CONFIGS = (
    "baseline.yaml",
    "sft.yaml",
    "preference.yaml",
    "rlvr.yaml",
    "teacher.yaml",
)

SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}", re.IGNORECASE),
)

SECRET_ENV_NAMES = (
    "OPENAI_API_KEY",
    "DEEPSEEK_API_KEY",
    "DASHSCOPE_API_KEY",
    "ANTHROPIC_API_KEY",
    "TEACHER_API_KEY",
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    message: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _result(name: str, status: str, message: str) -> CheckResult:
    return CheckResult(name=name, status=status, message=message)


def check_python_version() -> CheckResult:
    version = sys.version_info
    version_text = platform.python_version()
    if version >= (3, 11):
        return _result("python", "ok", f"Python {version_text}")
    return _result("python", "fail", f"Python {version_text}; need >= 3.11")


def check_required_dirs(root: Path) -> CheckResult:
    missing = [path for path in REQUIRED_DIRS if not (root / path).is_dir()]
    if missing:
        return _result("directories", "fail", "missing: " + ", ".join(missing))
    return _result("directories", "ok", "all required directories exist")


def check_eval_configs(root: Path) -> CheckResult:
    eval_dir = root / "configs" / "eval"
    missing = [name for name in EVAL_CONFIGS if not (eval_dir / name).is_file()]
    if missing:
        return _result("eval_configs", "fail", "missing: " + ", ".join(missing))

    wrong_agent = []
    for name in EVAL_CONFIGS:
        text = (eval_dir / name).read_text(encoding="utf-8")
        if "agent_runtime:" not in text:
            wrong_agent.append(f"{name}: missing agent_runtime")
            continue
        if "name: official_openclaw" not in text:
            wrong_agent.append(f"{name}: agent is not official_openclaw")
        if "modification: none" not in text:
            wrong_agent.append(f"{name}: agent modification is not none")

    if wrong_agent:
        return _result("eval_configs", "fail", "; ".join(wrong_agent))

    return _result(
        "eval_configs",
        "ok",
        "all eval configs keep official OpenClaw / official agent unchanged",
    )


def _scan_files(root: Path) -> Iterable[Path]:
    include_dirs = ("configs", "docs", "scripts", "src", "tests")
    include_files = ("README.md", "pyproject.toml")

    for file_name in include_files:
        path = root / file_name
        if path.is_file():
            yield path

    for dir_name in include_dirs:
        base = root / dir_name
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".toml", ".yaml", ".yml", ".sh"}:
                yield path


def check_secret_leaks(root: Path) -> CheckResult:
    hits = []
    for path in _scan_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path.relative_to(root)))
                break

    if hits:
        return _result("secrets", "fail", "possible secret in: " + ", ".join(sorted(hits)))
    return _result("secrets", "ok", "no obvious API key pattern in tracked text files")


def check_optional_environment() -> CheckResult:
    optional = {
        "ARE2TRAIN_OPENCLAW_HOME": os.environ.get("ARE2TRAIN_OPENCLAW_HOME"),
        "ARE2TRAIN_MODEL_ENDPOINT": os.environ.get("ARE2TRAIN_MODEL_ENDPOINT"),
        "ARE2TRAIN_RUNS_DIR": os.environ.get("ARE2TRAIN_RUNS_DIR"),
    }
    missing = [name for name, value in optional.items() if not value]

    secret_status = []
    for name in SECRET_ENV_NAMES:
        secret_status.append(f"{name}={'set' if os.environ.get(name) else 'unset'}")

    if missing:
        return _result(
            "optional_env",
            "warn",
            "not set yet: " + ", ".join(missing) + "; secrets: " + ", ".join(secret_status),
        )

    return _result("optional_env", "ok", "runtime env is set; secrets: " + ", ".join(secret_status))


def run_checks(root: Path | None = None) -> list[CheckResult]:
    repo = (root or _repo_root()).resolve()
    return [
        check_python_version(),
        check_required_dirs(repo),
        check_eval_configs(repo),
        check_secret_leaks(repo),
        check_optional_environment(),
    ]


def _print_human(results: list[CheckResult]) -> None:
    for result in results:
        mark = {"ok": "OK", "warn": "WARN", "fail": "FAIL"}[result.status]
        print(f"[{mark}] {result.name}: {result.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check ARE2Train local environment.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--root", type=Path, default=None, help="Repository root. Defaults to current package root.")
    args = parser.parse_args(argv)

    results = run_checks(args.root)
    if args.json:
        print(json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2))
    else:
        _print_human(results)

    return 1 if any(result.status == "fail" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
