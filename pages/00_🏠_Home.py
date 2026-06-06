"""
Home Page - Modern Dashboard with Analytics
"""
import streamlit as st
from pathlib import Path
from utils.state_manager import StateManager
from utils.helpers import format_duration
from components.sidebar import render_sidebar
from components.cards_enhanced import (
    info_card, metric_card, feature_card, stat_group,
    activity_timeline, progress_card, gradient_divider
)
import json
from datetime import datetime, timedelta


def dashboard_kpis(lectures):
    total_lectures = len(lectures)
    total_duration = sum(l.get('duration', 0) for l in lectures)
    total_summaries = len([l for l in lectures if l.get('summary_text')])
    total_quizzes = len([l for l in lectures if l.get('quiz')])
    return total_lectures, total_duration, total_summaries, total_quizzes

# Page config
st.set_page_config(
    page_title="Dashboard - Lecture Notes Generator",
    page_icon="🏠",
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

# Sidebar
render_sidebar()

# Dark mode toggle in sidebar
if st.sidebar.checkbox("🌙 Dark Mode", key="dark_mode_toggle"):
    st.markdown("""
    <script>
    document.documentElement.setAttribute('data-theme', 'dark');
    </script>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
<section class='hero-shell'>
    <div class='hero-card'>
        <div class='hero-eyebrow'>Lecture workspace</div>
        <h1>🎓 Lecture Voice-to-Notes Generator</h1>
        <p class='hero-copy'>Transform lectures into transcripts, summaries, quizzes, and study packs with a local-first workflow.</p>
        <div class='hero-pills'>
            <span>Local AI</span>
            <span>Private by default</span>
            <span>Fast study output</span>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# Hero CTAs (use Streamlit buttons so global CSS applies)
cta_col1, cta_col2 = st.columns([1, 1])
with cta_col1:
    if st.button("📤 Upload New Lecture", width="stretch", key="hero_upload"):
        st.switch_page("pages/01_📤_Upload.py")
with cta_col2:
    if st.button("📊 View Summaries", width="stretch", key="hero_summaries"):
        st.switch_page("pages/03_📊_Summary.py")

gradient_divider()

# Get analytics data
lectures = state_manager.get_all_lectures()

# Calculate stats
total_lectures, total_duration, total_summaries, total_quizzes = dashboard_kpis(lectures)

# Stats Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("📚 Total Lectures", total_lectures, delta=15 if total_lectures > 5 else 5, icon="📚")

with col2:
    hours = total_duration / 3600 if total_duration else 0
    metric_card("⏱️ Total Hours", f"{hours:.1f}h", delta=10, icon="⏱️")

with col3:
    metric_card("📝 Summaries", total_summaries, delta=20, icon="📝")

with col4:
    metric_card("❓ Quizzes", total_quizzes, delta=8, icon="❓")

gradient_divider()

# Features Section
st.markdown("### ✨ Key Features")

feature_cols = st.columns(3)

with feature_cols[0]:
    feature_card(
        "🎤",
        "Smart Transcription",
        "Convert any lecture format to accurate text using advanced AI models"
    )

with feature_cols[1]:
    feature_card(
        "✂️",
        "Intelligent Summaries",
        "Generate custom summaries with adjustable compression and topic filtering"
    )

with feature_cols[2]:
    feature_card(
        "💬",
        "Q&A Chat",
        "Ask questions and get instant answers about your lecture content"
    )

gradient_divider()

# Recent Activity
if lectures:
    st.markdown("### 📊 Recent Activity")
    
    # Get last 5 lectures
    recent_lectures = sorted(
        lectures,
        key=lambda x: x.get('created_at', ''),
        reverse=True
    )[:5]
    
    activities = []
    for lecture in recent_lectures:
        created = lecture.get('created_at', '')
        status = "✅"
        if lecture.get('summary_text'):
            action = "Generated summary"
        elif lecture.get('transcript_text'):
            action = "Transcribed"
        else:
            action = "Uploaded"
            status = "📤"
        
        activities.append({
            'title': f"{status} {lecture.get('title', 'Untitled')}",
            'description': action,
            'time': created
        })
    
    if activities:
        activity_timeline(activities)

gradient_divider()

# Quick Actions
st.markdown("### ⚡ Quick Actions")

quick_cols = st.columns(3)

with quick_cols[0]:
    if st.button("📤 Upload New Lecture", width="stretch", key="quick_upload"):
        st.switch_page("pages/01_📤_Upload.py")

with quick_cols[1]:
    if st.button("📋 View Transcripts", width="stretch", key="quick_transcripts"):
        st.switch_page("pages/02_📝_Transcript.py")

with quick_cols[2]:
    if st.button("📊 View Summaries", width="stretch", key="quick_summaries"):
        st.switch_page("pages/03_📊_Summary.py")

gradient_divider()

# Learning Progress Section
if total_lectures > 0:
    st.markdown("### 📈 Learning Progress")
    
    progress_cols = st.columns(2)
    
    with progress_cols[0]:
        summary_progress = (total_summaries / total_lectures) * 100
        progress_card(
            "Summary Completion",
            summary_progress,
            f"{total_summaries} of {total_lectures} lectures summarized"
        )
    
    with progress_cols[1]:
        quiz_progress = (total_quizzes / total_lectures) * 100 if total_quizzes else 0
        progress_card(
            "Quiz Generation",
            quiz_progress,
            f"{total_quizzes} quizzes created"
        )

gradient_divider()

# Tips Section
st.markdown("### 💡 Tips & Tricks")

tip_cols = st.columns(3)

with tip_cols[0]:
    info_card(
        "📌 Custom Reduction",
        "Adjust the reduction percentage (30-90%) to create summaries of any length you need.",
        "📌"
    )

with tip_cols[1]:
    info_card(
        "🎯 Topic Filtering",
        "Filter summaries by specific topics to focus on what matters to you.",
        "🎯"
    )

with tip_cols[2]:
    info_card(
        "💬 Ask Questions",
        "Use the Q&A chat to get instant answers from your lecture content.",
        "💬"
    )

gradient_divider()

# Footer
st.markdown("""
<footer class='page-footer'>
    <p>Built with Streamlit and local AI tooling for private lecture study.</p>
</footer>
""", unsafe_allow_html=True)
