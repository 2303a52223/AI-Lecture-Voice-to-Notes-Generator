import sys
from pathlib import Path
import html


def simple_md_to_html(text: str) -> str:
    lines = text.splitlines()
    out_lines = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out_lines.append('</ul>')
            in_list = False

    for raw in lines:
        line = raw.rstrip()
        if not line:
            close_list()
            out_lines.append('<p></p>')
            continue

        if line.startswith('# '):
            close_list()
            out_lines.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
            continue
        if line.startswith('## '):
            close_list()
            out_lines.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            continue
        if line.lstrip().startswith('- '):
            if not in_list:
                out_lines.append('<ul>')
                in_list = True
            out_lines.append(f"<li>{html.escape(line.lstrip()[2:].strip())}</li>")
            continue

        close_list()
        out_lines.append(f"<p>{html.escape(line)}</p>")

    close_list()
    return '\n'.join(out_lines)


def convert(md_path: str, out_html: str = None):
    p = Path(md_path)
    if not p.exists():
        raise SystemExit(f"Markdown file not found: {md_path}")

    text = p.read_text(encoding='utf-8')
    body = simple_md_to_html(text)
    html_doc = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset='utf-8'/>
      <title>{p.stem}</title>
      <style>
        body {{ font-family: Arial, Helvetica, sans-serif; margin: 24px; color: #111; max-width: 800px }}
        h1 {{ font-size: 18px }}
        h2 {{ font-size: 14px }}
      </style>
    </head>
    <body>
    {body}
    </body>
    </html>
    """

    out = Path(out_html) if out_html else p.with_suffix('.html')
    out.write_text(html_doc, encoding='utf-8')
    print(f"Wrote HTML: {out}")


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'data/summaries/Text-Image-GenAI_methods_summary.md'
    convert(arg)
