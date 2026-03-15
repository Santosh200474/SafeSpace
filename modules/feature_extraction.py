"""
Feature Extraction Module
Handles TF-IDF vectorization for converting text to numerical features
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

class FeatureExtractor:
    def __init__(self, max_features=5000, ngram_range=(1, 2)):
        """
        Initialize TF-IDF vectorizer
        
        Args:
            max_features (int): Maximum number of features
            ngram_range (tuple): N-gram range for feature extraction
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=2,
            max_df=0.8
        )
        self.is_fitted = False
    
    def fit(self, texts):
        """
        Fit vectorizer on training texts
        
        Args:
            texts (list): List of preprocessed text strings
        """
        self.vectorizer.fit(texts)
        self.is_fitted = True
    
    def transform(self, texts):
        """
        Transform texts to TF-IDF features
        
        Args:
            texts (list): List of preprocessed text strings
            
        Returns:
            array: TF-IDF feature matrix
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before transform!")
        
        return self.vectorizer.transform(texts)
    
    def fit_transform(self, texts):
        """
        Fit vectorizer and transform texts in one step
        
        Args:
            texts (list): List of preprocessed text strings
            
        Returns:
            array: TF-IDF feature matrix
        """
        self.is_fitted = True
        return self.vectorizer.fit_transform(texts)
    
    def save_vectorizer(self, filepath):
        """
        Save fitted vectorizer to disk
        
        Args:
            filepath (str): Path to save the vectorizer
        """
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted vectorizer!")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.vectorizer, filepath)
        print(f"Vectorizer saved to {filepath}")
    
    def load_vectorizer(self, filepath):
        """
        Load fitted vectorizer from disk
        
        Args:
            filepath (str): Path to load the vectorizer from
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Vectorizer file not found: {filepath}")
        
        self.vectorizer = joblib.load(filepath)
        self.is_fitted = True
        print(f"Vectorizer loaded from {filepath}")
    
    def get_feature_names(self):
        """
        Get feature names from the vectorizer
        
        Returns:
            array: Feature names
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted first!")
        
        return self.vectorizer.get_feature_names_out()
    
    def get_vocabulary_size(self):
        """
        Get the size of the vocabulary
        
        Returns:
            int: Number of features in vocabulary
        """
        if not self.is_fitted:
            return 0
        
        return len(self.vectorizer.vocabulary_)


# Bag of Words alternative (simpler approach)
class BagOfWordsExtractor:
    def __init__(self, max_features=5000):
        """
        Initialize Bag of Words vectorizer
        
        Args:
            max_features (int): Maximum number of features
        """
        from sklearn.feature_extraction.text import CountVectorizer
        
        self.vectorizer = CountVectorizer(
            max_features=max_features,
            min_df=2,
            max_df=0.8
        )
        self.is_fitted = False
    
    def fit(self, texts):
        """Fit vectorizer on training texts"""
        self.vectorizer.fit(texts)
        self.is_fitted = True
    
    def transform(self, texts):
        """Transform texts to BoW features"""
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before transform!")
        
        return self.vectorizer.transform(texts)
    
    def fit_transform(self, texts):
        """Fit and transform in one step"""
        self.is_fitted = True
        return self.vectorizer.fit_transform(texts)
    
    def save_vectorizer(self, filepath):
        """Save fitted vectorizer"""
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted vectorizer!")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.vectorizer, filepath)
        print(f"BoW Vectorizer saved to {filepath}")
    
    def load_vectorizer(self, filepath):
        """Load fitted vectorizer"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Vectorizer file not found: {filepath}")
        
        self.vectorizer = joblib.load(filepath)
        self.is_fitted = True
        print(f"BoW Vectorizer loaded from {filepath}")


# Example usage
if __name__ == "__main__":
    # Test feature extraction
    sample_texts = [
        "you are stupid",
        "great work keep going",
        "nobody likes you loser",
        "amazing job well done"
    ]
    
    print("=== Feature Extraction Test ===\n")
    
    # TF-IDF
    tfidf_extractor = FeatureExtractor(max_features=100)
    features = tfidf_extractor.fit_transform(sample_texts)
    
    print(f"TF-IDF Shape: {features.shape}")
    print(f"Vocabulary Size: {tfidf_extractor.get_vocabulary_size()}")
    print(f"\nSample Features (first 10):")
    print(tfidf_extractor.get_feature_names()[:10])
