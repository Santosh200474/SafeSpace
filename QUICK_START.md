# 🚀 QUICK START GUIDE

## ⚡ Get Started in 4 Steps

### Step 1: Extract Files
Extract the `cyberbullying_detection_system` folder to your desired location.

### Step 2: Prepare Your Datasets

**IMPORTANT**: Copy your CSV files to the `data/` directory:

```bash
cd cyberbullying_detection_system/data
```

Your CSV files should be:
- `aggression_parsed_dataset.csv`
- `toxicity_parsed_dataset.csv`
- `twitter_sexism_parsed_dataset.csv`
- `youtube_parsed_dataset.csv`

Each file must have columns: `Text` and `oh_label`
- `oh_label` = 0 (non-cyberbullying)
- `oh_label` = 1 (cyberbullying)

**Verify your datasets:**
```bash
python inspect_data.py
```

This will show you detailed statistics about your data!

### Step 3: Install Dependencies

**Option A - Using pip (Recommended):**
```bash
cd cyberbullying_detection_system
pip install streamlit pandas numpy scikit-learn joblib
```

**Option B - Using the setup script:**
```bash
cd cyberbullying_detection_system
chmod +x setup.sh
./setup.sh
```

### Step 4: Train the Model

```bash
python train_model.py
```

This will:
- Load all 4 CSV datasets from `data/` folder
- Combine and preprocess the data
- Train the ML model
- Save model files to `models/` directory
- Show evaluation metrics

**Expected output:**
```
Found 4 CSV file(s)...
✅ TOTAL SAMPLES LOADED: [your total]
Training completed!
Accuracy: [your accuracy]
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 6: Create Account & Test

1. Click **Register** tab
2. Enter username: `testuser`
3. Enter password: `password123`
4. Click **Register**
5. Login with your credentials
6. Try commenting on posts!

---

## 🧪 Test the System

### Test 1: Post Safe Comment
```
Comment: "Great post! Really enjoyed this!"
→ Click "Analyze Comment"
→ Result: ✅ Safe
→ Click "Post Comment"
→ Success!
```

### Test 2: Attempt Cyberbullying
```
Comment: "You're so stupid and worthless"
→ Click "Analyze Comment"
→ Result: ❌ Cyberbullying Detected
→ Warning 1/3 issued
→ Post button disabled
```

### Test 3: Get Account Blocked
```
Try 3 cyberbullying comments:
1. "You're an idiot"
2. "Nobody likes you"
3. "Go away loser"
→ After 3rd attempt: Account Blocked
→ Can't comment anymore
```

---

## 📁 Project Structure

```
cyberbullying_detection_system/
├── app.py                    # Main Streamlit application
├── train_model.py           # Model training script
├── verify_system.py         # System verification
├── requirements.txt         # Python dependencies
├── setup.sh                 # Setup script
│
├── modules/                 # Core system modules
│   ├── database.py         # SQLite operations
│   ├── authentication.py   # User auth & sessions
│   ├── nlp_processing.py   # Text preprocessing
│   ├── feature_extraction.py  # TF-IDF vectorization
│   ├── ml_classifier.py    # ML model
│   └── moderation.py       # Warning & blocking logic
│
├── models/                  # Trained models (after training)
│   ├── cyberbullying_classifier.pkl
│   └── tfidf_vectorizer.pkl
│
├── database/                # SQLite database (auto-created)
│   └── cyberbullying.db
│
├── data/                    # Training datasets (optional)
│   └── [your CSV files]
│
└── Documentation/
    ├── README.md           # Complete documentation
    ├── USER_GUIDE.md       # Detailed user guide
    └── PRESENTATION_GUIDE.md  # Project presentation
```

---

## 🎯 Key Features

✅ **Real-time Detection**: Instant analysis of comments
✅ **Warning System**: 3 strikes before account block
✅ **Confidence Scores**: ML model certainty levels
✅ **User-Friendly UI**: Social media style interface
✅ **Persistent Storage**: SQLite database
✅ **Modular Architecture**: Clean, maintainable code

---

## ⚠️ Troubleshooting

### Issue: "Module not found" errors
**Solution**: Install required packages
```bash
pip install streamlit pandas numpy scikit-learn joblib
```

### Issue: "Model files not found"
**Solution**: Train the model first
```bash
python train_model.py
```

### Issue: "Port already in use"
**Solution**: Use a different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Database errors
**Solution**: Delete and recreate database
```bash
rm database/cyberbullying.db
# Restart the app, database will be recreated
```

---

## 📚 Full Documentation

- **README.md**: Complete technical documentation
- **USER_GUIDE.md**: Detailed usage instructions
- **PRESENTATION_GUIDE.md**: Project presentation guide

---

## 🎓 For Academic Evaluation

### What to Show:
1. ✅ Architecture diagrams (in uploaded images)
2. ✅ Live demo of the application
3. ✅ Code walkthrough of key modules
4. ✅ Database schema and data
5. ✅ ML model evaluation metrics

### Key Points:
- Modular design with 8 components
- End-to-end ML pipeline
- Real-time NLP processing
- Progressive moderation system
- Production-ready architecture

---

## 💡 Tips for Success

1. **Practice the demo** before presentation
2. **Prepare test accounts** in advance
3. **Show database** to prove persistence
4. **Explain algorithms** clearly
5. **Highlight innovations** in your approach

---

## 🤝 Support

For questions or issues:
1. Read the full documentation in README.md
2. Check USER_GUIDE.md for detailed instructions
3. Review PRESENTATION_GUIDE.md for demo tips

---

**Ready to get started? Run these 3 commands:**

```bash
cd cyberbullying_detection_system
python train_model.py
streamlit run app.py
```

Good luck with your project! 🎓
