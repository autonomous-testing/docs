"""Fix and check the Markdown export (`<page>/index.md`, llms-full.txt) after `zensical build`.

Zensical's llmstxt export converts each page's HTML to Markdown and drops what agents need:

- `pymdownx.tabbed` labels (`=== "Claude Code"`): each tab gets a heading with its label again.
- code block titles (`title=".vscode/mcp.json"`): the bare filename line goes back into the fence as `title="..."`.
- escaped home paths (`\\~/.codex/config.toml`): written as `~/.codex/config.toml`.

The script fixes every page, then fails when a tabbed page still lacks a label, a title or a `~` path.

Usage: python scripts/markdown-export.py [site]
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
PREFIX = 40


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.parent, self.children = tag, parent, []
        self.classes = set((dict(attrs).get("class") or "").split())

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def elements(self):
        return [c for c in self.children if isinstance(c, Node)]

    def walk(self):
        yield self
        for c in self.elements():
            yield from c.walk()


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("root", [], None)
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        node = self.cur
        while node.parent and node.tag != tag:
            node = node.parent
        if node.parent:
            self.cur = node.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def norm(text):
    text = re.sub(r"\]\(<[^>]*>\)|\]\([^)]*\)", "]", text)
    return re.sub(r"[\W_]+", "", text).lower()


def article(root):
    return next((n for n in root.walk() if "md-content__inner" in n.classes), root)


def tabs(node):
    """(label, key text) for every tab in document order, nested tabs after their parent tab."""
    out = []
    for el in node.elements():
        if "tabbed-set" in el.classes:
            labels = [l.text().strip() for c in el.elements() if "tabbed-labels" in c.classes for l in c.elements()]
            content = next((c for c in el.elements() if "tabbed-content" in c.classes), None)
            blocks = [b for b in content.elements() if "tabbed-block" in b.classes] if content else []
            for index, (label, block) in enumerate(zip(labels, blocks)):
                first = next((c for c in block.elements() if norm(c.text())), block)
                out.append((label, norm(first.text())[:PREFIX], index == 0))
                out.extend(tabs(block))
        else:
            out.extend(tabs(el))
    return out


def stream(lines):
    """Normalised text of the page with, per character, the line a heading must go before."""
    chars, where, fence, first = [], [], None, False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fence, first = (i, True) if fence is None else (None, False)
            continue
        anchor = fence if first else i
        first = False
        for ch in norm(line):
            chars.append(ch)
            where.append(anchor)
    return "".join(chars), where


def last_heading_level(lines, upto):
    level, fence = 3, False
    for line in lines[:upto]:
        if FENCE.match(line):
            fence = not fence
        elif not fence and (m := HEADING.match(line)):
            level = len(m.group(1))
    return level


def add_labels(lines, items):
    cursor, level = 0, 4
    for label, key, starts_set in items:
        text, where = stream(lines)
        pos = text.find(key, cursor) if key else -1
        if pos < 0:
            raise LookupError(f'tab "{label}": its content was not found in the Markdown export')
        at = where[pos]
        prev = next((j for j in range(at - 1, -1, -1) if lines[j].strip()), None)
        done = prev is not None and (m := HEADING.match(lines[prev])) and m.group(2) == label
        if starts_set:
            level = len(m.group(1)) if done else min(last_heading_level(lines, at) + 1, 6)
        if not done:
            lines[at:at] = [f"{'#' * level} {label}", ""] if at == 0 or not lines[at - 1].strip() else ["", f"{'#' * level} {label}", ""]
        text, where = stream(lines)
        cursor = text.find(key, pos) + max(len(key), 1)
    return lines


def add_titles(lines, filenames):
    for name in filenames:
        for i, line in enumerate(lines):
            if re.sub(r"\\(.)", r"\1", line.strip()) != name or FENCE.match(line):
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            m = j < len(lines) and re.match(r"^(\s*)(`{3,}|~{3,})(\S*)\s*$", lines[j])
            if m:
                indent, ticks, lang = m.groups()
                lines[i : j + 1] = [f'{indent}{ticks}{lang or "text"} title="{name}"']
                break
    return lines


def unescape_home(lines):
    fence = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fence = not fence
        elif not fence:
            lines[i] = line.replace("\\~/", "~/")
    return lines


def problems(lines, items, filenames):
    found, fence = [], False
    for line in lines:
        if FENCE.match(line):
            fence = not fence
        elif not fence and (m := HEADING.match(line)):
            found.append(m.group(2))
    out, it = [], iter(found)
    for label, _, _ in items:
        if label not in it:
            out.append(f'tab label "{label}" is missing (or out of order)')
    body = "\n".join(lines)
    for name in filenames:
        if f'title="{name}"' not in body:
            out.append(f'code block title "{name}" is missing')
    if "\\~/" in body:
        out.append("a ~ path is still escaped as \\~/")
    return out


def main(site):
    full_path = site / "llms-full.txt"
    full = full_path.read_text() if full_path.exists() else None
    errors, fixed = [], 0
    for md in sorted(site.rglob("index.md")):
        html_path = md.with_name("index.html")
        if not html_path.exists():
            continue
        root = article(Tree(html_path.read_text()).root)
        items = tabs(root)
        filenames = [n.text().strip() for n in root.walk() if "filename" in n.classes]
        before = md.read_text()
        lines = before.split("\n")
        try:
            lines = add_labels(lines, items)
        except LookupError as e:
            errors.append(f"{md}: {e}")
        lines = unescape_home(add_titles(lines, filenames))
        errors += [f"{md}: {p}" for p in problems(lines, items, filenames)]
        after = "\n".join(lines)
        if after != before:
            md.write_text(after)
            fixed += 1
            if full is not None:
                if before.strip() in full:
                    full = full.replace(before.strip(), after.strip())
                elif after.strip() not in full:
                    errors.append(f"{full_path}: the page {md} was not found in it")
    if full is not None:
        full_path.write_text(full)
    print(f"Markdown export: {fixed} pages fixed")
    if errors:
        print("Markdown export problems:\n" + "\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "site"))
