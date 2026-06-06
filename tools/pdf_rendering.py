from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


MASTER_TITLE = "Text-Image-GenAI Master Study Pack"
ACCENT = HexColor("#2F5BEA")
TEXT = HexColor("#1D2433")
MUTED = HexColor("#5B6475")
SOFT = HexColor("#E9EEF9")


SECTION_CARD_THEME = {
    "methods": {
        "accent": HexColor("#2F5BEA"),
        "bg": HexColor("#F4F7FF"),
        "border": HexColor("#CAD8FF"),
        "icon": "[M]",
    },
    "evaluation": {
        "accent": HexColor("#0F766E"),
        "bg": HexColor("#F1FBF9"),
        "border": HexColor("#BDEADF"),
        "icon": "[E]",
    },
    "ethics": {
        "accent": HexColor("#B45309"),
        "bg": HexColor("#FFF8EE"),
        "border": HexColor("#F1D6B3"),
        "icon": "[H]",
    },
}


def _theme_for_section(section_name: str):
    key = section_name.lower().strip()
    for known, theme in SECTION_CARD_THEME.items():
        if known in key:
            return theme
    return {
        "accent": HexColor("#475569"),
        "bg": HexColor("#F8FAFC"),
        "border": HexColor("#DCE3ED"),
        "icon": "[S]",
    }


def make_styles() -> StyleSheet1:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="PackTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=TEXT,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PackSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetaLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=TEXT,
            spaceAfter=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.4,
            leading=14,
            textColor=TEXT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=ACCENT,
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubSectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=TEXT,
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MinorTitle",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=TEXT,
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOCHeading",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=TEXT,
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOCEntry",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            leftIndent=16,
            firstLineIndent=-16,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardQuestion",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=TEXT,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardAnswer",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.2,
            leading=13.5,
            textColor=TEXT,
            leftIndent=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallMeta",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    return styles


def _rich(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


def split_text(text: str, max_words: int) -> List[str]:
    words = text.split()
    if not words:
        return []
    chunks: List[str] = []
    current: List[str] = []
    for word in words:
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        chunks.append(" ".join(current))
    return chunks


def markdown_to_flowables(markdown_text: str, styles: StyleSheet1, *, body_style: str = "Body") -> List:
    story: List = []
    bullet_buffer: List[str] = []

    def flush_bullets() -> None:
        nonlocal bullet_buffer
        if not bullet_buffer:
            return
        items = [ListItem(Paragraph(_rich(item), styles[body_style]), leftIndent=14) for item in bullet_buffer]
        story.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=16))
        story.append(Spacer(1, 5))
        bullet_buffer = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            flush_bullets()
            story.append(Spacer(1, 4))
            continue

        if line.startswith("# "):
            flush_bullets()
            story.append(Paragraph(_rich(line[2:].strip()), styles["SectionTitle"]))
            continue
        if line.startswith("## "):
            flush_bullets()
            story.append(Paragraph(_rich(line[3:].strip()), styles["SubSectionTitle"]))
            continue
        if line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(_rich(line[4:].strip()), styles["MinorTitle"]))
            continue

        stripped = line.lstrip()
        if stripped.startswith(("- ", "• ")):
            bullet_buffer.append(stripped[2:].strip())
            continue

        flush_bullets()
        story.append(Paragraph(_rich(line), styles[body_style]))

    flush_bullets()
    return story


