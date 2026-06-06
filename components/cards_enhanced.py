"""
Enhanced Cards Component - Modern glassmorphism design with animations
"""
from typing import Any, Callable, Optional
import streamlit as st

def info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """Display a modern information card with glassmorphism"""
    st.markdown(f"""
    <div class="card-glass animate-fade" style="
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.9) 0%, rgba(236, 72, 153, 0.9) 100%);
        border-radius: 16px; 
        padding: 2rem; 
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="display: flex; align-items: flex-start; gap: 1rem;">
            <div style="font-size: 2.5rem; flex-shrink: 0;">{icon}</div>
            <div>
                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.5rem;">
                    {title}
                </h3>
                <p style="color: rgba(255, 255, 255, 0.95); margin: 0; line-height: 1.6;">
                    {content}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(label: str, value: Any, delta: Optional[float] = None, icon: str = "📊") -> None:
    """Display a modern metric card with animations"""
    delta_html = ""
    if delta:
        delta_color = "#10B981" if delta > 0 else "#EF4444"
        delta_text = f"+" if delta > 0 else ""
        delta_html = f"""
        <div style="
            background: linear-gradient(135deg, {delta_color}20 0%, {delta_color}10 100%);
            color: {delta_color};
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.75rem;
            border-left: 3px solid {delta_color};
        ">
            {delta_text}{delta}% from last week
        </div>
        """
    
    st.markdown(f"""
    <div class="metric-card hover-lift animate-fade" style="
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
        border-radius: 16px;
        padding: 1.75rem;
        border-left: 5px solid;
        background-clip: padding-box;
        border-image: linear-gradient(180deg, #6366F1 0%, #EC4899 100%) 1;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        margin: 1rem 0;
    ">
        <div style="display: flex; align-items: flex-start; justify-content: space-between;">
            <div style="flex: 1;">
                <p style="color: #64748B; margin: 0; font-size: 0.95rem; font-weight: 500;">
                    {label}
                </p>
                <h2 style="
                    background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin: 0.75rem 0 0 0;
                    font-size: 2rem;
                    font-weight: 800;
                ">
                    {value}
                </h2>
                {delta_html}
            </div>
            <div style="font-size: 2.5rem; opacity: 0.2; flex-shrink: 0;">
                {icon}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def feature_card(icon: str, title: str, description: str) -> None:
    """Display a modern feature card"""
    st.markdown(f"""
    <div class="card-glass hover-lift animate-fade" style="
        border: 2px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #6366F1 0%, #EC4899 100%) border-box;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    ">
        <div style="
            font-size: 3.5rem;
            margin-bottom: 1rem;
            animation: bounce 3s infinite;
        ">
            {icon}
        </div>
        <h3 style="
            color: #1E293B;
            margin: 0 0 0.75rem 0;
            font-size: 1.25rem;
            font-weight: 700;
        ">
            {title}
        </h3>
        <p style="
            color: #64748B;
            margin: 0;
            font-size: 0.95rem;
            line-height: 1.6;
        ">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)

def stat_group(stats: list[dict[str, Any]]) -> None:
    """Display a group of stat cards in a grid"""
    cols = st.columns(len(stats))
    for i, (col, stat) in enumerate(zip(cols, stats)):
        with col:
            metric_card(
                label=stat.get('label', 'Stat'),
                value=stat.get('value', '0'),
                delta=stat.get('delta'),
                icon=stat.get('icon', '📊')
            )

def activity_timeline(activities: list[dict[str, Any]]) -> None:
    """Display an activity timeline"""
    timeline_html = '<div style="position: relative; padding: 1rem 0 1rem 2rem;">'
    
    for i, activity in enumerate(activities):
        is_last = i == len(activities) - 1
        timeline_html += f"""
        <div style="
            position: relative;
            margin-bottom: 2rem;
            animation: slideIn 0.5s ease-out;
            animation-delay: {i * 0.1}s;
        ">
            <div style="
                position: absolute;
                left: -1.75rem;
                top: 0.5rem;
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
                border: 3px solid white;
                box-shadow: 0 0 0 3px #6366F1;
            "></div>
            {'' if is_last else '<div style="position: absolute; left: -1.41rem; top: 2rem; width: 2px; height: 2rem; background: #E2E8F0;"></div>'}
            
            <div class="card-glass" style="
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%);
                border-left: 4px solid #6366F1;
                padding: 1rem 1.5rem;
            ">
                <p style="margin: 0; font-weight: 600; color: #1E293B;">
                    {activity.get('title', 'Activity')}
                </p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #64748B;">
                    {activity.get('description', '')}
                </p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #94A3B8;">
                    {activity.get('time', '')}
                </p>
            </div>
        </div>
        """
    
    timeline_html += '</div>'
    st.markdown(timeline_html, unsafe_allow_html=True)

def progress_card(title: str, progress: float, description: str = "") -> None:
    """Display a progress card with animation"""
    st.markdown(f"""
    <div class="card-glass animate-fade" style="padding: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #1E293B; font-size: 1rem;">
                {title}
            </h4>
            <span style="
                background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
                font-size: 1.1rem;
            ">
                {int(progress)}%
            </span>
        </div>
        
        <div style="
            width: 100%;
            height: 8px;
            background: #E2E8F0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 0.75rem;
        ">
            <div style="
                width: {progress}%;
                height: 100%;
                background: linear-gradient(90deg, #6366F1 0%, #EC4899 100%);
                border-radius: 10px;
                transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
            "></div>
        </div>
        
        {f'<p style="margin: 0; font-size: 0.9rem; color: #64748B;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)

def gradient_divider() -> None:
    """Display a gradient divider"""
    st.markdown("""
    <div style="
        height: 2px;
        background: linear-gradient(90deg, #6366F1 0%, #EC4899 50%, transparent 100%);
        margin: 2rem 0;
        border-radius: 2px;
    "></div>
    """, unsafe_allow_html=True)
