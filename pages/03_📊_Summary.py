"""
Summary Page - Enhanced with custom reduction, topic filtering, and Q&A chat
"""
import streamlit as st
from pathlib import Path
import time
import re
from utils.state_manager import StateManager
from utils.helpers import format_duration
from utils.progress_tracker import ProgressTracker
from utils.error_handler import report_error
from components.sidebar import render_sidebar
from components.cards import info_card, summary_card

# Page config
st.set_page_config(
    page_title="Summary - Lecture Notes Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize
state_manager = StateManager()

# Initialize chat history if not exists
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def format_summary_paragraphs(text: str, max_sentences: int = 2) -> str:
    """Break a long summary into short markdown paragraphs."""
    if not text:
        return ""

    normalized = re.sub(r"\s+", " ", text.strip())
    if not normalized:
        return ""

    chunks = re.split(r"(?<=[.!?])\s+", normalized)
    paragraphs = []
    current = []

    for chunk in chunks:
        if not chunk:
            continue

        current.append(chunk)
        if len(current) >= max_sentences:
            paragraphs.append(" ".join(current).strip())
            current = []

    if current:
        paragraphs.append(" ".join(current).strip())

    return "\n\n".join(f"<div class='summary-paragraph'>{paragraph}</div>" for paragraph in paragraphs)

# Sidebar
render_sidebar()

# Main content
st.title("📊 Summary & Notes")
st.markdown("View AI-generated summaries with custom reduction, topic filtering, and Q&A.")

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
    format_func=lambda x: lecture_titles[x],
    key="lecture_selector"
)

lecture = lectures[selected_idx]
st.session_state.current_lecture_id = lecture.get('id')

st.divider()

# Summary content
summary_text = (lecture.get('summary_text', '') or '').strip()
transcript_text = (lecture.get('transcript_text', '') or '').strip()

# Fallback: derive summary preview from saved study notes if summary_text is empty.
if not summary_text:
    summary_path = lecture.get('summary_path', '')
    if summary_path and Path(summary_path).exists():
        try:
            notes_text = Path(summary_path).read_text(encoding='utf-8')
            if "## 📋 Summary" in notes_text:
                summary_section = notes_text.split("## 📋 Summary", 1)[1]
                if "##" in summary_section:
                    summary_section = summary_section.split("##", 1)[0]
                summary_text = summary_section.strip()
            elif notes_text.strip():
                summary_text = notes_text.strip().splitlines()[0]
        except Exception:
            pass

# Main layout with sidebar for controls
col_main, col_chat = st.columns([2, 1])

