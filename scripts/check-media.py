"""Fail when a Markdown image points to a file that does not exist (Zensical strict mode does not check images)."""
import re
import sys
from pathlib import Path

docs = Path("docs")
missing = []
for md in docs.rglob("*.md"):
    for target in re.findall(r"!\[[^\]]*\]\(([^)\s]+)", md.read_text()):
        if target.startswith(("http://", "https://", "data:", "#")):
            continue
        base = docs if target.startswith("/") else md.parent
        if not (base / target.lstrip("/").split("#")[0]).exists():
            missing.append(f"{md}: {target}")
if missing:
    print("Missing images:\n" + "\n".join(missing))
    sys.exit(1)
