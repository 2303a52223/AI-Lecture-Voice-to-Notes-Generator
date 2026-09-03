from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.pdf_rendering import build_flashcards_pdf


def parse_flashcards(md_text: str):
    cards = []
    q = None
    for raw in md_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith('- Q:') or line.startswith('Q:'):
            q = line.split(':', 1)[1].strip()
            continue
        if line.startswith('- A:') or line.startswith('A:'):
            a = line.split(':', 1)[1].strip()
            if q is not None:
                cards.append((q, a))
                q = None
    return cards


def render(md_path: str, out_pdf: str | None = None):
    p = Path(md_path)
    if not p.exists():
        raise SystemExit(f"File not found: {md_path}")

    output = Path(out_pdf) if out_pdf else p.with_suffix('.pdf')
    markdown_text = p.read_text(encoding='utf-8')
    qas = parse_flashcards(markdown_text)
    section_title = p.stem.replace('_', ' ').replace('-', ' ')
    build_flashcards_pdf([(section_title, qas)], output, title=section_title, subtitle="Printable flashcards")
    print(f"Wrote flashcards PDF: {output}")


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'data/summaries/Text-Image-GenAI_methods_flashcards.md'
    out = sys.argv[2] if len(sys.argv) > 2 else None
    render(arg, out)
