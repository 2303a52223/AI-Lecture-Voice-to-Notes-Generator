"""
Health Check Page - one-click diagnostics for core app workflows.
"""

from __future__ import annotations

import importlib
import json
import time
from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar
from utils.state_manager import StateManager


st.set_page_config(
    page_title="Health Check - Lecture Notes Generator",
    page_icon="🩺",
    layout="wide",
)

css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

render_sidebar()
state_manager = StateManager()

st.markdown(
    """
    <section class='page-hero'>
        <div class='page-hero-badge'>🩺 Diagnostics</div>
        <h1>System Health Check</h1>
        <p class='page-hero-copy'>Run quick checks to confirm transcription, extraction, summary, quiz, flashcard exports, and data storage are working.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


def dep_check(module_name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(module_name)
        return True, "installed"
    except Exception as exc:
        return False, str(exc)


st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
st.subheader("1) Dependency checks")

deps = [
    "faster_whisper",
    "fitz",
    "pdfplumber",
    "pypdf",
    "pptx",
    "docx",
    "genanki",
    "nltk",
    "transformers",
]

ok_count = 0
for dep in deps:
    ok, msg = dep_check(dep)
    if ok:
        ok_count += 1
        st.success(f"{dep}: OK")
    else:
        st.error(f"{dep}: Missing ({msg})")

st.info(f"Dependencies healthy: {ok_count}/{len(deps)}")
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
st.subheader("2) Storage and database")

data_dirs = [
    Path("data/uploads"),
    Path("data/transcripts"),
    Path("data/summaries"),
]

for directory in data_dirs:
    if directory.exists():
        file_count = sum(1 for _ in directory.iterdir())
        st.success(f"{directory}: {file_count} item(s)")
    else:
        st.error(f"{directory}: missing")

db_path = Path("data/database.json")
if db_path.exists():
    try:
        db = json.loads(db_path.read_text(encoding="utf-8"))
        lectures = db.get("lectures", [])
        st.success(f"database.json: OK ({len(lectures)} lectures)")
    except Exception as exc:
        st.error(f"database.json: invalid JSON ({exc})")
else:
    st.error("database.json: missing")

st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
st.subheader("3) Pipeline quick-check")

if st.button("Run quick pipeline checks", type="primary", width="stretch"):
    start = time.time()

    # Summarizer smoke check
    try:
        from processors.summarizer import Summarizer

        sample = (
            "Machine learning systems learn patterns from data. "
            "Evaluation measures how well models generalize. "
            "Ethics and fairness are important when deploying models."
        )
        s = Summarizer()
        result = s.summarize(sample, max_length=60, min_length=20, style="concise")
        if result.get("summary", "").strip():
            st.success("Summary generation: OK")
        else:
            st.error("Summary generation: Empty output")
    except Exception as exc:
        st.error(f"Summary generation: FAILED ({exc})")

    # Quiz and flashcards smoke check
    try:
        from processors.quiz_generator import QuizGenerator

        qg = QuizGenerator()
        quiz = qg.generate_quiz(sample, num_questions=3, difficulty="easy", question_types=["multiple_choice"])
        cards = qg.generate_flashcards(sample, num_cards=3)

        if quiz:
            st.success(f"Quiz generation: OK ({len(quiz)} question(s))")
        else:
            st.error("Quiz generation: returned no questions")

        if cards:
            st.success(f"Flashcard generation: OK ({len(cards)} card(s))")
        else:
            st.error("Flashcard generation: returned no cards")
    except Exception as exc:
        st.error(f"Quiz/Flashcards: FAILED ({exc})")

    # Document extraction smoke-check (first available file)
    try:
        from processors.document_extractor import route_file

        uploads = Path("data/uploads")
        candidates = []
        for ext in ("*.pdf", "*.pptx", "*.docx"):
            candidates.extend(list(uploads.glob(ext)))

        if candidates:
            target = candidates[0]
            extraction = route_file(str(target), ocr=False, max_units=1)
            text = extraction.get("text", "")
            segments = extraction.get("segments", [])
            if text.strip() and segments:
                st.success(f"Document extraction: OK ({target.name}, {len(segments)} unit)")
            else:
                st.warning(f"Document extraction: No text from {target.name}")
        else:
            st.info("Document extraction: skipped (no PDF/PPTX/DOCX in data/uploads)")
    except Exception as exc:
        st.error(f"Document extraction: FAILED ({exc})")

    elapsed = time.time() - start
    st.caption(f"Quick checks finished in {elapsed:.2f}s")

st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
st.subheader("4) Current app data snapshot")

lectures = state_manager.get_all_lectures()
st.write(f"Lectures in DB: {len(lectures)}")

if lectures:
    latest = lectures[-1]
    st.json(
        {
            "id": latest.get("id"),
            "title": latest.get("title"),
            "has_transcript": bool((latest.get("transcript_text") or "").strip()),
            "has_summary": bool((latest.get("summary_text") or "").strip()),
            "transcript_path": latest.get("transcript_path"),
            "summary_path": latest.get("summary_path"),
            "model": latest.get("whisper_model"),
        }
    )

st.markdown("</div>", unsafe_allow_html=True)
