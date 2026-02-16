"""
File Handler - Manages file operations for audio, transcripts, and summaries
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import streamlit as st

class FileHandler:
    """Handles all file operations"""
    
    def __init__(self):
        self.base_dir = Path("data")
        self.uploads_dir = self.base_dir / "uploads"
        self.transcripts_dir = self.base_dir / "transcripts"
        self.summaries_dir = self.base_dir / "summaries"
        
        # Ensure directories exist
        for directory in [self.uploads_dir, self.transcripts_dir, self.summaries_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file):
        """
        Save uploaded file to uploads directory
        Returns: (success: bool, file_path: str, file_info: dict)
        """
        try:
            # Create unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uploaded_file.name}"
            file_path = self.uploads_dir / filename
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Get file info
            file_info = {
                "original_name": uploaded_file.name,
                "saved_name": filename,
                "path": str(file_path),
                "size": uploaded_file.size,
                "type": uploaded_file.type,
                "uploaded_at": datetime.now().isoformat()
            }
            
            return True, str(file_path), file_info
            
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return False, None, None
    
    def save_transcript(self, lecture_id, transcript_text):
        """Save transcript to file"""
        try:
            transcript_file = self.transcripts_dir / f"transcript_{lecture_id}.txt"
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(transcript_text)
            return True, str(transcript_file)
        except Exception as e:
            st.error(f"Error saving transcript: {e}")
            return False, None
    
    def load_transcript(self, lecture_id):
        """Load transcript from file"""
        try:
            transcript_file = self.transcripts_dir / f"transcript_{lecture_id}.txt"
            if transcript_file.exists():
                with open(transcript_file, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            st.error(f"Error loading transcript: {e}")
            return None
    
    def save_summary(self, lecture_id, summary_data):
        """Save summary to JSON file"""
        try:
            summary_file = self.summaries_dir / f"summary_{lecture_id}.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=4, ensure_ascii=False)
            return True, str(summary_file)
        except Exception as e:
            st.error(f"Error saving summary: {e}")
            return False, None
    
    def load_summary(self, lecture_id):
        """Load summary from JSON file"""
        try:
            summary_file = self.summaries_dir / f"summary_{lecture_id}.json"
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            st.error(f"Error loading summary: {e}")
            return None
    
    def delete_lecture_files(self, lecture_id, audio_path=None):
        """Delete all files associated with a lecture"""
        try:
            # Delete audio file
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            
            # Delete transcript
            transcript_file = self.transcripts_dir / f"transcript_{lecture_id}.txt"
            if transcript_file.exists():
                transcript_file.unlink()
            
            # Delete summary
            summary_file = self.summaries_dir / f"summary_{lecture_id}.json"
            if summary_file.exists():
                summary_file.unlink()
            
            return True
        except Exception as e:
            st.error(f"Error deleting files: {e}")
            return False
    
    def get_file_size(self, file_path):
        """Get file size in human-readable format"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except:
            return "Unknown"
    
    def get_audio_duration(self, file_path):
        """Get audio duration using librosa"""
        try:
            import librosa
            duration = librosa.get_duration(path=file_path)
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes}m {seconds}s", duration
        except Exception as e:
            return "Unknown", 0
    
    def cleanup_old_files(self, days=30):
        """Delete files older than specified days"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            deleted_count = 0
            for directory in [self.uploads_dir, self.transcripts_dir, self.summaries_dir]:
                for file_path in directory.iterdir():
                    if file_path.is_file():
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_time < cutoff_date:
                            file_path.unlink()
                            deleted_count += 1
            
            return True, deleted_count
        except Exception as e:
            st.error(f"Error during cleanup: {e}")
            return False, 0
    
    def get_storage_info(self):
        """Get storage information"""
        try:
            total_size = 0
            file_count = 0
            
            for directory in [self.uploads_dir, self.transcripts_dir, self.summaries_dir]:
                for file_path in directory.iterdir():
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
                        file_count += 1
            
            return {
                "total_size": self.format_size(total_size),
                "total_size_bytes": total_size,
                "file_count": file_count
            }
        except Exception as e:
            return {"total_size": "Unknown", "file_count": 0}
    
    def format_size(self, size_bytes):
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def save_upload(self, uploaded_file):
        """Save uploaded file (alias for save_uploaded_file). Returns file path or None."""
        success, file_path, _ = self.save_uploaded_file(uploaded_file)
        return file_path if success else None
    
    def get_transcript_path(self, title):
        """Get path for saving transcript file"""
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
        safe_name = safe_name.replace(' ', '_')[:100]
        return str(self.transcripts_dir / f"{safe_name}_transcript.json")
    
    def get_summary_path(self, title):
        """Get path for saving summary file"""
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
        safe_name = safe_name.replace(' ', '_')[:100]
        return str(self.summaries_dir / f"{safe_name}_summary.md")
