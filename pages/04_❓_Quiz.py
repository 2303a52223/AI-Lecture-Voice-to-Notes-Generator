"""
Quiz Page - Auto-generated quizzes from lecture content
"""
import streamlit as st
from pathlib import Path
import time
from utils.state_manager import StateManager
from utils.progress_tracker import ProgressTracker
from components.sidebar import render_sidebar
from components.cards import quiz_question_card, result_card

# Page config
st.set_page_config(
    page_title="Quiz - Lecture Notes Generator",
    page_icon="❓",
    layout="wide"
)

# Load custom CSS
css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize
state_manager = StateManager()

# Sidebar
render_sidebar()

# Main content - Hero
st.markdown(
    """
    <section class='page-hero'>
        <div class='page-hero-badge'>❓ Quiz</div>
        <h1>Test Your Knowledge</h1>
        <p class='page-hero-copy'>Auto-generated quiz questions to reinforce learning and assess understanding of lecture content.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Get lectures
lectures = state_manager.get_all_lectures()

if not lectures:
    st.info("📤 No lectures found. Upload a lecture first!")
    st.page_link("pages/01_📤_Upload.py", label="Go to Upload", icon="📤")
    st.stop()

# Lecture selector
lecture_titles = [l.get('title', f"Lecture {l.get('id', '?')}") for l in lectures]
selected_idx = st.selectbox(
    "Select Lecture",
    range(len(lectures)),
    format_func=lambda x: lecture_titles[x]
)

lecture = lectures[selected_idx]
transcript_text = lecture.get('transcript_text', '')

if not transcript_text:
    st.warning("No transcript text available for quiz generation.")
    st.stop()

st.divider()

# Quiz options
col1, col2, col3 = st.columns(3)

with col1:
    num_questions = st.slider("Number of Questions", 3, 15, 5)

with col2:
    difficulty = st.selectbox(
        "Difficulty",
        options=['easy', 'medium', 'hard'],
        index=1
    )

with col3:
    question_types = st.multiselect(
        "Question Types",
        options=['multiple_choice', 'true_false', 'fill_blank'],
        default=['multiple_choice', 'true_false']
    )

if not question_types:
    question_types = ['multiple_choice']

# Initialize quiz state
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

st.divider()

# Generate Quiz
if st.button("🎯 Generate Quiz", type="primary", width="stretch"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.write("📍 Initializing quiz generator...")
        progress_bar.progress(10)
        
        from processors.quiz_generator import QuizGenerator
        
        generator = QuizGenerator()
        
        status_text.write(f"📍 Generating {num_questions} {difficulty} level questions...")
        start_time = time.time()
        progress_bar.progress(20)
        
        questions = generator.generate_quiz(
            transcript_text,
            num_questions=num_questions,
            difficulty=difficulty,
            question_types=question_types
        )
        progress_bar.progress(85)
        
        st.session_state.quiz_questions = questions
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        
        elapsed = ProgressTracker.get_elapsed_time(start_time)
        progress_bar.progress(100)
        status_text.write(f"✅ Generated {len(questions)} questions in {elapsed}!")
        
        st.success(f"✅ Generated {len(questions)} questions!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error generating quiz: {e}")

# Display Quiz
if st.session_state.quiz_questions:
    questions = st.session_state.quiz_questions
    
    st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
    st.subheader(f"📝 Quiz ({len(questions)} Questions)")
    
    if not st.session_state.quiz_submitted:
        # Display questions
        for i, question in enumerate(questions):
            st.markdown(f"---")
            q_type = question.get('type', 'multiple_choice')
            q_text = question.get('question', '')
            
            st.markdown(f"**Q{i+1}.** {q_text}")
            
            if q_type == 'multiple_choice':
                options = question.get('options', {})
                if options:
                    # Handle both dict and list formats
                    if isinstance(options, dict):
                        # Dict format: {"A": "answer1", "B": "answer2", ...}
                        option_list = [f"{k}. {v}" for k, v in sorted(options.items())]
                        option_keys = sorted(options.keys())
                    else:
                        # List format: ["answer1", "answer2", ...]
                        option_list = options
                        option_keys = list(range(len(options)))
                    
                    answer = st.radio(
                        f"Select your answer",
                        options=option_list,
                        index=None,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    if answer:
                        # Extract the key from the answer string
                        if isinstance(options, dict):
                            key = answer.split(".")[0]
                            st.session_state.quiz_answers[i] = key
                        else:
                            st.session_state.quiz_answers[i] = answer
                    
            elif q_type == 'true_false':
                answer = st.radio(
                    f"Select your answer",
                    options=['True', 'False'],
                    index=None,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                st.session_state.quiz_answers[i] = answer
                
            elif q_type == 'fill_blank':
                options = question.get('options', {})
                if isinstance(options, dict):
                    option_list = list(options.values())
                else:
                    option_list = options if isinstance(options, list) else []
                
                if option_list:
                    answer = st.selectbox(
                        f"Select the word that fits",
                        options=option_list,
                        index=None,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[i] = answer
                else:
                    answer = st.text_input(
                        "Your answer",
                        key=f"q_{i}",
                        placeholder="Type your answer..."
                    )
                    st.session_state.quiz_answers[i] = answer
        
        st.divider()
        
        # Submit button
        if st.button("✅ Submit Quiz", type="primary", width="stretch"):
            st.session_state.quiz_submitted = True
            st.rerun()
    
    else:
        # Show results
        correct = 0
        total = len(questions)
        
        for i, question in enumerate(questions):
            st.markdown(f"---")
            q_text = question.get('question', '')
            correct_answer = question.get('correct_answer', question.get('answer', ''))
            user_answer = st.session_state.quiz_answers.get(i, '')
            explanation = question.get('explanation', '')
            
            # Check answer
            is_correct = False
            if isinstance(correct_answer, str) and isinstance(user_answer, str):
                is_correct = correct_answer.lower().strip() == user_answer.lower().strip()
            
            if is_correct:
                correct += 1
                st.markdown(f"**Q{i+1}.** {q_text}")
                st.success(f"✅ Your answer: {user_answer}")
            else:
                st.markdown(f"**Q{i+1}.** {q_text}")
                st.error(f"❌ Your answer: {user_answer}")
                st.info(f"Correct answer: {correct_answer}")
            
            if explanation:
                with st.expander("💡 Explanation"):
                    st.markdown(explanation)
        
        # Score summary
        st.divider()
        
        score_pct = round(correct / total * 100, 1) if total > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{score_pct}%")
        with col2:
            st.metric("Correct", f"{correct}/{total}")
        with col3:
            grade = "A" if score_pct >= 90 else "B" if score_pct >= 80 else "C" if score_pct >= 70 else "D" if score_pct >= 60 else "F"
            st.metric("Grade", grade)
        
        # Results chart
        try:
            from components.charts import render_quiz_results_chart
            render_quiz_results_chart({'correct': correct, 'total': total})
        except:
            pass
        
        # Save results
        try:
            quiz_result = {
                'lecture_id': lecture.get('id'),
                'score': score_pct,
                'correct': correct,
                'total': total,
                'difficulty': difficulty
            }
            state_manager.add_quiz_result(quiz_result)
        except:
            pass
        
        # Retry button
        if st.button("🔄 Try Again", width="stretch"):
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.rerun()
        
        if st.button("🎯 New Quiz", width="stretch"):
            st.session_state.quiz_questions = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Flashcards section
st.divider()
st.markdown("<div class='pack-card'>", unsafe_allow_html=True)
st.subheader("🎴 Flashcards & Study Tools")

# Initialize session state for flashcards
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = None
if 'anki_package_bytes' not in st.session_state:
    st.session_state.anki_package_bytes = None
if 'flashcards_csv' not in st.session_state:
    st.session_state.flashcards_csv = None

col1, col2 = st.columns(2)

with col1:
    num_flashcards = st.slider("Number of flashcards", 5, 50, 15)

with col2:
    if st.button("📇 Generate Flashcards", type="primary", width="stretch"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.write("📍 Initializing flashcard generator...")
            progress_bar.progress(10)
            
            from processors.quiz_generator import QuizGenerator
            
            generator = QuizGenerator()
            
            status_text.write(f"📍 Generating {num_flashcards} flashcards...")
            start_time = time.time()
            progress_bar.progress(20)
            
            flashcards = generator.generate_flashcards(transcript_text, num_flashcards)
            progress_bar.progress(90)
            
            st.session_state.flashcards = flashcards
            st.session_state.anki_package_bytes = None
            st.session_state.flashcards_csv = None
            
            elapsed = ProgressTracker.get_elapsed_time(start_time)
            progress_bar.progress(100)
            status_text.write(f"✅ Generated {len(flashcards)} flashcards in {elapsed}!")
            
            st.success(f"✅ Generated {len(flashcards)} flashcards!")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error generating flashcards: {e}")

# Display and export flashcards
if st.session_state.flashcards:
    flashcards = st.session_state.flashcards
    
    st.markdown(f"**{len(flashcards)} Flashcards** | Topics: {', '.join(set(c.get('topic', 'Other') for c in flashcards[:3]))}...")
    
    # Preview flashcards
    with st.expander(f"Preview ({len(flashcards)} cards)"):
        for i, card in enumerate(flashcards[:5]):
            st.markdown(f"**Card {i+1}**")
            st.markdown(f"**Q**: {card.get('front', '')}")
            st.markdown(f"**A**: {card.get('back', '')}")
            st.divider()
    
    # Export options
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        if st.button("📲 Prepare Anki (.apkg)", width="stretch"):
            with st.spinner("Creating Anki deck..."):
                try:
                    from utils.file_handler import FileHandler
                    file_handler = FileHandler()
                    apkg_bytes = file_handler.export_flashcards_anki(
                        flashcards,
                        deck_name=f"{lecture.get('title', 'Lecture')} - Flashcards"
                    )
                    if apkg_bytes:
                        st.session_state.anki_package_bytes = apkg_bytes
                    else:
                        st.error("Failed to create Anki deck. Is genanki installed?")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.anki_package_bytes:
            st.download_button(
                "⬇️ Download Anki Deck",
                data=st.session_state.anki_package_bytes,
                file_name=f"{lecture.get('title', 'flashcards')}.apkg",
                mime="application/octet-stream",
                width="stretch",
                key="download_anki_deck"
            )
    
    with export_col2:
        if st.button("📋 Prepare CSV", width="stretch"):
            try:
                from utils.file_handler import FileHandler
                file_handler = FileHandler()
                csv_content = file_handler.export_flashcards_csv(flashcards)
                st.session_state.flashcards_csv = csv_content
            except Exception as e:
                st.error(f"Error: {e}")

        if st.session_state.flashcards_csv:
            st.download_button(
                "⬇️ Download CSV",
                data=st.session_state.flashcards_csv,
                file_name=f"{lecture.get('title', 'flashcards')}.csv",
                mime="text/csv",
                width="stretch",
                key="download_flashcards_csv"
            )
    
    with export_col3:
        if st.button("🔄 Generate New", width="stretch"):
            st.session_state.flashcards = None
            st.session_state.anki_package_bytes = None
            st.session_state.flashcards_csv = None
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
