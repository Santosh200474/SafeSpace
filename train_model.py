"""
Model Training Script
Train and save the cyberbullying detection model using proven approach
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# --------------------------------------------------
# Configuration
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

# Model paths (using names expected by app.py)
MODEL_PATH = os.path.join(MODELS_DIR, "cyberbullying_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def load_datasets():
    """
    Load and combine all CSV files from the dataset directory
    
    Returns:
        DataFrame: Combined dataset with 'text' and 'oh_label' columns
    """
    print_section("LOADING DATASETS")
    
    if not os.path.exists(DATASET_DIR):
        print(f"\n❌ Dataset directory not found: {DATASET_DIR}")
        print("Please create 'data' directory and add your CSV files.")
        return None
    
    all_dfs = []
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(DATASET_DIR) if f.endswith(".csv")]
    
    if not csv_files:
        print(f"\n❌ No CSV files found in {DATASET_DIR}")
        print("\nPlease add your CSV files to the 'data' directory.")
        print("Expected files:")
        print("  - aggression_parsed_dataset.csv")
        print("  - toxicity_parsed_dataset.csv")
        print("  - twitter_sexism_parsed_dataset.csv")
        print("  - youtube_parsed_dataset.csv")
        return None
    
    print(f"\n📂 Found {len(csv_files)} CSV file(s)\n")
    
    # Load each CSV file
    for file in csv_files:
        filepath = os.path.join(DATASET_DIR, file)
        
        try:
            print(f"Loading: {file}...", end=" ")
            
            # Read CSV with latin1 encoding (handles special characters)
            df = pd.read_csv(filepath, encoding="latin1")
            
            # Normalize column names to lowercase
            df.columns = df.columns.str.lower().str.strip()
            
            # Check if required columns exist
            if {"text", "oh_label"}.issubset(df.columns):
                # Keep only required columns
                df = df[["text", "oh_label"]]
                
                # Remove rows with missing values
                original_len = len(df)
                df.dropna(inplace=True)
                
                # Add to collection
                all_dfs.append(df)
                
                # Count classes
                class_counts = df["oh_label"].value_counts().to_dict()
                non_cyber = class_counts.get(0, 0)
                cyber = class_counts.get(1, 0)
                
                print(f"✅ {len(df):,} rows")
                print(f"   - Non-cyberbullying (0): {non_cyber:,}")
                print(f"   - Cyberbullying (1): {cyber:,}")
                
                if len(df) < original_len:
                    print(f"   - Removed {original_len - len(df)} rows with missing values")
            else:
                print(f"❌ SKIPPED")
                print(f"   Required columns 'text' and 'oh_label' not found")
                print(f"   Found columns: {df.columns.tolist()}")
        
        except Exception as e:
            print(f"❌ ERROR")
            print(f"   {str(e)}")
    
    # Combine all dataframes
    if not all_dfs:
        print("\n❌ No valid data loaded from CSV files")
        return None
    
    df_combined = pd.concat(all_dfs, ignore_index=True)
    
    print("\n" + "-"*70)
    print(f"✅ TOTAL SAMPLES LOADED: {len(df_combined):,}")
    
    # Overall class distribution
    class_counts = df_combined["oh_label"].value_counts().to_dict()
    non_cyber = class_counts.get(0, 0)
    cyber = class_counts.get(1, 0)
    
    print(f"\n📊 Overall Class Distribution:")
    print(f"   Non-cyberbullying (0): {non_cyber:,} ({non_cyber/len(df_combined)*100:.1f}%)")
    print(f"   Cyberbullying (1): {cyber:,} ({cyber/len(df_combined)*100:.1f}%)")
    
    # Check balance
    balance_ratio = min(non_cyber, cyber) / max(non_cyber, cyber)
    if balance_ratio < 0.5:
        print(f"\n⚠️  Class imbalance detected (ratio: {balance_ratio:.2f})")
        print("   Using class_weight='balanced' in model training")
    else:
        print(f"\n✅ Dataset is well balanced (ratio: {balance_ratio:.2f})")
    
    return df_combined


def train_model(df):
    """
    Train the cyberbullying detection model
    
    Args:
        df: DataFrame with 'text' and 'oh_label' columns
    """
    print_section("MODEL TRAINING")
    
    # Prepare data
    print("\n[1/5] Preparing data...")
    X = df["text"].astype(str)
    y = df["oh_label"]
    
    # Train-test split with stratification
    print("[2/5] Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    
    print(f"   Training samples: {len(X_train):,}")
    print(f"   Test samples: {len(X_test):,}")
    
    # TF-IDF Vectorization
    print("\n[3/5] Creating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=12000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    
    print("   Fitting vectorizer on training data...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"   Feature matrix shape: {X_train_vec.shape}")
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_):,}")
    
    # Model Training
    print("\n[4/5] Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
        solver='lbfgs'
    )
    
    model.fit(X_train_vec, y_train)
    print("   ✅ Training completed!")
    
    # Model Evaluation
    print("\n[5/5] Evaluating model performance...")
    y_pred = model.predict(X_test_vec)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')
    f1 = f1_score(y_test, y_pred, average='binary')
    
    print("\n" + "="*70)
    print("  MODEL EVALUATION RESULTS")
    print("="*70)
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"   F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n📈 Confusion Matrix:")
    print(f"   True Negatives:  {cm[0][0]:,}")
    print(f"   False Positives: {cm[0][1]:,}")
    print(f"   False Negatives: {cm[1][0]:,}")
    print(f"   True Positives:  {cm[1][1]:,}")
    
    # Detailed classification report
    print(f"\n📋 Detailed Classification Report:")
    print("-"*70)
    print(classification_report(
        y_test, 
        y_pred, 
        target_names=['Non-Cyberbullying', 'Cyberbullying'],
        digits=4
    ))
    
    # Save model and vectorizer
    print("="*70)
    print("  SAVING MODEL AND VECTORIZER")
    print("="*70)
    
    joblib.dump(model, MODEL_PATH)
    print(f"\n✅ Model saved: {MODEL_PATH}")
    
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"✅ Vectorizer saved: {VECTORIZER_PATH}")
    
    # Verify saved files
    model_size = os.path.getsize(MODEL_PATH) / 1024  # KB
    vectorizer_size = os.path.getsize(VECTORIZER_PATH) / 1024  # KB
    
    print(f"\n📦 File Sizes:")
    print(f"   Model: {model_size:.2f} KB")
    print(f"   Vectorizer: {vectorizer_size:.2f} KB")
    
    return model, vectorizer, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm
    }


def create_sample_dataset():
    """Create a minimal sample dataset for testing"""
    print("\n⚠️  Creating sample dataset for demonstration...")
    
    data = {
        'text': [
            "You're so stupid and worthless",
            "Great job! Keep up the good work!",
            "Nobody likes you, loser",
            "I really appreciate your help",
            "You should kill yourself",
            "This is amazing content!",
            "You're ugly and dumb",
            "Thanks for sharing this",
            "Everyone hates you",
            "Well done, proud of you!",
            "Go away, nobody wants you here",
            "Excellent presentation!",
            "You're a complete idiot",
            "Thank you so much!",
            "What a waste of space",
            "Great contribution to the team",
            "You're pathetic",
            "Wonderful job!",
            "I hope you fail",
            "Keep up the excellent work!"
        ] * 5,  # Duplicate to have 100 samples
        'oh_label': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] * 5
    }
    
    df = pd.DataFrame(data)
    print(f"   Created {len(df)} sample entries")
    return df


def main():
    """Main training function"""
    print("\n" + "="*70)
    print("  CYBERBULLYING DETECTION - MODEL TRAINING")
    print("  Using Proven Training Approach")
    print("="*70)
    
    # Load datasets
    df = load_datasets()
    
    # If no datasets found, use sample data
    if df is None or len(df) == 0:
        print("\n⚠️  No datasets found in 'data' directory")
        print("\n📝 To use your own data:")
        print("   1. Create a 'data' folder in the project directory")
        print("   2. Add your CSV files with 'Text' and 'oh_label' columns")
        print("   3. Run this script again")
        print("\n   Using sample dataset for demonstration...")
        
        df = create_sample_dataset()
    
    # Train model
    try:
        model, vectorizer, metrics = train_model(df)
        
        print("\n" + "="*70)
        print("  ✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n🎯 Next Steps:")
        print("   1. Run: streamlit run app.py")
        print("   2. Test the system with real comments")
        print("   3. Verify detection accuracy")
        
        print("\n📊 Model Summary:")
        print(f"   - Trained on {len(df):,} samples")
        print(f"   - Accuracy: {metrics['accuracy']*100:.2f}%")
        print(f"   - F1 Score: {metrics['f1']*100:.2f}%")
        print(f"   - Ready for deployment!")
        
    except Exception as e:
        print("\n" + "="*70)
        print("  ❌ TRAINING FAILED")
        print("="*70)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
