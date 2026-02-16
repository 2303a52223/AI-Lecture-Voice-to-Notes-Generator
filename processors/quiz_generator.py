"""
Quiz Generator - Generate quizzes from lecture content
"""
import streamlit as st
import random
import re
from nltk.tokenize import sent_tokenize
import nltk

class QuizGenerator:
    """Generates quizzes and flashcards from text"""
    
    def __init__(self):
        """Initialize quiz generator"""
        # Download NLTK data
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            with st.spinner("Downloading language models..."):
                nltk.download('punkt_tab', quiet=True)
                nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    
    def generate_quiz(self, text, num_questions=10, difficulty="medium"):
        """
        Generate quiz from text
        
        Args:
            text: Input text
            num_questions: Number of questions to generate
            difficulty: "easy", "medium", or "hard"
        
        Returns:
            list of quiz questions
        """
        try:
            st.info(f"🎯 Generating {num_questions} quiz questions...")
            
            # Extract sentences
            sentences = sent_tokenize(text)
            
            if len(sentences) < num_questions:
                st.warning(f"Text too short. Generating {len(sentences)} questions instead.")
                num_questions = len(sentences)
            
            # Generate different types of questions
            questions = []
            
            # Multiple choice questions (60%)
            num_mcq = int(num_questions * 0.6)
            mcq_questions = self._generate_mcq(sentences, num_mcq, difficulty)
            questions.extend(mcq_questions)
            
            # True/False questions (20%)
            num_tf = int(num_questions * 0.2)
            tf_questions = self._generate_true_false(sentences, num_tf)
            questions.extend(tf_questions)
            
            # Fill in the blank questions (20%)
            num_fib = num_questions - len(questions)
            fib_questions = self._generate_fill_blank(sentences, num_fib)
            questions.extend(fib_questions)
            
            # Shuffle questions
            random.shuffle(questions)
            
            st.success(f"✅ Generated {len(questions)} quiz questions!")
            
            return questions[:num_questions]
            
        except Exception as e:
            st.error(f"Error generating quiz: {e}")
            return []
    
    def _generate_mcq(self, sentences, num_questions, difficulty):
        """Generate multiple choice questions"""
        questions = []
        used_sentences = set()
        
        # Select sentences with good content
        candidate_sentences = [s for s in sentences if len(s.split()) >= 8 and len(s.split()) <= 30]
        
        if not candidate_sentences:
            candidate_sentences = sentences
        
        random.shuffle(candidate_sentences)
        
        for sentence in candidate_sentences:
            if len(questions) >= num_questions:
                break
            
            if sentence in used_sentences:
                continue
            
            # Extract key term (simplified approach)
            words = sentence.split()
            
            # Find nouns/important terms (words that are capitalized or longer)
            key_terms = [w.strip('.,!?;:') for w in words 
                        if len(w) > 4 and (w[0].isupper() or len(w) > 8)]
            
            if not key_terms:
                continue
            
            # Select a key term to make the question about
            key_term = random.choice(key_terms)
            
            # Create question by replacing key term
            question_text = sentence.replace(key_term, "______")
            
            # Generate distractors (wrong answers)
            distractors = self._generate_distractors(key_term, difficulty)
            
            # Create options
            options = [key_term] + distractors[:3]
            random.shuffle(options)
            
            correct_answer = chr(65 + options.index(key_term))  # A, B, C, D
            
            questions.append({
                "type": "multiple_choice",
                "question": f"What fits best in the blank?\n\n{question_text}",
                "options": {chr(65 + i): opt for i, opt in enumerate(options)},
                "correct_answer": correct_answer,
                "explanation": f"The correct answer is from the lecture: '{sentence}'"
            })
            
            used_sentences.add(sentence)
        
        return questions
    
    def _generate_true_false(self, sentences, num_questions):
        """Generate true/false questions"""
        questions = []
        candidate_sentences = [s for s in sentences if len(s.split()) >= 6]
        
        if not candidate_sentences:
            return questions
        
        random.shuffle(candidate_sentences)
        
        for i, sentence in enumerate(candidate_sentences[:num_questions * 2]):
            if len(questions) >= num_questions:
                break
            
            # Half true, half false
            if i % 2 == 0:
                # True statement
                questions.append({
                    "type": "true_false",
                    "question": sentence,
                    "correct_answer": "True",
                    "explanation": "This statement is directly from the lecture."
                })
            else:
                # False statement (modify the sentence)
                modified = self._create_false_statement(sentence)
                if modified != sentence:
                    questions.append({
                        "type": "true_false",
                        "question": modified,
                        "correct_answer": "False",
                        "explanation": f"The correct statement is: '{sentence}'"
                    })
        
        return questions
    
    def _generate_fill_blank(self, sentences, num_questions):
        """Generate fill in the blank questions"""
        questions = []
        candidate_sentences = [s for s in sentences if len(s.split()) >= 8]
        
        if not candidate_sentences:
            return questions
        
        random.shuffle(candidate_sentences)
        
        for sentence in candidate_sentences[:num_questions]:
            words = sentence.split()
            
            # Find a good word to blank out
            # Prefer longer words or capitalized words
            key_words = [(i, w) for i, w in enumerate(words) 
                        if len(w) > 4 and not w.lower() in ['which', 'where', 'there', 'these', 'those']]
            
            if not key_words:
                continue
            
            # Select word to remove
            idx, key_word = random.choice(key_words)
            key_word = key_word.strip('.,!?;:')
            
            # Create question
            question_words = words.copy()
            question_words[idx] = "______"
            question_text = " ".join(question_words)
            
            questions.append({
                "type": "fill_blank",
                "question": f"Fill in the blank:\n\n{question_text}",
                "correct_answer": key_word.strip('.,!?;:').lower(),
                "explanation": f"The complete sentence is: '{sentence}'"
            })
        
        return questions
    
    def _generate_distractors(self, correct_answer, difficulty):
        """Generate plausible wrong answers"""
        # Simple distractor generation
        # In a more advanced version, you could use word embeddings
        
        distractors = []
        
        # Similar length words
        if len(correct_answer) > 6:
            distractors.extend([
                correct_answer[:3] + "ology",
                correct_answer[:-2] + "tion",
                correct_answer + "al"
            ])
        
        # Common alternatives based on word patterns
        if correct_answer.istitle():
            distractors.extend(["Alternative", "Different", "Another"])
        
        # Generic distractors
        generic = ["None of the above", "All of the above", "Both A and B", "None"]
        distractors.extend(generic)
        
        return distractors[:4]
    
    def _create_false_statement(self, sentence):
        """Modify a sentence to make it false"""
        # Simple modifications
        modifications = [
            (r'\bnot\b', ''),  # Remove "not"
            (r'\bis\b', 'is not'),  # Add negation
            (r'\bcan\b', 'cannot'),
            (r'\bwill\b', 'will not'),
            (r'\balways\b', 'never'),
            (r'\bnever\b', 'always'),
        ]
        
        for pattern, replacement in modifications:
            modified = re.sub(pattern, replacement, sentence, count=1)
            if modified != sentence:
                return modified
        
        # If no modification worked, try replacing a number
        numbers = re.findall(r'\b\d+\b', sentence)
        if numbers:
            old_num = numbers[0]
            new_num = str(int(old_num) + random.randint(1, 10))
            return sentence.replace(old_num, new_num, 1)
        
        return sentence
    
    def generate_flashcards(self, text, num_cards=15):
        """Generate flashcards from text"""
        try:
            st.info(f"🎴 Generating {num_cards} flashcards...")
            
            sentences = sent_tokenize(text)
            flashcards = []
            
            # Select informative sentences
            candidate_sentences = [s for s in sentences if len(s.split()) >= 8 and len(s.split()) <= 30]
            
            if not candidate_sentences:
                candidate_sentences = sentences
            
            random.shuffle(candidate_sentences)
            
            for sentence in candidate_sentences[:num_cards]:
                # Extract question and answer from sentence
                words = sentence.split()
                
                # Find key terms
                key_terms = [w.strip('.,!?;:') for w in words 
                            if len(w) > 4 and (w[0].isupper() or len(w) > 7)]
                
                if key_terms:
                    key_term = random.choice(key_terms)
                    
                    # Front: question
                    front = f"What is {key_term}?"
                    
                    # Back: answer
                    back = sentence
                    
                    flashcards.append({
                        "front": front,
                        "back": back,
                        "topic": key_term
                    })
            
            st.success(f"✅ Generated {len(flashcards)} flashcards!")
            
            return flashcards
            
        except Exception as e:
            st.error(f"Error generating flashcards: {e}")
            return []
    
    def grade_quiz(self, questions, answers):
        """Grade quiz answers"""
        try:
            correct = 0
            total = len(questions)
            results = []
            
            for i, question in enumerate(questions):
                user_answer = answers.get(i, "")
                correct_answer = question["correct_answer"]
                
                # Check answer based on question type
                if question["type"] == "fill_blank":
                    is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
                else:
                    is_correct = user_answer == correct_answer
                
                if is_correct:
                    correct += 1
                
                results.append({
                    "question_num": i + 1,
                    "correct": is_correct,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": question.get("explanation", "")
                })
            
            score = (correct / total * 100) if total > 0 else 0
            
            return {
                "score": score,
                "correct": correct,
                "total": total,
                "results": results
            }
            
        except Exception as e:
            st.error(f"Error grading quiz: {e}")
            return None
