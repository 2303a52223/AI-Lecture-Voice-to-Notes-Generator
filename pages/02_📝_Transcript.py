"""
Transcript Page - View and interact with lecture transcripts
"""
import streamlit as st
from pathlib import Path
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

# Main content
st.title("📝 Transcript")
st.markdown("View and interact with your lecture transcripts.")

st.divider()

# Get lectures
lectures = state_manager.get_all_lectures()

if not lectures:
    st.info("📤 No lectures found. Upload a lecture first!")
    st.page_link("pages/01_📤_Upload.py", label="Go to Upload", icon="📤")
    st.stop()

# Lecture selector
lecture_titles = [l.get('title', f"Lecture {l.get('id', '?')}") for l in lectures]
selected_idx = st.selectbox(
    "Select Lecture",
    range(len(lectures)),
    format_func=lambda x: lecture_titles[x]
)

lecture = lectures[selected_idx]
st.session_state.current_lecture_id = lecture.get('id')

st.divider()

# Lecture info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Language", lecture.get('language', 'Unknown').upper())
with col2:
    duration = lecture.get('duration', 0)
    st.metric("Duration", format_duration(duration) if duration else "N/A")
with col3:
    word_count = len(lecture.get('transcript_text', '').split())
    st.metric("Words", f"{word_count:,}")

st.divider()

# Audio player (if available)
audio_path = lecture.get('audio_path', '')
if audio_path and Path(audio_path).exists():
    with st.expander("🎵 Audio Player", expanded=False):
        render_mini_player(audio_path)

# Transcript content
transcript_text = lecture.get('transcript_text', '')

if not transcript_text:
    st.warning("No transcript text available for this lecture.")
    st.stop()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📄 Full Text", "📋 Segments", "🔍 Search"])

with tab1:
    st.subheader("Full Transcript")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col2:
        font_size = st.slider("Font Size", 12, 24, 16, key="transcript_font")
    
    # Display transcript
    st.markdown(
        f'<div style="font-size: {font_size}px; line-height: 1.8; padding: 1rem; '
        f'background-color: #f8f9fa; border-radius: 8px;">{transcript_text}</div>',
        unsafe_allow_html=True
    )
    
    # Copy button
    st.code(transcript_text, language=None)

with tab2:
    st.subheader("Transcript Segments")
    
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
        for segment in segments:
            start = segment.get('start', 0)
            end = segment.get('end', 0)
            text = segment.get('text', '')
            
            start_fmt = f"{int(start//60):02d}:{int(start%60):02d}"
            end_fmt = f"{int(end//60):02d}:{int(end%60):02d}"
            
            st.markdown(
                f'<div style="padding: 0.5rem; margin: 0.3rem 0; border-left: 3px solid #667eea; '
                f'padding-left: 1rem;">'
                f'<span style="color: #667eea; font-weight: bold;">[{start_fmt} → {end_fmt}]</span> '
                f'{text}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("Segment data not available. Showing full text instead.")
        st.text(transcript_text)

with tab3:
    st.subheader("Search Transcript")
    
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
                r'<mark style="background-color: #fff3cd; padding: 2px 4px; border-radius: 3px;">\1</mark>',
                transcript_text,
                flags=re.IGNORECASE
            )
            
            st.markdown(
                f'<div style="font-size: 14px; line-height: 1.8; padding: 1rem; '
                f'background-color: #f8f9fa; border-radius: 8px;">{highlighted}</div>',
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

# Download section
st.divider()
st.subheader("📥 Download")

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
    
    st.download_button(
        "⏱️ Download with Timestamps",
        data=timestamped_text,
        file_name=f"{lecture.get('title', 'transcript')}_timestamped.txt",
        mime="text/plain",
        use_container_width=True
    )
