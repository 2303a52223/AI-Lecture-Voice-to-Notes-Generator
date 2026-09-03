# Usage Guide

## Complete User Guide for Lecture Voice-to-Notes Generator

### Table of Contents
1. [Getting Started](#getting-started)
2. [Uploading Lectures](#uploading-lectures)
3. [Viewing Transcripts](#viewing-transcripts)
4. [Generating Summaries](#generating-summaries)
5. [Taking Quizzes](#taking-quizzes)
6. [Analytics & Progress](#analytics-progress)
7. [Settings](#settings)
8. [Tips & Best Practices](#tips-best-practices)

---

## Getting Started

### First Launch

1. Open terminal/command prompt
2. Navigate to project directory
3. Run: `streamlit run app.py`
4. Application opens in browser at `http://localhost:8501`

### Understanding the Interface

- **Sidebar**: Navigation and quick stats
- **Main Area**: Content and interactions
- **Top Tabs**: Multi-page navigation

---

## Uploading Lectures

### Step 1: Navigate to Upload Page

Click **"📤 Upload"** from home page or sidebar

### Step 2: Select Audio File

- Click "Choose an audio file"
- Select your lecture recording
- Supported formats: MP3, WAV, M4A, OGG, FLAC
- Maximum size: 500MB

### Step 3: Configure Settings

**Lecture Title**: Give your lecture a descriptive name

**Whisper Model**: Choose transcription model
- **Tiny**: Fastest, less accurate
- **Base**: Recommended (balanced)
- **Small**: More accurate, slower
- **Medium/Large**: Best accuracy, very slow

**Language**: Select audio language or use auto-detect

**Options**:
- ✅ Auto-generate summary after transcription
- ✅ Save transcript to file

### Step 4: Process

Click **"🚀 Process Lecture"**

Watch progress:
- Saving audio file ✓
- Loading Whisper model ✓
- Transcribing audio ✓
- Processing results ✓

**Estimated Time**: 
- 1-hour lecture ≈ 9 minutes (base model on CPU)
- 1-hour lecture ≈ 3 minutes (base model on GPU)

---

## Viewing Transcripts

### Navigate to Transcript Page

From sidebar or after upload completion

### View Options

**Plain Text**: Clean transcript without timestamps

**With Timestamps**: Each segment marked with time
```
[00:32] Welcome to today's lecture
[00:45] We'll be discussing...
```

### Edit Transcript

1. Enable **"✏️ Enable Editing"** checkbox
2. Make corrections to text
3. Click **"💾 Save Changes"**

### Search Transcript

1. Use search box to find words/phrases
2. View results with context
3. See all occurrences highlighted

### Download Options

- **📄 TXT**: Plain text format
- **⏱️ Timestamped**: With time markers
- **📋 JSON**: Structured data format

---

## Generating Summaries

### Generate New Summary

1. Navigate to **"📊 Summary"** page
2. Choose settings:
   - **Length**: Short / Medium / Long
   - **Style**: Bullets / Paragraph / Detailed
3. Click **"✨ Generate Summary"**

### View Summary Sections

**📄 Summary Tab**: Main AI-generated summary

**🎯 Key Points Tab**: Important points extracted

**🏷️ Topics Tab**: Main themes identified

**📚 Full Notes Tab**: Complete study guide

### Download Study Materials

Each section has download button:
- Summary as TXT
- Key Points as TXT
- Full Study Notes as Markdown

### Regenerate Summary

Want different length/style?
1. Expand **"🔄 Regenerate Summary"**
2. Choose new settings
3. Click regenerate

---

## Taking Quizzes

### Generate Quiz

1. Navigate to **"❓ Quiz"** page
2. Configure:
   - **Number of Questions**: 5-20
   - **Difficulty**: Easy / Medium / Hard
3. Click **"🎲 Generate Quiz"**

### Quiz Types

**Multiple Choice**: Select correct answer from 4 options

**True/False**: Determine if statement is accurate

**Fill in the Blank**: Complete the sentence

### Taking the Quiz

1. Answer each question
2. No time limit - take your time
3. Click **"✅ Submit Quiz"** when done

### View Results

See your score and breakdown:
- **80%+**: Excellent! 🌟
- **60-79%**: Good job! 👍
- **Below 60%**: Keep practicing! 📚

Review each question:
- ✅ Correct answers
- ❌ Incorrect with explanations

### Flashcards Mode

1. Click **"🎴 Generate Flashcards"**
2. Choose number of cards (5-25)
3. Navigate with Previous/Next
4. Flip card to see answer

**Flashcard Controls**:
- ⬅️ Previous
- 🔄 Flip Card
- ➡️ Next

---

## Analytics & Progress

### Overview Dashboard

View your learning statistics:
- Total lectures processed
- Total study time
- Quizzes completed
- Storage used

### Lecture Timeline

Visual timeline showing:
- Upload dates
- Lecture durations
- Processing status

### Text Analysis

For current lecture, analyze:

**Basic Stats**:
- Word count
- Sentence count
- Reading time
- Lexical diversity

**Readability**:
- Flesch Reading Ease
- Grade level
- Complexity scores

**Word Frequency**:
- Most common words
- Word cloud visualization

**Complexity Analysis**:
- Long sentences
- Complex words
- Passive voice usage
- Sentiment

### Compare Lectures

1. Select two lectures
2. Click **"📊 Compare"**
3. See side-by-side statistics

---

## Settings

### Transcription Settings

**Default Whisper Model**: Choose preferred model

**Default Language**: Set primary language

**Auto-transcribe**: Start automatically on upload

### Summarization Settings

**Default Length**: Short / Medium / Long

**Default Style**: Bullets / Paragraph / Detailed

**Auto-summarize**: Generate after transcription

### Quiz Settings

**Default Questions**: How many questions

**Default Difficulty**: Easy / Medium / Hard

**Show Explanations**: Display after quiz

### Display Settings

**Color Theme**: Visual appearance

**Compact View**: Dense UI layout

**Show Timestamps**: In transcripts

### Performance Settings

**Use GPU**: Enable GPU acceleration

**Cache Models**: Keep in memory

**Max File Size**: Upload limit

### Storage Settings

**Auto-save**: Save transcripts automatically

**Auto-cleanup**: Delete old files

**Cleanup Days**: Age threshold

### Save Settings

Click **"💾 Save Settings"** to apply changes

---

## Tips & Best Practices

### Audio Quality

✅ **Do:**
- Use high-quality microphone
- Record in quiet environment
- Ensure speaker is clear
- Test audio before full lecture

❌ **Don't:**
- Record with background music
- Use very compressed formats
- Have multiple speakers overlapping
- Record from low-quality sources

### Choosing Models

**For Speed** (CPU users):
- Use **tiny** or **base** model
- Process shorter segments
- Generate shorter summaries

**For Accuracy** (GPU users):
- Use **small** or **medium** model
- Full-length processing
- Detailed summaries

### Organizing Lectures

- Use descriptive titles
- Include date/topic in name
- Tag by subject/course
- Regular cleanup of old files

### Study Workflow

1. **Upload** lecture immediately after class
2. **Review** transcript within 24 hours
3. **Study** summary before next class
4. **Quiz** yourself weekly
5. **Track** progress monthly

### Storage Management

- Regularly delete old lectures
- Export important notes
- Monitor storage usage
- Clean up temporary files

### Keyboard Shortcuts

- `Ctrl+R`: Refresh page
- `Ctrl+/`: Focus sidebar
- `Esc`: Close modals

---

## Troubleshooting

### Slow Transcription

**Solutions:**
- Use smaller model (tiny/base)
- Enable GPU acceleration
- Close other applications
- Process shorter audio

### Inaccurate Transcription

**Solutions:**
- Use larger model
- Specify correct language
- Improve audio quality
- Manually edit transcript

### Poor Summary Quality

**Solutions:**
- Use longer summary length
- Try different style
- Ensure good transcript
- Use detailed mode

### Crashes During Processing

**Solutions:**
- Reduce file size
- Use smaller model
- Free up RAM
- Check system requirements

---

## Advanced Features

### Batch Processing

Process multiple lectures:
1. Upload first lecture
2. While processing, prepare next
3. Queue subsequent uploads

### Export All Data

1. Go to Settings
2. Enable "Allow data export"
3. Download database.json
4. Save all transcripts/summaries

### Custom Workflows

Create your study system:
- Immediate transcription
- Next-day summary review
- Weekly quiz sessions
- Monthly progress check

---

## Support & Help

**Need help?**
- Check INSTALLATION.md for setup
- Review this guide thoroughly
- Check system requirements
- Verify all dependencies

**Reporting Issues:**
Include:
- Error message
- Steps to reproduce
- System information
- Screenshots if relevant

---

## Conclusion

You now know how to:
- ✅ Upload and transcribe lectures
- ✅ Generate and customize summaries
- ✅ Create and take quizzes
- ✅ Track your progress
- ✅ Optimize your workflow

Happy studying! 📚🎓
