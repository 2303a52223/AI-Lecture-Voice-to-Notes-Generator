# 🎓 Lecture Voice-to-Notes Generator

An AI-powered study assistant that converts lecture audio recordings into comprehensive study materials — transcripts, summaries, quizzes, and analytics.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AssemblyAI](https://img.shields.io/badge/AssemblyAI-000000?style=for-the-badge&logo=assemblyai&logoColor=white)

## ✨ Features

- **🎤 Audio Transcription** — Upload lecture audio files (MP3, WAV, M4A, OGG, FLAC, WebM) and get accurate transcriptions powered by AssemblyAI's universal speech models with automatic language detection.
- **📝 Smart Summaries** — AI-generated summaries and study notes in multiple styles (concise, detailed, bullet points).
- **❓ Quiz Generation** — Auto-generated quiz questions (multiple choice, true/false, fill-in-the-blank) to test your understanding.
- **📊 Text Analytics** — Readability scores, word frequency analysis, key term extraction, and more.
- **📈 Analytics Dashboard** — Track your learning progress across all uploaded lectures.

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

3. **Download NLTK data**
   ```bash
   python setup_nltk.py
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at **http://localhost:8501**

## 📁 Project Structure

```
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
│   └── 07_📦_Study_Packs.py # Download PDFs and Anki decks
├── processors/             # Core processing modules
│   ├── transcriber.py      # AssemblyAI transcription
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
| Transcription | AssemblyAI API |
| NLP | NLTK, TextStat |
| Visualization | Plotly, Matplotlib |
| Data | Pandas, JSON |

## 📸 How It Works

1. **Upload** your lecture audio file on the Upload page
2. The app **transcribes** the audio using AssemblyAI
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

This rebuilds the Methods, Evaluation, and Ethics summary PDFs, flashcard PDFs, Anki `.apkg` decks, and the combined master study pack with table of contents from the markdown sources in `data/summaries/`.

Open the new **📦 Study Packs** page in Streamlit to download the generated PDFs and decks directly from the app.

---

Built with ❤️ using Streamlit & AssemblyAI
