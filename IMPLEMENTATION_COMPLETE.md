# Lecture Voice-to-Notes Generator - Complete Implementation

## Overview
A comprehensive, local-first lecture processing system that converts audio, PDF, PPTX, and DOCX files into study materials including transcripts, summaries, quizzes, and flashcards.

## Features Implemented

### ✅ Step 1: Multi-Format Upload & Routing
- Accept audio (MP3, WAV, M4A, OGG, FLAC, WebM)
- Accept documents (PDF, PPTX, DOCX)
- File type detection and intelligent routing
- Advanced options: OCR toggle, output selection, glossary upload

### ✅ Step 2: Document Extraction
- **PDF**: Text extraction with optional OCR support
- **PPTX**: Slide text extraction
- **DOCX**: Paragraph extraction
- Fallback error handling with informative messages

### ✅ Step 3: Local Audio Transcription
- `faster-whisper` wrapper for local, offline ASR
- GPU/CPU auto-detection and fallback
- Model size options (tiny → large)
- Timestamped segments and metadata

### ✅ Step 4: Deterministic Pre-Clean & Glossary
- **Pre-clean**: Remove fillers (um, uh, like, basically), fix repeated words, clean noise markers
- **Glossary mapping**: Load CSV with incorrect/correct term pairs
- Deterministic (reproducible) cleaning without ML
- Whitespace normalization and punctuation fixes

### ✅ Step 5: Concept Extraction & Simple Explanations
- Extract keyphrases using frequency + TF-IDF-like scoring
- Generate simple 1-2 sentence definitions from context
- Topic classification (process, property, concept, term)
- Group concepts by inferred theme

### ✅ Step 6: Notes & Key-Concepts Generator
- Hybrid extractive + abstractive summarization
- Chunked processing for long documents
- Generate study notes with TOC, bullets, timestamps
- Include key concepts with definitions
- Compression ratio and statistics

### ✅ Step 7: Quiz & Flashcards + Anki Export
- **Quiz types**: Multiple choice, True/False, Fill-in-the-blank
- **Difficulty levels**: easy, medium, hard
- **Flashcards**: Auto-generated Q/A pairs with topics
- **Anki export**: Direct `.apkg` file generation
- **CSV export**: For manual Anki import or other tools

### ✅ Step 8: Multi-Format Export
- **PDF**: Professional styled PDFs with Markdown rendering
- **Markdown (.md)**: Structured notes with headers and formatting
- **Plain text (.txt)**: Clean, readable text version
- **Anki (.apkg)**: Direct Anki deck import
- **CSV (.csv)**: Flashcards in spreadsheet format
- **HTML**: Interactive web-viewable notes

### ✅ Step 9: UX, Settings & Privacy Controls
- **Privacy tab** in Settings with:
  - Auto-delete audio after processing option
  - Local data encryption toggle (beta)
  - Transcriber selection (local vs API)
  - Whisper model and device selection
  - Model cache management
  - Optional telemetry consent
- Comprehensive system information display
- Package dependency status check
- Storage usage monitoring
- Data management and cleanup options

### ✅ Step 10: Infrastructure & Dependencies
- Complete `requirements.txt` with all ML/processing libraries
- Local model caching under `models/` directory
- Support for both CPU and GPU backends
- Streamlit integration with error handling
- Modular architecture for easy extension

## Architecture

```
Lecture Voice-to-Notes Generator/
├── pages/
│   ├── 01_📤_Upload.py          # Multi-format upload with routing
│   ├── 02_📝_Transcript.py      # View/edit transcripts
│   ├── 03_📊_Summary.py         # Summary & multi-format export
│   ├── 04_❓_Quiz.py             # Quiz & flashcard generation + Anki export
│   ├── 05_📈_Analytics.py       # Lecture analytics & visualization
│   └── 06_⚙️_Settings.py        # Privacy, models, data management
├── processors/
│   ├── document_extractor.py    # PDF/PPTX/DOCX extraction
│   ├── audio_transcriber.py     # Local Whisper ASR wrapper
│   ├── concept_extractor.py     # Keyphrase & concept extraction
│   ├── export_handler.py        # Multi-format export (PDF/MD/TXT/HTML)
│   ├── quiz_generator.py        # Quiz + Anki export (ENHANCED)
│   ├── summarizer.py            # Hybrid summarization (ENHANCED)
│   └── text_analyzer.py         # Text statistics & analysis
├── utils/
│   ├── state_manager.py         # DB and state persistence
│   ├── file_handler.py          # File I/O (ENHANCED with exports)
│   ├── helpers.py               # Utilities (ENHANCED with pre-clean)
│   └── setup_nltk.py            # NLTK data setup
├── components/
│   ├── sidebar.py               # Navigation
│   ├── cards.py                 # UI card components
│   ├── audio_player.py          # Audio playback
│   └── charts.py                # Visualizations
├── data/                         # Local data storage
│   ├── uploads/                 # Uploaded files
│   ├── transcripts/             # Extracted text & transcriptions
│   ├── summaries/               # Generated study notes
│   └── database.json            # Metadata & state
├── models/                       # Cached ML models
│   └── (whisper models downloaded on first use)
├── assets/
│   ├── style.css                # Custom styling
│   └── logo.png                 # App logo
├── app.py                        # Main entry point
├── requirements.txt             # Dependencies (COMPREHENSIVE)
├── setup_nltk.py                # Initial NLTK setup
└── README.md / QUICKSTART.md    # Documentation
```

