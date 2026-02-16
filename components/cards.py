"""
Cards Component - Reusable card layouts
"""
from typing import Any, Callable, Optional
import streamlit as st

def info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """Display an information card"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: white; margin: 0 0 0.5rem 0;">
            {icon} {title}
        </h3>
        <p style="color: white; margin: 0; opacity: 0.95;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)

def metric_card(label: str, value: Any, delta: Optional[float] = None, icon: str = "📊") -> None:
    """Display a metric card"""
    delta_html = ""
    if delta:
        delta_color = "#28a745" if delta > 0 else "#dc3545"
        delta_html = f'<p style="color: {delta_color}; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{"+" if delta > 0 else ""}{delta}</p>'
    
    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 1.5rem;
                border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin: 0.5rem 0;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">{label}</p>
                <h2 style="color: #2c3e50; margin: 0.5rem 0;">{value}</h2>
                {delta_html}
            </div>
            <div style="font-size: 2.5rem; opacity: 0.3;">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def lecture_card(lecture: dict[str, Any], on_click_callback: Optional[Callable[..., Any]] = None) -> None:
    """Display a lecture card"""
    from utils.helpers import time_ago, format_duration
    
    title = lecture.get('title', 'Untitled Lecture')
    created = time_ago(lecture.get('created_at', ''))
    duration = format_duration(lecture.get('duration', 0))
    _ = lecture.get('id')  # lecture_id available for future use
    
    # Determine status badge
    status = "📝 Transcribed"
    if lecture.get('summary'):
        status = "✅ Complete"
    elif lecture.get('transcript'):
        status = "📝 Transcribed"
    else:
        status = "🎤 Uploaded"
    
    card_html = f"""
    <div style="background: white; border-radius: 10px; padding: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 1rem 0;
                border-left: 4px solid #667eea; transition: transform 0.2s;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <h3 style="color: #2c3e50; margin: 0 0 0.5rem 0;">{title}</h3>
                <p style="color: #666; margin: 0.25rem 0; font-size: 0.9rem;">
                    ⏱️ {duration} • 📅 {created}
                </p>
                <p style="color: #667eea; margin: 0.5rem 0 0 0; font-size: 0.85rem; font-weight: 600;">
                    {status}
                </p>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def feature_card(icon: str, title: str, description: str) -> None:
    """Display a feature card"""
    st.markdown(f"""
    <div style="background: #f8f9fa; border-radius: 10px; padding: 1.5rem;
                margin: 1rem 0; text-align: center; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="color: #2c3e50; margin: 0 0 0.5rem 0;">{title}</h3>
        <p style="color: #666; margin: 0; font-size: 0.95rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def quiz_question_card(question: str, question_num: int) -> None:
    """Display a quiz question card"""
    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 1.5rem;
                margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;">
        <h4 style="color: #2c3e50; margin: 0 0 1rem 0;">
            Question {question_num}
        </h4>
        <p style="color: #444; margin: 0; font-size: 1.05rem; line-height: 1.6;">
            {question}
        </p>
    </div>
    """, unsafe_allow_html=True)

def result_card(title: str, content: str, card_type: str = "info") -> None:
    """Display a result card"""
    colors = {
        "success": {"bg": "#d4edda", "border": "#28a745", "text": "#155724"},
        "error": {"bg": "#f8d7da", "border": "#dc3545", "text": "#721c24"},
        "warning": {"bg": "#fff3cd", "border": "#ffc107", "text": "#856404"},
        "info": {"bg": "#d1ecf1", "border": "#17a2b8", "text": "#0c5460"}
    }
    
    color = colors.get(card_type, colors["info"])
    
    st.markdown(f"""
    <div style="background: {color['bg']}; border-radius: 8px; padding: 1.25rem;
                margin: 1rem 0; border-left: 4px solid {color['border']};">
        <h4 style="color: {color['text']}; margin: 0 0 0.5rem 0;">{title}</h4>
        <p style="color: {color['text']}; margin: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def summary_card(title: str, content: str, icon: str = "📝") -> None:
    """Display a summary card"""
    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 1.5rem;
                margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3 style="color: #667eea; margin: 0 0 1rem 0;">
            {icon} {title}
        </h3>
        <div style="color: #444; line-height: 1.8;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def stat_card(value: Any, label: str, color: str = "#667eea") -> None:
    """Display a statistic card"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                border-radius: 10px; padding: 1.5rem; margin: 0.5rem 0;
                text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h2 style="color: white; margin: 0 0 0.5rem 0; font-size: 2.5rem;">{value}</h2>
        <p style="color: white; margin: 0; opacity: 0.9;">{label}</p>
    </div>
    """, unsafe_allow_html=True)
