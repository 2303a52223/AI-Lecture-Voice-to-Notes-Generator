"""
Upload validation utilities.
Provides functions to validate uploaded files (type and size) and return user-friendly messages.
"""
from typing import Tuple


def human_readable_size(bytes_size: int) -> str:
    """Return human-readable size string for a number of bytes."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}PB"


def validate_upload(uploaded_file, *, max_audio_mb: int = 200, max_doc_mb: int = 50) -> Tuple[bool, str]:
    """
    Validate an uploaded file.

    Args:
        uploaded_file: Streamlit UploadedFile-like object with attributes `name`, `type`, and `size`.
        max_audio_mb: Maximum allowed size for audio files in megabytes.
        max_doc_mb: Maximum allowed size for document files in megabytes.

    Returns:
        (is_valid, message) - is_valid True if file passes checks, otherwise False and a user-facing message.
    """
    if not uploaded_file:
        return False, "No file provided. Please upload a file."

    name = getattr(uploaded_file, 'name', 'uploaded_file')
    content_type = getattr(uploaded_file, 'type', '') or ''
    size = getattr(uploaded_file, 'size', None)

    if size is None:
        return False, "Unable to determine file size. Try re-uploading."

    # Determine extension
    lower_name = name.lower()
    ext = ''
    if '.' in lower_name:
        ext = lower_name.rsplit('.', 1)[1]

    audio_exts = {'mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm'}
    doc_exts = {'pdf', 'pptx', 'docx'}

    # Audio files
    if ext in audio_exts or content_type.startswith('audio'):
        max_bytes = max_audio_mb * 1024 * 1024
        if size > max_bytes:
            return False, f"Audio file too large ({human_readable_size(size)}). Limit is {max_audio_mb} MB."
        return True, ""

    # Documents
    if ext in doc_exts or content_type in ('application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        max_bytes = max_doc_mb * 1024 * 1024
        if size > max_bytes:
            return False, f"Document too large ({human_readable_size(size)}). Limit is {max_doc_mb} MB."
        return True, ""

    # Unknown types - reject
    return False, f"Unsupported file type: {name}. Supported: audio (mp3,wav,m4a,ogg,flac,webm) and documents (pdf,pptx,docx)."
