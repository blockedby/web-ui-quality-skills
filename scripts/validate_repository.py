#!/usr/bin/env python3
"""Dependency-free repository checks for the three web UI quality skills."""

from __future__ import annotations

import json
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "skills/static-html-browser-audit/scripts/audit.py"
SKILLS = {
    "frontend-quality": {
        "path": ROOT / "skills/frontend-quality/SKILL.md",
        "terms": ("requirements", "current frontend stack", "verified implementation guidance", "review"),
    },
    "visual-composition": {
        "path": ROOT / "skills/visual-composition/SKILL.md",
        "terms": ("visual brief", "coherent composition", "responsive transformation", "outputs"),
    },
    "static-html-browser-audit": {
        "path": ROOT / "skills/static-html-browser-audit/SKILL.md",
        "terms": ("local HTML", "parse errors", "broken local links", "horizontal overflow"),
    },
}


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_frontmatter(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    require(end != -1, f"{path.relative_to(ROOT)} has no closing frontmatter delimiter")
    values: Dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"\'')
    return values


def check_repository_files() -> None:
    for name, spec in SKILLS.items():
        path = spec["path"]
        require(path.is_file(), f"missing skill file: {path.relative_to(ROOT)}")
        frontmatter = read_frontmatter(path)
        require(frontmatter.get("name") == name, f"{path.relative_to(ROOT)} has incorrect name frontmatter")
        require(bool(frontmatter.get("description")), f"{path.relative_to(ROOT)} needs a description")
        require(frontmatter.get("license") == "MIT", f"{path.relative_to(ROOT)} needs license: MIT")
        body = path.read_text(encoding="utf-8").lower()
        for term in spec["terms"]:
            require(term.lower() in body, f"{path.relative_to(ROOT)} is missing contract term: {term}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for skill in SKILLS:
        require(
            f"npx skills add blockedby/web-ui-quality-skills --skill {skill}" in readme,
            f"README.md is missing selective install command for {skill}",
        )
    require("python3 scripts/validate_repository.py" in readme, "README.md is missing validation command")
    require("MIT © 2026 Alexandr Kondakov" in readme, "README.md is missing license attribution")
    require((ROOT / "validate.sh").is_file(), "missing validate.sh wrapper")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    require("MIT License" in license_text, "LICENSE is not the MIT license text")
    require("Copyright 2026 Alexandr Kondakov" in license_text, "LICENSE has incorrect copyright")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    require("__pycache__/" in gitignore, ".gitignore should exclude Python caches")


def run_audit(*args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(AUDIT), *args, "--json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"audit did not emit JSON (exit {completed.returncode}): {completed.stdout[:500]!r}; {exc}"
        ) from exc
    return completed.returncode, payload


def check_audit_contract() -> None:
    valid = ROOT / "tests/fixtures/valid/index.html"
    broken = ROOT / "tests/fixtures/broken/index.html"
    code, payload = run_audit(str(valid), "--viewport", "390x844")
    require(code == 0, f"valid audit fixture returned {code}")
    require(len(payload.get("results", [])) == 1, "valid audit should produce one result")
    checks = payload["results"][0]["checks"]
    for check in ("parse", "dependencies", "links", "horizontal_overflow"):
        require(check in checks, f"audit result is missing {check} check")
    require(checks["parse"]["status"] == "pass", "valid fixture should pass parsing")
    require(checks["dependencies"]["status"] == "pass", "valid fixture should pass dependencies")
    require(checks["links"]["status"] == "pass", "valid fixture should pass local links")
    require(checks["horizontal_overflow"]["mode"] == "static", "default audit should use static overflow mode")
    require(checks["dependencies"]["external"], "valid fixture should expose an external dependency")

    code, payload = run_audit(str(broken), "--viewport", "390x844")
    require(code == 1, f"broken audit fixture should return 1, got {code}")
    checks = payload["results"][0]["checks"]
    require(checks["parse"]["status"] == "fail", "broken fixture should fail parsing")
    require(checks["dependencies"]["status"] == "fail", "broken fixture should find a missing dependency")
    require(checks["links"]["status"] == "fail", "broken fixture should find broken links")
    require(checks["horizontal_overflow"]["status"] == "warn", "broken fixture should flag static overflow risk")


def check_browser_mode_if_available() -> str:
    chromium = next(
        (
            shutil.which(candidate)
            for candidate in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")
            if shutil.which(candidate)
        ),
        None,
    )
    if chromium is None:
        return "browser mode skipped (Chromium unavailable)"
    valid = ROOT / "tests/fixtures/valid/index.html"
    code, payload = run_audit(str(valid), "--viewport", "390x844", "--browser", "--chromium", chromium)
    require(code == 0, f"browser-mode audit returned {code}")
    check = payload["results"][0]["checks"]["horizontal_overflow"]
    require(check["mode"] == "browser", "browser-mode audit did not report browser mode")
    require(check["verified"] is True, "browser-mode audit did not report a verified measurement")
    require(check["measurements"], "browser-mode audit returned no measurements")
    return "browser mode passed"


def main() -> int:
    try:
        check_repository_files()
        py_compile.compile(str(AUDIT), doraise=True)
        py_compile.compile(str(Path(__file__)), doraise=True)
        check_audit_contract()
        browser_status = check_browser_mode_if_available()
    except (OSError, py_compile.PyCompileError, ValidationError) as exc:
        print(f"validate: FAIL — {exc}", file=sys.stderr)
        return 1
    print("validate: PASS")
    print("- frontmatter, license, README, and all three skill contracts")
    print("- dependency-light audit and repository validator compile")
    print("- valid and broken audit fixtures")
    print(f"- {browser_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