## Installation & Setup

### 1. Clone & Create Virtual Environment
```bash
cd "Lecture Voice-to-Notes Generator"
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python setup_nltk.py  # Download NLTK data
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` with navigation pages visible in the sidebar.

## Quick Start Guide

### Upload a Lecture
1. Go to **Upload** page
2. Select audio/PDF/PPTX/DOCX file
3. Fill in title, subject, tags
4. (Optional) Check Advanced options for OCR, outputs, glossary
5. Click **Process Lecture**

### View & Export Notes
1. Go to **Summary** page
2. Select lecture from dropdown
3. View summary & study notes
4. Export as TXT, MD, PDF, or HTML

### Generate & Export Flashcards
1. Go to **Quiz** page
2. Select lecture
3. Click **Generate Flashcards**
4. Export as Anki (.apkg) or CSV

### Configure Settings
1. Go to **Settings** page
2. **Transcription**: Language & model settings
3. **Summary**: Default style and length
4. **Quiz**: Default question count and difficulty
5. **Privacy**: Choose local vs cloud transcription, set cache options
6. **Data**: Manage storage and clear old files

## Key Features in Detail

### Privacy & Local Operation
- All transcription can run **offline** using `faster-whisper`
- No API keys required for local transcription
- Audio files optional auto-delete after processing
- Local model cache prevents re-downloads
- Optional data encryption (beta)

### Deterministic Pre-Cleaning
- Remove common fillers: "um", "uh", "like", "basically", "you know"
- Fix repeated words: "the the" → "the"
- Remove noise markers: [inaudible], (background noise)
- Glossary mapping for domain-specific terms (CSV upload)

### Quality Outputs
- **Transcripts**: Cleaned, timestamped, searchable
- **Study Notes**: Markdown with TOC, summaries, concepts, key points
- **Quizzes**: Multiple choice, T/F, fill-blank with explanations
- **Flashcards**: Anki-compatible with topics and difficulty tags
- **Analytics**: Readability scores, word frequency, speaker pace

### Export Formats
- **PDF**: Professional styling with Markdown rendering
- **Markdown (.md)**: Portable, version-control friendly
- **Plain Text (.txt)**: Universal compatibility
- **Anki (.apkg)**: Direct import to Anki for spaced repetition
- **CSV (.csv)**: Spreadsheet tools and manual imports
- **HTML**: Offline viewing in browser

## Performance & Optimization

- **Model Caching**: Whisper models cached locally, no re-download on each use
- **Chunked Processing**: Large documents processed in chunks for memory efficiency
- **Hybrid Summarization**: Combines extractive (fast) + abstractive (accurate) methods
- **GPU Support**: Automatic detection and fallback to CPU
- **Progress Tracking**: Real-time UI updates during long operations

## Troubleshooting

### "faster-whisper not available"
- Install: `pip install faster-whisper`
- GPU support: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### "WeasyPrint or genanki not installed"
- Install: `pip install weasyprint genanki`
- WeasyPrint may require additional system dependencies (LibreOffice on Windows)

### OCR not working
- Install: `pip install pytesseract`
- Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

### Models not downloading
- Check internet connection
- Manually: `python -m spacy download en_core_web_sm`

## Next Steps / Future Enhancements

1. **Speaker Diarization**: Identify different speakers in audio
2. **Topic Modeling**: LDA or clustering for topic discovery
3. **Question Answering**: Answer user questions about the lecture
4. **Video Support**: Extract audio from MP4/WebM videos
5. **Batch Processing**: Queue multiple files for background processing
6. **Collaboration**: Share notes and quizzes with classmates
7. **Mobile App**: React Native or Flutter companion app
8. **API Server**: REST API for programmatic access
9. **Advanced Analytics**: Time-series analysis of learning progress
10. **Custom Models**: Fine-tune Whisper on domain-specific audio

## License & Acknowledgments

This project uses several open-source libraries:
- **Streamlit** for the UI framework
- **faster-whisper** for local speech-to-text
- **Transformers** for abstractive summarization
- **Genanki** for Anki deck generation
- **PyMuPDF**, **python-pptx**, **python-docx** for document processing

---

**Status**: ✅ **All 10 core modules implemented and integrated**

Start using the app now by running: `streamlit run app.py`
