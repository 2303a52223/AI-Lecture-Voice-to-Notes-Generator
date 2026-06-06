#!/usr/bin/env python3
"""
Regenerate study notes for Milestone2 lecture with extracted text
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from processors.summarizer import Summarizer
from utils.file_handler import FileHandler

# Load lecture from database
db_path = Path("data/database.json")
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Find Milestone2 lecture
lecture = None
for l in db.get('lectures', []):
    if 'Milestone2' in l.get('title', ''):
        lecture = l
        break

if not lecture:
    print("✗ Milestone2 lecture not found")
    sys.exit(1)

transcript_text = lecture.get('transcript_text', '')
if not transcript_text:
    print("✗ No transcript text found")
    sys.exit(1)

print(f"Generating study notes for: {lecture['title']}")
print(f"Transcript length: {len(transcript_text)} characters")

# Generate study notes
print("\nGenerating study notes...")
try:
    summarizer = Summarizer()
    study_notes = summarizer.generate_study_notes(
        transcript_text,
        title=lecture.get('title', 'Lecture')
    )
    
    print(f"✓ Generated {len(study_notes)} characters of study notes")
    
    # Save to file
    summary_path = Path("data/summaries") / f"{lecture['title']}_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(study_notes)
    
    print(f"✓ Saved to {summary_path}")
    
    # Update database
    lecture['summary_path'] = str(summary_path)
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)
    
    print(f"✓ Database updated")
    print(f"\nPreview of study notes:")
    print(study_notes[:500])
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
