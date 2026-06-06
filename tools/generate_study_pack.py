"""Generate printable study packs for the lecture text-image project.

This helper renders:
- one-page section summary PDF
- flashcards PDF
- Anki .apkg deck
- master study pack PDF with TOC
- master flashcards PDF and Anki deck

Defaults cover the three current sections: methods, evaluation, and ethics.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

SECTION_FILES = {
    "methods": {
        "summary_md": ROOT / "data" / "summaries" / "Text-Image-GenAI_methods_summary.md",
        "flash_md": ROOT / "data" / "summaries" / "Text-Image-GenAI_methods_flashcards.md",
    },
    "evaluation": {
        "summary_md": ROOT / "data" / "summaries" / "Text-Image-GenAI_evaluation_summary.md",
        "flash_md": ROOT / "data" / "summaries" / "Text-Image-GenAI_evaluation_flashcards.md",
    },
    "ethics": {
        "summary_md": ROOT / "data" / "summaries" / "Text-Image-GenAI_ethics_summary.md",
        "flash_md": ROOT / "data" / "summaries" / "Text-Image-GenAI_ethics_flashcards.md",
    },
}


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def generate_section(section: str, make_pdf: bool, make_anki: bool) -> None:
    if section not in SECTION_FILES:
        raise SystemExit(f"Unknown section: {section}")

    files = SECTION_FILES[section]
    summary_md = files["summary_md"]
    flash_md = files["flash_md"]

    if not summary_md.exists():
        raise SystemExit(f"Missing summary markdown: {summary_md}")
    if not flash_md.exists():
        raise SystemExit(f"Missing flashcards markdown: {flash_md}")

    if make_pdf:
        run([PYTHON, str(ROOT / "tools" / "render_md_to_pdf.py"), str(summary_md)])
        run([PYTHON, str(ROOT / "tools" / "flashcards_to_pdf.py"), str(flash_md)])

    if make_anki:
        run([PYTHON, str(ROOT / "tools" / "flashcards_to_anki.py"), str(flash_md)])


def generate_master_pack() -> None:
    run([PYTHON, str(ROOT / "tools" / "build_master_study_pack.py")])


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate study packs for methods/evaluation/ethics.")
    parser.add_argument(
        "--sections",
        nargs="+",
        default=["methods", "evaluation", "ethics"],
        choices=sorted(SECTION_FILES.keys()),
        help="Sections to regenerate.",
    )
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation.")
    parser.add_argument("--no-anki", action="store_true", help="Skip Anki export.")
    args = parser.parse_args()

    for section in args.sections:
        generate_section(section, make_pdf=not args.no_pdf, make_anki=not args.no_anki)

    generate_master_pack()

    print("Study pack generation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
