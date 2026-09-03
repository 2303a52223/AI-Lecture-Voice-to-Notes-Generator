"""
Upload Page - Upload and process audio lectures
"""
import streamlit as st
from pathlib import Path
import time
import json
from utils.state_manager import StateManager
from utils.file_handler import FileHandler
from utils.helpers import format_duration, format_file_size
from utils.progress_tracker import ProgressTracker, ProgressContext
from utils.error_handler import report_error
from utils.validation import validate_upload
from components.sidebar import render_sidebar
from components.cards import info_card, metric_card
from components.audio_player import render_audio_player

# Page config
st.set_page_config(
    page_title="Upload - Lecture Notes Generator",
    page_icon="📤",
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

# Main content (hero + upload card)
st.markdown(
    """
    <section class='page-hero'>
        <div class='page-hero-badge'>📤 Upload</div>
        <h1>Upload Lecture</h1>
        <p class='page-hero-copy'>Upload audio or documents to generate transcripts, summaries, and study materials.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='pack-card'>", unsafe_allow_html=True)

# Upload section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 Upload File")
    
    # File uploader: audio, pdf, pptx, docx
    uploaded_file = st.file_uploader(
        "Choose a file (audio / PDF / PPTX / DOCX)",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm', 'pdf', 'pptx', 'docx'],
        help="Supported formats: audio, PDF, PPTX, DOCX"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # File info
        file_size = format_file_size(uploaded_file.size)
        st.caption(f"📁 Size: {file_size}")
        
        # Audio preview for audio files
        if uploaded_file.type and uploaded_file.type.startswith('audio'):
            st.audio(uploaded_file)

with col2:
    st.subheader("📋 Lecture Details")
    
    lecture_title = st.text_input(
        "Lecture Title",
        placeholder="e.g., Introduction to Machine Learning",
        help="Give your lecture a descriptive title"
    )
    
    lecture_subject = st.text_input(
        "Subject / Course",
        placeholder="e.g., Computer Science 101",
        help="The subject or course this lecture belongs to"
    )
    
    lecture_tags = st.text_input(
        "Tags (comma-separated)",
        placeholder="e.g., ML, AI, neural networks",
        help="Add tags to help organize your lectures"
    )
# close pack card
st.markdown("</div>", unsafe_allow_html=True)
# Advanced options
with st.expander("Advanced options"):
    ocr = st.checkbox("Enable OCR for scanned PDFs (slow)", value=False)
    process_documents_by_unit = st.checkbox("Process PDF/PPT/DOC unit-by-unit (recommended)", value=True)
    max_document_units = st.number_input("Max pages/slides/units to process (0 = all)", min_value=0, max_value=500, value=0, step=1)
    transcription_profile = st.selectbox(
        "Audio transcription profile",
        options=["Fast", "Balanced"],
        index=0,
        help="Fast uses a smaller local model. Balanced uses a larger model with better accuracy."
    )
    glossary_file = st.file_uploader("Upload glossary CSV (optional)", type=['csv'])

st.divider()

# Processing options
st.subheader("⚙️ Processing Options")

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Language",
        options=['Auto-detect', 'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese'],
        index=0,
        help="Select the language of the lecture"
    )

with col2:
    summary_style = st.selectbox(
        "Summary Style",
        options=['concise', 'detailed', 'bullet_points'],
        index=0,
        help="Choose how the summary should be formatted"
    )

st.caption("🔗 Powered by local faster-whisper transcription")

# Language mapping
language_map = {
    'Auto-detect': None,
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh',
    'Japanese': 'ja'
}

st.divider()

# Process button
if uploaded_file:
    if st.button("🚀 Process Lecture", type="primary", width="stretch"):
        if not lecture_title:
            lecture_title = Path(uploaded_file.name).stem
        
        # Validate and save uploaded file
        is_valid, valid_msg = validate_upload(uploaded_file)
        if not is_valid:
            st.error(valid_msg)
            st.stop()

        with st.spinner("Saving file..."):
            try:
                saved_path = file_handler.save_upload(uploaded_file)
            except Exception as e:
                report_error(e, "Error saving uploaded file")
                st.stop()

            if not saved_path:
                st.error("❌ Error saving file. Please try again.")
                st.stop()
        
        # Use ProgressContext for better UX
        progress_steps = {
            "Saving file": "complete",
            "Extracting/Transcribing": "running",
            "Cleaning text": "pending",
            "Generating summary": "pending",
            "Analyzing content": "pending",
            "Saving database": "pending"
        }
        
        with ProgressContext("📊 Processing Lecture", total_steps=6) as progress:
            source_kind = "audio"
            # Type guard: saved_path is guaranteed to be str after the check above
            assert saved_path is not None
            ext = Path(saved_path).suffix.lower()
            
            # Step 1: File Extraction/Transcription
            progress.update(1, "Extracting/Transcribing...")
            progress_steps["Extracting/Transcribing"] = "running"
            
            try:
                if ext in ['.pdf', '.pptx', '.docx']:
                    source_kind = "document"
                    # Document extraction
                    from processors.document_extractor import route_file
                    unit_limit = int(max_document_units) if process_documents_by_unit and max_document_units > 0 else None
                    extraction = route_file(saved_path, ocr=ocr, max_units=unit_limit)

                    segments = extraction.get('segments', [])

                    if process_documents_by_unit and segments:
                        merged_segments = []
                        total_segments = len(segments)
                        for idx, seg in enumerate(segments, start=1):
                            seg_text = (seg.get('text') or '').strip()
                            if not seg_text:
                                continue
                            merged_segments.append(seg)
                            progress.update(1, f"Converting unit {idx}/{total_segments}...")
                        extracted_text = "\n\n".join(s.get('text', '') for s in merged_segments)
                        extraction['segments'] = merged_segments
                    else:
                        extracted_text = extraction.get('text', '').strip()
                    
                    if not extracted_text:
                        error_msg = extraction.get('metadata', {}).get('error', 'Unknown extraction error')
                        st.warning(f"⚠️ Text extraction returned empty.\n\n**Error:** {error_msg}")
                        if ext == '.pdf':
                            st.info("💡 **Tips for PDF extraction:**\n- Enable OCR if PDF is scanned/image-based\n- Ensure PDF has selectable text\n- Try converting to text-based format")
                        st.stop()
                    
                    transcription = {
                        'text': extracted_text,
                        'segments': extraction.get('segments', []),
                        'language': extraction.get('metadata', {}).get('language', 'unknown'),
                        'duration': 0,
                        'processing_time': 0,
                        'model_size': 'local-extractor',
                        'timestamp': None,
                        'method': extraction.get('metadata', {}).get('method', 'unknown')
                    }
                    
                    # Save transcript JSON
                    transcript_path = file_handler.get_transcript_path(lecture_title)
                    Path(transcript_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(transcript_path, 'w', encoding='utf-8') as f:
                        json.dump(transcription, f, ensure_ascii=False, indent=2)

                else:
                    # Audio transcription with progress
                    from processors.audio_transcriber import AudioTranscriber
                    model_name = "tiny" if transcription_profile == "Fast" else "base"
                    transcriber = AudioTranscriber(model_name=model_name)
                    lang_code = language_map.get(language)
                    
                    # Create progress callback
                    def transcription_progress(pct, msg):
                        progress.update(1, f"Transcribing: {msg}")
                    
                    transcription = transcriber.transcribe(
                        saved_path, 
                        language=lang_code, 
                        progress_callback=transcription_progress
                    )
                    
                    # Save transcript
                    transcript_path = file_handler.get_transcript_path(lecture_title)
                    try:
                        transcriber.save_transcript(transcription, transcript_path)
                    except:
                        Path(transcript_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(transcript_path, 'w', encoding='utf-8') as f:
                            json.dump(transcription, f, ensure_ascii=False, indent=2)

                progress_steps["Extracting/Transcribing"] = "complete"
                
            except Exception as e:
                report_error(e, "Extraction/Transcription error")
                progress_steps["Extracting/Transcribing"] = "error"
                st.stop()
            
            # Step 2: Text Cleaning
            progress.update(2, "Cleaning transcription...")
            progress_steps["Cleaning text"] = "running"
            
            try:
                from utils.helpers import pre_clean_text, apply_glossary, load_glossary_from_csv
                
                original_text = transcription['text']
                transcription['text'] = pre_clean_text(transcription['text'])
                
                if glossary_file:
                    glossary_content = glossary_file.getvalue().decode('utf-8')
                    glossary = load_glossary_from_csv(glossary_content)
                    transcription['text'] = apply_glossary(transcription['text'], glossary)
                
                progress_steps["Cleaning text"] = "complete"
                
            except Exception as e:
                st.warning(f"⚠️ Cleaning step issue: {e}")
                progress_steps["Cleaning text"] = "complete"

            # Step 3: Summarization
            progress.update(3, "Generating summary...")
            progress_steps["Generating summary"] = "running"
            
            try:
                from processors.summarizer import Summarizer
                
                summarizer = Summarizer()

                if source_kind == "document" and process_documents_by_unit and transcription.get('segments'):
                    unit_summaries = []
                    total_units = len(transcription['segments'])
                    for idx, segment in enumerate(transcription['segments'], start=1):
                        seg_text = (segment.get('text') or '').strip()
                        if len(seg_text.split()) < 20:
                            continue

                        partial = summarizer.summarize(seg_text, max_length=90, min_length=30, style="concise")
                        label = segment.get('page') or segment.get('slide') or segment.get('para') or idx
                        unit_summaries.append(f"Unit {label}: {partial.get('summary', '').strip()}")
                        progress.update(3, f"Summarizing unit {idx}/{total_units}...")

                    combined = "\n".join(s for s in unit_summaries if s.strip())
                    if combined.strip():
                        summary_result = summarizer.summarize(combined, max_length=220, min_length=70, style=summary_style)
                    else:
                        summary_result = summarizer.summarize(transcription['text'], style=summary_style)
                else:
                    summary_result = summarizer.summarize(
                        transcription['text'],
                        style=summary_style
                    )

                if not summary_result.get('summary', '').strip():
                    # Hard fallback so Summary page always has content.
                    fallback_words = transcription['text'].split()[:180]
                    summary_result = {
                        'summary': " ".join(fallback_words),
                        'method': 'fallback-truncate'
                    }
                
                study_notes = summarizer.generate_study_notes(
                    transcription['text'],
                    title=lecture_title
                )
                
                summary_path = file_handler.get_summary_path(lecture_title)
                Path(summary_path).parent.mkdir(parents=True, exist_ok=True)
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(study_notes)
                
                progress_steps["Generating summary"] = "complete"
                
            except Exception as e:
                st.warning(f"⚠️ Summary generation issue: {e}")
                summary_result = {'summary': 'Summary generation failed', 'method': 'none'}
                study_notes = ''
                summary_path = ''
                progress_steps["Generating summary"] = "complete"
            
            # Step 4: Text Analysis
            progress.update(4, "Analyzing content...")
            progress_steps["Analyzing content"] = "running"
            
            try:
                from processors.text_analyzer import TextAnalyzer
                
                analyzer = TextAnalyzer()
                analysis = analyzer.analyze(transcription['text'])
                progress_steps["Analyzing content"] = "complete"
                
            except Exception as e:
                st.warning(f"⚠️ Analysis issue: {e}")
                analysis = {}
                progress_steps["Analyzing content"] = "complete"
            
            # Step 5: Save to database
            progress.update(5, "Saving to database...")
            progress_steps["Saving database"] = "running"
            
            tags_list = [t.strip() for t in lecture_tags.split(',') if t.strip()] if lecture_tags else []
            
            lecture_data = {
                'title': lecture_title,
                'subject': lecture_subject,
                'tags': tags_list,
                'audio_path': str(saved_path),
                'transcript_path': str(transcript_path) if transcript_path else '',
                'summary_path': str(summary_path) if summary_path else '',
                'transcript_text': transcription.get('text', ''),
                'summary_text': summary_result.get('summary', ''),
                'duration': transcription.get('duration', 0),
                'language': transcription.get('language', 'unknown'),
                'whisper_model': transcription.get('model_size', 'local-extractor') if source_kind == 'audio' else 'document-extractor',
                'analysis': analysis
            }
            
            lecture_id = state_manager.add_lecture(lecture_data)
            progress.update(6, "Complete!")
            progress_steps["Saving database"] = "complete"
            
            if lecture_id:
                st.session_state.current_lecture_id = lecture_id
                
                # Success message
                st.success("🎉 Lecture processed successfully!")
                st.balloons()
                
                # Results summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    metric_card(
                        "Words",
                        str(len(transcription.get('text', '').split())),
                        icon="📝"
                    )
                with col2:
                    metric_card(
                        "Duration",
                        format_duration(transcription.get('duration', 0)),
                        icon="⏱️"
                    )
                with col3:
                    metric_card(
                        "Segments",
                        str(len(transcription.get('segments', []))),
                        icon="📋"
                    )
                
                st.divider()
                st.info("👉 Navigate to **Transcript**, **Summary**, or **Quiz** pages to explore your lecture!")
                
            else:
                st.error("❌ Error saving lecture data.")
else:
    # Show instructions when no file is uploaded
    st.info("👆 Upload an audio file to get started!")
    
    # Feature cards
    st.subheader("✨ What you'll get")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        info_card(
            "🎤 Transcription",
            "Accurate speech-to-text conversion using local faster-whisper models"
        )
    
    with col2:
        info_card(
            "📝 Summary",
            "AI-generated summaries and study notes from your lecture content"
        )
    
    with col3:
        info_card(
            "❓ Quiz",
            "Auto-generated quiz questions to test your understanding"
        )
    
    with col4:
        info_card(
            "📊 Analytics",
            "Text analysis with readability scores, word frequency, and more"
        )
