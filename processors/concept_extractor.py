"""
Concept Extractor - Extract key concepts and generate simple explanations
"""
import re
from collections import Counter
from typing import List, Dict, Any


class ConceptExtractor:
    """Extract and rank concepts with simple explanations"""

    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'what', 'which', 'who', 'that',
            'this', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'we', 'us',
            'you', 'your', 'i', 'me', 'my', 'as', 'if', 'about', 'just', 'like'
        }

    def extract_keyphrases(self, text: str, num_phrases: int = 15) -> List[str]:
        """Extract top keyphrases using frequency and TF-IDF-like scoring"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)

        # Extract potential phrases (2-4 word chunks)
        phrases = []
        for sentence in sentences:
            words = [w.lower() for w in re.findall(r'\b[a-z]+\b', sentence)]
            # Remove stop words
            words = [w for w in words if w not in self.stop_words and len(w) > 2]

            # Extract 2-4 word phrases
            for i in range(len(words)):
                for window in [2, 3, 4]:
                    if i + window <= len(words):
                        phrase = ' '.join(words[i:i+window])
                        if len(phrase.split()) >= 2:
                            phrases.append(phrase)

        # Count and rank
        phrase_counts = Counter(phrases)
        top_phrases = [p for p, _ in phrase_counts.most_common(num_phrases)]

        return top_phrases

    def extract_key_sentences(self, text: str, num_sentences: int = 5) -> List[str]:
        """Extract key sentences by TF-IDF scoring"""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

        if not sentences:
            return []

        # Simple TF-IDF: score sentences by word overlap with top keywords
        keywords = self.extract_keyphrases(text, num_phrases=20)
        keyword_set = set(keywords)

        scores = []
        for sent in sentences:
            words = set(w.lower() for w in re.findall(r'\b\w+\b', sent))
            overlap = len(words & keyword_set)
            scores.append((sent, overlap))

        # Sort by score and return top
        top_sents = sorted(scores, key=lambda x: x[1], reverse=True)[:num_sentences]
        return [s[0] for s in top_sents]

    def generate_simple_definition(self, concept: str, context: str) -> str:
        """Generate a simple 1-2 sentence definition from context"""
        # Extract sentences mentioning the concept
        sentences = [s.strip() for s in re.split(r'[.!?]+', context) if s.strip()]
        concept_lower = concept.lower()

        relevant_sents = [s for s in sentences if concept_lower in s.lower()]

        if not relevant_sents:
            return f"A key concept in the lecture: {concept}"

        # Return the first sentence mentioning it, or a condensed version
        first_sent = relevant_sents[0]
        if len(first_sent) > 150:
            # Truncate at a word boundary
            truncated = first_sent[:150]
            last_space = truncated.rfind(' ')
            return truncated[:last_space] + "..."
        else:
            return first_sent

    def extract_concepts(self, text: str, num_concepts: int = 10) -> List[Dict[str, str]]:
        """Extract key concepts with simple explanations"""
        phrases = self.extract_keyphrases(text, num_phrases=num_concepts)

        concepts = []
        for phrase in phrases:
            definition = self.generate_simple_definition(phrase, text)
            concepts.append({
                'term': phrase,
                'definition': definition,
                'type': self._infer_concept_type(phrase)
            })

        return concepts

    def _infer_concept_type(self, phrase: str) -> str:
        """Infer concept type (noun, process, property, etc.)"""
        # Simple heuristic
        if 'process' in phrase.lower() or 'method' in phrase.lower():
            return 'process'
        elif 'property' in phrase.lower() or 'characteristic' in phrase.lower():
            return 'property'
        elif any(word in phrase.lower() for word in ['definition', 'concept', 'theory']):
            return 'concept'
        else:
            return 'term'

    def group_concepts_by_theme(self, concepts: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """Group concepts by inferred theme or category"""
        grouped = {}
        for concept in concepts:
            concept_type = concept.get('type', 'term')
            if concept_type not in grouped:
                grouped[concept_type] = []
            grouped[concept_type].append(concept)

        return grouped
