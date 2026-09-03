from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Sequence

import genanki

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.pdf_rendering import build_flashcards_pdf, build_master_pdf


SUMMARY_DIR = ROOT / "data" / "summaries"


SECTION_SPECS = [
    {
        "key": "methods",
        "title": "Methods",
        "subtitle": "Pipeline design, diffusion models, and captioning mechanics",
        "summary_md": SUMMARY_DIR / "Text-Image-GenAI_methods_summary.md",
        "flash_md": SUMMARY_DIR / "Text-Image-GenAI_methods_flashcards.md",
    },
    {
        "key": "evaluation",
        "title": "Evaluation",
        "subtitle": "Metrics, ablations, and round-trip consistency",
        "summary_md": SUMMARY_DIR / "Text-Image-GenAI_evaluation_summary.md",
        "flash_md": SUMMARY_DIR / "Text-Image-GenAI_evaluation_flashcards.md",
    },
    {
        "key": "ethics",
        "title": "Ethics",
        "subtitle": "Bias, misuse, privacy, and mitigation strategies",
        "summary_md": SUMMARY_DIR / "Text-Image-GenAI_ethics_summary.md",
        "flash_md": SUMMARY_DIR / "Text-Image-GenAI_ethics_flashcards.md",
    },
]


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


def build_appendix_markdown(all_cards: Sequence[tuple[str, Sequence[tuple[str, str]]]]) -> str:
    lines: List[str] = ["# Flashcards Appendix"]
    for section_title, cards in all_cards:
        lines.append(f"## {section_title}")
        for idx, (question, answer) in enumerate(cards, start=1):
            lines.append(f"- Q{idx}: {question}")
            lines.append(f"- A: {answer}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_master_deck(all_cards: Sequence[tuple[str, Sequence[tuple[str, str]]]], output_path: Path) -> None:
    deck = genanki.Deck(2059400999, "Text-Image-GenAI Master Study Pack")
    model = genanki.Model(
        1607392999,
        "Master Simple Model",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Section"}],
        templates=[{
            "name": "Card 1",
            "qfmt": "{{Question}}<br><br><small>{{Section}}</small>",
            "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
        }],
    )

    for section_title, cards in all_cards:
        section_tag = section_title.lower().replace(" ", "_")
        for question, answer in cards:
            deck.add_note(genanki.Note(model=model, fields=[question, answer, section_title], tags=[section_tag]))

    genanki.Package(deck).write_to_file(str(output_path))


def main() -> int:
    section_markdowns = []
    flashcards_for_pdf = []
    flashcards_for_anki = []

    for spec in SECTION_SPECS:
        if not spec["summary_md"].exists() or not spec["flash_md"].exists():
            raise SystemExit(f"Missing source files for {spec['title']}")

        summary_text = spec["summary_md"].read_text(encoding="utf-8")
        flash_text = spec["flash_md"].read_text(encoding="utf-8")
        cards = parse_flashcards(flash_text)

        section_markdowns.append((spec["title"], spec["subtitle"], summary_text))
        flashcards_for_pdf.append((spec["title"], cards))
        flashcards_for_anki.append((spec["title"], cards))

    appendix_markdown = build_appendix_markdown(flashcards_for_pdf)
    section_markdowns.append(("Flashcards Appendix", "Combined question-and-answer review cards", appendix_markdown))

    total_sections = len(SECTION_SPECS)
    total_cards = sum(len(cards) for _, cards in flashcards_for_pdf)
    total_headings = sum(text.count('\n## ') + text.count('\n### ') for _, _, text in section_markdowns)

    master_pdf = SUMMARY_DIR / "Text-Image-GenAI_master_study_pack.pdf"
    master_flash_pdf = SUMMARY_DIR / "Text-Image-GenAI_master_flashcards.pdf"
    master_apkg = SUMMARY_DIR / "Text-Image-GenAI_master_flashcards.apkg"

    build_master_pdf(
        section_markdowns,
        master_pdf,
        subtitle="Methods • Evaluation • Ethics",
        cover_meta_lines=[
            f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
            f"Sections: {total_sections}   |   Flashcards: {total_cards}   |   Key subsections: {total_headings}",
            "Use this pack for quick revision, exam prep, and rapid flashcard practice.",
        ],
    )
    build_flashcards_pdf(flashcards_for_pdf, master_flash_pdf, title="Text-Image-GenAI Master Flashcards", subtitle="Methods • Evaluation • Ethics")
    build_master_deck(flashcards_for_anki, master_apkg)

    print(f"Wrote master pack: {master_pdf}")
    print(f"Wrote master flashcards PDF: {master_flash_pdf}")
    print(f"Wrote master Anki deck: {master_apkg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
