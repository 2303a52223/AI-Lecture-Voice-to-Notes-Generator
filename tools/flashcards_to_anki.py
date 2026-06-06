from pathlib import Path
import genanki

def md_to_qas(md_text: str):
    qas = []
    lines = [l.strip() for l in md_text.splitlines() if l.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('- Q:') or line.startswith('Q:') or line.startswith('- Q'):
            q = line.split(':',1)[1].strip() if ':' in line else line.split('Q',1)[1].strip()
            a = ''
            i += 1
            if i < len(lines):
                next_line = lines[i]
                if next_line.startswith('A:') or next_line.startswith('- A') or next_line.startswith('A:'):
                    a = next_line.split(':',1)[1].strip() if ':' in next_line else next_line
            qas.append((q,a))
        i += 1
    return qas

def build_deck(md_path: str, out_apkg: str = None):
    p = Path(md_path)
    if not p.exists():
        raise SystemExit(f"File not found: {md_path}")

    text = p.read_text(encoding='utf-8')
    qas = md_to_qas(text)

    deck = genanki.Deck(2059400110, f"{p.stem} Deck")
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[{'name': 'Question'}, {'name': 'Answer'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }]
    )

    for q,a in qas:
        note = genanki.Note(model=model, fields=[q, a])
        deck.add_note(note)

    out = Path(out_apkg) if out_apkg else p.with_suffix('.apkg')
    genanki.Package(deck).write_to_file(str(out))
    print(f"Wrote Anki deck: {out}")

if __name__ == '__main__':
    import sys
    md = sys.argv[1] if len(sys.argv) > 1 else 'data/summaries/Text-Image-GenAI_methods_flashcards.md'
    out = sys.argv[2] if len(sys.argv) > 2 else None
    build_deck(md, out)
