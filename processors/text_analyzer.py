"""
Text Analyzer - Analyze lecture transcripts for insights
"""
import streamlit as st
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import textstat  # type: ignore[import-unresolved]

class TextAnalyzer:
    """Analyzes text for various metrics and insights"""
    
    def __init__(self):
        """Initialize text analyzer"""
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            with st.spinner("Downloading language models..."):
                nltk.download('punkt_tab', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    
    def analyze(self, text):
        """
        Complete analysis of text
        
        Returns:
            dict with various analysis metrics
        """
        try:
            analysis = {
                "basic_stats": self.get_basic_stats(text),
                "readability": self.get_readability_scores(text),
                "word_frequency": self.get_word_frequency(text, top_n=20),
                "keywords": self.extract_keywords(text, num_keywords=15),
                "sentiment": self.analyze_sentiment(text),
                "topics": self.extract_topics(text),
                "complexity": self.analyze_complexity(text)
            }
            
            return analysis
            
        except Exception as e:
            st.error(f"Error during analysis: {e}")
            return None
    
    def get_basic_stats(self, text):
        """Get basic text statistics"""
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            # Count unique words
            unique_words = set(w.lower() for w in words if w.isalnum())
            
            # Average sentence length
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            
            # Average word length
            word_lengths = [len(w) for w in words if w.isalnum()]
            avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
            
            # Paragraphs
            paragraphs = [p for p in text.split('\n\n') if p.strip()]
            
            stats = {
                "total_words": len(words),
                "unique_words": len(unique_words),
                "total_sentences": len(sentences),
                "total_paragraphs": len(paragraphs),
                "avg_sentence_length": round(avg_sentence_length, 1),
                "avg_word_length": round(avg_word_length, 1),
                "lexical_diversity": round(len(unique_words) / len(words) * 100, 1) if words else 0
            }
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_readability_scores(self, text):
        """Calculate readability scores"""
        try:
            scores = {
                "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 1),  # type: ignore[attr-defined]
                "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 1),  # type: ignore[attr-defined]
                "gunning_fog": round(textstat.gunning_fog(text), 1),  # type: ignore[attr-defined]
                "automated_readability": round(textstat.automated_readability_index(text), 1),  # type: ignore[attr-defined]
                "coleman_liau": round(textstat.coleman_liau_index(text), 1),  # type: ignore[attr-defined]
            }
            
            # Interpret Flesch Reading Ease
            fre = scores["flesch_reading_ease"]
            if fre >= 90:
                interpretation = "Very Easy (5th grade)"
            elif fre >= 80:
                interpretation = "Easy (6th grade)"
            elif fre >= 70:
                interpretation = "Fairly Easy (7th grade)"
            elif fre >= 60:
                interpretation = "Standard (8th-9th grade)"
            elif fre >= 50:
                interpretation = "Fairly Difficult (10th-12th grade)"
            elif fre >= 30:
                interpretation = "Difficult (College)"
            else:
                interpretation = "Very Difficult (College Graduate)"
            
            scores["interpretation"] = interpretation
            
            return scores
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_word_frequency(self, text, top_n=20):
        """Get most frequent words"""
        try:
            from nltk.corpus import stopwords
            
            # Get stopwords
            try:
                stop_words = set(stopwords.words('english'))
            except:
                nltk.download('stopwords', quiet=True)
                stop_words = set(stopwords.words('english'))
            
            # Tokenize and filter
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalnum() and len(w) > 3 and w not in stop_words]
            
            # Count frequencies
            word_freq = Counter(words)
            top_words = word_freq.most_common(top_n)
            
            return [{"word": word, "count": count} for word, count in top_words]
            
        except Exception as e:
            return []
    
    def extract_keywords(self, text, num_keywords=15):
        """Extract keywords using TF-IDF-like approach"""
        try:
            from nltk.corpus import stopwords
            from collections import defaultdict
            
            # Get stopwords
            try:
                stop_words = set(stopwords.words('english'))
            except:
                nltk.download('stopwords', quiet=True)
                stop_words = set(stopwords.words('english'))
            
            # Tokenize
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalnum() and len(w) > 3 and w not in stop_words]
            
            # POS tagging to prefer nouns and adjectives
            try:
                pos_tags = nltk.pos_tag(words)
                # Keep only nouns (NN*) and adjectives (JJ*)
                filtered_words = [word for word, pos in pos_tags 
                                if pos.startswith('NN') or pos.startswith('JJ')]
            except:
                filtered_words = words
            
            # Count and get top keywords
            word_freq = Counter(filtered_words)
            keywords = [word for word, count in word_freq.most_common(num_keywords)]
            
            return keywords
            
        except Exception as e:
            return []
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        try:
            # Simple positive/negative word counts
            positive_words = set([
                'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                'positive', 'better', 'best', 'success', 'successful', 'improve',
                'benefit', 'advantage', 'effective', 'efficient', 'important'
            ])
            
            negative_words = set([
                'bad', 'poor', 'terrible', 'awful', 'negative', 'worse', 'worst',
                'fail', 'failure', 'problem', 'issue', 'difficult', 'challenge',
                'disadvantage', 'ineffective', 'wrong', 'error'
            ])
            
            words = word_tokenize(text.lower())
            
            pos_count = sum(1 for w in words if w in positive_words)
            neg_count = sum(1 for w in words if w in negative_words)
            
            total = pos_count + neg_count
            if total == 0:
                sentiment = "Neutral"
                score = 0
            else:
                score = (pos_count - neg_count) / total
                if score > 0.2:
                    sentiment = "Positive"
                elif score < -0.2:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"
            
            return {
                "sentiment": sentiment,
                "score": round(score, 2),
                "positive_words": pos_count,
                "negative_words": neg_count
            }
            
        except Exception as e:
            return {"sentiment": "Unknown", "score": 0}
    
    def extract_topics(self, text):
        """Extract main topics"""
        try:
            keywords = self.extract_keywords(text, num_keywords=10)
            
            # Group related keywords (simple approach)
            # In a more advanced version, use clustering or topic modeling
            
            topics = keywords[:8]  # Return top 8 as topics
            
            return topics
            
        except Exception as e:
            return []
    
    def analyze_complexity(self, text):
        """Analyze text complexity"""
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            # Long sentences
            long_sentences = [s for s in sentences if len(word_tokenize(s)) > 25]
            
            # Complex words (3+ syllables)
            complex_words = [w for w in words if textstat.syllable_count(w) >= 3]  # type: ignore[attr-defined]
            
            # Passive voice detection (simple heuristic)
            passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are', 'am']
            passive_count = sum(1 for s in sentences 
                              if any(ind in s.lower() for ind in passive_indicators))
            
            complexity = {
                "long_sentences_count": len(long_sentences),
                "long_sentences_percent": round(len(long_sentences) / len(sentences) * 100, 1) if sentences else 0,
                "complex_words_count": len(complex_words),
                "complex_words_percent": round(len(complex_words) / len(words) * 100, 1) if words else 0,
                "passive_voice_count": passive_count,
                "passive_voice_percent": round(passive_count / len(sentences) * 100, 1) if sentences else 0
            }
            
            return complexity
            
        except Exception as e:
            return {}
    
    def compare_transcripts(self, text1, text2):
        """Compare two transcripts"""
        try:
            analysis1 = self.analyze(text1)
            analysis2 = self.analyze(text2)
            
            if analysis1 is None or analysis2 is None:
                return None
            
            comparison = {
                "transcript1": analysis1,
                "transcript2": analysis2,
                "differences": {
                    "word_count_diff": analysis1["basic_stats"]["total_words"] - analysis2["basic_stats"]["total_words"],
                    "readability_diff": analysis1["readability"]["flesch_reading_ease"] - analysis2["readability"]["flesch_reading_ease"]
                }
            }
            
            return comparison
            
        except Exception as e:
            return None
