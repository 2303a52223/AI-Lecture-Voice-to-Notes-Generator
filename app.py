"""
Lecture Voice-to-Notes Generator
Main Application Entry Point

A powerful AI-powered study assistant that converts lecture recordings 
into comprehensive study materials using local AI models.

Features:
- Speech-to-text transcription using Whisper
- AI-powered summarization
- Quiz and flashcard generation
- Text analysis and insights
- 100% local processing - no API keys required

Author: AI Study Assistant Team
Version: 1.0.0
"""

import streamlit as st
from pathlib import Path
from components.sidebar import render_sidebar
from components.cards_enhanced import feature_card, info_card, gradient_divider
from utils.state_manager import init_session_state, get_state_manager

# Page configuration
st.set_page_config(
    page_title="Lecture Voice-to-Notes Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path(__file__).parent / "assets" / "style.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Dark mode toggle
col1, col2 = st.columns([10, 1])
with col2:
    st.session_state.theme_mode = "dark" if st.toggle("🌙", key="theme_mode_dark", help="Toggle dark mode") else "light"

# Render sidebar
render_sidebar()

# Main content
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1>🎓 Lecture Voice-to-Notes Generator</h1>
    <p style="font-size: 1.3rem; color: var(--text-light); margin: 1rem 0;">
        Transform lectures into comprehensive study materials with AI
    </p>
</div>
""", unsafe_allow_html=True)

gradient_divider()

st.divider()

# Feature showcase
st.markdown("### ✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    feature_card(
        "🎤",
        "Speech-to-Text",
        "Convert lecture audio to accurate text transcripts using local Whisper models"
    )

with col2:
    feature_card(
        "📝",
        "Smart Summaries",
        "Generate AI-powered summaries and key points from your lectures"
    )

with col3:
    feature_card(
        "❓",
        "Quiz Generator",
        "Create practice quizzes and flashcards to test your knowledge"
    )

gradient_divider()

# Getting started section
st.markdown("### 🚀 Getting Started")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    #### Follow these simple steps:
    
    1. **📤 Upload** your lecture audio file (MP3, WAV, M4A, etc.)
    2. **🎤 Transcribe** - AI converts speech to text automatically
    3. **📊 Summarize** - Get key points and study notes
    4. **❓ Practice** - Test yourself with AI-generated quizzes
    5. **📈 Track** - Monitor your learning progress
    
    All processing happens locally on your device - completely private!
    """)
    
    if st.button("📤 Upload Your First Lecture", type="primary", width="stretch"):
        st.switch_page("pages/01_📤_Upload.py")

with col2:
    # System status
    st.markdown("#### 🖥️ System Status")
    
    # Check GPU
    try:
        import torch  # type: ignore[import-unresolved]

        gpu_available = torch.cuda.is_available()
    except ImportError:
        gpu_available = False
        torch = None  # type: ignore[assignment]

    st.session_state.gpu_available = gpu_available
    
    if gpu_available:
        gpu_name = torch.cuda.get_device_name(0)  # type: ignore[possibly-undefined]
        st.success(f"✅ GPU: {gpu_name}")
    else:
        st.info("ℹ️ CPU Mode (GPU recommended for speed)")
    
    # Check models status
    import os
    models_dir = "models"
    if os.path.exists(models_dir) and os.listdir(models_dir):
        st.success("✅ AI Models Ready")
    else:
        st.warning("⚠️ Models will download on first use (~1GB)")

gradient_divider()

# Statistics overview
state_manager = get_state_manager()
analytics = state_manager.get_analytics()

if analytics.get('total_lectures', 0) > 0:
    st.markdown("### 📊 Your Progress")
    
    from utils.helpers import format_duration
    from utils.file_handler import FileHandler
    
    file_handler = FileHandler()
    storage = file_handler.get_storage_info()
    total_duration = analytics.get('total_duration', 0)
    duration_str = format_duration(total_duration) if total_duration > 0 else "0s"
    
    from components.cards_enhanced import stat_group
    stat_group([
        {'label': 'Lectures Processed', 'value': analytics.get('total_lectures', 0), 'icon': '📚'},
        {'label': 'Total Duration', 'value': duration_str, 'icon': '⏱️'},
        {'label': 'Quizzes Taken', 'value': analytics.get('total_quizzes', 0), 'icon': '❓'},
        {'label': 'Storage Used', 'value': storage.get('total_size', '0 KB'), 'icon': '💾'},
    ])
    
    gradient_divider()
    
    # Recent lectures
    lectures = state_manager.get_all_lectures()
    if lectures:
        st.markdown("### 📚 Recent Lectures")
        
        # Show last 3 lectures
        recent_lectures = sorted(
            lectures,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )[:3]
        
        for lecture in recent_lectures:
            from components.cards import lecture_card
            with st.container():
                lecture_card(lecture)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("📝 Transcript", key=f"trans_{lecture['id']}", width="stretch"):
                        st.session_state.current_lecture_id = lecture['id']
                        st.switch_page("pages/02_📝_Transcript.py")
                with col2:
                    if st.button("📊 Summary", key=f"sum_{lecture['id']}", width="stretch"):
                        st.session_state.current_lecture_id = lecture['id']
                        st.switch_page("pages/03_📊_Summary.py")
                with col3:
                    if st.button("❓ Quiz", key=f"quiz_{lecture['id']}", width="stretch"):
                        st.session_state.current_lecture_id = lecture['id']
                        st.switch_page("pages/04_❓_Quiz.py")
                with col4:
                    if st.button("🗑️ Delete", key=f"del_{lecture['id']}", width="stretch"):
                        if state_manager.delete_lecture(lecture['id']):
                            st.success("Deleted!")
                            st.rerun()
        
        if st.button("📈 View All Lectures", width="stretch"):
            st.switch_page("pages/05_📈_Analytics.py")

