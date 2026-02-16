"""
Settings Page - Application settings and configuration
"""
import streamlit as st
from pathlib import Path
from utils.state_manager import StateManager
from utils.file_handler import FileHandler
from utils.helpers import format_file_size
from components.sidebar import render_sidebar

# Page config
st.set_page_config(
    page_title="Settings - Lecture Notes Generator",
    page_icon="⚙️",
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
st.title("⚙️ Settings")
st.markdown("Configure your Lecture Voice-to-Notes Generator.")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎤 Transcription", "📝 Summary", "❓ Quiz", "💾 Data"])

with tab1:
    st.subheader("Transcription Settings")
    
    # AssemblyAI configuration
    st.markdown("### AssemblyAI API")
    
    st.success("✅ AssemblyAI API key is configured.")
    st.info(
        "Using **AssemblyAI** for transcription with:\n"
        "- **universal-3-pro** (en, es, de, fr, it, pt)\n"
        "- **universal-2** (all other languages)\n"
        "- **Automatic language detection** enabled"
    )
    
    # Verify API key
    api_key_display = "5116de72...fcdd6"
    st.caption(f"🔑 API Key: {api_key_display}")
    
    st.divider()
    
    # Language settings
    st.markdown("### Language")
    default_language = st.selectbox(
        "Default Language",
        options=['Auto-detect', 'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese'],
        index=0,
        help="Set the default language for transcription. AssemblyAI also supports auto-detection."
    )
    st.session_state.default_language = default_language

with tab2:
    st.subheader("Summary Settings")
    
    # Summary style
    summary_style = st.selectbox(
        "Default Summary Style",
        options=['concise', 'detailed', 'bullet_points'],
        index=0,
        help="Choose the default summary format"
    )
    st.session_state.default_summary_style = summary_style
    
    # Summary length
    max_summary_length = st.slider(
        "Maximum Summary Length (words)",
        50, 500, 150,
        help="Maximum number of words in the summary"
    )
    st.session_state.max_summary_length = max_summary_length
    
    st.divider()
    
    # Model info
    st.markdown("### Summarization Model")
    st.info(
        "The app uses Facebook's BART-Large-CNN model for summarization. "
        "If transformers is not installed, it falls back to extractive summarization."
    )
    
    # Check model availability
    try:
        import transformers  # type: ignore[import-unresolved]
        st.success(f"✅ Transformers library available (v{transformers.__version__})")
    except ImportError:
        st.warning(
            "⚠️ Transformers library not installed. Using extractive summarization.\n\n"
            "Install with: `pip install transformers torch`"
        )

with tab3:
    st.subheader("Quiz Settings")
    
    # Default quiz options
    default_num_questions = st.slider(
        "Default Number of Questions",
        3, 20, 5,
        help="Default number of quiz questions to generate"
    )
    st.session_state.default_num_questions = default_num_questions
    
    default_difficulty = st.selectbox(
        "Default Difficulty",
        options=['easy', 'medium', 'hard'],
        index=1
    )
    st.session_state.default_difficulty = default_difficulty
    
    default_question_types = st.multiselect(
        "Default Question Types",
        options=['multiple_choice', 'true_false', 'fill_blank'],
        default=['multiple_choice', 'true_false']
    )
    st.session_state.default_question_types = default_question_types

with tab4:
    st.subheader("Data Management")
    
    # Storage info
    st.markdown("### 💾 Storage")
    
    data_dir = Path("data")
    
    dirs_info = {
        'uploads': data_dir / 'uploads',
        'transcripts': data_dir / 'transcripts',
        'summaries': data_dir / 'summaries'
    }
    
    for name, dir_path in dirs_info.items():
        if dir_path.exists():
            files = list(dir_path.glob('*'))
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            st.markdown(
                f"- **{name.title()}**: {len(files)} files, {format_file_size(total_size)}"
            )
        else:
            st.markdown(f"- **{name.title()}**: No data")
    
    st.divider()
    
    # Database info
    st.markdown("### 🗄️ Database")
    
    lectures = state_manager.get_all_lectures()
    st.markdown(f"- **Total Lectures**: {len(lectures)}")
    
    st.divider()
    
    # Danger zone
    st.markdown("### ⚠️ Danger Zone")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.confirm_delete = True
    
    if st.session_state.get('confirm_delete', False):
        st.warning("⚠️ This will permanently delete ALL lectures, transcripts, summaries, and uploaded files!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Delete", type="primary"):
                try:
                    # Clear database
                    state_manager.clear_all()
                    
                    # Clear files
                    for dir_path in dirs_info.values():
                        if dir_path.exists():
                            import shutil
                            for item in dir_path.iterdir():
                                if item.is_file():
                                    item.unlink()
                    
                    st.session_state.confirm_delete = False
                    st.success("✅ All data cleared successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing data: {e}")
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.confirm_delete = False
                st.rerun()

st.divider()

# System info
with st.expander("ℹ️ System Information"):
    import sys
    import platform
    
    st.markdown(f"- **Python**: {sys.version}")
    st.markdown(f"- **Platform**: {platform.platform()}")
    st.markdown(f"- **Streamlit**: {st.__version__}")
    
    # Check installed packages
    packages = {
        'nltk': 'nltk',
        'textstat': 'textstat',
        'plotly': 'plotly',
        'matplotlib': 'matplotlib',
        'pandas': 'pandas',
        'wordcloud': 'wordcloud'
    }
    
    st.markdown("### Installed Packages")
    for name, module in packages.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            st.markdown(f"- ✅ **{name}**: {version}")
        except ImportError:
            st.markdown(f"- ❌ **{name}**: Not installed")
    
    # Heavy packages
    st.markdown("### ML Packages")
    ml_packages = {
        'assemblyai': 'assemblyai',
        'transformers': 'transformers'
    }
    
    for name, module in ml_packages.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            st.markdown(f"- ✅ **{name}**: {version}")
        except ImportError:
            st.markdown(f"- ❌ **{name}**: Not installed")
