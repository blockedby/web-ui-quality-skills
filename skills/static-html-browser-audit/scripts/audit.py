#!/usr/bin/env python3
"""Read-only checks for local static HTML pages.

The default pass uses only the Python standard library. ``--browser`` adds an
optional Chromium DevTools Protocol measurement without requiring a Python
browser package.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


TOOL_VERSION = "1.0"
DEFAULT_VIEWPORT = (1280, 800)
HTML_SUFFIXES = {".html", ".htm"}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
OPTIONAL_END_TAGS = {
    "html",
    "head",
    "body",
    "li",
    "dt",
    "dd",
    "p",
    "rt",
    "rp",
    "optgroup",
    "option",
    "colgroup",
    "thead",
    "tbody",
    "tfoot",
    "tr",
    "td",
    "th",
}
AUTO_CLOSE_ON_START = {
    "li": {"li"},
    "dt": {"dt", "dd"},
    "dd": {"dt", "dd"},
    "rt": {"rt", "rp"},
    "rp": {"rt", "rp"},
    "option": {"option", "optgroup"},
    "optgroup": {"optgroup"},
    "thead": {"tbody", "tfoot"},
    "tbody": {"tbody", "tfoot"},
    "tfoot": {"tbody", "tfoot"},
    "tr": {"tr"},
    "td": {"td", "th"},
    "th": {"td", "th"},
}
RESOURCE_ATTRIBUTES = {
    "script": ("src",),
    "link": ("href",),
    "img": ("src", "srcset"),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
    "audio": ("src",),
    "iframe": ("src",),
    "object": ("data",),
    "embed": ("src",),
    "track": ("src",),
    "input": ("src",),
    "image": ("href", "xlink:href"),
    "use": ("href", "xlink:href"),
}
NON_FILE_SCHEMES = {
    "about",
    "blob",
    "chrome",
    "chrome-extension",
    "data",
    "javascript",
    "mailto",
    "sms",
    "tel",
}
CSS_URL_RE = re.compile(
    r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)]*?))\s*\)", re.IGNORECASE
)
CSS_IMPORT_RE = re.compile(
    r"@import\s+(?:\"([^\"]+)\"|'([^']+)'|url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)]*?))\s*\))",
    re.IGNORECASE,
)
CSS_WIDTH_RE = re.compile(
    r"\b(min-width|width)\s*:\s*(-?\d+(?:\.\d+)?)\s*(px|rem|em|ch|vw|vh|%)\b",
    re.IGNORECASE,
)
CSS_CALC_WIDTH_RE = re.compile(
    r"\b(min-width|width)\s*:\s*calc\(\s*100vw\s*\+\s*(\d+(?:\.\d+)?)px",
    re.IGNORECASE,
)
HTML_WIDTH_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(?:px)?\s*$", re.IGNORECASE)
LONG_TOKEN_RE = re.compile(r"\S{32,}")


@dataclass
class Finding:
    severity: str
    message: str
    source: Optional[str] = None
    line: Optional[int] = None

    def as_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "severity": self.severity,
            "message": self.message,
        }
        if self.source is not None:
            result["source"] = self.source
        if self.line is not None:
            result["line"] = self.line
        return result


@dataclass
class ReferenceInfo:
    category: str
    reference: str
    path: Optional[Path] = None
    fragment: str = ""
    reason: Optional[str] = None
    outside_root: bool = False


class HtmlDocumentParser(HTMLParser):
    """Small structural and URL inventory parser; browsers remain forgiving."""

    def __init__(self, source_path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.source_path = source_path
        self.stack: List[str] = []
        self.findings: List[Finding] = []
        self.dependencies: List[Dict[str, Any]] = []
        self.links: List[Dict[str, Any]] = []
        self.elements: List[Dict[str, Any]] = []
        self.ids: Set[str] = set()
        self.named_anchors: Set[str] = set()
        self.text_chunks: List[str] = []
        self.pre_text_chunks: List[str] = []
        self.css_sources: List[Dict[str, Any]] = []
        self._style_buffers: List[List[str]] = []
        self._pre_depth = 0

    def _line(self) -> int:
        return self.getpos()[0]

    @staticmethod
    def _attributes(attrs: Sequence[Tuple[str, Optional[str]]]) -> Dict[str, Optional[str]]:
        return {name.lower(): value for name, value in attrs}

    def _add_dependency(self, reference: str, tag: str, attribute: str, line: int, kind: str = "html") -> None:
        value = reference.strip()
        if value:
            self.dependencies.append(
                {
                    "reference": value,
                    "tag": tag,
                    "attribute": attribute,
                    "source": str(self.source_path),
                    "line": line,
                    "kind": kind,
                }
            )

    def _add_resource_attributes(
        self, tag: str, attrs: Sequence[Tuple[str, Optional[str]]], line: int
    ) -> None:
        for name, value in attrs:
            name = name.lower()
            if value is None or name not in RESOURCE_ATTRIBUTES.get(tag, ()):
                continue
            if name == "srcset":
                for candidate in value.split(","):
                    candidate = candidate.strip()
                    if not candidate:
                        continue
                    self._add_dependency(candidate.split()[0], tag, name, line)
            else:
                self._add_dependency(value, tag, name, line)

    def _record_start(
        self,
        tag: str,
        attrs: Sequence[Tuple[str, Optional[str]]],
        self_closing: bool = False,
    ) -> None:
        tag = tag.lower()
        line = self._line()
        attributes = [(name.lower(), value) for name, value in attrs]
        attr_map = self._attributes(attributes)
        self.elements.append({"tag": tag, "attributes": attr_map, "line": line})

        element_id = attr_map.get("id")
        if element_id:
            self.ids.add(element_id)
        element_name = attr_map.get("name")
        if element_name:
            self.named_anchors.add(element_name)

        self._add_resource_attributes(tag, attributes, line)
        inline_style = attr_map.get("style")
        if inline_style:
            self.css_sources.append(
                {
                    "origin": self.source_path,
                    "text": inline_style,
                    "line": line,
                    "kind": "inline-style",
                }
            )

        if tag in {"a", "area"}:
            href = attr_map.get("href")
            if href is not None and href.strip():
                self.links.append(
                    {"reference": href.strip(), "tag": tag, "line": line, "source": str(self.source_path)}
                )

        if tag == "style" and not self_closing:
            self._style_buffers.append([])
        if tag == "pre" and not self_closing:
            self._pre_depth += 1

        if self_closing or tag in VOID_ELEMENTS:
            return
        while self.stack and self.stack[-1] in AUTO_CLOSE_ON_START:
            if tag not in AUTO_CLOSE_ON_START[self.stack[-1]]:
                break
            self.stack.pop()
        self.stack.append(tag)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self._record_start(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self._record_start(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        line = self._line()
        if tag == "style" and self._style_buffers:
            css_text = "".join(self._style_buffers.pop())
            self.css_sources.append(
                {"origin": self.source_path, "text": css_text, "line": line, "kind": "inline-style-block"}
            )
        if tag == "pre" and self._pre_depth:
            self._pre_depth -= 1

        if tag not in self.stack:
            self.findings.append(
                Finding("error", f"Closing tag </{tag}> has no matching open tag", str(self.source_path), line)
            )
            return
        index = len(self.stack) - 1 - self.stack[::-1].index(tag)
        between = self.stack[index + 1 :]
        non_optional = [item for item in between if item not in OPTIONAL_END_TAGS]
        if non_optional:
            self.findings.append(
                Finding(
                    "error",
                    f"Closing tag </{tag}> crosses still-open element(s): {', '.join(non_optional)}",
                    str(self.source_path),
                    line,
                )
            )
        self.stack = self.stack[:index]

    def handle_data(self, data: str) -> None:
        if not data:
            return
        if self._style_buffers:
            self._style_buffers[-1].append(data)
        else:
            self.text_chunks.append(data)
        if self._pre_depth:
            self.pre_text_chunks.append(data)

    def finish(self) -> None:
        if self._style_buffers:
            for buffer in self._style_buffers:
                self.css_sources.append(
                    {
                        "origin": self.source_path,
                        "text": "".join(buffer),
                        "line": None,
                        "kind": "unterminated-style-block",
                    }
                )
        for tag in reversed(self.stack):
            if tag not in OPTIONAL_END_TAGS:
                self.findings.append(
                    Finding("error", f"Unclosed element <{tag}>", str(self.source_path), None)
                )


def parse_html(path: Path) -> Tuple[str, HtmlDocumentParser]:
    parser = HtmlDocumentParser(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        text = path.read_text(encoding="utf-8", errors="replace")
        parser.findings.append(
            Finding("error", f"HTML is not valid UTF-8: {exc}", str(path), None)
        )
    except OSError as exc:
        return "", parser_with_error(parser, f"Cannot read HTML: {exc}")

    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # HTMLParser generally recovers, but keep the check explicit.
        parser.findings.append(Finding("error", f"HTML parser error: {exc}", str(path), None))
    parser.finish()
    return text, parser


def parser_with_error(parser: HtmlDocumentParser, message: str) -> HtmlDocumentParser:
    parser.findings.append(Finding("error", message, str(parser.source_path), None))
    return parser


def common_root(paths: Sequence[Path]) -> Path:
    parents = [str(path.parent) for path in paths]
    try:
        return Path(os.path.commonpath(parents)).resolve()
    except ValueError:
        return Path.cwd().absolute()


def is_within(path: Path, root: Path) -> bool:
    try:
        return os.path.commonpath([str(path), str(root)]) == str(root)
    except ValueError:
        return False


def classify_reference(raw: str, origin: Path, root: Path) -> ReferenceInfo:
    reference = raw.strip()
    if not reference:
        return ReferenceInfo("ignored", reference, reason="empty reference")
    try:
        parsed = urlsplit(reference)
    except ValueError as exc:
        return ReferenceInfo("invalid", reference, reason=f"malformed URL: {exc}")
    scheme = parsed.scheme.lower()
    if reference.startswith("//") or scheme not in {"", "file"}:
        if scheme in NON_FILE_SCHEMES:
            return ReferenceInfo("ignored", reference, fragment=unquote(parsed.fragment), reason=f"{scheme} scheme")
        return ReferenceInfo("external", reference, fragment=unquote(parsed.fragment), reason=f"{scheme or 'protocol-relative'} URL")

    fragment = unquote(parsed.fragment)
    path_part = unquote(parsed.path)
    if not path_part:
        return ReferenceInfo("ignored", reference, fragment=fragment, reason="fragment or query only")
    if scheme == "file":
        candidate = Path(path_part)
    elif path_part.startswith("/"):
        candidate = root / path_part.lstrip("/")
    else:
        candidate = origin.parent / path_part
    candidate = Path(os.path.normpath(str(candidate))).resolve()
    return ReferenceInfo(
        "local",
        reference,
        path=candidate,
        fragment=fragment,
        outside_root=not is_within(candidate, root),
    )


def split_css_reference(match: re.Match[str]) -> str:
    for group in match.groups():
        if group is not None:
            return group.strip()
    return ""


def css_references(text: str) -> Iterable[Tuple[str, int, str]]:
    seen: Set[Tuple[str, int]] = set()
    for match in CSS_URL_RE.finditer(text):
        reference = split_css_reference(match)
        if reference:
            key = (reference, match.start())
            seen.add(key)
            yield reference, text.count("\n", 0, match.start()) + 1, "css-url"
    for match in CSS_IMPORT_RE.finditer(text):
        reference = split_css_reference(match)
        if reference:
            key = (reference, match.start())
            if key not in seen:
                yield reference, text.count("\n", 0, match.start()) + 1, "css-import"


def finding_status(findings: Sequence[Finding]) -> str:
    if any(item.severity == "error" for item in findings):
        return "fail"
    if any(item.severity == "warning" for item in findings):
        return "warn"
    return "pass"


def dependency_record(
    reference: str,
    origin: Path,
    line: Optional[int],
    kind: str,
    tag: str = "css",
    attribute: str = "url",
) -> Dict[str, Any]:
    return {
        "reference": reference.strip(),
        "tag": tag,
        "attribute": attribute,
        "source": str(origin),
        "line": line,
        "kind": kind,
    }


def audit_dependencies(
    path: Path,
    parser: HtmlDocumentParser,
    root: Path,
) -> Tuple[Dict[str, Any], List[Tuple[Path, str, Optional[int]]]]:
    records: List[Dict[str, Any]] = list(parser.dependencies)
    for css_source in parser.css_sources:
        for reference, line, kind in css_references(css_source["text"]):
            records.append(
                dependency_record(
                    reference,
                    Path(css_source["origin"]),
                    line if line else css_source.get("line"),
                    kind,
                )
            )

    local: List[Dict[str, Any]] = []
    external: List[Dict[str, Any]] = []
    non_file: List[Dict[str, Any]] = []
    findings: List[Finding] = []
    css_queue: List[Path] = []
    scanned_css: Set[Path] = set()
    css_texts: List[Tuple[Path, str, Optional[int]]] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        reference = record["reference"]
        origin = Path(record["source"])
        info = classify_reference(reference, origin, root)
        base = {
            "reference": reference,
            "source": record["source"],
            "line": record.get("line"),
            "kind": record.get("kind", "html"),
            "tag": record.get("tag"),
            "attribute": record.get("attribute"),
        }
        if info.category == "external":
            base["status"] = "unverified"
            base["reason"] = info.reason
            external.append(base)
            continue
        if info.category == "invalid":
            base["status"] = "invalid"
            base["reason"] = info.reason
            non_file.append(base)
            findings.append(
                Finding(
                    "error",
                    f"Malformed dependency URL: {reference} ({info.reason})",
                    record.get("source"),
                    record.get("line"),
                )
            )
            continue
        if info.category == "ignored":
            base["status"] = "non-file"
            base["reason"] = info.reason
            non_file.append(base)
            continue

        assert info.path is not None
        base["resolved"] = str(info.path)
        base["status"] = "present" if info.path.exists() else "missing"
        if info.outside_root:
            base["outside_root"] = True
            findings.append(
                Finding(
                    "warning",
                    f"Local dependency resolves outside the audit root: {reference} -> {info.path}",
                    record.get("source"),
                    record.get("line"),
                )
            )
        if not info.path.exists():
            local.append(base)
            findings.append(
                Finding(
                    "error",
                    f"Missing local dependency: {reference} -> {info.path}",
                    record.get("source"),
                    record.get("line"),
                )
            )
            continue
        local.append(base)
        if info.path.suffix.lower() == ".css" and info.path not in scanned_css:
            scanned_css.add(info.path)
            css_queue.append(info.path)

        while css_queue:
            css_path = css_queue.pop(0)
            try:
                css_text = css_path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                findings.append(
                    Finding("warning", f"Local CSS is not valid UTF-8: {exc}", str(css_path), None)
                )
                continue
            except OSError as exc:
                findings.append(Finding("warning", f"Cannot inspect local CSS: {exc}", str(css_path), None))
                continue
            css_texts.append((css_path, css_text, None))
            for reference, line, kind in css_references(css_text):
                records.append(dependency_record(reference, css_path, line, kind))

    dependencies = {
        "status": finding_status(findings),
        "local": local,
        "external": external,
        "non_file": non_file,
        "findings": [item.as_dict() for item in findings],
    }
    return dependencies, css_texts


def target_with_index(path: Path) -> Optional[Path]:
    if path.is_dir():
        for name in ("index.html", "index.htm"):
            candidate = path / name
            if candidate.is_file():
                return candidate
        return None
    return path if path.exists() else None


def document_fragments(path: Path, cache: Dict[Path, Set[str]]) -> Set[str]:
    path = Path(str(path)).resolve()
    if path in cache:
        return cache[path]
    _, parser = parse_html(path)
    fragments = set(parser.ids) | set(parser.named_anchors)
    cache[path] = fragments
    return fragments


def audit_links(
    path: Path,
    parser: HtmlDocumentParser,
    root: Path,
) -> Dict[str, Any]:
    findings: List[Finding] = []
    broken: List[Dict[str, Any]] = []
    external: List[Dict[str, Any]] = []
    cache: Dict[Path, Set[str]] = {path: set(parser.ids) | set(parser.named_anchors)}
    for link in parser.links:
        reference = link["reference"]
        info = classify_reference(reference, path, root)
        if info.category == "external":
            external.append(
                {
                    "reference": reference,
                    "source": link["source"],
                    "line": link["line"],
                    "status": "unverified",
                }
            )
            continue
        if info.category == "invalid":
            findings.append(
                Finding(
                    "error",
                    f"Malformed local link URL: {reference} ({info.reason})",
                    link["source"],
                    link["line"],
                )
            )
            broken.append({**link, "status": "invalid"})
            continue
        if info.category == "ignored":
            if info.fragment and info.fragment not in cache[path]:
                item = {**link, "status": "missing-fragment", "fragment": info.fragment}
                broken.append(item)
                findings.append(
                    Finding(
                        "error",
                        f"Broken same-document fragment: #{info.fragment}",
                        link["source"],
                        link["line"],
                    )
                )
            continue

        assert info.path is not None
        target = target_with_index(info.path)
        if target is None:
            item = {**link, "status": "missing-target", "resolved": str(info.path)}
            broken.append(item)
            findings.append(
                Finding(
                    "error",
                    f"Broken local link: {reference} -> {info.path}",
                    link["source"],
                    link["line"],
                )
            )
            continue
        if info.outside_root:
            findings.append(
                Finding(
                    "warning",
                    f"Local link resolves outside the audit root: {reference} -> {target}",
                    link["source"],
                    link["line"],
                )
            )
        if info.fragment and target.suffix.lower() in HTML_SUFFIXES:
            fragments = document_fragments(target, cache)
            if info.fragment not in fragments:
                item = {
                    **link,
                    "status": "missing-fragment",
                    "resolved": str(target),
                    "fragment": info.fragment,
                }
                broken.append(item)
                findings.append(
                    Finding(
                        "error",
                        f"Broken local fragment: {reference} -> {target}",
                        link["source"],
                        link["line"],
                    )
                )

    return {
        "status": finding_status(findings),
        "checked": len(parser.links),
        "broken": broken,
        "external": external,
        "findings": [item.as_dict() for item in findings],
    }


def length_in_pixels(value: float, unit: str, viewport: Tuple[int, int]) -> Optional[float]:
    unit = unit.lower()
    if unit == "px":
        return value
    if unit in {"rem", "em"}:
        return value * 16
    if unit == "ch":
        return value * 8
    if unit == "vw":
        return value * viewport[0] / 100
    if unit == "vh":
        return value * viewport[1] / 100
    return None


def overflow_risks(
    parser: HtmlDocumentParser,
    css_sources: Sequence[Tuple[Path, str, Optional[int]]],
    viewport: Tuple[int, int],
) -> List[Dict[str, Any]]:
    width, _ = viewport
    risks: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str, Optional[int]]] = set()

    def add(kind: str, message: str, source: Optional[Path], line: Optional[int]) -> None:
        key = (kind, message, line)
        if key in seen:
            return
        seen.add(key)
        risks.append(
            {
                "kind": kind,
                "message": message,
                "source": str(source) if source is not None else None,
                "line": line,
            }
        )

    all_css_sources: List[Tuple[Path, str, Optional[int]]] = []
    for source in parser.css_sources:
        all_css_sources.append((Path(source["origin"]), source["text"], source.get("line")))
    all_css_sources.extend(css_sources)
    for source, text, source_line in all_css_sources:
        for match in CSS_WIDTH_RE.finditer(text):
            property_name = match.group(1).lower()
            value = float(match.group(2))
            pixels = length_in_pixels(value, match.group(3), viewport)
            if pixels is not None and pixels > width + 1:
                local_line = text.count("\n", 0, match.start()) + 1
                line = (source_line + local_line - 1) if source_line is not None else local_line
                add(
                    "fixed-width",
                    f"{property_name}: {match.group(2)}{match.group(3)} is wider than the {width}px viewport",
                    source,
                    line,
                )
        for match in CSS_CALC_WIDTH_RE.finditer(text):
            extra = float(match.group(2))
            local_line = text.count("\n", 0, match.start()) + 1
            line = (source_line + local_line - 1) if source_line is not None else local_line
            add(
                "calc-width",
                f"{match.group(1).lower()}: calc(100vw + {match.group(2)}px) adds {extra:g}px beyond the viewport",
                source,
                line,
            )

    for element in parser.elements:
        attributes = element["attributes"]
        raw_width = attributes.get("width")
        if raw_width:
            match = HTML_WIDTH_RE.match(raw_width)
            if match and float(match.group(1)) > width + 1:
                add(
                    "html-width",
                    f"<{element['tag']} width=\"{raw_width}\"> is wider than the {width}px viewport",
                    parser.source_path,
                    element["line"],
                )

    css_text = "\n".join(text for _, text, _ in all_css_sources)
    document_text = " ".join(parser.text_chunks)
    if re.search(r"white-space\s*:\s*nowrap", css_text, re.IGNORECASE):
        long_tokens = LONG_TOKEN_RE.findall(document_text)
        if long_tokens:
            add(
                "nowrap-content",
                "white-space: nowrap appears with an unbreakable text token; inspect its computed width",
                parser.source_path,
                None,
            )

    for pre_text in parser.pre_text_chunks:
        for line_number, line in enumerate(pre_text.splitlines(), start=1):
            if len(line) * 8 > width + 1:
                add(
                    "preformatted-content",
                    f"preformatted line is approximately {len(line) * 8}px wide at an {width}px viewport",
                    parser.source_path,
                    line_number,
                )
                break

    for token in LONG_TOKEN_RE.findall(document_text):
        if len(token) * 8 > width + 1:
            add(
                "unbreakable-content",
                f"unbreakable text token is approximately {len(token) * 8}px wide at an {width}px viewport",
                parser.source_path,
                None,
            )
            break
    return risks


class WebSocketError(RuntimeError):
    pass


class SimpleWebSocket:
    """Tiny text-frame client for the subset of CDP used by this helper."""

    def __init__(self, url: str, timeout: float = 5.0) -> None:
        parsed = urlsplit(url)
        if parsed.scheme != "ws" or not parsed.hostname or not parsed.port:
            raise WebSocketError(f"Unsupported DevTools websocket URL: {url}")
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        ).encode("ascii")
        self.sock.sendall(request)
        response = self._read_http_headers()
        if not response.startswith(b"HTTP/1.1 101"):
            self.close()
            raise WebSocketError(f"DevTools websocket handshake failed: {response[:120]!r}")

    def _read_http_headers(self) -> bytes:
        data = bytearray()
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise WebSocketError("DevTools websocket closed during handshake")
            data.extend(chunk)
            if len(data) > 64 * 1024:
                raise WebSocketError("DevTools websocket handshake is too large")
        return bytes(data)

    def _read_exact(self, size: int, deadline: float) -> bytes:
        data = bytearray()
        while len(data) < size:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Timed out waiting for DevTools message")
            self.sock.settimeout(min(remaining, 0.25))
            try:
                chunk = self.sock.recv(size - len(data))
            except socket.timeout:
                continue
            if not chunk:
                raise WebSocketError("DevTools websocket closed")
            data.extend(chunk)
        return bytes(data)

    def _send_frame(self, payload: bytes, opcode: int = 1) -> None:
        length = len(payload)
        first = 0x80 | (opcode & 0x0F)
        if length < 126:
            header = bytes([first, 0x80 | length])
        elif length < 65536:
            header = bytes([first, 0x80 | 126]) + struct.pack("!H", length)
        else:
            header = bytes([first, 0x80 | 127]) + struct.pack("!Q", length)
        mask = os.urandom(4)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def _receive_frame(self, deadline: float) -> Tuple[int, bytes]:
        first, second = self._read_exact(2, deadline)
        opcode = first & 0x0F
        length = second & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._read_exact(2, deadline))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._read_exact(8, deadline))[0]
        if length > 20 * 1024 * 1024:
            raise WebSocketError("DevTools websocket frame is too large")
        if second & 0x80:
            mask = self._read_exact(4, deadline)
            payload = self._read_exact(length, deadline)
            payload = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        else:
            payload = self._read_exact(length, deadline)
        if opcode == 9:  # ping
            self._send_frame(payload, opcode=10)
        return opcode, payload

    def send_json(self, value: Dict[str, Any]) -> None:
        self._send_frame(json.dumps(value, separators=(",", ":")).encode("utf-8"))

    def receive_json(self, timeout: float = 10.0) -> Dict[str, Any]:
        deadline = time.monotonic() + timeout
        while True:
            opcode, payload = self._receive_frame(deadline)
            if opcode == 8:
                raise WebSocketError("DevTools websocket closed")
            if opcode == 1:
                return json.loads(payload.decode("utf-8"))

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass


class ChromiumProbe:
    """Disposable, network-blocked Chromium session for layout measurements."""

    def __init__(self, executable: str, allow_page_javascript: bool = False) -> None:
        self.executable = executable
        self.allow_page_javascript = allow_page_javascript
        self.temp_dir = tempfile.TemporaryDirectory(prefix="static-html-audit-")
        self.process: Optional[subprocess.Popen[bytes]] = None
        self.websocket: Optional[SimpleWebSocket] = None
        self.target_id: Optional[str] = None
        self.message_id = 0
        self.start()

    def _request_json(self, url: str, method: str = "GET") -> Any:
        request = Request(url, method=method)
        with urlopen(request, timeout=1.5) as response:
            return json.loads(response.read().decode("utf-8"))

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe_socket:
            probe_socket.bind(("127.0.0.1", 0))
            port = probe_socket.getsockname()[1]
        command = [
            self.executable,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-sync",
            "--no-first-run",
            "--no-default-browser-check",
            "--remote-debugging-address=127.0.0.1",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={self.temp_dir.name}",
            # Prevent page resources from reaching a network host. file:// resources still work.
            "--host-resolver-rules=MAP * ~NOTFOUND",
            "about:blank",
        ]
        if not self.allow_page_javascript:
            command.append("--disable-javascript")
        try:
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as exc:
            self.close()
            raise RuntimeError(f"Cannot start Chromium ({self.executable}): {exc}") from exc

        base_url = f"http://127.0.0.1:{port}"
        listing: Optional[List[Dict[str, Any]]] = None
        for _ in range(100):
            if self.process.poll() is not None:
                self.close()
                raise RuntimeError("Chromium exited before its DevTools endpoint became ready")
            try:
                value = self._request_json(base_url + "/json/list")
                if isinstance(value, list):
                    listing = value
                    break
            except Exception:
                time.sleep(0.05)
        if listing is None:
            self.close()
            raise RuntimeError("Timed out waiting for Chromium DevTools endpoint")

        page = next((item for item in listing if item.get("type") == "page"), None)
        if page is None:
            page = self._request_json(base_url + "/json/new?about:blank", method="PUT")
        websocket_url = page.get("webSocketDebuggerUrl")
        self.target_id = page.get("id")
        if not websocket_url or not self.target_id:
            self.close()
            raise RuntimeError("Chromium did not expose a page DevTools target")
        try:
            self.websocket = SimpleWebSocket(websocket_url)
            self.call("Page.enable")
            self.call("Runtime.enable")
            self.call("Network.enable")
            self.call(
                "Network.setBlockedURLs",
                {"urls": ["http://*", "https://*", "ws://*", "wss://*"]},
            )
        except Exception:
            self.close()
            raise

    def call(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: float = 10.0) -> Dict[str, Any]:
        if self.websocket is None:
            raise RuntimeError("Chromium probe is not connected")
        self.message_id += 1
        message_id = self.message_id
        payload: Dict[str, Any] = {"id": message_id, "method": method}
        if params is not None:
            payload["params"] = params
        self.websocket.send_json(payload)
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"Timed out waiting for Chromium method {method}")
            message = self.websocket.receive_json(timeout=remaining)
            if message.get("id") != message_id:
                continue
            if "error" in message:
                raise RuntimeError(f"Chromium {method} failed: {message['error']}")
            result = message.get("result", {})
            if "exceptionDetails" in result:
                raise RuntimeError(f"Chromium evaluation failed: {result['exceptionDetails']}")
            return result

    def evaluate(self, expression: str, timeout: float = 10.0) -> Any:
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
            timeout=timeout,
        )
        remote = result.get("result", {})
        if remote.get("subtype") == "error":
            raise RuntimeError(f"Chromium expression failed: {remote}")
        return remote.get("value")

    def measure(self, path: Path, viewport: Tuple[int, int]) -> Dict[str, Any]:
        width, height = viewport
        self.call(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": False,
                "screenWidth": width,
                "screenHeight": height,
            },
        )
        navigation = self.call("Page.navigate", {"url": path.absolute().as_uri()})
        if navigation.get("errorText"):
            raise RuntimeError(navigation["errorText"])
        ready_deadline = time.monotonic() + 8
        while time.monotonic() < ready_deadline:
            state = self.evaluate("document.readyState", timeout=2)
            if state == "complete":
                break
            time.sleep(0.05)
        time.sleep(0.1)
        expression = r"""
