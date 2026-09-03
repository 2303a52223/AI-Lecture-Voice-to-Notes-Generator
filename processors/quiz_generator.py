"""
Quiz Generator - Generate quizzes from lecture content
"""
import streamlit as st
import random
import re
from nltk.tokenize import sent_tokenize
import nltk
from utils.retry import retry_call
from utils.error_handler import report_error

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
    
    def generate_quiz(self, text, num_questions=10, difficulty="medium", question_types=None):
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
            
            if question_types is None:
                question_types = ['multiple_choice', 'true_false', 'fill_blank']

            # Generate different types of questions
            questions = []
            
            requested = [qt for qt in question_types if qt in ['multiple_choice', 'true_false', 'fill_blank']]
            if not requested:
                requested = ['multiple_choice']

            # Balanced distribution over selected types.
            base_count = max(1, num_questions // len(requested))
            remaining = num_questions

            if 'multiple_choice' in requested:
                count = min(remaining, base_count)
                mcq_questions = self._generate_mcq(sentences, count, difficulty)
                questions.extend(mcq_questions)
                remaining = max(0, remaining - len(mcq_questions))

            if 'true_false' in requested and remaining > 0:
                count = min(remaining, base_count)
                tf_questions = self._generate_true_false(sentences, count)
                questions.extend(tf_questions)
                remaining = max(0, remaining - len(tf_questions))

            if 'fill_blank' in requested and remaining > 0:
                count = min(remaining, base_count + remaining)
                fib_questions = self._generate_fill_blank(sentences, count)
                questions.extend(fib_questions)
                remaining = max(0, remaining - len(fib_questions))

            # Backfill with MCQ if fewer questions were generated than requested.
            if len(questions) < num_questions:
                backfill = self._generate_mcq(sentences, num_questions - len(questions), difficulty)
                questions.extend(backfill)
            
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
            
            for sentence in candidate_sentences[:num_cards * 3]:
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

                if len(flashcards) >= num_cards:
                    break

            # Fallback if strict term extraction produced too few cards.
            if len(flashcards) < num_cards:
                for sentence in candidate_sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    first_words = " ".join(sentence.split()[:6]).strip('.,!?;:')
                    flashcards.append({
                        "front": f"Explain: {first_words}...",
                        "back": sentence,
                        "topic": "General"
                    })
                    if len(flashcards) >= num_cards:
                        break
            
            st.success(f"✅ Generated {len(flashcards)} flashcards!")
            
            return flashcards[:num_cards]
            
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

    def export_to_anki(self, flashcards, deck_name="Lecture Notes"):
        """
        Export flashcards to Anki format (.apkg)
        
        Args:
            flashcards: List of flashcard dicts with 'front' and 'back'
            deck_name: Name for the Anki deck
            
        Returns:
            bytes: .apkg file content or None if failed
        """
        try:
            import genanki
            import random
            import tempfile
            import os
            
            def _build_and_write():
                # Create deck
                deck = genanki.Deck(random.randint(1e16, 9e16), deck_name)

                # Create model
                model = genanki.Model(
                    random.randint(1e16, 9e16),
                    'Basic',
                    fields=[
                        {'name': 'Front'},
                        {'name': 'Back'}
                    ],
                    templates=[
                        {
                            'name': 'Card 1',
                            'qfmt': '{{Front}}',
                            'afmt': '{{FrontSide}}<hr id=answer>{{Back}}'
                        }
                    ]
                )

                # Add cards
                for card in flashcards:
                    note = genanki.Note(
                        model=model,
                        fields=[card.get('front', ''), card.get('back', '')]
                    )
                    deck.add_notes(note)

                # Package deck
                package = genanki.Package(deck)

                # Create temporary file and export
                with tempfile.NamedTemporaryFile(delete=False, suffix='.apkg') as tmp:
                    tmp_path = tmp.name

                try:
                    retry_call(lambda: package.write_to_file(tmp_path), tries=3, delay=0.5, backoff=2.0)

                    # Read file content
                    with open(tmp_path, 'rb') as f:
                        return f.read()
                finally:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass

            return retry_call(_build_and_write, tries=2, delay=0.5, backoff=2.0)
            
        except ImportError:
            st.error("genanki library not installed. Install with: pip install genanki")
            return None
        except Exception as e:
            report_error(e, "Error exporting to Anki", user_facing=True)
            return None

    def export_flashcards_csv(self, flashcards):
        """
        Export flashcards to CSV format for manual import
        
        Returns:
            str: CSV content
        """
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Front', 'Back', 'Topic', 'Difficulty'])
        
        # Cards
        for card in flashcards:
            writer.writerow([
                card.get('front', ''),
                card.get('back', ''),
                card.get('topic', ''),
                card.get('difficulty', 'medium')
            ])
        
        return output.getvalue()
