"""
Sidebar Component - Navigation and status information
"""
import streamlit as st
from utils.state_manager import get_state_manager

def render_sidebar():
    """Render application sidebar"""
    
    with st.sidebar:
        # Logo and title
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #667eea; margin: 0;">🎓</h1>
            <h3 style="margin: 0.5rem 0;">Lecture Notes</h3>
            <p style="color: #666; font-size: 0.9rem;">AI-Powered Study Assistant</p>
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
        - **Settings**: Configure app
        """)
        
        st.divider()
        
        # Current lecture info
        state_manager = get_state_manager()
        
        if st.session_state.get('current_lecture_id'):
            lecture = state_manager.get_lecture(st.session_state.current_lecture_id)
            if lecture:
                st.markdown("### 📖 Current Lecture")
                st.info(f"**{lecture.get('title', 'Untitled')}**")
                
                if 'duration' in lecture:
                    from utils.helpers import format_duration
                    st.caption(f"⏱️ Duration: {format_duration(lecture['duration'])}")
                
                if st.button("Clear Current", use_container_width=True):
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
        
        if st.button("🆕 New Lecture", use_container_width=True):
            st.session_state.current_lecture_id = None
            st.session_state.transcript = None
            st.switch_page("pages/01_📤_Upload.py")
        
        if st.button("📚 View All", use_container_width=True):
            st.switch_page("pages/05_📈_Analytics.py")
        
        st.divider()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #888; font-size: 0.8rem;">
            <p>Powered by Local AI</p>
            <p>🔒 100% Private • No API Keys</p>
        </div>
        """, unsafe_allow_html=True)

def render_minimal_sidebar():
    """Render minimal sidebar for pages that need more space"""
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #667eea; margin: 0;">🎓</h1>
            <h3 style="margin: 0.5rem 0;">Lecture Notes</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Essential navigation only
        state_manager = get_state_manager()
        analytics = state_manager.get_analytics()
        
        st.metric("Total Lectures", analytics.get('total_lectures', 0))
        
        st.divider()
        
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #888;">
            🔒 100% Private & Local
        </div>
        """, unsafe_allow_html=True)
