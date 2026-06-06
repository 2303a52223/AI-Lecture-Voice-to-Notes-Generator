from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.pdf_rendering import build_section_pdf


def render(md_path: str, out_pdf: str | None = None):
    p = Path(md_path)
    if not p.exists():
        raise SystemExit(f"Markdown file not found: {md_path}")

    output = Path(out_pdf) if out_pdf else p.with_suffix('.pdf')
    markdown_text = p.read_text(encoding='utf-8')
    title = p.stem.replace('_', ' ').replace('-', ' ')
    subtitle = "Printable exam-prep summary"
    build_section_pdf(markdown_text, output, title=title, subtitle=subtitle)
    print(f"Wrote PDF: {output}")


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'data/summaries/Text-Image-GenAI_methods_summary.md'
    out = sys.argv[2] if len(sys.argv) > 2 else None
    render(arg, out)
