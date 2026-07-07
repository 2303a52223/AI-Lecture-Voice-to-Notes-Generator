"""Study Packs page - download generated PDFs and Anki decks."""

from __future__ import annotations

import io
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar


st.set_page_config(
    page_title="Study Packs - Lecture Notes Generator",
    page_icon="📦",
    layout="wide",
)

css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Define data directory and download groups BEFORE functions
data_dir = Path(__file__).parent.parent / "data" / "summaries"

DOWNLOAD_GROUPS = [
    ("Master Study Pack", [
        "Text-Image-GenAI_master_study_pack.pdf",
        "Text-Image-GenAI_master_flashcards.pdf",
        "Text-Image-GenAI_master_flashcards.apkg",
    ]),
    ("Methods", [
        "Text-Image-GenAI_methods_summary.pdf",
        "Text-Image-GenAI_methods_flashcards.pdf",
        "Text-Image-GenAI_methods_flashcards.apkg",
    ]),
    ("Evaluation", [
        "Text-Image-GenAI_evaluation_summary.pdf",
        "Text-Image-GenAI_evaluation_flashcards.pdf",
        "Text-Image-GenAI_evaluation_flashcards.apkg",
    ]),
    ("Ethics", [
        "Text-Image-GenAI_ethics_summary.pdf",
        "Text-Image-GenAI_ethics_flashcards.pdf",
        "Text-Image-GenAI_ethics_flashcards.apkg",
    ]),
]


def _artifact_counts() -> tuple[int, int]:
    ready = 0
    total = 0
    for _, filenames in DOWNLOAD_GROUPS:
        for filename in filenames:
            total += 1
            if (data_dir / filename).exists():
                ready += 1
    return ready, total


def _group_ready_count(filenames: list[str]) -> int:
    return sum(1 for filename in filenames if (data_dir / filename).exists())


def _render_download_button(label: str, path: Path, key_suffix: str, primary: bool = False) -> None:
    if path.exists():
        st.download_button(
            label,
            data=path.read_bytes(),
            file_name=path.name,
            mime="application/octet-stream",
            use_container_width=True,
            key=f"dl_{key_suffix}",
        )
        st.caption(f"{path.name} · {path.stat().st_size / 1024:.0f} KB")
    else:
        st.button(label, disabled=True, use_container_width=True, key=f"missing_{key_suffix}")
        st.caption(f"Missing: {path.name}")

render_sidebar()

ready_count, total_count = _artifact_counts()

