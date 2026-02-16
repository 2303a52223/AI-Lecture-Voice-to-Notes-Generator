"""
Summarizer Module - Text summarization using transformer models
"""
import nltk
import re
from pathlib import Path

class Summarizer:
    """Handles text summarization using BART or fallback extractive methods"""
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize summarizer
        
        Args:
            model_name: HuggingFace model name for summarization
        """
        self.model_name = model_name
        self.summarizer = None
        self.use_transformers = True
        
        # Ensure NLTK data available
        self._ensure_nltk_data()
    
    def _ensure_nltk_data(self):
        """Download required NLTK data if not available"""
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    
    def load_model(self):
        """Load the summarization model"""
        try:
            from transformers import pipeline  # type: ignore[import-unresolved]
            self.summarizer = pipeline("summarization", model=self.model_name)
            self.use_transformers = True
            return True
        except ImportError:
            self.use_transformers = False
            return False
        except Exception as e:
            self.use_transformers = False
            return False
    
    def summarize(self, text, max_length=150, min_length=50, style="concise"):
        """
        Generate summary of text
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            style: Summary style (concise, detailed, bullet_points)
            
        Returns:
            dict: Summary result with text and metadata
        """
        if not text or len(text.strip()) < 50:
            return {
                'summary': text,
                'method': 'none',
                'original_length': len(text) if text else 0,
                'summary_length': len(text) if text else 0
            }
        
        # Adjust lengths based on style
        if style == "detailed":
            max_length = max(max_length, 300)
            min_length = max(min_length, 100)
        elif style == "bullet_points":
            summary_result = self._generate_bullet_points(text)
            return summary_result
        
        # Try transformer-based summarization
        if self.use_transformers:
            try:
                if self.summarizer is None:
                    self.load_model()
                
                if self.summarizer is not None:
                    return self._transformer_summarize(text, max_length, min_length)
            except Exception:
                pass
        
        # Fallback to extractive summarization
        return self._extractive_summarize(text, max_length)
    
    def _transformer_summarize(self, text, max_length, min_length):
        """Summarize using transformer model"""
        # Split text into chunks if too long (BART has 1024 token limit)
        max_chunk_length = 1024
        chunks = self._split_text(text, max_chunk_length)
        
        summaries = []
        assert self.summarizer is not None
        for chunk in chunks:
            if len(chunk.split()) < 30:
                summaries.append(chunk)
                continue
            
            try:
                result = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                summaries.append(result[0]['summary_text'])
            except Exception:
                summaries.append(chunk[:max_length * 5])
        
        combined_summary = ' '.join(summaries)
        
        # If combined summary is still too long, summarize again
        if len(combined_summary.split()) > max_length and self.summarizer:
            try:
                result = self.summarizer(
                    combined_summary,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                combined_summary = result[0]['summary_text']
            except:
                pass
        
        return {
            'summary': combined_summary,
            'method': 'transformer',
            'model': self.model_name,
            'original_length': len(text),
            'summary_length': len(combined_summary)
        }
    
    def _extractive_summarize(self, text, max_length=150):
        """Fallback extractive summarization using sentence scoring"""
        from nltk.corpus import stopwords
        from nltk.tokenize import sent_tokenize, word_tokenize
        
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 3:
            return {
                'summary': text,
                'method': 'extractive',
                'original_length': len(text),
                'summary_length': len(text)
            }
        
        # Calculate word frequencies
        stop_words = set(stopwords.words('english'))
        word_frequencies = {}
        
        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1
        
        # Normalize frequencies
        if word_frequencies:
            max_freq = max(word_frequencies.values())
            word_frequencies = {
                word: freq / max_freq
                for word, freq in word_frequencies.items()
            }
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            score = sum(word_frequencies.get(word, 0) for word in words if word.isalnum())
            
            # Position bonus (first and last sentences are usually important)
            if i == 0:
                score *= 1.5
            elif i == len(sentences) - 1:
                score *= 1.2
            
            # Length penalty (too short or too long)
            word_count = len(words)
            if 10 <= word_count <= 30:
                score *= 1.2
            elif word_count < 5:
                score *= 0.5
            
            sentence_scores[i] = score
        
        # Select top sentences
        num_sentences = max(3, len(sentences) // 4)
        top_indices = sorted(
            sentence_scores.keys(),
            key=lambda x: sentence_scores[x],
            reverse=True
        )[:num_sentences]
        
        # Maintain original order
        top_indices.sort()
        summary = ' '.join(sentences[i] for i in top_indices)
        
        return {
            'summary': summary,
            'method': 'extractive',
            'original_length': len(text),
            'summary_length': len(summary)
        }
    
    def _generate_bullet_points(self, text):
        """Generate bullet point summary"""
        from nltk.tokenize import sent_tokenize
        
        sentences = sent_tokenize(text)
        
        # Extract key sentences
        extractive_result = self._extractive_summarize(text, max_length=300)
        key_sentences = sent_tokenize(extractive_result['summary'])
        
        # Format as bullet points
        bullet_points = []
        for sentence in key_sentences:
            # Clean up sentence
            sentence = sentence.strip()
            if sentence:
                bullet_points.append(f"• {sentence}")
        
        summary = '\n'.join(bullet_points)
        
        return {
            'summary': summary,
            'method': 'bullet_points',
            'original_length': len(text),
            'summary_length': len(summary),
            'num_points': len(bullet_points)
        }
    
    def generate_key_topics(self, text, num_topics=5):
        """
        Extract key topics from text
        
        Args:
            text: Input text
            num_topics: Number of topics to extract
            
        Returns:
            list: Key topics
        """
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        
        stop_words = set(stopwords.words('english'))
        
        # Tokenize and filter
        words = word_tokenize(text.lower())
        filtered_words = [
            word for word in words
            if word.isalnum() and word not in stop_words and len(word) > 3
        ]
        
        # Count word frequencies
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top words as topics
        topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:num_topics]
        
        return [topic[0].title() for topic in topics]
    
    def generate_study_notes(self, text, title="Lecture"):
        """
        Generate structured study notes
        
        Args:
            text: Input text
            title: Lecture title
            
        Returns:
            str: Formatted study notes in Markdown
        """
        # Generate summary
        summary_result = self.summarize(text, style="concise")
        
        # Generate bullet points
        bullets_result = self._generate_bullet_points(text)
        
        # Generate key topics
        topics = self.generate_key_topics(text)
        
        # Format study notes
        notes = f"""# 📝 Study Notes: {title}

## 📋 Summary
{summary_result['summary']}

## 🔑 Key Topics
{chr(10).join(f'- **{topic}**' for topic in topics)}

## 📌 Key Points
{bullets_result['summary']}

## 📊 Statistics
- Original text length: {summary_result['original_length']} characters
- Summary length: {summary_result['summary_length']} characters
- Compression ratio: {round(summary_result['summary_length'] / max(summary_result['original_length'], 1) * 100, 1)}%
- Method: {summary_result['method']}

---
*Generated automatically from lecture transcript*
"""
        return notes
    
    def _split_text(self, text, max_length=1024):
        """Split text into chunks"""
        from nltk.tokenize import sent_tokenize
        
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length > max_length and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
