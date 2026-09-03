"""
Transcript Page - View and interact with lecture transcripts
"""
import streamlit as st
from pathlib import Path
import html
from utils.state_manager import StateManager
from utils.helpers import format_duration
from components.sidebar import render_sidebar
from components.cards import info_card
from components.audio_player import render_mini_player

# Page config
st.set_page_config(
    page_title="Transcript - Lecture Notes Generator",
    page_icon="📝",
    layout="wide"
)

# Load custom CSS
css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize
state_manager = StateManager()

# Sidebar
render_sidebar()

# Main content - Hero
st.markdown(
    """
    <section class='page-hero transcript-hero'>
        <div class='page-hero-badge'>📝 Transcript</div>
        <h1>View & Interact with Transcripts</h1>
        <p class='page-hero-copy'>Read the complete transcription of your lectures with full text search and segment playback.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown("<div class='transcript-shell'>", unsafe_allow_html=True)

# Get lectures
lectures = state_manager.get_all_lectures()

if not lectures:
<<<<<<< HEAD
    st.markdown(
        """
        <div class='transcript-empty-state'>
            <div class='pack-card-head'>
                <div>
                    <h3>No lectures yet</h3>
                    <p>Upload a lecture first so you can read transcripts, search the text, and review segments here.</p>
                </div>
                <div class='pack-card-pill'>Ready when you are</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
=======
    st.info("📤 No lectures found. Upload a lecture first!")
>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
    st.page_link("pages/01_📤_Upload.py", label="Go to Upload", icon="📤")
    st.stop()

# Lecture selector
lecture_titles = [l.get('title', f"Lecture {l.get('id', '?')}") for l in lectures]
<<<<<<< HEAD

st.markdown("<div class='pack-card transcript-control-card'>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class='pack-card-head'>
        <div>
            <h3>Choose a lecture</h3>
            <p>Jump between transcripts without losing your place in the workspace.</p>
        </div>
        <div class='pack-card-pill'>{len(lectures)} available</div>
    </div>
    """,
    unsafe_allow_html=True,
)

selected_idx = st.selectbox(
    "Select Lecture",
    range(len(lectures)),
    format_func=lambda x: lecture_titles[x],
    label_visibility="collapsed",
)

st.markdown("</div>", unsafe_allow_html=True)

lecture = lectures[selected_idx]
st.session_state.current_lecture_id = lecture.get('id')

=======
selected_idx = st.selectbox(
    "Select Lecture",
    range(len(lectures)),
    format_func=lambda x: lecture_titles[x]
)

lecture = lectures[selected_idx]
st.session_state.current_lecture_id = lecture.get('id')

st.divider()

>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
# Lecture info
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='transcript-meta-chip'>", unsafe_allow_html=True)
    st.metric("Language", lecture.get('language', 'Unknown').upper())
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    duration = lecture.get('duration', 0)
    st.markdown("<div class='transcript-meta-chip'>", unsafe_allow_html=True)
    st.metric("Duration", format_duration(duration) if duration else "N/A")
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    word_count = len(lecture.get('transcript_text', '').split())
    st.markdown("<div class='transcript-meta-chip'>", unsafe_allow_html=True)
    st.metric("Words", f"{word_count:,}")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Audio player (if available)
audio_path = lecture.get('audio_path', '')
if audio_path and Path(audio_path).exists():
    with st.expander("🎵 Audio Player", expanded=False):
        render_mini_player(audio_path)

<<<<<<< HEAD
=======
# Debug info
with st.expander("🔧 Debug Info"):
    st.json({
        "lecture_id": lecture.get('id'),
        "title": lecture.get('title'),
        "transcript_path": lecture.get('transcript_path'),
        "method": lecture.get('method', 'unknown'),
        "text_length": len(lecture.get('transcript_text', '')),
        "audio_path": lecture.get('audio_path')
    })

>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
# Transcript content
transcript_text = lecture.get('transcript_text', '')

if not transcript_text:
    st.warning("⚠️ No transcript text available for this lecture.")
    
    # Offer re-processing
    if st.button("🔄 Re-process Lecture", use_container_width=True):
        with st.spinner("Re-processing lecture..."):
            try:
                audio_path = lecture.get('audio_path', '')
                if audio_path and Path(audio_path).exists():
                    # Re-extract from file
                    from processors.audio_transcriber import AudioTranscriber
                    transcriber = AudioTranscriber()
                    
                    # Re-transcribe
                    result = transcriber.transcribe(audio_path)
                    
                    # Update database
                    db = state_manager.load_database()
                    for lec in db['lectures']:
                        if lec['id'] == lecture['id']:
                            lec['transcript_text'] = result.get('text', '')
                            lec['duration'] = result.get('duration', 0)
                            break
                    state_manager.save_database(db)
                    
                    st.success("✅ Re-processing complete! Please refresh the page.")
                    st.rerun()
                else:
                    # Try document extraction instead
                    ext = Path(audio_path).suffix.lower() if audio_path else ''
                    if ext in ['.pdf', '.pptx', '.docx']:
                        from processors.document_extractor import route_file
                        result = route_file(audio_path, ocr=True)
                        
                        # Update database
                        db = state_manager.load_database()
                        for lec in db['lectures']:
                            if lec['id'] == lecture['id']:
                                lec['transcript_text'] = result.get('text', '')
                                break
                        state_manager.save_database(db)
                        
                        st.success("✅ Re-extraction complete! Please refresh the page.")
                        st.rerun()
                    else:
                        st.error("❌ Cannot re-process: file not found or unsupported format")
            except Exception as e:
                st.error(f"❌ Re-processing failed: {e}")
    
    st.stop()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📄 Full Text", "📋 Segments", "🔍 Search"])

with tab1:
    st.markdown("<div class='transcript-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='transcript-section-title'>Full Transcript</div>", unsafe_allow_html=True)
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col2:
        font_size = st.slider("Font Size", 12, 24, 16, key="transcript_font")
    
    # Display transcript
    safe_transcript_text = html.escape(transcript_text)
    st.markdown(
        f'<div class="transcript-text" style="font-size: {font_size}px; line-height: 1.8;">{safe_transcript_text}</div>',
        unsafe_allow_html=True
    )
    
    # Copy button
    st.code(transcript_text, language=None)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='transcript-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='transcript-section-title'>Transcript Segments</div>", unsafe_allow_html=True)
    
    # Try to load segments from transcript file
    transcript_path = lecture.get('transcript_path', '')
    segments = []
    
    if transcript_path and Path(transcript_path).exists():
        try:
            import json
            with open(transcript_path, 'r') as f:
                transcript_data = json.load(f)
            segments = transcript_data.get('segments', [])
        except:
            pass
    
    if segments:
<<<<<<< HEAD
        for index, segment in enumerate(segments):
=======
        for segment in segments:
>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
            start = segment.get('start', 0)
            end = segment.get('end', 0)
            text = segment.get('text', '')
            
            start_fmt = f"{int(start//60):02d}:{int(start%60):02d}"
            end_fmt = f"{int(end//60):02d}:{int(end%60):02d}"
            
            safe_text = html.escape(text)
<<<<<<< HEAD
            segment_class = "transcript-segment transcript-segment-alt" if index % 2 else "transcript-segment"
            st.markdown(
                f'<div class="{segment_class}">'
                f'<div class="transcript-segment-meta">[{start_fmt} → {end_fmt}]</div>'
                f'<div class="transcript-segment-text">{safe_text}</div>'
                f'</div>',
=======
            st.markdown(
                f'<div class="transcript-segment">'
                f'<span style="color: var(--primary-dark); font-weight: 800;">[{start_fmt} → {end_fmt}]</span> '
                f'{safe_text}</div>',
>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
                unsafe_allow_html=True
            )
    else:
        st.info("Segment data not available. Showing full text instead.")
        st.text(transcript_text)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='transcript-search-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='transcript-section-title'>Search Transcript</div>", unsafe_allow_html=True)
    
    search_query = st.text_input(
        "🔍 Search for keywords or phrases",
        placeholder="Enter search term..."
    )
    
    if search_query:
        # Simple search
        query_lower = search_query.lower()
        text_lower = transcript_text.lower()
        
        # Count occurrences
        count = text_lower.count(query_lower)
        
        if count > 0:
            st.success(f"Found **{count}** occurrence(s) of '{search_query}'")
            
            # Highlight matches in text
            import re
            highlighted = re.sub(
                f'({re.escape(search_query)})',
                r'<mark class="transcript-mark">\1</mark>',
                transcript_text,
                flags=re.IGNORECASE
            )
            
            st.markdown(
                f'<div class="transcript-match" style="font-size: 14px;">{highlighted}</div>',
                unsafe_allow_html=True
            )
            
            # Search in segments if available
            if segments:
                st.subheader("Matching Segments")
                for segment in segments:
                    if query_lower in segment.get('text', '').lower():
                        start = segment.get('start', 0)
                        start_fmt = f"{int(start//60):02d}:{int(start%60):02d}"
                        st.markdown(f"**[{start_fmt}]** {segment['text']}")
        else:
            st.warning(f"No matches found for '{search_query}'")
    st.markdown("</div>", unsafe_allow_html=True)

# Download section
<<<<<<< HEAD
st.markdown("<div class='pack-card transcript-download-card'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='pack-card-head'>
        <div>
            <h3>Download transcript</h3>
            <p>Export the clean text version or keep timestamps for easier revision.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
=======
st.divider()
st.subheader("📥 Download")
>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "📄 Download as Text",
        data=transcript_text,
        file_name=f"{lecture.get('title', 'transcript')}.txt",
        mime="text/plain",
        use_container_width=True
    )

with col2:
    # Format with timestamps if segments available
    if segments:
        formatted = []
        for seg in segments:
            start = seg.get('start', 0)
            end = seg.get('end', 0)
            formatted.append(f"[{int(start//60):02d}:{int(start%60):02d} --> {int(end//60):02d}:{int(end%60):02d}] {seg.get('text', '')}")
        timestamped_text = '\n'.join(formatted)
    else:
        timestamped_text = transcript_text
<<<<<<< HEAD

=======
    
>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
    st.download_button(
        "⏱️ Download with Timestamps",
        data=timestamped_text,
        file_name=f"{lecture.get('title', 'transcript')}_timestamped.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)
<<<<<<< HEAD

# Debug info
with st.expander("🔧 Debug Info"):
    st.json({
        "lecture_id": lecture.get('id'),
        "title": lecture.get('title'),
        "transcript_path": lecture.get('transcript_path'),
        "method": lecture.get('method', 'unknown'),
        "text_length": len(lecture.get('transcript_text', '')),
        "audio_path": lecture.get('audio_path')
    })

st.markdown("</div>", unsafe_allow_html=True)
=======
>>>>>>> 8bde74a17c6cfcf6d98366c2df5856aefa789153
