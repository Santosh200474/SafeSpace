#!/bin/bash

# Cyberbullying Detection System - Setup Script

echo "=================================================="
echo "  Cyberbullying Detection System - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
python3 --version

# Install dependencies
echo ""
echo "[2/5] Installing dependencies..."
echo "Note: If you see network errors, the system will work with pre-installed packages."
pip install streamlit pandas numpy scikit-learn nltk joblib --break-system-packages -q 2>/dev/null || echo "Using system packages..."

# Create directories
echo ""
echo "[3/5] Creating directories..."
mkdir -p models database data

# Train model
echo ""
echo "[4/5] Training ML model..."
python3 train_model.py

# Check if model was created
echo ""
echo "[5/5] Verifying setup..."
if [ -f "models/cyberbullying_classifier.pkl" ] && [ -f "models/tfidf_vectorizer.pkl" ]; then
    echo "✅ Model files created successfully!"
else
    echo "❌ Model files not found. Please run: python3 train_model.py"
    exit 1
fi

echo ""
echo "=================================================="
echo "  Setup Complete!"
echo "=================================================="
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
echo "Or for systems without Streamlit installed:"
echo "  python3 -m streamlit run app.py"
echo ""
echo "Default login credentials:"
echo "  Create a new account using the Register tab"
echo ""
echo "=================================================="
