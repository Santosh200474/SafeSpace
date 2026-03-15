"""
ML Classification Module
Handles machine learning model training, evaluation, and prediction
"""

import joblib
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

class MLClassifier:
    def __init__(self, model_type='logistic_regression'):
        """
        Initialize ML classifier
        
        Args:
            model_type (str): Type of model ('logistic_regression', 'svm', 'decision_tree', 'random_forest', 'naive_bayes')
        """
        self.model_type = model_type
        self.model = self._create_model(model_type)
        self.is_trained = False
    
    def _create_model(self, model_type):
        """Create the specified model"""
        if model_type == 'logistic_regression':
            return LogisticRegression(max_iter=1000, random_state=42)
        elif model_type == 'svm':
            return SVC(kernel='linear', probability=True, random_state=42)
        elif model_type == 'decision_tree':
            return DecisionTreeClassifier(random_state=42)
        elif model_type == 'random_forest':
            return RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'naive_bayes':
            return MultinomialNB()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(self, X_train, y_train):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("Training completed!")
    
    def predict(self, X):
        """
        Predict labels
        
        Args:
            X: Features to predict
            
        Returns:
            array: Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction!")
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predict probabilities
        
        Args:
            X: Features to predict
            
        Returns:
            array: Prediction probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction!")
        
        return self.model.predict_proba(X)
    
    def classify_text(self, X):
        """
        Classify text and return label with confidence
        
        Args:
            X: Features (single sample or batch)
            
        Returns:
            dict: Dictionary containing label and confidence
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before classification!")
        
        # Get prediction
        prediction = self.model.predict(X)
        
        # Get confidence score
        probabilities = self.model.predict_proba(X)
        confidence = np.max(probabilities, axis=1)
        
        # For single prediction
        if len(prediction) == 1:
            return {
                'label': int(prediction[0]),
                'confidence': float(confidence[0]),
                'is_cyberbullying': bool(prediction[0] == 1)
            }
        
        # For batch predictions
        return {
            'labels': prediction.tolist(),
            'confidences': confidence.tolist(),
            'is_cyberbullying': [bool(p == 1) for p in prediction]
        }
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            dict: Evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation!")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='binary')
        recall = recall_score(y_test, y_pred, average='binary')
        f1 = f1_score(y_test, y_pred, average='binary')
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm
        }
        
        # Print results
        print("\n=== Model Evaluation ===")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print("\nConfusion Matrix:")
        print(cm)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Non-Bullying', 'Cyberbullying']))
        
        return metrics
    
    def save_model(self, filepath):
        """
        Save trained model to disk
        
        Args:
            filepath (str): Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model!")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load trained model from disk
        
        Args:
            filepath (str): Path to load the model from
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        self.model = joblib.load(filepath)
        self.is_trained = True
        print(f"Model loaded from {filepath}")


# Admin module for model management
class AdminModule:
    """
    Admin module for model retraining and management
    """
    
    @staticmethod
    def retrain_model(X_train, y_train, model_type='logistic_regression'):
        """
        Retrain a model with new data
        
        Args:
            X_train: Training features
            y_train: Training labels
            model_type: Type of model to train
            
        Returns:
            MLClassifier: Trained classifier
        """
        classifier = MLClassifier(model_type=model_type)
        classifier.train(X_train, y_train)
        return classifier
    
    @staticmethod
    def unblock_user(database_manager, username):
        """
        Unblock a user (admin function)
        
        Args:
            database_manager: Database manager instance
            username: Username to unblock
        """
        conn = database_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET is_blocked = 0, warning_count = 0 WHERE username = ?",
            (username,)
        )
        conn.commit()
        conn.close()
        
        database_manager.log_action(username, "ADMIN_UNBLOCK", "User unblocked by admin")
        print(f"User {username} has been unblocked and warnings reset.")


# Example usage
if __name__ == "__main__":
    # This would normally be called with actual training data
    print("ML Classifier module loaded successfully!")
    print("Available models: logistic_regression, svm, decision_tree, random_forest, naive_bayes")
