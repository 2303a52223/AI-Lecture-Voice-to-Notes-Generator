"""
Upload Page - Upload and process audio lectures
"""
import streamlit as st
from pathlib import Path
import time
from utils.state_manager import StateManager
from utils.file_handler import FileHandler
from utils.helpers import format_duration, format_file_size
from components.sidebar import render_sidebar
from components.cards import info_card, metric_card
from components.audio_player import render_audio_player

# Page config
st.set_page_config(
    page_title="Upload - Lecture Notes Generator",
    page_icon="📤",
    layout="wide"
)

# Load custom CSS
css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize
state_manager = StateManager()
file_handler = FileHandler()

# Sidebar
render_sidebar()

# Main content
st.title("📤 Upload Lecture")
st.markdown("Upload your lecture audio file for transcription and analysis.")

st.divider()

# Upload section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎵 Audio File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm'],
        help="Supported formats: MP3, WAV, M4A, OGG, FLAC, WebM"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # File info
        file_size = format_file_size(uploaded_file.size)
        st.caption(f"📁 Size: {file_size}")
        
        # Audio preview
        st.audio(uploaded_file)

with col2:
    st.subheader("📋 Lecture Details")
    
    lecture_title = st.text_input(
        "Lecture Title",
        placeholder="e.g., Introduction to Machine Learning",
        help="Give your lecture a descriptive title"
    )
    
    lecture_subject = st.text_input(
        "Subject / Course",
        placeholder="e.g., Computer Science 101",
        help="The subject or course this lecture belongs to"
    )
    
    lecture_tags = st.text_input(
        "Tags (comma-separated)",
        placeholder="e.g., ML, AI, neural networks",
        help="Add tags to help organize your lectures"
    )

st.divider()

# Processing options
st.subheader("⚙️ Processing Options")

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Language",
        options=['Auto-detect', 'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese'],
        index=0,
        help="Select the language of the lecture"
    )

with col2:
    summary_style = st.selectbox(
        "Summary Style",
        options=['concise', 'detailed', 'bullet_points'],
        index=0,
        help="Choose how the summary should be formatted"
    )

st.caption("🔗 Powered by AssemblyAI (universal-3-pro + universal-2 models)")

# Language mapping
language_map = {
    'Auto-detect': None,
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh',
    'Japanese': 'ja'
}

st.divider()

# Process button
if uploaded_file:
    if st.button("🚀 Process Lecture", type="primary", use_container_width=True):
        if not lecture_title:
            lecture_title = Path(uploaded_file.name).stem
        
        # Save uploaded file
        with st.spinner("Saving audio file..."):
            saved_path = file_handler.save_upload(uploaded_file)
            
            if not saved_path:
                st.error("❌ Error saving file. Please try again.")
                st.stop()
        
        # Create progress container
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Transcription
            status_text.text("🎤 Transcribing audio with AssemblyAI...")
            progress_bar.progress(5)
            
            try:
                from processors.transcriber import Transcriber
                
                transcriber = Transcriber()
                
                lang_code = language_map.get(language)
                
                # Progress callback that updates the Streamlit UI in real-time
                def update_progress(pct, msg):
                    progress_bar.progress(int(pct * 50))  # 0-50% for transcription
                    status_text.text(f"🎤 {msg}")
                
                transcription = transcriber.transcribe(
                    saved_path, language=lang_code, progress_callback=update_progress
                )
                
                # Save transcript
                transcript_path = file_handler.get_transcript_path(lecture_title)
                transcriber.save_transcript(transcription, transcript_path)
                
                progress_bar.progress(50)
                status_text.text("📝 Transcription complete! Generating summary...")
                
            except Exception as e:
                st.error(f"❌ Transcription error: {e}")
                st.stop()
            
            # Step 2: Summarization
            try:
                from processors.summarizer import Summarizer
                
                summarizer = Summarizer()
                summary_result = summarizer.summarize(
                    transcription['text'],
                    style=summary_style
                )
                
                # Generate study notes
                study_notes = summarizer.generate_study_notes(
                    transcription['text'],
                    title=lecture_title
                )
                
                # Save summary
                summary_path = file_handler.get_summary_path(lecture_title)
                Path(summary_path).parent.mkdir(parents=True, exist_ok=True)
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(study_notes)
                
                progress_bar.progress(75)
                status_text.text("📊 Analyzing text...")
                
            except Exception as e:
                st.warning(f"⚠️ Summary generation issue: {e}")
                summary_result = {'summary': 'Summary generation failed', 'method': 'none'}
                study_notes = ''
                summary_path = ''
                progress_bar.progress(75)
            
            # Step 3: Text Analysis
            try:
                from processors.text_analyzer import TextAnalyzer
                
                analyzer = TextAnalyzer()
                analysis = analyzer.analyze(transcription['text'])
                
                progress_bar.progress(90)
                
            except Exception as e:
                st.warning(f"⚠️ Analysis issue: {e}")
                analysis = {}
            
            # Step 4: Save to database
            status_text.text("💾 Saving lecture data...")
            
            tags_list = [t.strip() for t in lecture_tags.split(',') if t.strip()] if lecture_tags else []
            
            lecture_data = {
                'title': lecture_title,
                'subject': lecture_subject,
                'tags': tags_list,
                'audio_path': str(saved_path),
                'transcript_path': str(transcript_path) if transcript_path else '',
                'summary_path': str(summary_path) if summary_path else '',
                'transcript_text': transcription.get('text', ''),
                'summary_text': summary_result.get('summary', ''),
                'duration': transcription.get('duration', 0),
                'language': transcription.get('language', 'unknown'),
                'whisper_model': 'assemblyai',
                'analysis': analysis
            }
            
            lecture_id = state_manager.add_lecture(lecture_data)
            
            if lecture_id:
                st.session_state.current_lecture_id = lecture_id
                progress_bar.progress(100)
                status_text.text("✅ Processing complete!")
                
                # Success message
                st.success("🎉 Lecture processed successfully!")
                
                # Results summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    metric_card(
                        "Words",
                        str(len(transcription.get('text', '').split())),
                        icon="📝"
                    )
                with col2:
                    metric_card(
                        "Duration",
                        format_duration(transcription.get('duration', 0)),
                        icon="⏱️"
                    )
                with col3:
                    metric_card(
                        "Segments",
                        str(len(transcription.get('segments', []))),
                        icon="📋"
                    )
                
                st.info("👉 Navigate to **Transcript**, **Summary**, or **Quiz** pages to explore your lecture!")
                
            else:
                st.error("❌ Error saving lecture data.")
else:
    # Show instructions when no file is uploaded
    st.info("👆 Upload an audio file to get started!")
    
    # Feature cards
    st.subheader("✨ What you'll get")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        info_card(
            "🎤 Transcription",
            "Accurate speech-to-text conversion using AssemblyAI's universal models"
        )
    
    with col2:
        info_card(
            "📝 Summary",
            "AI-generated summaries and study notes from your lecture content"
        )
    
    with col3:
        info_card(
            "❓ Quiz",
            "Auto-generated quiz questions to test your understanding"
        )
    
    with col4:
        info_card(
            "📊 Analytics",
            "Text analysis with readability scores, word frequency, and more"
        )
