"""
Audio Player Component - Custom audio player with controls
"""
import streamlit as st
import base64
from pathlib import Path

def render_audio_player(audio_file_path, title="Audio Lecture"):
    """
    Render custom audio player
    
    Args:
        audio_file_path: Path to audio file
        title: Title to display above player
    """
    try:
        # Read audio file
        with open(audio_file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        # Get file extension
        file_ext = Path(audio_file_path).suffix.lower().replace('.', '')
        
        # Map extensions to MIME types
        mime_types = {
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'ogg': 'audio/ogg',
            'm4a': 'audio/mp4',
            'flac': 'audio/flac'
        }
        
        mime_type = mime_types.get(file_ext, 'audio/mpeg')
        
        # Display title
        st.markdown(f"### 🎵 {title}")
        
        # Native Streamlit audio player
        st.audio(audio_bytes, format=mime_type)
        
        # Additional info
        from utils.file_handler import FileHandler
        file_handler = FileHandler()
        file_size = file_handler.get_file_size(audio_file_path)
        duration_str, duration_sec = file_handler.get_audio_duration(audio_file_path)
        
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"📁 Size: {file_size}")
        with col2:
            st.caption(f"⏱️ Duration: {duration_str}")
        
        return True
        
    except Exception as e:
        st.error(f"Error loading audio: {e}")
        return False

def render_waveform_player(audio_file_path, title="Audio Lecture"):
    """
    Render audio player with waveform visualization
    (Simplified version - full waveform requires additional libraries)
    """
    try:
        st.markdown(f"### 🎵 {title}")
        
        # Display standard player
        with open(audio_file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        file_ext = Path(audio_file_path).suffix.lower().replace('.', '')
        mime_types = {
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'ogg': 'audio/ogg',
            'm4a': 'audio/mp4'
        }
        mime_type = mime_types.get(file_ext, 'audio/mpeg')
        
        st.audio(audio_bytes, format=mime_type)
        
        # Try to display simple waveform (if librosa is available)
        try:
            import librosa
            import librosa.display
            import matplotlib.pyplot as plt
            import numpy as np
            
            with st.spinner("Generating waveform..."):
                # Load audio
                y, sr = librosa.load(audio_file_path, duration=60)  # First 60 seconds
                
                # Create waveform
                fig, ax = plt.subplots(figsize=(12, 3))
                librosa.display.waveshow(y, sr=sr, ax=ax, color='#667eea')
                ax.set_xlabel('Time (s)')
                ax.set_ylabel('Amplitude')
                ax.set_title('Waveform (First 60s)')
                plt.tight_layout()
                
                st.pyplot(fig)
                plt.close()
        
        except ImportError:
            pass  # librosa not available, skip waveform
        except Exception:
            pass  # Error generating waveform, skip
        
        return True
        
    except Exception as e:
        st.error(f"Error loading audio: {e}")
        return False

def render_mini_player(audio_file_path):
    """
    Render minimal audio player
    """
    try:
        with open(audio_file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        file_ext = Path(audio_file_path).suffix.lower().replace('.', '')
        mime_types = {
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'ogg': 'audio/ogg',
            'm4a': 'audio/mp4'
        }
        mime_type = mime_types.get(file_ext, 'audio/mpeg')
        
        st.audio(audio_bytes, format=mime_type)
        return True
        
    except Exception as e:
        st.error(f"Error loading audio: {e}")
        return False
