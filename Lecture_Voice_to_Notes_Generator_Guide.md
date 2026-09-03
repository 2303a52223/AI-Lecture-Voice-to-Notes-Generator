# 🎓 Lecture Voice-to-Notes Generator
## Complete Project Guide & Interview Preparation Manual

---

## 1. Project Overview & Purpose (Simplified)
The **Lecture Voice-to-Notes Generator** is an AI-powered study assistant that helps students turn lecture recordings and documents (like slides or PDFs) into clean transcripts, concise summaries, flashcards, and quizzes. 

**How it works in plain English:**
1. **Input**: A student uploads a recording of their class (audio) or a textbook chapter (PDF, PPTX, or Word document).
2. **ASR (Speech-to-Text)**: If audio is uploaded, the app transcribes it to text word-for-word.
3. **Cleaning**: The app automatically cleans up conversational speech by removing filler words like *"um"*, *"uh"*, *"like"*, or *"basically"*, and corrects misspelled terms using a custom glossary.
4. **Summary & Notes**: It generates structured, readable notes with bullet points and a Table of Contents.
5. **Study Aids**: It automatically creates practice questions (multiple choice, true/false) and Q&A flashcards.
6. **Export**: The student can download the summaries as styled PDFs or export the flashcards directly to **Anki** (a popular spaced-repetition app) as an `.apkg` file.

**Crucial Technical Highlight**: Everything is processed **100% locally** on the user's computer. It does not send any files to external cloud servers, ensuring absolute privacy, offline availability, and zero API costs.

---

## 2. Technical Stack & Tools Used

The project uses a wide range of libraries, categorized by their purpose:

| Category | Library/Tool | What It Does (Simple Terms) |
|---|---|---|
| **User Interface** | `Streamlit` | Web framework to create interactive sliders, file uploaders, tabs, and dashboards. |
| **Speech-to-Text** | `faster-whisper` | Re-implementation of OpenAI's Whisper model that runs locally to convert spoken words into text segments. |
| **Document Processing** | `PyMuPDF (fitz)` / `pdfplumber` / `pypdf` | Extracts text layouts from PDF textbooks. |
| **OCR (Optical Character Recognition)**| `pytesseract` / `Pillow` | Converts pictures or scanned pages of PDFs into searchable text. |
| **Presentation Processing** | `python-pptx` | Extracts text from PowerPoint presentation slides. |
| **Word Doc Processing** | `python-docx` | Extracts text from Microsoft Word documents. |
| **Summary Model** | `transformers` (BART-large-cnn) | Abstractive deep learning model that reads transcripts and writes summaries in natural, human-like sentences. |
| **Text Analytics** | `nltk` / `textstat` / `yake` / `rake-nltk` | Tokenizes sentences, calculates reading difficulty scores, and extracts key vocabulary terms. |
| **Format Export** | `weasyprint` | Converts HTML and Markdown study notes into styled PDFs. |
| **Flashcard Export** | `genanki` | Packages generated Q&A flashcards into a binary `.apkg` deck that Anki can import directly. |

---

## 3. Core Processing Pipelines

### Pipeline A: Audio Processing & Cleaning
1. The user uploads an audio recording.
2. The `AudioTranscriber` initializes the local `WhisperModel`. It auto-detects if the computer has an NVIDIA GPU (CUDA) and falls back to CPU if it doesn't.
3. The audio is transcribed into text segments.
4. The cleaner step normalizes whitespace, fixes repeated words (e.g. *"the the"* to *"the"*), deletes noise markers, and replaces incorrect words using a custom glossary CSV.

### Pipeline B: Document Text Extraction
1. The user uploads a document.
2. The `route_file` function detects the file extension (`.pdf`, `.pptx`, `.docx`).
3. If it's a **PDF**, the code extracts the text. If the PDF is scanned (has no copyable text), it uses `pytesseract` to run OCR page-by-page.
4. If it's a **PPTX** or **DOCX**, it extracts the slide layout structures or document paragraphs respectively.

### Pipeline C: Summarization & Notes
1. The text is split into chunks of appropriate sizes to fit the model's limitations.
2. Each chunk is processed by the local **BART** model to produce high-quality abstractive summaries.
3. The summaries are structured into Markdown with automatic titles, headings, and bullet points.

