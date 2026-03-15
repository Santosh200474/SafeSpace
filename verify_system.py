"""
System Verification and Testing Script
Verifies all components are working correctly
"""

import os
import sys

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_imports():
    """Test if all required modules can be imported"""
    print_section("Testing Module Imports")
    
    modules_to_test = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('joblib', 'joblib'),
    ]
    
    all_passed = True
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - Not installed")
            all_passed = False
    
    return all_passed

def test_model_files():
    """Test if model files exist"""
    print_section("Testing Model Files")
    
    files_to_check = [
        'models/cyberbullying_classifier.pkl',
        'models/tfidf_vectorizer.pkl'
    ]
    
    all_passed = True
    for filepath in files_to_check:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {filepath} ({size} bytes)")
        else:
            print(f"❌ {filepath} - Not found")
            all_passed = False
    
    return all_passed

def test_directories():
    """Test if required directories exist"""
    print_section("Testing Directory Structure")
    
    directories = [
        'modules',
        'models',
        'database',
        'data'
    ]
    
    all_passed = True
    for directory in directories:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✅ {directory}/")
            
            # Check data directory for CSV files
            if directory == 'data':
                csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
                if csv_files:
                    print(f"   📊 Found {len(csv_files)} CSV file(s):")
                    for f in csv_files:
                        print(f"      - {f}")
                else:
                    print(f"   ⚠️  No CSV files found (will use sample data)")
        else:
            print(f"❌ {directory}/ - Not found")
            all_passed = False
    
    return all_passed

def test_model_loading():
    """Test model and vectorizer loading"""
    print_section("Testing Model Loading")
    
    try:
        import joblib
        
        # Load model
        model = joblib.load('models/cyberbullying_classifier.pkl')
        print("✅ Model loaded successfully")
        
        # Load vectorizer  
        vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
        print("✅ Vectorizer loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_end_to_end():
    """Test complete pipeline"""
    print_section("Testing End-to-End Pipeline")
    
    try:
        import joblib
        
        # Load models
        model = joblib.load('models/cyberbullying_classifier.pkl')
        vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
        
        print("✅ Models loaded successfully")
        
        # Test comments
        test_comments = [
            "Great job! Keep up the good work!",
            "You're so stupid and worthless"
        ]
        
        print("\nTesting predictions:")
        print("-" * 60)
        
        for comment in test_comments:
            # Transform using vectorizer (handles preprocessing internally)
            features = vectorizer.transform([comment])
            
            # Predict
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities)
            
            label_text = "Cyberbullying" if prediction == 1 else "Safe"
            print(f"\nComment: {comment}")
            print(f"Result:  {label_text}")
            print(f"Confidence: {confidence:.2%}")
        
        print("\n✅ End-to-end pipeline working")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database operations"""
    print_section("Testing Database Operations")
    
    try:
        from modules.database import DatabaseManager
        
        db = DatabaseManager('database/test_db.db')
        
        # Test user registration
        success, msg = db.register_user('test_user', 'test_pass')
        if success:
            print("✅ User registration working")
        
        # Test authentication
        success, msg = db.authenticate_user('test_user', 'test_pass')
        if success:
            print("✅ User authentication working")
        
        # Test user info
        user_info = db.get_user_info('test_user')
        if user_info:
            print("✅ User info retrieval working")
        
        # Clean up
        os.remove('database/test_db.db')
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("  CYBERBULLYING DETECTION SYSTEM - VERIFICATION")
    print("="*60)
    
    results = {}
    
    # Run tests
    results['imports'] = test_imports()
    results['directories'] = test_directories()
    results['model_files'] = test_model_files()
    results['model_loading'] = test_model_loading()
    results['database'] = test_database()
    results['end_to_end'] = test_end_to_end()
    
    # Summary
    print_section("Test Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print("\n" + "="*60)
    if passed == total:
        print("  ✅ ALL TESTS PASSED - SYSTEM READY!")
    else:
        print("  ⚠️ SOME TESTS FAILED - CHECK ABOVE")
    print("="*60)
    
    print("\nNext Steps:")
    if passed == total:
        print("  1. Run: streamlit run app.py")
        print("  2. Open browser at http://localhost:8501")
        print("  3. Register a new account")
        print("  4. Start testing the system!")
    else:
        print("  1. Review failed tests above")
        print("  2. Run: python train_model.py (if models missing)")
        print("  3. Install missing packages (if imports failed)")
        print("  4. Run this script again")
    
    print("")

if __name__ == "__main__":
    main()
