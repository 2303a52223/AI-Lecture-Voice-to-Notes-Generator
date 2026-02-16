"""
Analytics Page - Text analysis and visualizations
"""
import streamlit as st
from pathlib import Path
from utils.state_manager import StateManager
from utils.helpers import format_duration
from components.sidebar import render_sidebar
from components.cards import metric_card

# Page config
st.set_page_config(
    page_title="Analytics - Lecture Notes Generator",
    page_icon="📈",
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
st.title("📈 Analytics")
st.markdown("Analyze your lecture content with detailed text statistics and visualizations.")

st.divider()

# Get lectures
lectures = state_manager.get_all_lectures()

if not lectures:
    st.info("📤 No lectures found. Upload a lecture first!")
    st.page_link("pages/01_📤_Upload.py", label="Go to Upload", icon="📤")
    st.stop()

# Dashboard or single lecture view
view_mode = st.radio(
    "View Mode",
    options=["📊 Single Lecture", "📈 Dashboard"],
    horizontal=True
)

st.divider()

if view_mode == "📊 Single Lecture":
    # Lecture selector
    lecture_titles = [l.get('title', f"Lecture {l.get('id', '?')}") for l in lectures]
    selected_idx = st.selectbox(
        "Select Lecture",
        range(len(lectures)),
        format_func=lambda x: lecture_titles[x]
    )
    
    lecture = lectures[selected_idx]
    transcript_text = lecture.get('transcript_text', '')
    
    if not transcript_text:
        st.warning("No transcript text available for analysis.")
        st.stop()
    
    # Run analysis
    analysis = lecture.get('analysis', {})
    
    if not analysis:
        with st.spinner("Analyzing text..."):
            try:
                from processors.text_analyzer import TextAnalyzer
                analyzer = TextAnalyzer()
                analysis = analyzer.analyze(transcript_text)
                
                if analysis is None:
                    st.error("Analysis returned no results.")
                    st.stop()
                
                # Save analysis
                state_manager.update_lecture(lecture.get('id'), {'analysis': analysis})
            except Exception as e:
                st.error(f"Error analyzing text: {e}")
                st.stop()
    
    if not analysis:
        st.error("No analysis data available.")
        st.stop()
    
    # Display analysis results
    st.subheader("📊 Text Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Words", f"{analysis.get('total_words', 0):,}")
    with col2:
        st.metric("Unique Words", f"{analysis.get('unique_words', 0):,}")
    with col3:
        st.metric("Sentences", f"{analysis.get('total_sentences', 0):,}")
    with col4:
        st.metric("Paragraphs", f"{analysis.get('total_paragraphs', 0):,}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Sentence Length", f"{analysis.get('avg_sentence_length', 0)} words")
    with col2:
        st.metric("Lexical Diversity", f"{analysis.get('lexical_diversity', 0)}%")
    with col3:
        st.metric("Reading Time", analysis.get('reading_time', 'N/A'))
    with col4:
        st.metric("Speaking Rate", f"{analysis.get('speaking_rate', 'N/A')} wpm")
    
    st.divider()
    
    # Readability
    st.subheader("📖 Readability Analysis")
    
    readability = analysis.get('readability', {})
    
    if readability:
        col1, col2 = st.columns(2)
        
        with col1:
            flesch_score = readability.get('flesch_reading_ease', 0)
            try:
                from components.charts import render_readability_gauge
                render_readability_gauge(flesch_score)
            except:
                st.metric("Flesch Reading Ease", f"{flesch_score}")
        
        with col2:
            st.markdown("### Readability Scores")
            for key, value in readability.items():
                label = key.replace('_', ' ').title()
                st.markdown(f"- **{label}**: {value}")
    
    st.divider()
    
    # Word frequency
    st.subheader("📊 Word Frequency")
    
    word_freq = analysis.get('word_frequency', [])
    
    if word_freq:
        try:
            from components.charts import render_word_frequency_chart
            render_word_frequency_chart(word_freq)
        except Exception as e:
            st.warning(f"Could not render chart: {e}")
            # Fallback to table
            import pandas as pd
            df = pd.DataFrame(word_freq[:20])
            st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # Word cloud
    st.subheader("☁️ Word Cloud")
    
    try:
        from components.charts import render_word_cloud
        render_word_cloud(transcript_text)
    except Exception as e:
        st.info(f"Word cloud not available: {e}")
    
    st.divider()
    
    # Text stats chart
    st.subheader("📈 Statistics Overview")
    try:
        from components.charts import render_text_stats_chart
        render_text_stats_chart(analysis)
    except:
        pass

else:
    # Dashboard view
    st.subheader("📈 Overall Dashboard")
    
    # Overall metrics
    total_lectures = len(lectures)
    total_words = sum(len(l.get('transcript_text', '').split()) for l in lectures)
    total_duration = sum(l.get('duration', 0) for l in lectures)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Lectures", total_lectures)
    with col2:
        st.metric("Total Words", f"{total_words:,}")
    with col3:
        st.metric("Total Duration", format_duration(total_duration))
    
    st.divider()
    
    # Analytics dashboard
    try:
        from components.charts import render_analytics_dashboard
        
        analytics_data = {
            'total_lectures': total_lectures,
            'total_duration': total_duration,
            'total_quizzes': 0  # Could fetch from quiz results
        }
        
        render_analytics_dashboard(analytics_data, lectures)
    except Exception as e:
        st.warning(f"Could not render dashboard: {e}")
    
    st.divider()
    
    # Lecture comparison table
    st.subheader("📋 Lecture Comparison")
    
    import pandas as pd
    
    comparison_data = []
    for lecture in lectures:
        text = lecture.get('transcript_text', '')
        comparison_data.append({
            'Title': lecture.get('title', 'Untitled'),
            'Subject': lecture.get('subject', 'N/A'),
            'Words': len(text.split()) if text else 0,
            'Duration': format_duration(lecture.get('duration', 0)),
            'Language': lecture.get('language', 'Unknown').upper()
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
