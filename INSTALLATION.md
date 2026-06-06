# Installation Guide

## Quick Start Installation

### Step 1: Install Python
Ensure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Install FFmpeg

#### Windows:
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH

Or use Chocolatey:
```bash
choco install ffmpeg
```

#### Mac:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install ffmpeg
```

### Step 3: Install Python Dependencies

Navigate to the project directory and run:
```bash
pip install -r requirements.txt
```

**Note:** This will download ~2GB of packages. Be patient!

### Step 4: Download NLTK Data

Run Python and execute:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

Or use the automated script:
```bash
python setup_nltk.py
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## First Run

On first use, the application will:
1. Download Whisper model (~150MB) on first transcription
2. Download BART model (~1.6GB) on first summarization
3. Create local database and folders

This is a one-time setup. Subsequent runs will be instant.

## GPU Support (Optional but Recommended)

For faster processing with NVIDIA GPU:

### Install CUDA (if not already installed):
- Download from https://developer.nvidia.com/cuda-downloads
- Version 11.8 or higher recommended

### Install PyTorch with CUDA:
```bash
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Verify GPU is detected:
```python
import torch
print(torch.cuda.is_available())  # Should print True
print(torch.cuda.get_device_name(0))  # Shows your GPU name
```

## Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution:** Install requirements again:
```bash
pip install -r requirements.txt
```

### Issue: "FFmpeg not found"
**Solution:** Ensure FFmpeg is installed and in PATH. Test with:
```bash
ffmpeg -version
```

### Issue: "Out of memory" during transcription
**Solution:** 
- Use a smaller Whisper model (tiny or base)
- Close other applications
- Process shorter audio files
- Upgrade RAM if possible

### Issue: Models downloading very slowly
**Solution:**
- Use wired internet connection
- Download models manually from Hugging Face:
  - Whisper: https://huggingface.co/openai/whisper-base
  - BART: https://huggingface.co/facebook/bart-large-cnn

### Issue: "CUDA out of memory"
**Solution:**
- Use smaller batch sizes
- Use CPU mode instead
- Use smaller models
- Reduce input length

## Advanced Configuration

### Custom Model Cache Location

Set environment variable:
```bash
# Windows
set TORCH_HOME=D:\AI_Models

# Linux/Mac
export TORCH_HOME=~/ai_models
```

### Running on a Server

To access from other devices on your network:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then access from other devices using: `http://YOUR_IP:8501`

### Running in Production

For production deployment:
```bash
streamlit run app.py --server.headless true --server.enableCORS false
```

## System Requirements

### Minimum:
- CPU: 4 cores, 2.5 GHz
- RAM: 8GB
- Storage: 5GB free
- Internet: For initial setup only

### Recommended:
- CPU: 8 cores, 3.0+ GHz
- RAM: 16GB
- GPU: NVIDIA with 4GB+ VRAM
- Storage: 10GB free (SSD preferred)
- Internet: Fast connection for initial download

## Performance Tips

1. **Use GPU if available** - 2-3x faster processing
2. **Use base model** for best speed/accuracy balance
3. **Process audio in chunks** for very long lectures
4. **Close other applications** during processing
5. **Use SSD** for faster model loading

## Updating

To update to the latest version:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

To remove the application:
1. Delete the project folder
2. Remove models cache: Delete `models/` folder
3. Remove data: Delete `data/` folder
4. Uninstall Python packages (optional):
```bash
pip uninstall -r requirements.txt -y
```

## Getting Help

If you encounter issues:
1. Check this installation guide
2. Review the README.md file
3. Check system requirements
4. Verify all dependencies are installed
5. Try running with verbose logging

## Success Checklist

- ✅ Python 3.8+ installed
- ✅ FFmpeg installed and in PATH
- ✅ All Python packages installed
- ✅ NLTK data downloaded
- ✅ Application starts without errors
- ✅ Can upload audio file
- ✅ Can transcribe audio
- ✅ Can generate summary
- ✅ Can create quiz

Congratulations! You're ready to use the Lecture Voice-to-Notes Generator! 🎉