with col_main:
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "📝 Study Notes", "⚙️ Customize", "🔄 Regenerate"])

    with tab1:
        st.subheader("Lecture Summary")
        
        if summary_text:
            st.markdown(
                f"<div class='summary-body'>{format_summary_paragraphs(summary_text)}</div>",
                unsafe_allow_html=True,
            )
            
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
                if st.button("📊 Generate Summary", type="primary", width="stretch"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.write("📍 Initializing summarizer...")
                        progress_bar.progress(10)
                        
                        from processors.summarizer import Summarizer
                        summarizer = Summarizer()
                        
                        status_text.write("📍 Summarizing text (this may take a minute)...")
                        start_time = time.time()
                        progress_bar.progress(20)
                        
                        result = summarizer.summarize(transcript_text)
                        progress_bar.progress(80)
                        
                        status_text.write("📍 Saving to database...")
                        progress_bar.progress(90)
                        
                        # Update lecture
                        state_manager.update_lecture(
                            lecture.get('id'),
                            {'summary_text': result['summary']}
                        )
                        
                        elapsed = ProgressTracker.get_elapsed_time(start_time)
                        progress_bar.progress(100)
                        status_text.write(f"✅ Summary generated in {elapsed}!")
                        
                        st.success("Summary generated!")
                        st.rerun()
                    except Exception as e:
                        report_error(e, "Error generating summary")

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
            
            if st.button("📝 Generate Study Notes", type="primary", width="stretch"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.write("📍 Initializing note generator...")
                    progress_bar.progress(10)
                    
                    from processors.summarizer import Summarizer
                    from utils.file_handler import FileHandler
                    
                    summarizer = Summarizer()
                    file_handler = FileHandler()
                    
                    status_text.write("📍 Generating study notes (this may take a minute)...")
                    start_time = time.time()
                    progress_bar.progress(20)
                    
                    notes = summarizer.generate_study_notes(
                        transcript_text,
                        title=lecture.get('title', 'Lecture')
                    )
                    progress_bar.progress(70)
                    
                    status_text.write("📍 Saving notes...")
                    notes_path = file_handler.get_summary_path(lecture.get('title', 'lecture'))
                    Path(notes_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(notes_path, 'w', encoding='utf-8') as f:
                        f.write(notes)
                    
                    progress_bar.progress(85)
                    
                    # Update lecture
                    state_manager.update_lecture(
                        lecture.get('id'),
                        {'summary_path': str(notes_path)}
                    )
                    
                    elapsed = ProgressTracker.get_elapsed_time(start_time)
                    progress_bar.progress(100)
                    status_text.write(f"✅ Study notes generated in {elapsed}!")
                    
                    st.success("Study notes generated!")
                    st.rerun()
                except Exception as e:
                    report_error(e, "Error generating study notes")
        else:
            st.warning("No transcript available to generate study notes.")

    with tab3:
        st.subheader("⚙️ Customization Options")
        
        if not transcript_text:
            st.warning("No transcript text available.")
        else:
            # Custom Reduction Percentage
            st.markdown("### 1️⃣ Custom Reduction Percentage")
            reduction_pct = st.slider(
                "Reduce content by (%)",
                min_value=30,
                max_value=90,
                value=50,
                step=5,
                help="Choose how much to reduce (50% means keep 50% of original)"
            )
            st.caption(f"📊 This will reduce content to approximately {100-reduction_pct}% of original size")
            
            # Topic-Based Extraction
            st.markdown("### 2️⃣ Topic-Based Filtering")
            topics_input = st.text_input(
                "Enter specific topics (comma-separated)",
                placeholder="e.g., machine learning, neural networks, algorithms",
                help="Leave empty to include all content, or filter by specific topics"
            )
            
            # Extract and show key topics
            st.markdown("### 📌 Key Topics Found")
            try:
                from processors.summarizer import Summarizer
                summarizer = Summarizer()
                key_topics = summarizer.generate_key_topics(transcript_text, num_topics=10)
                
                # Display as selectable chips
                st.write("**Auto-detected topics:**")
                cols = st.columns(len(key_topics))
                for i, topic in enumerate(key_topics):
                    with cols[i]:
                        st.button(f"#{topic}", key=f"topic_{i}", disabled=True)
            except:
                st.info("Unable to extract topics")
            
            # Generate customized summary
            if st.button("✨ Generate Customized Summary", type="primary", width="stretch"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.write("📍 Initializing summarizer...")
                    progress_bar.progress(10)
                    
                    from processors.summarizer import Summarizer
                    summarizer = Summarizer()
                    
                    filter_topics = [t.strip() for t in topics_input.split(',')] if topics_input else None
                    
                    status_text.write("📍 Generating customized summary...")
                    start_time = time.time()
                    progress_bar.progress(20)
                    
                    result = summarizer.summarize(
                        transcript_text,
                        reduction_percentage=reduction_pct,
                        filter_topics=filter_topics,
                        style="concise"
                    )
                    progress_bar.progress(90)
                    
                    elapsed = ProgressTracker.get_elapsed_time(start_time)
                    progress_bar.progress(100)
                    status_text.write(f"✅ Summary generated in {elapsed}!")
                    
                    st.success("✅ Customized summary generated!")
                    st.markdown("### 📄 Your Customized Summary")
                    st.markdown(
                        f"<div class='summary-body'>{format_summary_paragraphs(result['summary'])}</div>",
                        unsafe_allow_html=True,
                    )
                    
                    # Statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        original_words = len(transcript_text.split())
                        st.metric("Original Words", f"{original_words:,}")
                    with col2:
                        summary_words = len(result['summary'].split())
                        st.metric("Summary Words", f"{summary_words:,}")
                    with col3:
                        if original_words > 0:
                            ratio = round(summary_words / original_words * 100, 1)
                            st.metric("Final Compression", f"{ratio}%")
                    
                    # Save option
                    if st.button("💾 Save as Summary", width="stretch"):
                        state_manager.update_lecture(
                            lecture.get('id'),
                            {'summary_text': result['summary']}
                        )
                        st.success("Summary saved!")
                        st.rerun()
                except Exception as e:
                    report_error(e, "Generating customized summary")

    with tab4:
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
        
        if st.button("🔄 Regenerate Summary", type="primary", width="stretch"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.write("📍 Initializing summarizer...")
                progress_bar.progress(10)
                
                from processors.summarizer import Summarizer
                summarizer = Summarizer()
                
                status_text.write("📍 Regenerating summary...")
                start_time = time.time()
                progress_bar.progress(20)
                
                result = summarizer.summarize(
                    transcript_text,
                    max_length=max_length,
                    style=style
                )
                progress_bar.progress(80)
                
                status_text.write("📍 Saving to database...")
                progress_bar.progress(90)
                
                # Update lecture
                state_manager.update_lecture(
                    lecture.get('id'),
                    {'summary_text': result['summary']}
                )
                
                elapsed = ProgressTracker.get_elapsed_time(start_time)
                progress_bar.progress(100)
                status_text.write(f"✅ Summary regenerated in {elapsed}!")
                
                st.success("Summary regenerated!")
                st.markdown("### New Summary")
                st.markdown(result['summary'])
            except Exception as e:
                report_error(e, "Regenerating summary")

with col_chat:
    st.subheader("💬 Q&A Chat")
    st.markdown("Ask questions about the lecture content")
    
    # Display chat history
    if st.session_state.chat_history:
        with st.container(height=400):
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
    
    # Chat input
    st.divider()
    
    if question := st.chat_input("Ask a question about the lecture..."):
        if not transcript_text:
            st.error("No transcript available to answer questions.")
        else:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(question)
            
            # Generate answer with progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.write("📍 Searching lecture content...")
                progress_bar.progress(20)
                
                from processors.summarizer import Summarizer
                summarizer = Summarizer()
                
                status_text.write("📍 Analyzing and generating answer...")
                start_time = time.time()
                progress_bar.progress(40)
                
                answer_result = summarizer.answer_question(transcript_text, question)
                progress_bar.progress(90)
                
                # Add bot response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer_result['answer']
                })
                
                elapsed = ProgressTracker.get_elapsed_time(start_time)
                progress_bar.progress(100)
                status_text.write(f"✅ Answer found in {elapsed}!")
                
                # Display bot response
                with st.chat_message("assistant"):
                    st.markdown(answer_result['answer'])
                    st.caption(f"✅ Confidence: {answer_result['confidence']:.0f}%")
                
                # Rerun to update chat display
                st.rerun()
            except Exception as e:
                report_error(e, "Answering question")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", width="stretch"):
        st.session_state.chat_history = []
        st.rerun()
