"""Markdown section extraction shared by source and portable skill views."""

from __future__ import annotations

import re


SECTION_HEADING_PATTERN = re.compile(r"^[ ]{0,3}##\s+(.+?)\s*$")
FENCE_DELIMITER_PATTERN = re.compile(r"^[ ]{0,3}((?:\x60){3,}|~{3,})")


def trim_boundary_blank_lines(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def extract_top_level_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    active_fence: tuple[str, int] | None = None

    def flush() -> None:
        nonlocal current_heading, current_lines
        if current_heading is not None:
            sections.append(
                (
                    current_heading,
                    trim_boundary_blank_lines("\n".join(current_lines)),
                )
            )
        current_heading = None
        current_lines = []

    for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        fence_match = FENCE_DELIMITER_PATTERN.match(line)
        if fence_match:
            delimiter = fence_match.group(1)
            key = (delimiter[0], len(delimiter))
            if active_fence is None:
                active_fence = key
            elif key[0] == active_fence[0] and key[1] >= active_fence[1]:
                active_fence = None
            if current_heading is not None:
                current_lines.append(line)
            continue
        heading_match = SECTION_HEADING_PATTERN.match(line)
        if active_fence is None and heading_match:
            flush()
            current_heading = heading_match.group(1).strip()
        elif current_heading is not None:
            current_lines.append(line)
    flush()
    return sections