(() => {
  const root = document.documentElement;
  const body = document.body;
  const width = window.innerWidth;
  const elements = Array.from(document.querySelectorAll('*'));
  const bounds = elements.map((element) => {
    const rect = element.getBoundingClientRect();
    return {
      tag: element.tagName.toLowerCase(),
      id: element.id || '',
      className: typeof element.className === 'string' ? element.className.slice(0, 80) : '',
      left: Math.round(rect.left * 100) / 100,
      right: Math.round(rect.right * 100) / 100,
      width: Math.round(rect.width * 100) / 100
    };
  }).filter((item) => item.right > width + 1 || item.left < -1);
  bounds.sort((a, b) => Math.max(b.right - width, -b.left) - Math.max(a.right - width, -a.left));
  return {
    innerWidth: width,
    innerHeight: window.innerHeight,
    scrollWidth: root ? root.scrollWidth : 0,
    bodyScrollWidth: body ? body.scrollWidth : 0,
    offenders: bounds.slice(0, 20)
  };
})()
"""
        value = self.evaluate(expression)
        if not isinstance(value, dict):
            raise RuntimeError("Chromium returned no layout measurement")
        value["viewport"] = {"width": width, "height": height}
        value["overflow"] = (
            max(float(value.get("scrollWidth", 0)), float(value.get("bodyScrollWidth", 0))) > width + 1
            or bool(value.get("offenders"))
        )
        return value

    def close(self) -> None:
        if self.websocket is not None:
            self.websocket.close()
            self.websocket = None
        if self.process is not None:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except Exception:
                try:
                    self.process.kill()
                    self.process.wait(timeout=2)
                except Exception:
                    pass
            self.process = None
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def __enter__(self) -> "ChromiumProbe":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


def locate_chromium(requested: Optional[str]) -> Optional[str]:
    candidates = [requested] if requested else []
    candidates.extend(["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"])
    for candidate in candidates:
        if candidate:
            found = shutil.which(candidate) or (candidate if Path(candidate).is_file() else None)
            if found:
                return found
    return None


def audit_file(
    path: Path,
    root: Path,
    viewports: Sequence[Tuple[int, int]],
    browser: Optional[ChromiumProbe],
    browser_error: Optional[str],
) -> Dict[str, Any]:
    text, parser = parse_html(path)
    parse_check = {"status": finding_status(parser.findings), "findings": [item.as_dict() for item in parser.findings]}
    dependencies, css_texts = audit_dependencies(path, parser, root)
    links = audit_links(path, parser, root)

    static_risks: List[Dict[str, Any]] = []
    overflow_findings: List[Finding] = []
    for viewport in viewports:
        risks = overflow_risks(parser, css_texts, viewport)
        static_risks.append(
            {
                "viewport": {"width": viewport[0], "height": viewport[1]},
                "risks": risks,
            }
        )
        for risk in risks:
            overflow_findings.append(
                Finding(
                    "warning",
                    risk["message"],
                    risk.get("source"),
                    risk.get("line"),
                )
            )

    measurements: List[Dict[str, Any]] = []
    if browser is not None:
        for viewport in viewports:
            try:
                measurement = browser.measure(path, viewport)
                measurements.append(measurement)
                if measurement.get("overflow"):
                    overflow_findings.append(
                        Finding(
                            "error",
                            "Rendered document extends beyond the viewport",
                            str(path),
                            None,
                        )
                    )
            except Exception as exc:
                overflow_findings.append(
                    Finding("error", f"Chromium overflow measurement failed: {exc}", str(path), None)
                )
    elif browser_error:
        overflow_findings.append(
            Finding("warning", f"Browser overflow measurement not run: {browser_error}", str(path), None)
        )

    if browser is not None:
        mode = "browser"
        verified = bool(measurements) and not any(
            finding.severity == "error" and "measurement failed" in finding.message
            for finding in overflow_findings
        )
    else:
        mode = "static"
        verified = False
    overflow_check = {
        "status": finding_status(overflow_findings),
        "mode": mode,
        "verified": verified,
        "risks": static_risks,
        "measurements": measurements,
        "findings": [item.as_dict() for item in overflow_findings],
    }

    checks = {
        "parse": parse_check,
        "dependencies": dependencies,
        "links": links,
        "horizontal_overflow": overflow_check,
    }
    errors = 0
    warnings = 0
    for check in checks.values():
        for finding in check.get("findings", []):
            if finding["severity"] == "error":
                errors += 1
            elif finding["severity"] == "warning":
                warnings += 1
    return {
        "path": str(path),
        "viewport": {"width": viewports[0][0], "height": viewports[0][1]} if len(viewports) == 1 else None,
        "viewports": [{"width": width, "height": height} for width, height in viewports],
        "checks": checks,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "external_dependencies": len(dependencies["external"]),
        },
        "_source_text_length": len(text),
    }


def expand_inputs(raw_paths: Sequence[str]) -> List[Path]:
    paths: Set[Path] = set()
    for raw in raw_paths:
        candidate = Path(raw).expanduser()
        if not candidate.exists():
            raise ValueError(f"Input path does not exist: {raw}")
        if candidate.is_dir():
            for child in candidate.rglob("*"):
                if child.is_file() and child.suffix.lower() in HTML_SUFFIXES:
                    paths.add(child.resolve())
        elif candidate.suffix.lower() in HTML_SUFFIXES:
            paths.add(candidate.resolve())
        else:
            raise ValueError(f"Input is not an HTML file or directory: {raw}")
    if not paths:
        raise ValueError("No .html or .htm files found in the supplied paths")
    return sorted(paths, key=lambda item: str(item))


def parse_viewport(raw: str) -> Tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*[xX×]\s*(\d+)\s*", raw)
    if not match:
        raise ValueError(f"Invalid viewport {raw!r}; use WIDTHxHEIGHT, for example 390x844")
    width, height = int(match.group(1)), int(match.group(2))
    if width < 1 or height < 1:
        raise ValueError("Viewport dimensions must be positive")
    return width, height


def finding_from_dict(value: Dict[str, Any]) -> Finding:
    return Finding(value["severity"], value["message"], value.get("source"), value.get("line"))


def format_finding(value: Dict[str, Any]) -> str:
    location = ""
    if value.get("source"):
        location = f" ({value['source']}"
        if value.get("line") is not None:
            location += f":{value['line']}"
        location += ")"
    return f"    {value['severity'].upper()}: {value['message']}{location}"


def print_human_report(payload: Dict[str, Any]) -> None:
    print("Static HTML browser audit")
    print(
        "Viewport(s): "
        + ", ".join(f"{item['width']}x{item['height']}" for item in payload["viewports"])
        + f" | root: {payload['root']}"
    )
    for result in payload["results"]:
        print(f"\n{result['path']}")
        checks = result["checks"]
        labels = {
            "parse": "parse errors",
            "dependencies": "dependencies",
            "links": "broken local links",
            "horizontal_overflow": "horizontal overflow",
        }
        for name in ("parse", "dependencies", "links", "horizontal_overflow"):
            check = checks[name]
            extra = ""
            if name == "dependencies":
                extra = f"; {len(check.get('local', []))} local, {len(check.get('external', []))} external"
            elif name == "links":
                extra = f"; {len(check.get('broken', []))} broken of {check.get('checked', 0)} checked"
            elif name == "horizontal_overflow":
                extra = f"; mode={check.get('mode')}, verified={check.get('verified')}"
            print(f"  {labels[name]}: {check['status'].upper()}{extra}")
            for finding in check.get("findings", []):
                print(format_finding(finding))
        summary = result["summary"]
        print(f"  summary: {summary['errors']} error(s), {summary['warnings']} warning(s)")
    summary = payload["summary"]
    print(
        f"\nConclusion: {summary['errors']} error(s), {summary['warnings']} warning(s) "
        f"across {summary['files']} file(s)."
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only checks for local static HTML: parsing, dependencies, links, and overflow."
    )
    parser.add_argument("paths", nargs="+", help="HTML files or directories to audit")
    parser.add_argument(
        "--viewport",
        action="append",
        metavar="WIDTHxHEIGHT",
        help="viewport for overflow checks; repeat for multiple viewports (default: 1280x800)",
    )
    parser.add_argument("--root", type=Path, help="site root used for leading / references")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit machine-readable JSON")
    parser.add_argument(
        "--browser",
        action="store_true",
        help="measure rendered overflow with disposable local Chromium when available",
    )
    parser.add_argument("--chromium", metavar="PATH", help="Chromium/Chrome executable for --browser")
    parser.add_argument(
        "--allow-page-javascript",
        action="store_true",
        help="allow local page scripts in --browser mode (off by default)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return failure for warnings as well as errors",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    try:
        paths = expand_inputs(args.paths)
        viewports = [parse_viewport(value) for value in args.viewport] if args.viewport else [DEFAULT_VIEWPORT]
        root = args.root.expanduser().resolve() if args.root else common_root(paths)
        if not root.exists() or not root.is_dir():
            raise ValueError(f"Audit root is not a directory: {root}")
    except ValueError as exc:
        parser.error(str(exc))

    browser: Optional[ChromiumProbe] = None
    browser_error: Optional[str] = None
    if args.browser:
        executable = locate_chromium(args.chromium)
        if executable is None:
            browser_error = "no Chromium/Chrome executable found"
        else:
            try:
                browser = ChromiumProbe(executable, args.allow_page_javascript)
            except Exception as exc:
                browser_error = str(exc)

    try:
        results = [audit_file(path, root, viewports, browser, browser_error) for path in paths]
    finally:
        if browser is not None:
            browser.close()

    for result in results:
        result.pop("_source_text_length", None)
    error_count = sum(result["summary"]["errors"] for result in results)
    warning_count = sum(result["summary"]["warnings"] for result in results)
    external_count = sum(result["summary"]["external_dependencies"] for result in results)
    payload = {
        "tool": "static-html-browser-audit",
        "version": TOOL_VERSION,
        "root": str(root),
        "viewports": [{"width": width, "height": height} for width, height in viewports],
        "results": results,
        "summary": {
            "files": len(results),
            "errors": error_count,
            "warnings": warning_count,
            "external_dependencies": external_count,
        },
    }
    if args.json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human_report(payload)
    if error_count or (args.strict and warning_count):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
