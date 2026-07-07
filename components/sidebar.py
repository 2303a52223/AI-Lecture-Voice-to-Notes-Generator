"""
Sidebar Component - Navigation and status information
"""
import streamlit as st
from utils.state_manager import get_state_manager

DEFAULT_APP_BACKGROUND = "#F8FAFC"
DEFAULT_APP_DARK_BACKGROUND = "#0F172A"


def _apply_theme_overrides(state_manager):
    """Apply global visual overrides from user settings."""
    theme_mode = st.session_state.get("theme_mode", "light")

    if theme_mode == "dark":
        st.markdown(
            f"""
            <style>
                :root {{
                    --bg-light: #0F172A;
                    --bg-white: #111827;
                    --bg-dark: #0F172A;
                    --bg-darker: #020617;
                    --app-bg-base: {DEFAULT_APP_DARK_BACKGROUND};
                    --app-bg-end: #111827;
                    --text-dark: #F8FAFC;
                    --text-light: #CBD5E1;
                    --text-muted: #94A3B8;
                    --surface: rgba(15, 23, 42, 0.82);
                    --surface-strong: rgba(15, 23, 42, 0.94);
                    --border-soft: rgba(148, 163, 184, 0.18);
                }}

                body {{
                    background:
                        radial-gradient(circle at top left, rgba(99, 102, 241, 0.14), transparent 28%),
                        radial-gradient(circle at top right, rgba(236, 72, 153, 0.12), transparent 30%),
                        linear-gradient(180deg, var(--app-bg-base) 0%, var(--app-bg-end) 100%);
                    color: var(--text-dark);
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        return

    saved_background = state_manager.get_settings().get("app_background_color", DEFAULT_APP_BACKGROUND)
    if "app_background_color" not in st.session_state:
        st.session_state.app_background_color = saved_background

    app_background_color = st.session_state.get("app_background_color", DEFAULT_APP_BACKGROUND)
    st.markdown(
        f"""
        <style>
            :root {{
                --app-bg-base: {app_background_color};
                --app-bg-end: {app_background_color};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    """Render application sidebar"""
    state_manager = get_state_manager()
    _apply_theme_overrides(state_manager)
    
    with st.sidebar:
        # Logo and title
        st.markdown("""
        <div class="sidebar-hero">
            <h1 class="brand-emoji">🎓</h1>
            <h3 class="brand-title">Lecture Notes</h3>
            <p class="brand-sub">AI-Powered Study Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

        # Navigation info
        st.markdown("### 📚 Quick Navigation")
        st.markdown("""
        - **Upload**: Add lecture audio
        - **Transcript**: View transcription
        - **Summary**: Generate notes
        - **Quiz**: Test knowledge
        - **Analytics**: Track progress
        - **Study Packs**: Download PDFs and Anki decks
        - **Settings**: Configure app
        """)
        
        st.divider()
        
        # Current lecture info
        if st.session_state.get('current_lecture_id'):
            lecture = state_manager.get_lecture(st.session_state.current_lecture_id)
            if lecture:
                st.markdown("### 📖 Current Lecture")
                st.info(f"**{lecture.get('title', 'Untitled')}**")
                
                if 'duration' in lecture:
                    from utils.helpers import format_duration
                    st.caption(f"⏱️ Duration: {format_duration(lecture['duration'])}")
                
                if st.button("Clear Current", width="stretch"):
                    st.session_state.current_lecture_id = None
                    st.session_state.transcript = None
                    st.session_state.summary = None
                    st.session_state.quiz = None
                    st.rerun()
        
        st.divider()
        
        # Statistics
        analytics = state_manager.get_analytics()
        st.markdown("### 📊 Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Lectures", analytics.get('total_lectures', 0))
        with col2:
            st.metric("Quizzes", analytics.get('total_quizzes', 0))
        
        # Total duration
        total_duration = analytics.get('total_duration', 0)
        if total_duration > 0:
            from utils.helpers import format_duration
            st.caption(f"⏱️ Total: {format_duration(total_duration)}")
        
        st.divider()
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🆕 New Lecture", width="stretch"):
            st.session_state.current_lecture_id = None
            st.session_state.transcript = None
            st.switch_page("pages/01_📤_Upload.py")
        
        if st.button("📚 View All", width="stretch"):
            st.switch_page("pages/05_📈_Analytics.py")
        
        st.divider()
        
        # Footer
        st.markdown("""
        <div class="sidebar-footer">
            <p>Powered by Local AI</p>
            <p>🔒 100% Private • No API Keys</p>
        </div>
        """, unsafe_allow_html=True)

def render_minimal_sidebar():
    """Render minimal sidebar for pages that need more space"""
    state_manager = get_state_manager()
    _apply_theme_overrides(state_manager)
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-hero">
            <h1 class="brand-emoji">🎓</h1>
            <h3 class="brand-title">Lecture Notes</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Essential navigation only
        analytics = state_manager.get_analytics()
        
        st.metric("Total Lectures", analytics.get('total_lectures', 0))
        
        st.divider()
        
        st.markdown("""
        <div class="sidebar-footer">
            🔒 100% Private & Local
        </div>
        """, unsafe_allow_html=True)
