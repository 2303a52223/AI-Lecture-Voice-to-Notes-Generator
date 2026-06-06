"""
Settings Page - Application settings and configuration
"""
import streamlit as st
from pathlib import Path
from utils.state_manager import StateManager
from utils.file_handler import FileHandler
from utils.helpers import format_file_size
from components.sidebar import render_sidebar
from utils.error_handler import get_recent_errors

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
saved_settings = state_manager.get_settings()

if "app_background_color" not in st.session_state:
    st.session_state.app_background_color = saved_settings.get("app_background_color", "#F8FAFC")

# Sidebar
render_sidebar()

# Main content - Hero
st.markdown(
    """
    <section class='page-hero'>
        <div class='page-hero-badge'>⚙️ Settings</div>
        <h1>Configure Your Workspace</h1>
        <p class='page-hero-copy'>Customize transcription, summarization, quiz generation, privacy controls, and data management settings.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎤 Transcription",
    "📝 Summary",
    "❓ Quiz",
    "🔒 Privacy",
    "💾 Data",
    "🎨 Appearance",
])

with tab1:
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
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

st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
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

st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
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

st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
    st.subheader("Privacy & Model Settings")
    
    st.markdown("### 🔒 Privacy Controls")
    
    # Auto-delete audio
    auto_delete_audio = st.checkbox(
        "Auto-delete raw audio after transcription",
        value=False,
        help="Automatically remove uploaded audio files after successful transcription to save space"
    )
    st.session_state.auto_delete_audio = auto_delete_audio
    
    # Encryption option
    enable_encryption = st.checkbox(
        "Enable local data encryption (beta)",
        value=False,
        help="Encrypt sensitive data in the local database"
    )
    st.session_state.enable_encryption = enable_encryption
    
    st.divider()
    
    st.markdown("### 🎤 Transcription Model")
    
    transcriber_choice = st.radio(
        "Select transcriber",
        options=["Local (faster-whisper)", "Online API (AssemblyAI)"],
        index=0,
        help="Choose between local offline transcription or cloud-based API"
    )
    st.session_state.transcriber_choice = transcriber_choice
    
    if transcriber_choice == "Local (faster-whisper)":
        st.info(
            "✅ Using **faster-whisper** for local, offline transcription\n\n"
            "- **Privacy**: All processing happens locally\n"
            "- **Speed**: GPU/CPU fallback supported\n"
            "- **Models**: tiny, base, small, medium, large\n"
            "- **Download**: Models cached locally under `models/`"
        )
        
        model_size = st.selectbox(
            "Model size (larger = more accurate but slower)",
            options=['tiny', 'base', 'small', 'medium', 'large'],
            index=2,  # default to 'small'
            help="Smaller models are faster, larger models are more accurate"
        )
        st.session_state.whisper_model = model_size
        
        # Device selection
        device = st.radio(
            "Processing device",
            options=["Auto-detect", "CPU", "GPU"],
            index=0
        )
        st.session_state.whisper_device = device
        
    else:
        st.info(
            "Using **AssemblyAI API** for transcription\n\n"
            "- **Models**: universal-3-pro, universal-2\n"
            "- **Languages**: Supports all major languages\n"
            "- **Requires**: Internet connection and API key"
        )
    
    st.divider()
    
    st.markdown("### 📊 Model Cache")
    
    # Model cache info
    models_dir = Path("models")
    if models_dir.exists():
        cached_files = list(models_dir.glob('**/*'))
        cached_size = sum(f.stat().st_size for f in cached_files if f.is_file())
        st.markdown(f"- **Cached models**: {len([f for f in cached_files if f.is_file()])} files")
        st.markdown(f"- **Cache size**: {format_file_size(cached_size)}")
        
        if st.button("🗑️ Clear model cache"):
            try:
                import shutil
                shutil.rmtree(models_dir)
                models_dir.mkdir(parents=True, exist_ok=True)
                st.success("✅ Model cache cleared. Models will be re-downloaded on next use.")
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing cache: {e}")
    else:
        st.markdown("- **No cached models** (will be downloaded on first use)")
    
    st.divider()
    
    st.markdown("### 📥 Data Management")
    
    enable_telemetry = st.checkbox(
        "Enable anonymized telemetry (optional)",
        value=False,
        help="Help improve the app by sending anonymized usage statistics"
    )
    st.session_state.enable_telemetry = enable_telemetry

st.markdown("</div>", unsafe_allow_html=True)

with tab5:
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
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

st.markdown("</div>", unsafe_allow_html=True)

with tab6:
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
    st.subheader("Appearance")

    st.markdown("### Background")
    selected_background = st.color_picker(
        "Choose app background color",
        value=st.session_state.app_background_color,
        help="Applies to all pages in the app."
    )

    if selected_background != st.session_state.app_background_color:
        st.session_state.app_background_color = selected_background
        state_manager.update_settings({"app_background_color": selected_background})
        st.success("✅ Background color updated.")
        st.rerun()

    if st.button("Reset background color", key="reset_app_background"):
        st.session_state.app_background_color = "#F8FAFC"
        state_manager.update_settings({"app_background_color": "#F8FAFC"})
        st.success("✅ Background color reset to default.")
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

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

    # Recent error logs (admin)
    with st.expander("🛠️ Recent Errors (admin)"):
        errors = get_recent_errors(50)
        if not errors:
            st.markdown("- No recent errors recorded.")
        else:
            for err in errors:
                ts = err.get('timestamp', '')
                eid = err.get('id', '')
                ctx = err.get('context', '')
                msg = err.get('message', '')
                header = f"{ts} — {eid} — {ctx}"
                with st.expander(header):
                    st.markdown(f"**Message:** {msg}")
                    st.markdown("**Traceback (truncated):**")
                    tb = err.get('traceback', '')
                    st.code('\n'.join(tb.splitlines()[:200]))
