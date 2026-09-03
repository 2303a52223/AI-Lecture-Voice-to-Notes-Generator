"""
Cards Component - Reusable card layouts (legacy support)
These complement cards_enhanced.py with additional card types
"""
from typing import Any, Callable, Optional
import streamlit as st


def lecture_card(lecture: dict[str, Any], on_click_callback: Optional[Callable[..., Any]] = None) -> None:
    """Display a lecture card"""
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h4 style="margin: 0 0 0.5rem 0; color: #333;">
            {lecture.get('title', 'Untitled Lecture')}
        </h4>
        <p style="margin: 0.5rem 0; color: #666; font-size: 0.9rem;">
            📚 {lecture.get('subject', 'No subject')}
        </p>
        <p style="margin: 0.5rem 0; color: #666; font-size: 0.9rem;">
            📅 {lecture.get('date', 'No date')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    if on_click_callback:
        on_click_callback()


def quiz_question_card(question: str, question_num: int) -> None:
    """Display a quiz question card"""
    st.markdown(f"""
    <div style="background: #f8f9fa; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;
                border-left: 4px solid #667eea;">
        <p style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #333;">
            Question {question_num}
        </p>
        <p style="margin: 1rem 0 0 0; color: #555;">
            {question}
        </p>
    </div>
    """, unsafe_allow_html=True)


def result_card(title: str, content: str, card_type: str = "info") -> None:
    """Display a result card"""
    color_map = {
        "success": "#28a745",
        "error": "#dc3545",
        "warning": "#ffc107",
        "info": "#17a2b8"
    }
    color = color_map.get(card_type, "#17a2b8")
    
    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;
                border-left: 4px solid {color};">
        <h4 style="margin: 0 0 0.5rem 0; color: {color};">
            {title}
        </h4>
        <p style="margin: 0; color: #555;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)


def summary_card(title: str, content: str, icon: str = "📝") -> None:
    """Display a summary card"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: white; margin: 0 0 0.5rem 0;">
            {icon} {title}
        </h3>
        <p style="color: white; margin: 0; opacity: 0.95; line-height: 1.6;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """Display an information card (alias to cards_enhanced version)"""
    from components.cards_enhanced import info_card as info_card_enhanced
    info_card_enhanced(title, content, icon)


def metric_card(label: str, value: Any, delta: Optional[float] = None, icon: str = "📊") -> None:
    """Display a metric card (alias to cards_enhanced version)"""
    from components.cards_enhanced import metric_card as metric_card_enhanced
    metric_card_enhanced(label, value, delta, icon)