def _page_footer(canvas, doc, title: str) -> None:
    canvas.saveState()
    width, height = doc.pagesize
    canvas.setStrokeColor(SOFT)
    canvas.setLineWidth(0.6)
    canvas.line(doc.leftMargin, 14 * mm, width - doc.rightMargin, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(doc.leftMargin, 8 * mm, title)
    canvas.drawRightString(width - doc.rightMargin, 8 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def _draw_cover_band(canvas, doc, title: str, subtitle: str, meta_lines: Sequence[str]) -> None:
    width, height = doc.pagesize
    canvas.saveState()
    canvas.setFillColor(HexColor("#F7F9FF"))
    canvas.rect(0, 0, width, height, stroke=0, fill=1)

    canvas.setFillColor(ACCENT)
    canvas.rect(0, height - 92 * mm, width, 92 * mm, stroke=0, fill=1)

    canvas.setFillColor(HexColor("#4C6EF5"))
    canvas.circle(width - 28 * mm, height - 26 * mm, 20 * mm, stroke=0, fill=1)
    canvas.setFillColor(HexColor("#6C8CFF"))
    canvas.circle(26 * mm, height - 30 * mm, 12 * mm, stroke=0, fill=1)
    canvas.setFillColor(HexColor("#DDE7FF"))
    canvas.circle(width - 54 * mm, height - 48 * mm, 8 * mm, stroke=0, fill=1)

    canvas.setFillColor(colors.white)
    canvas.roundRect(18 * mm, height - 64 * mm, width - 36 * mm, 20 * mm, radius=6 * mm, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawCentredString(width / 2, height - 56 * mm, "STUDY PACK")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 25)
    canvas.drawCentredString(width / 2, height - 82 * mm, title)

    # Subtitle block for stronger visual hierarchy on the cover
    canvas.setFillColor(HexColor("#ECF1FF"))
    canvas.roundRect(30 * mm, height - 104 * mm, width - 60 * mm, 12 * mm, radius=4 * mm, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawCentredString(width / 2, height - 98.5 * mm, subtitle)

    y = height - 122 * mm
    canvas.setFillColor(TEXT)
    canvas.setFont("Helvetica", 9.5)
    for line in meta_lines:
        canvas.drawCentredString(width / 2, y, line)
        y -= 5.5 * mm

    canvas.setStrokeColor(HexColor("#C7D2FE"))
    canvas.setLineWidth(1.1)
    canvas.line(25 * mm, height - 132 * mm, width - 25 * mm, height - 132 * mm)

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(doc.leftMargin, 8 * mm, title)
    canvas.drawRightString(width - doc.rightMargin, 8 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


class TocDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, title: str):
        self.document_title = title
        super().__init__(filename, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="AllPages", frames=[frame], onPage=self._on_page)])

    def _on_page(self, canvas, doc):
        _page_footer(canvas, doc, self.document_title)

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()
            if style_name == "SectionTitle":
                self.notify("TOCEntry", (0, text, self.page))
            elif style_name == "SubSectionTitle":
                self.notify("TOCEntry", (1, text, self.page))
            elif style_name == "MinorTitle":
                self.notify("TOCEntry", (2, text, self.page))


def cover_page(title: str, subtitle: str, meta_lines: Sequence[str], styles: StyleSheet1) -> List:
    story: List = []
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(title, styles["PackTitle"]))
    story.append(Paragraph(subtitle, styles["PackSubtitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(HRFlowable(width="70%", thickness=1.4, color=ACCENT, spaceBefore=8, spaceAfter=14, hAlign="CENTER"))

    meta_table: List[List[Paragraph]] = []
    for line in meta_lines:
        meta_table.append([Paragraph(_rich(line), styles["Body"])])

    for item in meta_lines:
        story.append(Paragraph(_rich(item), styles["Body"]))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 0.15 * inch))
    return story


def cover_canvas(title: str, subtitle: str, meta_lines: Sequence[str]):
    def _callback(canvas, doc):
        _draw_cover_band(canvas, doc, title, subtitle, meta_lines)
    return _callback


def toc_page(styles: StyleSheet1) -> List:
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name="TOCLevel0", fontName="Helvetica", fontSize=10.5, leading=13, leftIndent=16, firstLineIndent=-16, textColor=TEXT),
        ParagraphStyle(name="TOCLevel1", fontName="Helvetica", fontSize=9.8, leading=12, leftIndent=28, firstLineIndent=-12, textColor=MUTED),
        ParagraphStyle(name="TOCLevel2", fontName="Helvetica", fontSize=9.2, leading=11, leftIndent=40, firstLineIndent=-10, textColor=MUTED),
    ]
    return [Paragraph("Table of Contents", styles["TOCHeading"]), Spacer(1, 4), toc]


def build_section_pdf(markdown_text: str, output_path: Path, title: str, subtitle: str, *, extra_meta: Sequence[str] = ()) -> None:
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    story: List = []
    meta_lines = [f"Generated: {datetime.now():%Y-%m-%d %H:%M}"] + list(extra_meta)
    story.extend(cover_page(title, subtitle, meta_lines, styles))
    story.append(HRFlowable(width="100%", thickness=0.8, color=SOFT, spaceBefore=4, spaceAfter=8))
    story.extend(markdown_to_flowables(markdown_text, styles))
    doc.build(story, onFirstPage=cover_canvas(title, subtitle, meta_lines), onLaterPages=lambda c, d: _page_footer(c, d, title))