st.markdown(
    """
    <section class='page-hero page-hero-pack'>
        <div class='page-hero-badge'>📦 Export center</div>
        <h1>Study Packs</h1>
        <p class='page-hero-copy'>Download the generated PDFs, flashcards, and Anki decks in a cleaner, more polished workspace.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class='stats-strip'>
        <div class='stats-chip'><span class='stats-value'>{ready_count}</span><span class='stats-label'>Ready artifacts</span></div>
        <div class='stats-chip'><span class='stats-value'>{total_count}</span><span class='stats-label'>Total files</span></div>
        <div class='stats-chip'><span class='stats-value'>ZIP</span><span class='stats-label'>One-click bundle</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)


def build_download_all_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for group_name, filenames in DOWNLOAD_GROUPS:
            for filename in filenames:
                path = data_dir / filename
                if path.exists():
                    zf.write(path, arcname=f"{group_name}/{path.name}")
    buffer.seek(0)
    return buffer.read()


def _format_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def _artifact_rows() -> list[dict]:
    rows = []
    for group, filenames in DOWNLOAD_GROUPS:
        for filename in filenames:
            path = data_dir / filename
            exists = path.exists()
            rows.append({
                "Group": group,
                "File": filename,
                "Status": "Ready" if exists else "Missing",
                "Size": _format_size(path.stat().st_size) if exists else "-",
                "Updated": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M") if exists else "-",
            })
    return rows


def file_block(title: str, description: str, files: list[tuple[str, str]]) -> None:
    available = _group_ready_count([filename for _, filename in files])
    block_key = title.lower().replace(" ", "_")
    st.markdown(
        f"""
        <div class='pack-card'>
            <div class='pack-card-head'>
                <div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                <div class='pack-card-pill'>{available}/{len(files)} ready</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for idx, (label, filename) in enumerate(files):
        path = data_dir / filename
        with cols[idx % 3]:
            _render_download_button(label, path, f"{block_key}_{idx}_{path.stem}")
            # Show per-file delete control when delete mode is enabled
            if globals().get("ENABLE_DELETE", False) and path.exists():
                if st.button("🗑️ Delete", key=f"del_{path.stem}"):
                    try:
                        path.unlink()
                        st.success(f"Deleted {path.name}")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Failed to delete {path.name}: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='action-shell'>", unsafe_allow_html=True)
col_actions1, col_actions2 = st.columns([1, 1])
with col_actions1:
    if st.button("🔄 Regenerate Packs", type="primary", width="stretch"):
        with st.spinner("Regenerating study packs..."):
            proc = subprocess.run([sys.executable, "tools/generate_study_pack.py"], capture_output=True, text=True)
            if proc.returncode == 0:
                st.success("Study packs regenerated successfully.")
            else:
                st.error("Regeneration failed. See details below.")
                if proc.stderr:
                    st.code(proc.stderr[-3000:], language="text")
            if proc.stdout:
                st.code(proc.stdout[-3000:], language="text")
with col_actions2:
    st.markdown(
        "<div class='action-note'>Use this after editing summaries or flashcards to rebuild all PDFs and decks.</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='info-banner'>Tip: If a file is missing, run python tools/generate_study_pack.py from the project root.</div>",
    unsafe_allow_html=True,
)

zip_bytes = build_download_all_zip()
st.markdown("<div class='download-hero'>", unsafe_allow_html=True)
st.download_button(
    "⬇️ Download All Study Packs (ZIP)",
    data=zip_bytes,
    file_name="Text-Image-GenAI_study_packs.zip",
    mime="application/zip",
    use_container_width=True,
)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Includes the master pack plus Methods, Evaluation, and Ethics PDFs and Anki decks.")

# Delete controls
ENABLE_DELETE = st.checkbox("Enable delete controls (show delete buttons)", value=False)
if ENABLE_DELETE:
    st.markdown("<div class='info-banner'>Delete mode is ON — use carefully. Deletions are permanent.</div>", unsafe_allow_html=True)
    if st.checkbox("I confirm I want to permanently delete all generated study pack files"):
        if st.button("🧹 Delete all generated study pack files (permanent)"):
            deleted = 0
            failed = 0
            for _, filenames in DOWNLOAD_GROUPS:
                for filename in filenames:
                    path = data_dir / filename
                    if path.exists():
                        try:
                            path.unlink()
                            deleted += 1
                        except Exception:
                            failed += 1
            st.success(f"Deleted {deleted} files; {failed} failures")
            st.experimental_rerun()

with st.expander("📊 Artifact status"):
    rows = _artifact_rows()
    ready_count = sum(1 for r in rows if r["Status"] == "Ready")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Ready artifacts", ready_count)
    with col_b:
        st.metric("Total artifacts", len(rows))
    st.dataframe(rows, width="stretch", hide_index=True)

st.markdown("<h2 class='section-heading'>Master Pack</h2>", unsafe_allow_html=True)
file_block(
    "Combined study pack",
    "One master PDF with a table of contents plus combined flashcards and Anki deck.",
    [
        ("⬇️ Download Master Study Pack PDF", "Text-Image-GenAI_master_study_pack.pdf"),
        ("⬇️ Download Master Flashcards PDF", "Text-Image-GenAI_master_flashcards.pdf"),
        ("⬇️ Download Master Anki Deck", "Text-Image-GenAI_master_flashcards.apkg"),
    ],
)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("<h2 class='section-heading'>Section Packs</h2>", unsafe_allow_html=True)
file_block(
    "Methods",
    "Polished section summary, flashcards PDF, and Anki deck.",
    [
        ("⬇️ Methods Summary PDF", "Text-Image-GenAI_methods_summary.pdf"),
        ("⬇️ Methods Flashcards PDF", "Text-Image-GenAI_methods_flashcards.pdf"),
        ("⬇️ Methods Anki Deck", "Text-Image-GenAI_methods_flashcards.apkg"),
    ],
)

file_block(
    "Evaluation",
    "Polished section summary, flashcards PDF, and Anki deck.",
    [
        ("⬇️ Evaluation Summary PDF", "Text-Image-GenAI_evaluation_summary.pdf"),
        ("⬇️ Evaluation Flashcards PDF", "Text-Image-GenAI_evaluation_flashcards.pdf"),
        ("⬇️ Evaluation Anki Deck", "Text-Image-GenAI_evaluation_flashcards.apkg"),
    ],
)

file_block(
    "Ethics",
    "Polished section summary, flashcards PDF, and Anki deck.",
    [
        ("⬇️ Ethics Summary PDF", "Text-Image-GenAI_ethics_summary.pdf"),
        ("⬇️ Ethics Flashcards PDF", "Text-Image-GenAI_ethics_flashcards.pdf"),
        ("⬇️ Ethics Anki Deck", "Text-Image-GenAI_ethics_flashcards.apkg"),
    ],
)
