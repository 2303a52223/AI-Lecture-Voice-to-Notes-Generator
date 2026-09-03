#!/usr/bin/env python3
"""
Re-process Milestone2 lecture - extract PPTX text and update database
"""
import json
from pathlib import Path
import sys

# Add processors to path
sys.path.insert(0, str(Path(__file__).parent))

from processors.document_extractor import extract_from_pptx

# Find the PPTX file
uploads_dir = Path("data/uploads")
pptx_files = list(uploads_dir.glob("*Milestone2*.pptx"))

if not pptx_files:
    print("✗ No Milestone2 PPTX file found")
    sys.exit(1)

pptx_file = pptx_files[0]
print(f"Processing: {pptx_file.name}")

# Extract text
result = extract_from_pptx(str(pptx_file))

print(f"\n✓ Extraction result:")
print(f"  Text length: {len(result['text'])} characters")
print(f"  Segments: {len(result['segments'])}")
print(f"  Method: {result['metadata'].get('method', 'unknown')}")
print(f"  Error: {result['metadata'].get('error', 'none')}")

# Update database
db_path = Path("data/database.json")
with open(db_path, 'r') as f:
    db = json.load(f)

# Find and update the Milestone2 lecture
for lecture in db.get('lectures', []):
    if 'Milestone2' in lecture.get('title', ''):
        print(f"\nUpdating lecture: {lecture['title']}")
        
        # Update transcript
        transcript_path = Path("data/transcripts") / f"{lecture['title']}_transcript.json"
        transcript_data = {
            "text": result["text"],
            "segments": result["segments"],
            "language": "en",
            "duration": 0,
            "processing_time": 0,
            "model_size": "pptx-extractor",
            "timestamp": None
        }
        
        with open(transcript_path, 'w') as f:
            json.dump(transcript_data, f, indent=2)
        
        # Update database entry
        lecture['transcript_text'] = result['text']
        lecture['transcript_path'] = str(transcript_path)
        
        print(f"  ✓ Updated transcript_text ({len(result['text'])} chars)")
        print(f"  ✓ Saved to {transcript_path}")
        
        break

# Save updated database
with open(db_path, 'w') as f:
    json.dump(db, f, indent=2)

print(f"\n✓ Database updated")
print(f"\nPreview of extracted text:")
print(f"{result['text'][:500]}...")
