# 🚀 QUICK START GUIDE

## Get Up and Running in 5 Minutes!

### Step 1: Install FFmpeg (Required for Audio Processing)

**Windows:**
```powershell
# Using Chocolatey (easiest):
choco install ffmpeg

# Or download manually from: https://ffmpeg.org/download.html
# Extract and add to PATH
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### Step 2: Install Python Dependencies

```bash
# Navigate to project directory
cd "c:\Users\ksair\OneDrive\Desktop\Lecture Voice-to-Notes Generator"

# Install all requirements
pip install -r requirements.txt
```

**Note:** This will take 5-10 minutes and download ~2GB of packages.

### Step 3: Download NLTK Data

```bash
python setup_nltk.py
```

Or manually:
```python
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
>>> nltk.download('averaged_perceptron_tagger')
>>> exit()
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

**First Run:** The app will download AI models (~500MB-1GB) when you first use each feature. This is one-time only!

---

## Quick Test

### Test with a Sample Lecture

1. **Record a short test** (30 seconds):
   - Use your phone voice recorder
   - Say: "This is a test lecture about machine learning. Neural networks are computational models inspired by the brain."
   - Save as MP3

2. **Upload to app:**
   - Click "📤 Upload"
   - Select your test audio
   - Title: "Test Lecture"
   - Click "🚀 Process Lecture"

3. **Wait for transcription** (~30 seconds for 30-second audio)

4. **Try features:**
   - View transcript
   - Generate summary
   - Create quiz

---

## Troubleshooting Quick Fixes

### "FFmpeg not found"
```bash
# Verify FFmpeg is installed:
ffmpeg -version

# If not found, add to PATH or reinstall
```

### "No module named 'streamlit'"
```bash
pip install streamlit
```

### "CUDA out of memory" or slow processing
- Use smaller model in Settings
- Close other applications
- GPU is optional (CPU works fine)

### Application won't start
```bash
# Clear Streamlit cache:
streamlit cache clear

# Then run again:
streamlit run app.py
```

---

## What Happens on First Run?

### Automatic Downloads:

1. **First Transcription:**
   - Downloads Whisper base model (~150MB)
   - Takes 2-3 minutes

2. **First Summary:**
   - Downloads BART model (~1.6GB)
   - Takes 5-10 minutes

3. **Subsequent Uses:**
   - Uses cached models
   - Much faster!

### Storage Locations:

- Models: `models/` directory
- Data: `data/` directory
- Database: `data/database.json`

---

## Your First Workflow

### Complete First Lecture (15 minutes)

1. **Prepare** (1 minute):
   ```bash
   streamlit run app.py
   ```

2. **Upload** (1 minute):
   - Go to Upload page
   - Select your lecture audio
   - Enter title
   - Click Process

3. **Transcribe** (varies by length):
   - 10-min lecture ≈ 1.5 minutes
   - 60-min lecture ≈ 9 minutes
   - Wait for "✅ Transcription complete!"

4. **Review Transcript** (2 minutes):
   - Check for errors
   - Edit if needed
   - Download if desired

5. **Generate Summary** (2 minutes):
   - Click "Generate Summary"
   - Choose length & style
   - Wait for processing

6. **Create Quiz** (1 minute):
   - Select number of questions
   - Choose difficulty
   - Click "Generate Quiz"

7. **Study** (5 minutes):
   - Review summary
   - Take quiz
   - Check answers

**Congratulations!** You've completed your first lecture processing! 🎉

---

## Performance Tips

### For Faster Processing:

1. **Use GPU** (if available):
   - Install CUDA
   - Install PyTorch with CUDA support
   - 2-3x faster

2. **Choose Right Model:**
   - **Tiny**: 3-4x faster than base
   - **Base**: Recommended balance
   - **Small**: 2x slower than base

3. **Optimize Settings:**
   - Use shorter summaries
   - Fewer quiz questions
   - Disable auto-features

### For Better Accuracy:

1. **Use Larger Models:**
   - Small or Medium Whisper
   - Slower but more accurate

2. **Better Audio:**
   - Clear recording
   - Minimal noise
   - Good microphone

3. **Manual Review:**
   - Edit transcripts
   - Verify key points

---

## Next Steps

### Learn More:

- 📖 Read `README.md` for overview
- 📚 Check `USAGE.md` for detailed guide  
- ⚙️ Review `INSTALLATION.md` for advanced setup

### Customize:

- ⚙️ Open Settings page
- Choose your default models
- Set preferred options
- Save settings

### Get Help:

- Check documentation files
- Review error messages
- Verify system requirements
- Test with short audio first

---

## System Check

Before you start, verify:

- ✅ Python 3.8+ installed: `python --version`
- ✅ FFmpeg installed: `ffmpeg -version`
- ✅ Packages installed: `pip list | grep streamlit`
- ✅ NLTK data ready: `python -c "import nltk"`
- ✅ 5GB free disk space
- ✅ 8GB+ RAM available

---

## Common First-Time Questions

**Q: Do I need internet?**
A: Only for initial setup and model downloads. After that, fully offline!

**Q: Do I need GPU?**
A: No, CPU works fine! GPU just makes it 2-3x faster.

**Q: Is my data private?**
A: 100% Yes! Everything runs locally. No data leaves your computer.

**Q: How long does it take?**
A: Setup: 10 minutes. Processing: ~15% of audio length with base model.

**Q: Can I process multiple lectures?**
A: Yes! Process one at a time or queue them up.

**Q: What languages are supported?**
A: 50+ languages! Whisper supports most major languages.

---

## Success!

You're all set! 🎉

```bash
streamlit run app.py
```

**Happy Learning!** 📚🎓

---

## Need Help?

If you encounter issues:

1. Check error message carefully
2. Review this guide
3. Check INSTALLATION.md
4. Verify all dependencies installed
5. Try with a short test audio first

**Most issues are due to:**
- Missing FFmpeg
- Insufficient RAM
- Incorrect file format
- First-time model downloads

**Remember:** First run is slowest due to downloads. Be patient!