def build_flashcards_pdf(qas_by_section: Sequence[tuple[str, Sequence[tuple[str, str]]]], output_path: Path, title: str, subtitle: str) -> None:
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    story: List = []
    meta_lines = [f"Generated: {datetime.now():%Y-%m-%d %H:%M}", "Format: question and answer study cards"]
    story.extend(cover_page(title, subtitle, meta_lines, styles))
    story.append(HRFlowable(width="100%", thickness=0.8, color=SOFT, spaceBefore=4, spaceAfter=10))
    story.append(_flashcard_legend_table(qas_by_section, styles))
    story.append(Spacer(1, 8))

    for section_name, qas in qas_by_section:
        story.append(Paragraph(section_name, styles["SectionTitle"]))
        section_theme = _theme_for_section(section_name)
        card_rows = []
        cards = [(q, a) for q, a in qas]
        if not cards:
            story.append(Paragraph("No flashcards available.", styles["Body"]))
            continue

        for i in range(0, len(cards), 2):
            left = _flashcard_table(section_name, cards[i][0], cards[i][1], styles, section_theme)
            right = _flashcard_table(section_name, cards[i + 1][0], cards[i + 1][1], styles, section_theme) if i + 1 < len(cards) else ""
            card_rows.append([left, right])

        table = Table(card_rows, colWidths=[doc.width / 2 - 4, doc.width / 2 - 4], hAlign="LEFT")
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 6))

    doc.build(story, onFirstPage=cover_canvas(title, subtitle, meta_lines), onLaterPages=lambda c, d: _page_footer(c, d, title))


def _flashcard_table(section_name: str, question: str, answer: str, styles: StyleSheet1, theme: dict):
    section_badge = f"<b>{theme['icon']} {_rich(section_name)}</b>"
    inner = Table(
        [
            [Paragraph(section_badge, ParagraphStyle("Badge", parent=styles["SmallMeta"], textColor=theme["accent"], alignment=TA_CENTER))],
            [Paragraph(f"Q. {_rich(question)}", styles["CardQuestion"])],
            [Paragraph(f"A. {_rich(answer)}", styles["CardAnswer"])],
        ],
        colWidths=[0.5 * (A4[0] - 36 * mm) / 2 - 8],
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), theme["bg"]),
        ("BACKGROUND", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 1.0, theme["border"]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, theme["border"]),
        ("ROUNDEDCORNERS", [6]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return inner


def _flashcard_legend_table(qas_by_section: Sequence[tuple[str, Sequence[tuple[str, str]]]], styles: StyleSheet1):
    seen = set()
    cells = []
    for section_name, _ in qas_by_section:
        theme = _theme_for_section(section_name)
        key = section_name.lower().strip()
        if key in seen:
            continue
        seen.add(key)
        label = Paragraph(
            f"<b><font color='{theme['accent']}'>{theme['icon']}</font> {_rich(section_name)}</b>",
            ParagraphStyle("Legend", parent=styles["Body"], alignment=TA_CENTER, spaceAfter=0),
        )
        cell = Table([[label]], colWidths=[58 * mm])
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), theme["bg"]),
            ("BOX", (0, 0), (-1, -1), 0.8, theme["border"]),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        cells.append(cell)

    if not cells:
        return Spacer(1, 1)

    rows = [cells]
    legend = Table(rows, hAlign="LEFT")
    legend.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return legend


def build_master_pdf(
    sections: Sequence[tuple[str, str, str]],
    output_path: Path,
    *,
    subtitle: str = "Methods • Evaluation • Ethics",
    cover_meta_lines: Sequence[str] | None = None,
) -> None:
    """Build master study pack with TOC and all sections."""
    styles = make_styles()
    doc = TocDocTemplate(str(output_path), MASTER_TITLE)
    story: List = []

    default_meta = [
        f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
        "Use this pack for quick revision, exam prep, and flashcard practice.",
    ]
    meta_lines = list(cover_meta_lines) if cover_meta_lines else default_meta

    story.extend(cover_page(MASTER_TITLE, subtitle, meta_lines, styles))
    story.append(PageBreak())
    story.extend(toc_page(styles))
    story.append(PageBreak())

    for section_title, subtitle, markdown_text in sections:
        story.append(Paragraph(section_title, styles["SectionTitle"]))
        story.append(Paragraph(subtitle, styles["Body"]))
        story.append(Spacer(1, 6))
        story.extend(markdown_to_flowables(markdown_text, styles))
        story.append(PageBreak())

    doc.multiBuild(story)
