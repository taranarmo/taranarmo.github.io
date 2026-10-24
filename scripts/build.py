#!/usr/bin/env python3
"""
Landing page compiler for taranarmo.github.io
Renders Markdown content and Jinja2 templates into static HTML.
"""

import os
import sys
import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Please run within nix-shell or nix build.")
    sys.exit(1)

try:
    import markdown
except ImportError:
    print("Error: markdown is required. Please run within nix-shell or nix build.")
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Error: jinja2 is required. Please run within nix-shell or nix build.")
    sys.exit(1)


def parse_markdown_with_frontmatter(md_path: Path):
    """Parses a markdown file with optional YAML frontmatter."""
    text = md_path.read_text(encoding="utf-8")
    meta = {}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_meta = parts[1]
            body = parts[2]
            meta = yaml.safe_load(raw_meta) or {}

    html_content = markdown.markdown(
        body,
        extensions=[
            "fenced_code",
            "tables",
            "attr_list",
            "toc",
            "sane_lists"
        ]
    )

    return meta, html_content


def main():
    parser = argparse.ArgumentParser(description="Build Sergei Volkov personal landing page")
    parser.add_argument(
        "--out-dir",
        type=str,
        default=".",
        help="Target output directory for the compiled site (default: current directory)"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_dir = Path(args.out_dir).resolve()
    content_dir = repo_root / "content"
    templates_dir = repo_root / "templates"
    assets_dir = repo_root / "assets"
    index_md = content_dir / "index.md"

    if not index_md.exists():
        print(f"Error: Content file not found: {index_md}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"📄 Parsing {index_md}...")
    meta, content_html = parse_markdown_with_frontmatter(index_md)

    print(f"🎨 Rendering with Jinja2 template...")
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("index.html")

    now_utc = datetime.now(timezone.utc)
    rendered_html = template.render(
        meta=meta,
        content=content_html,
        build_year=now_utc.year,
        build_timestamp=now_utc.isoformat()
    )

    out_index = out_dir / "index.html"
    out_index.write_text(rendered_html, encoding="utf-8")
    print(f"✅ Generated: {out_index}")

    # Copy assets
    style_src = assets_dir / "style.css"
    if style_src.exists():
        style_dst = out_dir / "style.css"
        shutil.copy2(style_src, style_dst)
        print(f"✅ Copied asset: {style_dst}")

    # If building to an isolated output directory (like Nix $out), copy cv directory if present
    cv_dir = repo_root / "cv"
    if out_dir != repo_root and cv_dir.is_dir():
        out_cv = out_dir / "cv"
        if not out_cv.exists():
            shutil.copytree(cv_dir, out_cv, symlinks=True)
            print(f"✅ Bundled cv directory into: {out_cv}")

    print("✨ Landing page built successfully!")


if __name__ == "__main__":
    main()
