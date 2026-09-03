import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from processors.document_extractor import route_file
from processors.summarizer import Summarizer


def main(pdf_path: str):
    p = Path(pdf_path)
    if not p.exists():
        print(f"File not found: {pdf_path}")
        return 2

    extraction = route_file(str(p), ocr=False)
    text = extraction.get('text', '')
    if not text:
        print("No text extracted from PDF. Try enabling OCR.")
        return 3

    summarizer = Summarizer()
    notes = summarizer.generate_study_notes(text, title=p.stem)

    out_dir = Path('data') / 'summaries'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{p.stem}_study_notes.md"
    out_path.write_text(notes, encoding='utf-8')

    print(f"Study notes written to: {out_path}")
    print('\n---BEGIN NOTES---\n')
    print(notes[:2000])
    print('\n---END NOTES (truncated)---\n')
    return 0


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'data/uploads/20260506_191856_text-to-image_research_paper.pdf'
    raise SystemExit(main(arg))
