"""
Charts Component - Data visualization charts
"""
from typing import Any
import streamlit as st
import plotly.graph_objects as go  # type: ignore
import plotly.express as px  # type: ignore
import pandas as pd
import matplotlib.pyplot as plt

def render_word_frequency_chart(word_freq_data: list[dict[str, Any]]) -> None:
    """
    Render word frequency bar chart
    
    Args:
        word_freq_data: List of dicts with 'word' and 'count' keys
    """
    if not word_freq_data:
        st.info("No word frequency data available")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(word_freq_data)
    
    # Create bar chart
    fig = px.bar(
        df.head(15),
        x='count',
        y='word',
        orientation='h',
        title='Most Frequent Words',
        labels={'count': 'Frequency', 'word': 'Word'},
        color='count',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_readability_gauge(readability_score: float) -> None:
    """
    Render readability gauge chart
    
    Args:
        readability_score: Flesch Reading Ease score (0-100)
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=readability_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Readability Score", 'font': {'size': 24}},
        delta={'reference': 60, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 30], 'color': "#f8d7da"},
                {'range': [30, 50], 'color': "#fff3cd"},
                {'range': [50, 70], 'color': "#d1ecf1"},
                {'range': [70, 100], 'color': "#d4edda"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def render_word_cloud(text: str, title: str = "Word Cloud") -> None:
    """
    Render word cloud
    
    Args:
        text: Text to generate word cloud from
        title: Chart title
    """
    try:
        from wordcloud import WordCloud
        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(text)
        
        # Display
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=16, pad=20)
        
        st.pyplot(fig)
        plt.close()
        
    except ImportError:
        st.info("Word cloud package not available. Install with: pip install wordcloud")
    except Exception as e:
        st.error(f"Error generating word cloud: {e}")

def render_lecture_timeline(lectures: list[dict[str, Any]]) -> None:
    """
    Render timeline of lectures
    
    Args:
        lectures: List of lecture objects
    """
    if not lectures:
        st.info("No lectures to display")
        return
    
    # Prepare data
    from datetime import datetime
    
    timeline_data = []
    for lecture in lectures:
        try:
            date = datetime.fromisoformat(lecture['created_at']).strftime('%Y-%m-%d')
            timeline_data.append({
                'Date': date,
                'Title': lecture.get('title', 'Untitled'),
                'Duration': lecture.get('duration', 0)
            })
        except:
            continue
    
    if not timeline_data:
        st.info("No valid lecture data")
        return
    
    df = pd.DataFrame(timeline_data)
    
    # Create timeline chart
    fig = px.scatter(
        df,
        x='Date',
        y='Duration',
        size='Duration',
        hover_data=['Title'],
        title='Lecture Timeline',
        color='Duration',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title='Date',
        yaxis_title='Duration (seconds)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_analytics_dashboard(analytics: dict[str, Any], lectures: list[dict[str, Any]]) -> None:
    """
    Render complete analytics dashboard
    
    Args:
        analytics: Analytics data dict
        lectures: List of lecture objects
    """
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Lectures",
            analytics.get('total_lectures', 0),
            delta=None
        )
    
    with col2:
        from utils.helpers import format_duration
        total_duration = analytics.get('total_duration', 0)
        st.metric(
            "Total Duration",
            format_duration(total_duration) if total_duration > 0 else "0s",
            delta=None
        )
    
    with col3:
        st.metric(
            "Quizzes Taken",
            analytics.get('total_quizzes', 0),
            delta=None
        )
    
    st.divider()
    
    # Lecture timeline
    if lectures:
        render_lecture_timeline(lectures)
    
    st.divider()
    
    # Lecture distribution by month
    if lectures:
        from datetime import datetime
        
        month_data = {}
        for lecture in lectures:
            try:
                date = datetime.fromisoformat(lecture['created_at'])
                month_key = date.strftime('%Y-%m')
                month_data[month_key] = month_data.get(month_key, 0) + 1
            except:
                continue
        
        if month_data:
            df = pd.DataFrame(list(month_data.items()), columns=['Month', 'Count'])
            
            fig = px.bar(
                df,
                x='Month',
                y='Count',
                title='Lectures per Month',
                color='Count',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

def render_quiz_results_chart(results: dict[str, Any]) -> None:
    """
    Render quiz results pie chart
    
    Args:
        results: Quiz results with correct/incorrect counts
    """
    correct = results.get('correct', 0)
    incorrect = results.get('total', 0) - correct
    
    fig = go.Figure(data=[go.Pie(
        labels=['Correct', 'Incorrect'],
        values=[correct, incorrect],
        hole=.4,
        marker_colors=['#28a745', '#dc3545']
    )])
    
    fig.update_layout(
        title="Quiz Results",
        height=350,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_text_stats_chart(stats: dict[str, Any]) -> None:
    """
    Render text statistics
    
    Args:
        stats: Dictionary with text statistics
    """
    # Create metrics display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Words", stats.get('total_words', 0))
        st.metric("Sentences", stats.get('total_sentences', 0))
    
    with col2:
        st.metric("Unique Words", stats.get('unique_words', 0))
        st.metric("Paragraphs", stats.get('total_paragraphs', 0))
    
    with col3:
        st.metric("Avg Sentence Length", f"{stats.get('avg_sentence_length', 0)} words")
        st.metric("Lexical Diversity", f"{stats.get('lexical_diversity', 0)}%")
