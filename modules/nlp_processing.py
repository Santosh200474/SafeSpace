"""
NLP Processing Module
Handles text preprocessing including tokenization, stopword removal, and normalization
"""

import re
import string

class NLPProcessor:
    def __init__(self):
        """Initialize NLP processor with stopwords"""
        # Common English stopwords
        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
            'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
            'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once'
        }
    
    def lowercase(self, text):
        """Convert text to lowercase"""
        return text.lower()
    
    def remove_urls(self, text):
        """Remove URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def remove_mentions(self, text):
        """Remove @mentions"""
        return re.sub(r'@\w+', '', text)
    
    def remove_hashtags(self, text):
        """Remove hashtags"""
        return re.sub(r'#\w+', '', text)
    
    def remove_special_characters(self, text):
        """Remove special characters and digits"""
        # Keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def remove_extra_whitespace(self, text):
        """Remove extra whitespace"""
        return ' '.join(text.split())
    
    def tokenize(self, text):
        """Tokenize text into words"""
        # Simple word tokenization using regex
        tokens = re.findall(r'\b[a-z]+\b', text.lower())
        return tokens
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list"""
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return filtered_tokens
    
    def normalize(self, text):
        """Apply all normalization steps"""
        # Lowercase
        text = self.lowercase(text)
        
        # Remove URLs
        text = self.remove_urls(text)
        
        # Remove mentions and hashtags
        text = self.remove_mentions(text)
        text = self.remove_hashtags(text)
        
        # Remove special characters
        text = self.remove_special_characters(text)
        
        # Remove extra whitespace
        text = self.remove_extra_whitespace(text)
        
        return text
    
    def preprocess(self, text):
        """Complete preprocessing pipeline
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Preprocessed text ready for feature extraction
        """
        # Normalize text
        normalized_text = self.normalize(text)
        
        # Tokenize
        tokens = self.tokenize(normalized_text)
        
        # Remove stopwords
        filtered_tokens = self.remove_stopwords(tokens)
        
        # Rejoin tokens
        preprocessed_text = ' '.join(filtered_tokens)
        
        return preprocessed_text
    
    def batch_preprocess(self, texts):
        """Preprocess multiple texts
        
        Args:
            texts (list): List of text strings
            
        Returns:
            list: List of preprocessed texts
        """
        return [self.preprocess(text) for text in texts]


# Example usage
if __name__ == "__main__":
    processor = NLPProcessor()
    
    # Test cases
    test_comments = [
        "You are so stupid! #loser @badperson",
        "Great work! Keep it up!",
        "Nobody likes you, go away!",
        "Check out this link: https://example.com"
    ]
    
    print("=== NLP Processing Test ===\n")
    for comment in test_comments:
        preprocessed = processor.preprocess(comment)
        print(f"Original: {comment}")
        print(f"Processed: {preprocessed}")
        print("-" * 50)
