"""
State Manager - Handles application state and session management
"""
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

class StateManager:
    """Manages application state across sessions"""
    
    def __init__(self):
        self.db_path = Path("data/database.json")
        self.ensure_database()
        
    def ensure_database(self):
        """Ensure database file exists"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            initial_data = {
                "lectures": [],
                "settings": {
                    "whisper_model": "base",
                    "summary_length": "medium",
                    "quiz_difficulty": "medium",
                    "language": "en"
                },
                "analytics": {
                    "total_lectures": 0,
                    "total_duration": 0,
                    "total_quizzes": 0
                }
            }
            self.save_database(initial_data)
    
    def load_database(self):
        """Load database from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading database: {e}")
            return None
    
    def save_database(self, data):
        """Save database to JSON file"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Error saving database: {e}")
            return False
    
    def add_lecture(self, lecture_data):
        """Add a new lecture to database. Returns lecture ID or None."""
        db = self.load_database()
        if db is None:
            return None
        
        lecture_data['id'] = len(db['lectures']) + 1
        lecture_data['created_at'] = datetime.now().isoformat()
        db['lectures'].append(lecture_data)
        
        # Update analytics
        db['analytics']['total_lectures'] += 1
        if 'duration' in lecture_data:
            db['analytics']['total_duration'] += lecture_data['duration']
        
        if self.save_database(db):
            return lecture_data['id']
        return None
    
    def get_lecture(self, lecture_id):
        """Get a specific lecture by ID"""
        db = self.load_database()
        if db is None:
            return None
        
        for lecture in db['lectures']:
            if lecture['id'] == lecture_id:
                return lecture
        return None
    
    def get_all_lectures(self):
        """Get all lectures"""
        db = self.load_database()
        if db is None:
            return []
        return db['lectures']
    
    def update_lecture(self, lecture_id, updates):
        """Update lecture data"""
        db = self.load_database()
        if db is None:
            return False
        
        for i, lecture in enumerate(db['lectures']):
            if lecture['id'] == lecture_id:
                db['lectures'][i].update(updates)
                return self.save_database(db)
        return False
    
    def delete_lecture(self, lecture_id):
        """Delete a lecture"""
        db = self.load_database()
        if db is None:
            return False
        
        db['lectures'] = [l for l in db['lectures'] if l['id'] != lecture_id]
        return self.save_database(db)
    
    def get_settings(self):
        """Get application settings"""
        db = self.load_database()
        if db is None:
            return {}
        return db.get('settings', {})
    
    def update_settings(self, settings):
        """Update application settings"""
        db = self.load_database()
        if db is None:
            return False
        
        db['settings'].update(settings)
        return self.save_database(db)
    
    def get_analytics(self):
        """Get analytics data"""
        db = self.load_database()
        if db is None:
            return {}
        return db.get('analytics', {})
    
    def update_analytics(self, key, value):
        """Update specific analytics value"""
        db = self.load_database()
        if db is None:
            return False
        
        db['analytics'][key] = value
        return self.save_database(db)
    
    def increment_quiz_count(self):
        """Increment quiz count in analytics"""
        db = self.load_database()
        if db is None:
            return False
        
        db['analytics']['total_quizzes'] = db['analytics'].get('total_quizzes', 0) + 1
        return self.save_database(db)
    
    def add_quiz_result(self, quiz_result):
        """Add a quiz result to database"""
        db = self.load_database()
        if db is None:
            return False
        
        if 'quiz_results' not in db:
            db['quiz_results'] = []
        
        quiz_result['taken_at'] = datetime.now().isoformat()
        db['quiz_results'].append(quiz_result)
        
        # Update analytics
        db['analytics']['total_quizzes'] = db['analytics'].get('total_quizzes', 0) + 1
        
        return self.save_database(db)
    
    def clear_all(self):
        """Clear all data from database"""
        initial_data = {
            "lectures": [],
            "settings": {
                "whisper_model": "base",
                "summary_length": "medium",
                "quiz_difficulty": "medium",
                "language": "en"
            },
            "analytics": {
                "total_lectures": 0,
                "total_duration": 0,
                "total_quizzes": 0
            },
            "quiz_results": []
        }
        return self.save_database(initial_data)

# Initialize session state variables
def init_session_state():
    """Initialize Streamlit session state"""
    if 'current_lecture_id' not in st.session_state:
        st.session_state.current_lecture_id = None
    
    if 'current_audio_file' not in st.session_state:
        st.session_state.current_audio_file = None
    
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    if 'state_manager' not in st.session_state:
        st.session_state.state_manager = StateManager()

def get_state_manager():
    """Get the state manager instance"""
    if 'state_manager' not in st.session_state:
        st.session_state.state_manager = StateManager()
    return st.session_state.state_manager
