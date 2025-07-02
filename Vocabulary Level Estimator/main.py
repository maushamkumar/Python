#!/usr/bin/env python3
"""
Vocabulary Level Estimator - CEFR Text Analysis Tool
====================================================

A robust system for analyzing English text and estimating CEFR proficiency levels
from A1 (Beginner) to C2 (Proficient).

Author: Assistant
Date: 2025
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Union
from collections import Counter, defaultdict
from dataclasses import dataclass
import statistics

# External libraries
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    import spacy
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
except ImportError as e:
    print(f"Missing required libraries. Please install: {e}")
    print("Run: pip install nltk spacy transformers torch")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TextAnalysisResult:
    """Data class to store text analysis results."""
    text: str
    estimated_level: str
    confidence_score: float
    word_count: int
    sentence_count: int
    avg_sentence_length: float
    vocabulary_distribution: Dict[str, int]
    level_percentages: Dict[str, float]
    representative_words: Dict[str, List[str]]
    complexity_metrics: Dict[str, float]

class CEFRVocabularyEstimator:
    """
    A comprehensive CEFR vocabulary level estimator using multiple approaches.
    """
    
    def __init__(self, model_name: str = "AnonymousSubmissions/cefr-classifier"):
        """
        Initialize the CEFR Vocabulary Estimator.
        
        Args:
            model_name: HuggingFace model name for CEFR classification
        """
        self.model_name = model_name
        self.classifier = None
        self.tokenizer = None
        self.nlp = None
        self.lemmatizer = None
        self.stop_words = set()
        
        # CEFR level hierarchy
        self.cefr_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        self.level_to_numeric = {level: i for i, level in enumerate(self.cefr_levels)}
        
        # Basic vocabulary lists (simplified for demonstration)
        self.vocabulary_lists = self._load_vocabulary_lists()
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize NLP components and models."""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            # Initialize NLTK components
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            
            # Initialize spaCy
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model 'en_core_web_sm' not found. Using basic tokenization.")
                self.nlp = None
            
            # Initialize transformer model
            try:
                self.classifier = pipeline(
                    "text-classification",
                    model=self.model_name,
                    tokenizer=self.model_name
                )
                logger.info(f"Loaded CEFR classifier: {self.model_name}")
            except Exception as e:
                logger.warning(f"Could not load transformer model: {e}")
                logger.info("Falling back to vocabulary-based estimation")
                
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
    
    def _load_vocabulary_lists(self) -> Dict[str, set]:
        """
        Load CEFR vocabulary lists. In a production system, these would be
        loaded from authoritative sources like Cambridge or Oxford wordlists.
        """
        # Simplified vocabulary lists for demonstration
        vocabulary_lists = {
            'A1': {
                'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
                'this', 'but', 'his', 'by', 'from', 'they', 'she', 'or', 'an', 'will',
                'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
                'cat', 'dog', 'house', 'car', 'book', 'water', 'food', 'good', 'bad',
                'big', 'small', 'red', 'blue', 'green', 'happy', 'sad', 'old', 'new'
            },
            'A2': {
                'about', 'if', 'go', 'me', 'no', 'just', 'know', 'get', 'people', 'him',
                'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
                'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most',
                'family', 'friend', 'school', 'work', 'home', 'place', 'time', 'year',
                'important', 'different', 'easy', 'difficult', 'interesting', 'beautiful'
            },
            'B1': {
                'state', 'never', 'become', 'between', 'high', 'really', 'something', 'most',
                'another', 'much', 'family', 'own', 'leave', 'put', 'old', 'while', 'mean',
                'keep', 'student', 'why', 'let', 'great', 'same', 'big', 'group', 'begin',
                'seem', 'country', 'help', 'talk', 'where', 'turn', 'problem', 'every',
                'experience', 'opportunity', 'environment', 'society', 'culture', 'education',
                'government', 'technology', 'development', 'community', 'relationship'
            },
            'B2': {
                'system', 'program', 'question', 'work', 'government', 'company', 'number',
                'group', 'problem', 'fact', 'hand', 'high', 'year', 'place', 'right',
                'great', 'public', 'man', 'woman', 'different', 'following', 'without',
                'under', 'might', 'while', 'last', 'should', 'american', 'small', 'another',
                'analysis', 'research', 'investigation', 'phenomenon', 'consequence',
                'significance', 'implementation', 'methodology', 'perspective', 'paradigm'
            },
            'C1': {
                'however', 'within', 'include', 'particularly', 'various', 'possible',
                'available', 'similar', 'according', 'financial', 'political', 'social',
                'economic', 'international', 'development', 'management', 'increase',
                'provide', 'require', 'consider', 'significant', 'individual', 'specific',
                'comprehensive', 'substantial', 'sophisticated', 'intricate', 'elaborate',
                'predominantly', 'considerably', 'extensively', 'fundamentally'
            },
            'C2': {
                'notwithstanding', 'albeit', 'hitherto', 'furthermore', 'nevertheless',
                'consequently', 'predominantly', 'sophisticated', 'encompass', 'paradigm',
                'ubiquitous', 'quintessential', 'unprecedented', 'juxtaposition',
                'dichotomy', 'exponential', 'trajectory', 'infrastructure', 'perpetuate',
                'exacerbate', 'mitigate', 'proliferate', 'consolidate', 'substantiate',
                'corroborate', 'exemplify', 'elucidate', 'facilitate', 'substantive'
            }
        }
        
        return vocabulary_lists
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess and clean the input text.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned and normalized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Basic cleaning
        text = re.sub(r'[^\w\s\.\?\!,;:]', ' ', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        return text
    
    def tokenize_text(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Tokenize text into words and sentences.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (words, sentences)
        """
        try:
            if self.nlp:
                doc = self.nlp(text)
                words = [token.text.lower() for token in doc if token.is_alpha]
                sentences = [sent.text for sent in doc.sents]
            else:
                words = [word.lower() for word in word_tokenize(text) if word.isalpha()]
                sentences = sent_tokenize(text)
            
            return words, sentences
        except Exception as e:
            logger.error(f"Error in tokenization: {e}")
            return [], []
    
    def get_word_cefr_level(self, word: str) -> str:
        """
        Determine the CEFR level of a word based on vocabulary lists.
        
        Args:
            word: Input word (lowercase)
            
        Returns:
            CEFR level (A1-C2) or 'Unknown'
        """
        # Check lemmatized form
        if self.lemmatizer:
            lemmatized = self.lemmatizer.lemmatize(word)
        else:
            lemmatized = word
        
        # Check both original and lemmatized forms
        for level in self.cefr_levels:
            if word in self.vocabulary_lists[level] or lemmatized in self.vocabulary_lists[level]:
                return level
        
        # If not found in any list, estimate based on word length and complexity
        if len(word) <= 4:
            return 'A1'
        elif len(word) <= 6:
            return 'A2'
        elif len(word) <= 8:
            return 'B1'
        elif len(word) <= 10:
            return 'B2'
        elif len(word) <= 12:
            return 'C1'
        else:
            return 'C2'
    
    def calculate_complexity_metrics(self, words: List[str], sentences: List[str]) -> Dict[str, float]:
        """
        Calculate various complexity metrics for the text.
        
        Args:
            words: List of words
            sentences: List of sentences
            
        Returns:
            Dictionary of complexity metrics
        """
        if not words or not sentences:
            return {}
        
        # Basic metrics
        avg_word_length = statistics.mean(len(word) for word in words)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Lexical diversity (TTR - Type-Token Ratio)
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words) if words else 0
        
        # Long word ratio (words > 6 characters)
        long_words = [word for word in words if len(word) > 6]
        long_word_ratio = len(long_words) / len(words) if words else 0
        
        # Syllable estimation (rough)
        def count_syllables(word):
            vowels = 'aeiouy'
            syllables = sum(1 for char in word.lower() if char in vowels)
            return max(1, syllables)  # At least 1 syllable
        
        avg_syllables = statistics.mean(count_syllables(word) for word in words)
        
        return {
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'lexical_diversity': lexical_diversity,
            'long_word_ratio': long_word_ratio,
            'avg_syllables_per_word': avg_syllables
        }
    
    def estimate_level_from_vocabulary(self, words: List[str]) -> Tuple[str, Dict[str, int], Dict[str, List[str]]]:
        """
        Estimate CEFR level based on vocabulary distribution.
        
        Args:
            words: List of words
            
        Returns:
            Tuple of (estimated_level, level_distribution, representative_words)
        """
        if not words:
            return 'A1', {}, {}
        
        # Analyze vocabulary levels
        word_levels = {}
        level_counts = Counter()
        representative_words = defaultdict(list)
        
        for word in words:
            if word not in self.stop_words and len(word) > 2:  # Filter out stop words and very short words
                level = self.get_word_cefr_level(word)
                word_levels[word] = level
                level_counts[level] += 1
                
                # Keep representative words (limit to avoid clutter)
                if len(representative_words[level]) < 10:
                    representative_words[level].append(word)
        
        if not level_counts:
            return 'A1', {}, {}
        
        # Calculate weighted level estimate
        total_words = sum(level_counts.values())
        level_weights = {}
        
        for level, count in level_counts.items():
            level_weights[level] = count / total_words
        
        # Estimate overall level based on distribution
        weighted_score = 0
        for level, weight in level_weights.items():
            weighted_score += self.level_to_numeric[level] * weight
        
        # Determine estimated level
        estimated_numeric = round(weighted_score)
        estimated_level = self.cefr_levels[min(estimated_numeric, len(self.cefr_levels) - 1)]
        
        # Adjust based on highest levels present
        if level_weights.get('C2', 0) > 0.15:
            estimated_level = 'C2'
        elif level_weights.get('C1', 0) > 0.2:
            estimated_level = 'C1'
        elif level_weights.get('B2', 0) > 0.3:
            estimated_level = 'B2'
        
        return estimated_level, dict(level_counts), dict(representative_words)
    
    def estimate_level_with_transformer(self, text: str) -> Tuple[str, float]:
        """
        Estimate CEFR level using the transformer model.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (estimated_level, confidence_score)
        """
        if not self.classifier:
            return None, 0.0
        
        try:
            # Truncate text if too long
            max_length = 512
            if len(text.split()) > max_length:
                text = ' '.join(text.split()[:max_length])
            
            result = self.classifier(text)
            
            if isinstance(result, list) and len(result) > 0:
                prediction = result[0]
                level = prediction['label']
                confidence = prediction['score']
                return level, confidence
            
        except Exception as e:
            logger.error(f"Error in transformer prediction: {e}")
        
        return None, 0.0
    
    def analyze_text(self, text: str) -> TextAnalysisResult:
        """
        Perform comprehensive text analysis and CEFR level estimation.
        
        Args:
            text: Input text to analyze
            
        Returns:
            TextAnalysisResult object with all analysis results
        """
        if not text or not isinstance(text, str):
            raise ValueError("Invalid input text")
        
        # Preprocess text
        cleaned_text = self.preprocess_text(text)
        if not cleaned_text:
            raise ValueError("Text is empty after preprocessing")
        
        # Tokenize
        words, sentences = self.tokenize_text(cleaned_text)
        
        if not words:
            raise ValueError("No words found in text")
        
        # Basic statistics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Vocabulary-based analysis
        vocab_level, level_counts, representative_words = self.estimate_level_from_vocabulary(words)
        
        # Transformer-based analysis
        transformer_level, confidence_score = self.estimate_level_with_transformer(cleaned_text)
        
        # Combine estimates
        if transformer_level and confidence_score > 0.5:
            estimated_level = transformer_level
        else:
            estimated_level = vocab_level
            confidence_score = 0.7  # Default confidence for vocabulary-based estimation
        
        # Calculate level percentages
        total_analyzed_words = sum(level_counts.values())
        level_percentages = {}
        if total_analyzed_words > 0:
            for level in self.cefr_levels:
                count = level_counts.get(level, 0)
                level_percentages[level] = (count / total_analyzed_words) * 100
        
        # Calculate complexity metrics
        complexity_metrics = self.calculate_complexity_metrics(words, sentences)
        
        return TextAnalysisResult(
            text=text[:200] + "..." if len(text) > 200 else text,
            estimated_level=estimated_level,
            confidence_score=confidence_score,
            word_count=word_count,
            sentence_count=sentence_count,
            avg_sentence_length=avg_sentence_length,
            vocabulary_distribution=level_counts,
            level_percentages=level_percentages,
            representative_words=representative_words,
            complexity_metrics=complexity_metrics
        )
    
    def generate_report(self, result: TextAnalysisResult) -> str:
        """
        Generate a detailed text analysis report.
        
        Args:
            result: TextAnalysisResult object
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("CEFR VOCABULARY LEVEL ESTIMATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Basic information
        report.append(f"📝 Text Sample: {result.text}")
        report.append(f"🎯 Estimated CEFR Level: {result.estimated_level}")
        report.append(f"📊 Confidence Score: {result.confidence_score:.2f}")
        report.append("")
        
        # Statistics
        report.append("📈 TEXT STATISTICS")
        report.append("-" * 30)
        report.append(f"Word Count: {result.word_count}")
        report.append(f"Sentence Count: {result.sentence_count}")
        report.append(f"Average Sentence Length: {result.avg_sentence_length:.1f} words")
        report.append("")
        
        # Complexity metrics
        if result.complexity_metrics:
            report.append("🧮 COMPLEXITY METRICS")
            report.append("-" * 30)
            for metric, value in result.complexity_metrics.items():
                report.append(f"{metric.replace('_', ' ').title()}: {value:.2f}")
            report.append("")
        
        # Level distribution
        report.append("📊 VOCABULARY LEVEL DISTRIBUTION")
        report.append("-" * 30)
        for level in self.cefr_levels:
            count = result.vocabulary_distribution.get(level, 0)
            percentage = result.level_percentages.get(level, 0)
            report.append(f"{level}: {count} words ({percentage:.1f}%)")
        report.append("")
        
        # Representative words
        report.append("💭 REPRESENTATIVE WORDS BY LEVEL")
        report.append("-" * 30)
        for level in self.cefr_levels:
            words = result.representative_words.get(level, [])
            if words:
                report.append(f"{level}: {', '.join(words[:10])}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)

def main():
    """Main function for command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CEFR Vocabulary Level Estimator")
    parser.add_argument("--text", type=str, help="Text to analyze")
    parser.add_argument("--file", type=str, help="File containing text to analyze")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Initialize estimator
    print("🚀 Initializing CEFR Vocabulary Level Estimator...")
    estimator = CEFRVocabularyEstimator()
    print("✅ Estimator ready!")
    print()
    
    if args.interactive or (not args.text and not args.file):
        # Interactive mode
        print("🎯 Interactive Mode - Enter 'quit' to exit")
        print("-" * 40)
        
        while True:
            try:
                text = input("\n📝 Enter text to analyze: ").strip()
                
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not text:
                    print("⚠️  Please enter some text to analyze.")
                    continue
                
                result = estimator.analyze_text(text)
                report = estimator.generate_report(result)
                print(report)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    elif args.file:
        # File mode
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            result = estimator.analyze_text(text)
            report = estimator.generate_report(result)
            print(report)
            
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
        except Exception as e:
            print(f"❌ Error processing file: {e}")
    
    elif args.text:
        # Direct text mode
        try:
            result = estimator.analyze_text(args.text)
            report = estimator.generate_report(result)
            print(report)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()