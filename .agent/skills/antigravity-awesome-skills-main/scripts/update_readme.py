#!/usr/bin/env python3
import io
import json
import os
import re
import sys


def configure_utf8_output() -> None:
    """Best-effort UTF-8 stdout/stderr on Windows without dropping diagnostics."""
    if sys.platform != "win32":
        return

    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            continue
        except Exception:
            pass

        buffer = getattr(stream, "buffer", None)
        if buffer is not None:
            setattr(
                sys,
                stream_name,
                io.TextIOWrapper(buffer, encoding="utf-8", errors="backslashreplace"),
            )


def update_readme():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(base_dir, "README.md")
    index_path = os.path.join(base_dir, "skills_index.json")

    print(f"📖 Reading skills index from: {index_path}")
    with open(index_path, "r", encoding="utf-8") as f:
        skills = json.load(f)

    total_skills = len(skills)
    print(f"🔢 Total skills found: {total_skills}")

    print(f"📝 Updating README at: {readme_path}")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Title Count
    content = re.sub(
        r"(# 🌌 Antigravity Awesome Skills: )\d+(\+ Agentic Skills)",
        rf"\g<1>{total_skills}\g<2>",
        content,
    )

    # 2. Update Blockquote Count
    content = re.sub(
        r"(Collection of )\d+(\+ Universal)",
        rf"\g<1>{total_skills}\g<2>",
        content,
    )

    # 3. Update Intro Text Count
    content = re.sub(
        r"(library of \*\*)\d+( high-performance agentic skills\*\*)",
        rf"\g<1>{total_skills}\g<2>",
        content,
    )

    # 4. Update Browse section header
    content = re.sub(
        r"## Browse \d+\+ Skills",
        f"## Browse {total_skills}+ Skills",
        content,
    )

    # 5. Update TOC link for Browse (anchor matches header-derived slug)
    content = re.sub(
        r"\[📚 Browse \d+\+ Skills\]\(#browse-\d+-skills\)",
        f"[📚 Browse {total_skills}+ Skills](#browse-{total_skills}-skills)",
        content,
    )

    with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print("✅ README.md updated successfully.")


if __name__ == "__main__":
    configure_utf8_output()
    update_readme()