gradient_divider()

# Information cards
col1, col2 = st.columns(2)

with col1:
    info_card(
        "🔒 100% Private",
        "All AI processing happens locally on your device. No data is sent to external servers. No API keys required.",
        "🔒"
    )

with col2:
    info_card(
        "🆓 Completely Free",
        "Uses open-source AI models like Whisper and BART. No subscriptions, no usage limits, no hidden costs.",
        "💰"
    )

gradient_divider()

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; opacity: 0.7;">
    <p style="margin: 0; font-size: 0.9rem; color: var(--text-light);">
        Built with ❤️ using Streamlit & AI | © 2026 Lecture Voice-to-Notes Generator
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# How it works
with st.expander("🤔 How does it work?"):
    st.markdown("""
    ### Technology Stack
    
    This application uses several powerful AI models running locally on your device:
    
    **🎤 Speech-to-Text: OpenAI Whisper**
    - State-of-the-art speech recognition
    - Supports multiple languages
    - Highly accurate transcription
    - Models range from 39M to 1550M parameters
    
    **📝 Summarization: BART / T5**
    - Advanced transformer models for text summarization
    - Generates coherent summaries from long texts
    - Extracts key points automatically
    
    **❓ Quiz Generation: Custom NLP Pipeline**
    - Uses NLTK for text processing
    - Multiple question types (MCQ, True/False, Fill-in-blank)
    - Intelligent distractor generation
    
    **📊 Text Analysis: NLTK + TextStat**
    - Readability scoring
    - Word frequency analysis
    - Sentiment analysis
    - Complexity metrics
    
    ### First Run Setup
    
    On first use, the application will download AI models (~500MB-1GB):
    - Whisper model: ~150MB (base model)
    - BART model: ~1.6GB (for summarization)
    - NLTK data: ~50MB (for text processing)
    
    These models are cached locally and reused for all future sessions.
    
    ### System Requirements
    
    **Minimum:**
    - Python 3.8+
    - 8GB RAM
    - 2GB disk space
    - CPU with AVX support
    
    **Recommended:**
    - 16GB RAM
    - NVIDIA GPU with 4GB+ VRAM (for faster processing)
    - 5GB disk space
    """)

# Tips
with st.expander("💡 Tips for Best Results"):
    st.markdown("""
    **Audio Quality:**
    - Use clear, high-quality recordings
    - Minimize background noise
    - Ensure speaker is audible
    - Avoid multiple overlapping voices
    
    **File Formats:**
    - MP3, WAV recommended for best compatibility
    - M4A, OGG, FLAC also supported
    - Maximum file size: 500MB
    
    **Processing Time:**
    - Base model: ~15% of audio length
    - Small model: ~30% of audio length
    - GPU can speed up 2-3x
    - First run takes longer (model download)
    
    **Accuracy:**
    - English audio: 95%+ accuracy with base model
    - Other languages: Use language-specific setting
    - Technical terms may need manual review
    """)

st.divider()

# Quick links
st.markdown("### 📚 Quick Links")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📤 Upload", width="stretch"):
        st.switch_page("pages/01_📤_Upload.py")

with col2:
    if st.button("📈 Analytics", width="stretch"):
        st.switch_page("pages/05_📈_Analytics.py")

with col3:
    if st.button("⚙️ Settings", width="stretch"):
        st.switch_page("pages/06_⚙️_Settings.py")

with col4:
    if st.button("ℹ️ About", width="stretch"):
        st.info("Lecture Voice-to-Notes Generator v1.0.0")

st.divider()

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #888;">
    <p style="margin: 0; font-size: 0.9rem;">
        Made with ❤️ for students worldwide
    </p>
    <p style="margin: 0.5rem 0; font-size: 0.85rem;">
        Open Source • Privacy First • Forever Free
    </p>
    <p style="margin: 0.5rem 0; font-size: 0.8rem;">
        🔒 100% Local Processing • No API Keys • No Data Collection
    </p>
</div>
""", unsafe_allow_html=True)