### Pipeline D: Quiz & Flashcard Generation
1. NLTK parses the text into sentences and tags parts of speech (nouns, verbs).
2. It identifies key concepts and automatically creates:
   - **MCQs** (generating wrong answers or "distractors" related to the content).
   - **True/False** statements.
   - **Fill-in-the-blank** prompts.
3. Flashcard Q&As are generated and structured into Anki format.

---

## 4. Interviewer Questions & Answers (Simplified for Humans)

### Q1: What is the benefit of using `faster-whisper` over OpenAI's official API?
**Simple Answer:**
Using the API means uploading user voice files to OpenAI, which raises privacy issues and costs money per minute. `faster-whisper` runs local model weights on your own computer. It is rewritten in C++ (CTranslate2) which makes it 4 times faster than standard local Whisper, uses less RAM, and is entirely free and secure.

### Q2: How does the system handle a massive 3-hour lecture recording that exceeds model context limits?
**Simple Answer:**
1. **Audio**: Whisper transcribes audio in short 30-second slots automatically, so audio length is not an issue.
2. **Text Summarization**: The summarization model (BART) has a strict limit of 1024 words at a time. To solve this, we split the transcript text into overlapping chunks, summarize each chunk, and combine them.

### Q3: How does the system detect if a PDF is scanned vs. text-based, and how does it extract text from it?
**Simple Answer:**
The code attempts to read text from the PDF using PyMuPDF. If the total characters extracted is zero, it concludes that the PDF consists of scanned pictures. It then uses the `pytesseract` library (OCR) to convert those scanned pictures into actual text.

### Q4: Why is there an "extractive fallback" in the summarizer module?
**Simple Answer:**
Deep learning models (BART) require a lot of memory (RAM) and can be slow if a user doesn't have a graphics card (GPU). If the system cannot load the deep learning libraries, it falls back to a math-based extractive method (TF-IDF). This method rates sentences by how often keywords appear and selects the most important ones. It is very fast and works on any low-end computer.

### Q5: How are the Anki flashcards (`.apkg` files) created programmatically?
**Simple Answer:**
We use a Python library called `genanki`. The code converts our generated questions and answers into "Card" objects. It then bundles them under a unique Deck ID (calculated by hashing the lecture title) and saves them as a binary `.apkg` file, which the user can directly import into their Anki app.

### Q6: How did you handle encoding issues on Windows?
**Simple Answer:**
Windows terminal consoles use an old encoding format called CP1252. Printing special unicode characters like checkmarks (`✓`), crosses (`✗`), or emojis (`📥`) makes Python crash. We solved this by writing a custom safe printing function that encodes text outputs to standard output using a fallback option (`errors='replace'`). This replaces incompatible symbols instead of crashing.

### Q7: What are the main limitations of running AI models locally, and how did you minimize them?
**Simple Answer:**
The main issues are high RAM usage and slow speeds on computers without graphics cards (GPUs). We minimized this by:
1. Using **faster-whisper** which is quantized (it uses smaller numbers like `int8` for calculations instead of large decimals, saving memory).
2. Allowing users to choose model sizes in the Settings (e.g. using the "base" model which is 150MB, instead of the "large" model which is 1.5GB).

### Q8: What database is used to store the user's lectures and notes?
**Simple Answer:**
A lightweight JSON-based file database (`data/database.json`). Since the app runs locally on a single user's machine, a heavy SQL database server isn't necessary. The JSON file acts as a simple lookup table, storing lecture IDs, titles, subject tags, timestamps, and file paths to the actual saved transcript text and PDF study note files.

### Q9: If two users upload lectures with the same name, how do you prevent them from overwriting each other?
**Simple Answer:**
Every lecture is assigned a unique random ID (UUID) when uploaded. All saved files (transcripts, summaries, audio) are renamed using this unique ID (e.g., `data/transcripts/<uuid>_transcript.json`). This ensures that matching titles do not cause conflicts or overwrite data.

### Q10: How does the quiz generator generate wrong answers (distractors) for multiple-choice questions?
**Simple Answer:**
It uses NLTK to identify nouns and important terms from the correct sentence context. The system then selects random terms and concepts from other parts of the text to serve as incorrect answers. This makes the quiz realistic because the wrong answers are still terms mentioned in the lecture.
