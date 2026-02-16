"""
Transcriber Module - Audio to text transcription using AssemblyAI
"""
import json
import time
from pathlib import Path
from datetime import datetime
from threading import Thread

import assemblyai as aai

# Set AssemblyAI API key
ASSEMBLYAI_API_KEY = "5116de72718b42b799f959b7969fcdd6"
aai.settings.api_key = ASSEMBLYAI_API_KEY


class Transcriber:
    """Handles audio transcription using AssemblyAI API"""
    
    def __init__(self):
        """Initialize transcriber"""
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm']
    
    def transcribe(self, audio_path, language=None, progress_callback=None):
        """
        Transcribe audio file to text using AssemblyAI SDK.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es') or None for auto-detect
            progress_callback: Optional (progress_float, message) callback
            
        Returns:
            dict: Transcription result with text, segments, and metadata
        """
        # Validate file
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        if audio_path.suffix.lower() not in self.supported_formats:
            raise ValueError(
                f"Unsupported format: {audio_path.suffix}. "
                f"Supported: {', '.join(self.supported_formats)}"
            )
        
        # Build config
        config_kwargs = {
            "speech_models": ["universal-3-pro", "universal-2"],
        }
        if language:
            config_kwargs["language_code"] = language
        else:
            config_kwargs["language_detection"] = True
        
        config = aai.TranscriptionConfig(**config_kwargs)
        
        if progress_callback:
            progress_callback(0.05, "Uploading audio to AssemblyAI...")
        
        start_time = time.time()
        
        # Run transcription in a thread so we can show progress
        result_holder = {"transcript": None, "error": None}
        
        def _run_transcription():
            try:
                transcriber = aai.Transcriber(config=config)
                result_holder["transcript"] = transcriber.transcribe(str(audio_path))
            except Exception as e:
                result_holder["error"] = e
        
        thread = Thread(target=_run_transcription)
        thread.start()
        
        # Show live progress while waiting
        while thread.is_alive():
            elapsed = int(time.time() - start_time)
            if progress_callback:
                # Progress from 0.10 to 0.85 over ~2 minutes
                pct = 0.10 + min(elapsed / 120, 1.0) * 0.75
                progress_callback(pct, f"AssemblyAI processing... {elapsed}s elapsed")
            time.sleep(2)
        
        thread.join()
        
        # Check for errors
        if result_holder["error"]:
            raise result_holder["error"]
        
        transcript = result_holder["transcript"]
        
        if transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(f"Transcription failed: {transcript.error}")
        
        elapsed_time = time.time() - start_time
        
        if progress_callback:
            progress_callback(0.90, "Processing transcript data...")
        
        # Format result
        detected_language = "unknown"
        if transcript.json_response and "language_code" in transcript.json_response:
            detected_language = transcript.json_response["language_code"]
        
        transcription = {
            'text': transcript.text or '',
            'segments': [],
            'language': detected_language,
            'duration': 0,
            'processing_time': round(elapsed_time, 2),
            'model_size': 'assemblyai',
            'timestamp': datetime.now().isoformat()
        }
        
        # Build segments from words (group ~15 words each)
        words = transcript.words or []
        if words:
            chunk_size = 15
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i + chunk_size]
                start_sec = chunk[0].start / 1000.0
                end_sec = chunk[-1].end / 1000.0
                text = ' '.join(w.text for w in chunk)
                transcription['segments'].append({
                    'id': i // chunk_size,
                    'start': round(start_sec, 2),
                    'end': round(end_sec, 2),
                    'text': text.strip()
                })
        
        # Duration
        if transcription['segments']:
            transcription['duration'] = transcription['segments'][-1]['end']
        elif transcript.json_response and "audio_duration" in transcript.json_response:
            transcription['duration'] = transcript.json_response["audio_duration"]
        
        return transcription
    
    def save_transcript(self, transcription, output_path):
        """
        Save transcription to JSON file
        
        Args:
            transcription: Transcription result dict
            output_path: Path to save JSON file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, indent=2, ensure_ascii=False)
    
    def load_transcript(self, file_path):
        """
        Load transcription from JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            dict: Transcription result
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search_transcript(self, transcription, query):
        """
        Search for text in transcript segments
        
        Args:
            transcription: Transcription result dict
            query: Search query string
            
        Returns:
            list: Matching segments
        """
        query_lower = query.lower()
        matches = []
        
        for segment in transcription.get('segments', []):
            if query_lower in segment['text'].lower():
                matches.append(segment)
        
        return matches
    
    def get_text_at_time(self, transcription, time_seconds):
        """
        Get text at a specific time
        
        Args:
            transcription: Transcription result dict
            time_seconds: Time in seconds
            
        Returns:
            dict or None: Segment at the given time
        """
        for segment in transcription.get('segments', []):
            if segment['start'] <= time_seconds <= segment['end']:
                return segment
        
        return None
    
    def format_transcript(self, transcription, include_timestamps=True):
        """
        Format transcription as readable text
        
        Args:
            transcription: Transcription result dict
            include_timestamps: Whether to include timestamps
            
        Returns:
            str: Formatted transcript text
        """
        if not include_timestamps:
            return transcription.get('text', '')
        
        lines = []
        for segment in transcription.get('segments', []):
            start = self._format_time(segment['start'])
            end = self._format_time(segment['end'])
            text = segment['text']
            lines.append(f"[{start} --> {end}] {text}")
        
        return '\n'.join(lines)
    
    def _format_time(self, seconds):
        """Format seconds to HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"
