"""
Audio transcriber using faster-whisper (local)

This wrapper tries to use `faster-whisper` for local, offline transcription.
If `faster-whisper` is not installed, the class will raise an informative error
when `transcribe()` is called.

Returned transcription format matches the rest of the app: a dict with keys
`text`, `segments`, `language`, `duration`.
"""
from pathlib import Path
import json
from utils.retry import retry_call
from utils.error_handler import report_error


class AudioTranscriber:
    def __init__(self, model_name="base", device=None):
        self.model = None
        self.model_name = model_name
        self.device = device
        try:
            # Lazily import and instantiate WhisperModel with retries
            def _init_whisper():
                from faster_whisper import WhisperModel
                # Auto-select device if not provided
                dev = self.device
                if not dev:
                    try:
                        import torch
                        dev = "cuda" if torch.cuda.is_available() else "cpu"
                    except Exception:
                        dev = "cpu"
                compute_type = "float16" if dev == "cuda" else "int8"
                return WhisperModel(self.model_name, device=dev, compute_type=compute_type)

            try:
                self._whisper = retry_call(_init_whisper, tries=3, delay=1.0, backoff=2.0)
                self.model = self._whisper
                # update device in case it was auto-selected
                self.device = getattr(self._whisper, 'device', self.device)
            except Exception as e:
                self.model = None
                self._init_error = e
        except Exception as e:
            # record init error
            self.model = None
            self._init_error = e

    def transcribe(self, audio_path, language=None, progress_callback=None):
        p = Path(audio_path)
        if not p.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if self.model is None:
            raise RuntimeError(
                "faster-whisper is not available. Install it with `pip install faster-whisper`\n"
                f"Init error: {getattr(self, '_init_error', 'unknown')}"
            )

        # Progress: load model
        if progress_callback:
            progress_callback(0.01, "Loading local ASR model...")

        segments_out = []
        try:
            # The faster-whisper API returns (segments, info)
            try:
                segments, info = retry_call(
                    lambda: self._whisper.transcribe(
                        str(p),
                        language=language if language else None,
                        beam_size=1,
                        vad_filter=True,
                        condition_on_previous_text=False,
                        word_timestamps=False,
                    ),
                    tries=2,
                    delay=1.0,
                    backoff=2.0
                )
            except Exception as e:
                report_error(e, "Transcription failed")
                raise RuntimeError(f"Local transcription failed: {e}")

            # Iterate segments and build simple structure
            for i, seg in enumerate(segments):
                # seg has attributes: start, end, text
                seg_text = seg.text if hasattr(seg, 'text') else str(seg)
                seg_start = float(getattr(seg, 'start', 0.0))
                seg_end = float(getattr(seg, 'end', 0.0))
                segments_out.append({
                    'id': i,
                    'start': round(seg_start, 2),
                    'end': round(seg_end, 2),
                    'text': seg_text.strip()
                })
                if progress_callback and info and getattr(info, 'duration', None):
                    pct = min(0.05 + (seg_end / info.duration) * 0.8, 0.95)
                    progress_callback(pct, f"Transcribing... {round(seg_end,1)}s")

            full_text = " ".join(s['text'] for s in segments_out)
            duration = segments_out[-1]['end'] if segments_out else getattr(info, 'duration', 0)

            result = {
                'text': full_text,
                'segments': segments_out,
                'language': getattr(info, 'language', 'unknown') if info else (language or 'unknown'),
                'duration': float(duration),
                'processing_time': None,
                'model_size': self.model_name,
                'timestamp': None
            }

            return result

        except Exception as e:
            raise RuntimeError(f"Local transcription failed: {e}")

    def save_transcript(self, transcription, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)
