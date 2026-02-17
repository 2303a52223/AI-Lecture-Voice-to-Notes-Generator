"""
Quiz Page - Auto-generated quizzes from lecture content
"""
import streamlit as st
from pathlib import Path
from utils.state_manager import StateManager
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

# Main content
st.title("❓ Quiz Generator")
st.markdown("Test your understanding with auto-generated quiz questions.")

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
if st.button("🎯 Generate Quiz", type="primary", use_container_width=True):
    with st.spinner("Generating quiz questions..."):
        try:
            from processors.quiz_generator import QuizGenerator
            
            generator = QuizGenerator()
            questions = generator.generate_quiz(
                transcript_text,
                num_questions=num_questions,
                difficulty=difficulty
            )
            
            st.session_state.quiz_questions = questions
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            
            st.success(f"✅ Generated {len(questions)} questions!")
            
        except Exception as e:
            st.error(f"Error generating quiz: {e}")

# Display Quiz
if st.session_state.quiz_questions:
    questions = st.session_state.quiz_questions
    
    st.subheader(f"📝 Quiz ({len(questions)} Questions)")
    
    if not st.session_state.quiz_submitted:
        # Display questions
        for i, question in enumerate(questions):
            st.markdown(f"---")
            q_type = question.get('type', 'multiple_choice')
            q_text = question.get('question', '')
            
            st.markdown(f"**Q{i+1}.** {q_text}")
            
            if q_type == 'multiple_choice':
                options = question.get('options', [])
                if options:
                    answer = st.radio(
                        f"Select your answer",
                        options=options,
                        index=None,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
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
                answer = st.text_input(
                    "Your answer",
                    key=f"q_{i}",
                    placeholder="Type your answer..."
                )
                st.session_state.quiz_answers[i] = answer
        
        st.divider()
        
        # Submit button
        if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
            st.session_state.quiz_submitted = True
            st.rerun()
    
    else:
        # Show results
        correct = 0
        total = len(questions)
        
        for i, question in enumerate(questions):
            st.markdown(f"---")
            q_text = question.get('question', '')
            correct_answer = question.get('answer', '')
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
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.rerun()
        
        if st.button("🎯 New Quiz", use_container_width=True):
            st.session_state.quiz_questions = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
