"""
Helper Functions - Utility functions used across the application
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Any
import re

def format_timestamp(iso_string: str) -> str:
    """Convert ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return "Unknown"

def format_date(iso_string: str) -> str:
    """Convert ISO timestamp to date only"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%B %d, %Y")
    except:
        return "Unknown"

def time_ago(iso_string: str) -> str:
    """Convert ISO timestamp to 'time ago' format"""
    try:
        dt = datetime.fromisoformat(iso_string)
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return "Unknown"

def format_duration(seconds: int | float) -> str:
    """Format seconds to readable duration"""
    try:
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    except:
        return "Unknown"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def calculate_reading_time(text: str) -> int:
    """Calculate estimated reading time in minutes"""
    words = len(text.split())
    # Average reading speed: 200 words per minute
    minutes = words / 200
    return max(1, round(minutes))

def extract_keywords(text: str, num_keywords: int = 10) -> list[str]:
    """Extract top keywords from text"""
    try:
        from collections import Counter
        import re
        
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Common words to exclude
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'will', 'your', 'about',
            'which', 'their', 'would', 'there', 'could', 'other', 'than',
            'then', 'them', 'these', 'some', 'such', 'into', 'just', 'only',
            'over', 'also', 'back', 'after', 'more', 'very', 'when', 'been',
            'well', 'much', 'where', 'should', 'being', 'through', 'before'
        }
        
        # Filter out stop words
        filtered_words = [w for w in words if w not in stop_words]
        
        # Get most common words
        word_counts = Counter(filtered_words)
        return [word for word, count in word_counts.most_common(num_keywords)]
    except:
        return []

def calculate_text_stats(text: str) -> dict[str, Any]:
    """Calculate various text statistics"""
    try:
        import textstat  # type: ignore[import-unresolved]
        
        stats = {
            "word_count": len(text.split()),
            "char_count": len(text),
            "sentence_count": text.count('.') + text.count('!') + text.count('?'),
            "paragraph_count": len([p for p in text.split('\n\n') if p.strip()]),
            "reading_time": calculate_reading_time(text),
            "reading_level": textstat.flesch_reading_ease(text),  # type: ignore[attr-defined]
            "grade_level": textstat.flesch_kincaid_grade(text)  # type: ignore[attr-defined]
        }
        
        return stats
    except Exception as e:
        return {
            "word_count": len(text.split()),
            "char_count": len(text),
            "reading_time": calculate_reading_time(text)
        }

def validate_audio_file(file: Any) -> tuple[bool, list[str]]:
    """Validate uploaded audio file"""
    allowed_types = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/m4a', 
                     'audio/x-m4a', 'audio/ogg', 'audio/flac']
    max_size = 500 * 1024 * 1024  # 500 MB
    
    errors = []
    
    if file.type not in allowed_types:
        errors.append("Invalid file type. Please upload MP3, WAV, M4A, OGG, or FLAC files.")
    
    if file.size > max_size:
        errors.append(f"File too large. Maximum size is 500 MB. Your file is {file.size / (1024*1024):.2f} MB.")
    
    return len(errors) == 0, errors

def show_success(message: str) -> None:
    """Display success message with custom styling"""
    st.markdown(f"""
    <div style="background-color: #d4edda; border-left: 4px solid #28a745; 
                padding: 1rem; border-radius: 4px; margin: 1rem 0;">
        <p style="color: #155724; margin: 0; font-weight: 500;">
            ✅ {message}
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_error(message: str) -> None:
    """Display error message with custom styling"""
    st.markdown(f"""
    <div style="background-color: #f8d7da; border-left: 4px solid #dc3545; 
                padding: 1rem; border-radius: 4px; margin: 1rem 0;">
        <p style="color: #721c24; margin: 0; font-weight: 500;">
            ❌ {message}
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_info(message: str) -> None:
    """Display info message with custom styling"""
    st.markdown(f"""
    <div style="background-color: #d1ecf1; border-left: 4px solid #17a2b8; 
                padding: 1rem; border-radius: 4px; margin: 1rem 0;">
        <p style="color: #0c5460; margin: 0; font-weight: 500;">
            ℹ️ {message}
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_warning(message: str) -> None:
    """Display warning message with custom styling"""
    st.markdown(f"""
    <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; 
                padding: 1rem; border-radius: 4px; margin: 1rem 0;">
        <p style="color: #856404; margin: 0; font-weight: 500;">
            ⚠️ {message}
        </p>
    </div>
    """, unsafe_allow_html=True)

def progress_bar_with_text(progress: float, text: str) -> None:
    """Display progress bar with text"""
    st.progress(progress)
    st.text(text)

def format_file_size(size_bytes: int | float) -> str:
    """Format bytes to human readable file size"""
    try:
        size_bytes = float(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
    except:
        return "Unknown"
