"""
Summary Page - View and generate lecture summaries
"""
import streamlit as st
from pathlib import Path
from utils.state_manager import StateManager
from utils.helpers import format_duration
from components.sidebar import render_sidebar
from components.cards import info_card, summary_card

# Page config
st.set_page_config(
    page_title="Summary - Lecture Notes Generator",
    page_icon="📊",
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
st.title("📊 Summary & Notes")
st.markdown("View AI-generated summaries and study notes from your lectures.")

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

# Summary content
summary_text = lecture.get('summary_text', '')
transcript_text = lecture.get('transcript_text', '')

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Summary", "📝 Study Notes", "🔄 Regenerate"])

with tab1:
    st.subheader("Lecture Summary")
    
    if summary_text:
        st.markdown(summary_text)
        
        st.divider()
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            original_words = len(transcript_text.split()) if transcript_text else 0
            st.metric("Original Words", f"{original_words:,}")
        with col2:
            summary_words = len(summary_text.split())
            st.metric("Summary Words", f"{summary_words:,}")
        with col3:
            if original_words > 0:
                ratio = round(summary_words / original_words * 100, 1)
                st.metric("Compression", f"{ratio}%")
            else:
                st.metric("Compression", "N/A")
    else:
        st.warning("No summary available for this lecture.")
        
        if transcript_text:
            if st.button("📊 Generate Summary", type="primary"):
                with st.spinner("Generating summary..."):
                    try:
                        from processors.summarizer import Summarizer
                        summarizer = Summarizer()
                        result = summarizer.summarize(transcript_text)
                        
                        # Update lecture
                        state_manager.update_lecture(
                            lecture.get('id'),
                            {'summary_text': result['summary']}
                        )
                        
                        st.success("Summary generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating summary: {e}")

with tab2:
    st.subheader("Study Notes")
    
    # Try to load study notes from file
    summary_path = lecture.get('summary_path', '')
    study_notes = ''
    
    if summary_path and Path(summary_path).exists():
        try:
            with open(summary_path, 'r', encoding='utf-8') as f:
                study_notes = f.read()
        except:
            pass
    
    if study_notes:
        st.markdown(study_notes)
    elif transcript_text:
        st.info("Study notes not generated yet.")
        
        if st.button("📝 Generate Study Notes", type="primary"):
            with st.spinner("Generating study notes..."):
                try:
                    from processors.summarizer import Summarizer
                    summarizer = Summarizer()
                    notes = summarizer.generate_study_notes(
                        transcript_text,
                        title=lecture.get('title', 'Lecture')
                    )
                    
                    # Save notes
                    from utils.file_handler import FileHandler
                    file_handler = FileHandler()
                    notes_path = file_handler.get_summary_path(lecture.get('title', 'lecture'))
                    Path(notes_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(notes_path, 'w', encoding='utf-8') as f:
                        f.write(notes)
                    
                    # Update lecture
                    state_manager.update_lecture(
                        lecture.get('id'),
                        {'summary_path': str(notes_path)}
                    )
                    
                    st.success("Study notes generated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating study notes: {e}")
    else:
        st.warning("No transcript available to generate study notes.")

with tab3:
    st.subheader("Regenerate Summary")
    
    if not transcript_text:
        st.warning("No transcript text available.")
        st.stop()
    
    # Options
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "Summary Style",
            options=['concise', 'detailed', 'bullet_points'],
            key="regen_style"
        )
    with col2:
        max_length = st.slider(
            "Max Length (words)",
            50, 500, 150,
            key="regen_max_length"
        )
    
    if st.button("🔄 Regenerate Summary", type="primary", use_container_width=True):
        with st.spinner("Regenerating summary..."):
            try:
                from processors.summarizer import Summarizer
                summarizer = Summarizer()
                result = summarizer.summarize(
                    transcript_text,
                    max_length=max_length,
                    style=style
                )
                
                # Update lecture
                state_manager.update_lecture(
                    lecture.get('id'),
                    {'summary_text': result['summary']}
                )
                
                st.success("Summary regenerated!")
                st.markdown("### New Summary")
                st.markdown(result['summary'])
                
                st.info("Refresh the page to see the updated summary in other tabs.")
                
            except Exception as e:
                st.error(f"Error regenerating summary: {e}")

# Download section
st.divider()
st.subheader("📥 Download")

col1, col2 = st.columns(2)

with col1:
    if summary_text:
        st.download_button(
            "📊 Download Summary",
            data=summary_text,
            file_name=f"{lecture.get('title', 'summary')}_summary.txt",
            mime="text/plain",
            use_container_width=True
        )

with col2:
    summary_path = lecture.get('summary_path', '')
    if summary_path and Path(summary_path).exists():
        with open(summary_path, 'r', encoding='utf-8') as f:
            notes_content = f.read()
        st.download_button(
            "📝 Download Study Notes",
            data=notes_content,
            file_name=f"{lecture.get('title', 'notes')}_study_notes.md",
            mime="text/markdown",
            use_container_width=True
        )
