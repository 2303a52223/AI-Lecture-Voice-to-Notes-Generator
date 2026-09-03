# 🎓 Lecture Voice-to-Notes Generator

An AI-powered study assistant that transforms lecture recordings and course materials into comprehensive learning resources: transcripts, summaries, interactive quizzes, study packs, and learning analytics.
An AI-powered study assistant that turns lecture recordings and course notes into transcripts, summaries, quizzes, study packs, and analytics.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Local AI](https://img.shields.io/badge/Local%20AI-0F766E?style=for-the-badge&logo=vercel&logoColor=white)

## ✨ Features

- **🎤 Audio Transcription** — Upload lecture audio files (MP3, WAV, M4A, OGG, FLAC, WebM) and receive accurate transcriptions using local **faster-whisper** AI models with automatic language detection. No API keys required.
- **📝 Smart Summaries** — Generate concise, detailed, or bullet-point study notes from transcripts and documents with customizable summary styles.
- **❓ Quiz Generation** — Automatically create multiple-choice, true/false, and fill-in-the-blank questions to test comprehension and retention.
- **📊 Text Analytics** — Analyze readability scores, extract key vocabulary, track word frequency, and identify important concepts using NLTK-powered NLP.
- **📦 Study Packs** — Download high-quality PDFs and Anki flashcard decks directly from the app for offline study and spaced repetition learning.
- **📈 Analytics Dashboard** — Track learning progress, monitor lecture statistics, and gain insights into study patterns across sessions.
- **🎨 Modern UI** — Clean, responsive multi-page Streamlit interface with glassmorphism design, intuitive navigation, and focused study workspace.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Install dependencies**
- **🎤 Audio Transcription** — Upload lecture audio files (MP3, WAV, M4A, OGG, FLAC, WebM) and get accurate transcriptions powered by local faster-whisper models with automatic language detection.
- **📝 Smart Summaries** — Generate concise, detailed, or bullet-style study notes from transcripts and text.
- **❓ Quiz Generation** — Create multiple-choice, true/false, and fill-in-the-blank questions to test understanding.
- **📊 Text Analytics** — Review readability scores, word frequency, and key-term extraction.
- **📦 Study Packs** — Download PDFs and Anki decks from the Study Packs page, with safe clear/delete controls for generated artifacts.
- **📈 Analytics Dashboard** — Track learning progress across uploaded lectures.
- **🎨 Polished UI** — Multi-page Streamlit app with a cleaner sidebar, modern cards, and a focused study workspace.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/2303a52223/AI-Lecture-Voice-to-Notes-Generator.git
   cd AI-Lecture-Voice-to-Notes-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
3. **Download NLTK data**
   ```bash
   python setup_nltk.py
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

3. **Access the app**
   - Open your browser to **http://localhost:8501**
   - The app will load with the 📤 Upload page ready for your first lecture

### Run on Your Local Network

To access the app from other devices on your network:
5. Open your browser at **http://localhost:8501**

### Host on your network

To make the app reachable from other devices on your LAN, run:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

The terminal will display both local and network URLs for accessing the app.
Streamlit will print a local URL and a network URL for your machine.

## 📁 Project Structure

```
.
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies (30+ packages)
├── pyrightconfig.json              # Python type-checking configuration
│
├── 📄 pages/                       # Multi-page application pages
│   ├── 00_🏠_Home.py              # Dashboard & welcome page
│   ├── 01_📤_Upload.py            # File upload & processing
│   ├── 02_📝_Transcript.py        # View & search transcripts
│   ├── 03_📊_Summary.py           # Study notes & summaries
│   ├── 04_❓_Quiz.py              # Take quizzes
│   ├── 05_📈_Analytics.py         # Learning analytics & stats
│   ├── 06_⚙️_Settings.py          # Application settings
│   ├── 07_📦_Study_Packs.py       # Download study materials
│   └── 08_Health_Check.py         # System diagnostics
│
├── 🎨 components/                 # Reusable UI components
│   ├── __init__.py
│   ├── cards_enhanced.py           # Modern glassmorphism card components
│   ├── cards.py                    # Legacy card components (compatibility)
│   ├── audio_player.py             # Audio playback component
│   ├── charts.py                   # Chart visualizations
│   └── sidebar.py                  # Navigation sidebar
│
├── ⚙️ processors/                  # Core processing modules
│   ├── __init__.py
│   ├── audio_transcriber.py        # Speech-to-text using faster-whisper
│   ├── summarizer.py               # Text summarization (NLTK-based)
│   ├── quiz_generator.py           # Automatic quiz generation
│   ├── concept_extractor.py        # Key concept extraction
│   ├── text_analyzer.py            # Readability & vocabulary analysis
│   ├── document_extractor.py       # PDF/PPTX/DOCX text extraction
│   └── export_handler.py           # Export to various formats
│
├── 🛠️ tools/                       # Utility scripts & tools
│   ├── generate_study_pack.py      # Create study packages
│   ├── build_master_study_pack.py  # Build comprehensive study packs
│   ├── flashcards_to_anki.py       # Convert to Anki format
│   ├── flashcards_to_pdf.py        # Generate flashcard PDFs
│   ├── pdf_rendering.py            # PDF generation utilities
│   ├── md_to_html.py               # Markdown to HTML conversion
│   └── summarize_pdf.py            # PDF summarization
│
├── 🔧 utils/                       # Utility modules
│   ├── __init__.py
│   ├── state_manager.py            # Streamlit session state management
│   ├── file_handler.py             # File I/O operations
│   ├── error_handler.py            # Error handling & logging
│   ├── validation.py               # Input validation
│   ├── helpers.py                  # Helper functions
│   ├── retry.py                    # Retry logic for resilience
│   └── progress_tracker.py         # Progress tracking
│
├── 📊 data/                        # Generated data (local storage)
│   ├── database.json               # Lecture metadata
│   ├── summaries/                  # Generated study notes
│   ├── transcripts/                # Transcription outputs
│   └── uploads/                    # Temporary uploaded files
│
├── 🎨 assets/                      # Static assets
│   └── style.css                   # Custom Streamlit styling
│
└── 📚 Documentation
    ├── QUICKSTART.md               # Quick start guide
    ├── INSTALLATION.md             # Detailed installation
    └── USAGE.md                    # Feature usage guide
```

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.54.0 | Web UI framework |
| **Speech-to-Text** | faster-whisper 1.2.1 | Local AI transcription (no API keys) |
| **NLP & Text Processing** | NLTK 3.9.2 | Tokenization, sentiment, POS tagging |
| **Term Extraction** | YAKE, RAKE-NLTK | Key concept identification |
| **Readability Analysis** | TextStat | Flesch-Kincaid, Coleman-Liau metrics |
| **Document Processing** | PyPDF2, python-pptx | PDF, PowerPoint, DOCX extraction |
| **PDF Rendering** | WeasyPrint, Reportlab | PDF generation |
| **Flashcards** | Anki (APKG format) | Spaced repetition learning |
| **Data Storage** | JSON | Local database (no external DB needed) |
| **Visualization** | Plotly, Matplotlib | Charts & analytics |
| **Task Management** | APScheduler | Background job scheduling |

## 🔄 How It Works

1. **Upload** — Choose an audio file or document (PDF/PPTX/DOCX) via the 📤 Upload page
2. **Process** — App extracts content and transcribes audio using local faster-whisper AI
3. **Summarize** — NLTK generates summaries, extracts key concepts, and analyzes readability
4. **Quiz** — Automatic quiz generation creates questions from lecture content
5. **Export** — Download as PDF notes, Anki flashcard decks, or markdown files
6. **Track** — View analytics dashboard for learning progress and engagement metrics

## 📦 Key Dependencies

All dependencies are installed via `pip install -r requirements.txt`:

- **faster-whisper** — OpenAI Whisper-compatible speech recognition (faster, local-only)
- **streamlit** — Web app framework
- **nltk** — Natural Language Toolkit for text processing
- **textstat** — Readability scoring algorithms
- **pandas** — Data manipulation and analysis
- **plotly** — Interactive visualizations
- **weasyprint** — PDF rendering from HTML/CSS
- **pydantic** — Data validation

## ⚡ Performance Notes

- First run downloads language models (~1-2 GB) for speech recognition
- Subsequent runs are faster as models are cached locally
- Processing time depends on lecture length and your system specs
- All processing happens locally—no data sent to external servers

## � Study Pack Export & Management

### Generate Study Packs

Rebuild printable study materials from markdown sources:
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── setup_nltk.py           # NLTK data downloader
├── assets/
│   └── style.css           # Custom styling
├── components/             # Reusable UI components
│   ├── audio_player.py
│   ├── cards.py
│   ├── charts.py
│   └── sidebar.py
├── pages/                  # Streamlit multi-page app
│   ├── 01_📤_Upload.py     # Upload & process lectures
│   ├── 02_📝_Transcript.py # View & search transcripts
│   ├── 03_📊_Summary.py    # View summaries & notes
│   ├── 04_❓_Quiz.py       # Take auto-generated quizzes
│   ├── 05_📈_Analytics.py  # Learning analytics dashboard
│   ├── 06_⚙️_Settings.py   # App configuration
│   └── 07_📦_Study_Packs.py # Download, regenerate, and clear study packs
├── processors/             # Core processing modules
│   ├── audio_transcriber.py # Local faster-whisper transcription
│   ├── summarizer.py       # Text summarization
│   ├── quiz_generator.py   # Quiz question generation
│   └── text_analyzer.py    # Text analysis & readability
├── utils/                  # Utility modules
│   ├── file_handler.py     # File I/O operations
│   ├── helpers.py          # Helper functions
│   └── state_manager.py    # Session & database management
└── data/                   # Generated data (local)
    ├── uploads/
    ├── transcripts/
    └── summaries/
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Transcription | faster-whisper |
| NLP | NLTK, TextStat |
| Visualization | Plotly, Matplotlib |
| Data | Pandas, JSON |

## 📸 How It Works

1. **Upload** your lecture audio file on the Upload page
2. The app **transcribes** the audio locally using faster-whisper
3. A **summary** and study notes are automatically generated
4. **Quiz questions** are created from the lecture content
5. View **analytics** and readability insights

## 📄 License

This project is for educational purposes.

## 📚 Study Pack Export

You can regenerate the printable study pack for the current sections with one command:

```bash
python tools/generate_study_pack.py
```

This creates:
- High-quality PDFs with formatting and styling
- Anki `.apkg` decks for spaced repetition learning
- Master study pack with table of contents

### Manage Study Packs

Use the **📦 Study Packs** page in the app to:
- 📥 Download generated PDFs and Anki decks
- 🔄 Regenerate materials (rebuilds from markdown)
- 🗑️ Delete old artifacts to free up storage

## 🐛 Troubleshooting

### Import Errors
If you get import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Slow Transcription
- First run downloads the Whisper model (~1-2 GB) — this only happens once
- Ensure you have 4+ GB of free disk space
- Use smaller audio files for faster processing
- Consider using the "base" or "small" model for faster transcription

### Audio File Issues
Supported formats: MP3, WAV, M4A, OGG, FLAC, WebM
- If upload fails, try converting to MP3 first
- Maximum recommended file size: 500 MB
- Mono or stereo audio both work

### Dashboard Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Restart the Streamlit app (Ctrl+C, then `streamlit run app.py`)
- Check Python version: `python --version` (requires 3.9+)

## 📄 License

This project is for educational purposes. Feel free to use, modify, and share for learning and study applications.

## 🌟 Features Highlight

### For Students
- ✅ Automatic lecture capture and note-taking
- ✅ Self-generated quizzes for practice
- ✅ Flashcard decks for spaced repetition
- ✅ Readability analysis to measure comprehension

### For Educators
- ✅ Bulk lecture processing
- ✅ Customizable quiz difficulty levels
- ✅ Export materials for sharing
- ✅ Analytics on student engagement

### Technical
- ✅ **100% local processing** — no cloud dependencies
- ✅ **No API keys required** — works offline
- ✅ **Extensible** — modular architecture for custom processors
- ✅ **Fast** — optimized NLTK pipelines and caching

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Windows, macOS, Linux | Any |
| **Python** | 3.9 | 3.10+ |
| **RAM** | 4 GB | 8 GB+ |
| **Disk** | 5 GB (2 GB for models) | 10 GB+ |
| **Internet** | Not required after setup | Required for initial setup |

## 🤝 Contributing

Found a bug or have a feature idea? We'd love your input!

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md) — Get running in 5 minutes
- [Installation Guide](INSTALLATION.md) — Detailed setup steps
- [Usage Guide](USAGE.md) — Feature documentation

---

**Built with ❤️ using Streamlit, NLTK, and local AI**

*Helping students learn smarter, not harder.*
This rebuilds the Methods, Evaluation, and Ethics summary PDFs, flashcard PDFs, Anki `.apkg` decks, and the combined master study pack with table of contents from the markdown sources in `data/summaries/`.

Open the new **📦 Study Packs** page in Streamlit to download the generated PDFs and decks directly from the app.

You can also use the delete controls on that page to remove generated study-pack artifacts when you want to start fresh.

## ☁️ Streamlit Cloud

This repository can also be deployed to Streamlit Community Cloud. If a page uses a newer Streamlit widget option on one environment, prefer the compatibility-safe version used in this repo so local and cloud deployments behave the same way.

---

Built with ❤️ using Streamlit & local AI
