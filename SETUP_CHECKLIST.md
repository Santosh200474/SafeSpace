# ✅ Setup Checklist - Cyberbullying Detection System

## Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] Terminal/Command prompt access
- [ ] Project folder extracted

---

## Dataset Preparation Checklist

### CSV Files Required

- [ ] `aggression_parsed_dataset.csv` available
- [ ] `toxicity_parsed_dataset.csv` available
- [ ] `twitter_sexism_parsed_dataset.csv` available
- [ ] `youtube_parsed_dataset.csv` available

### CSV Format Validation

- [ ] Each CSV has `Text` column (case-sensitive)
- [ ] Each CSV has `oh_label` column (case-sensitive)
- [ ] Labels are numeric (0 or 1)
- [ ] 0 = Non-cyberbullying
- [ ] 1 = Cyberbullying
- [ ] No missing values in critical columns

### Files Placement

- [ ] Created `data/` directory in project folder
- [ ] Copied all 4 CSV files to `data/` directory
- [ ] Verified files are in correct location:
  ```
  cyberbullying_detection_system/data/
  ├── aggression_parsed_dataset.csv
  ├── toxicity_parsed_dataset.csv
  ├── twitter_sexism_parsed_dataset.csv
  └── youtube_parsed_dataset.csv
  ```

---

## Installation Checklist

### Dependencies

- [ ] Navigated to project directory
  ```bash
  cd cyberbullying_detection_system
  ```

- [ ] Installed Python packages:
  ```bash
  pip install streamlit pandas numpy scikit-learn joblib
  ```
  OR
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

- [ ] No installation errors occurred

---

## Verification Checklist

### Dataset Inspection

- [ ] Ran dataset inspection:
  ```bash
  python inspect_data.py
  ```

- [ ] All 4 CSV files detected
- [ ] No missing column errors
- [ ] Class distribution shown
- [ ] Sample texts displayed
- [ ] No critical warnings

### System Verification

- [ ] Ran system verification:
  ```bash
  python verify_system.py
  ```

- [ ] Module imports successful
- [ ] Directories exist
- [ ] Custom modules loaded

---

## Model Training Checklist

### Training Process

- [ ] Ran training script:
  ```bash
  python train_model.py
  ```

- [ ] All CSV files loaded successfully
- [ ] Total samples count displayed
- [ ] Class distribution shown
- [ ] Preprocessing completed
- [ ] Feature extraction successful
- [ ] Model training completed
- [ ] Evaluation metrics displayed
- [ ] Model files saved

### Model Files Created

- [ ] `models/cyberbullying_classifier.pkl` exists
- [ ] `models/tfidf_vectorizer.pkl` exists
- [ ] File sizes > 0 bytes
- [ ] No error messages during save

### Training Results

Document your results:

- Total samples loaded: __________
- Non-cyberbullying (0): __________ (___%)
- Cyberbullying (1): __________ (___%)
- Accuracy: __________
- Precision: __________
- Recall: __________
- F1 Score: __________

---

## Application Launch Checklist

### Starting the App

- [ ] Ran Streamlit application:
  ```bash
  streamlit run app.py
  ```

- [ ] Browser opened automatically
- [ ] OR manually accessed: http://localhost:8501
- [ ] Login/Register page displayed
- [ ] No Python errors in terminal

---

## Functional Testing Checklist

### User Registration

- [ ] Clicked "Register" tab
- [ ] Entered username (3+ characters)
- [ ] Entered password (6+ characters)
- [ ] Confirmed password matches
- [ ] Registration successful
- [ ] Success message displayed

### User Login

- [ ] Clicked "Login" tab
- [ ] Entered registered username
- [ ] Entered correct password
- [ ] Login successful
- [ ] Redirected to feed

### Feed Display

- [ ] Feed page loads correctly
- [ ] 8 sample posts visible
- [ ] Each post has image emoji
- [ ] Each post has username
- [ ] Each post has caption
- [ ] Warning count displayed (0/3)
- [ ] Logout button works

### Comment Analysis (Safe)

- [ ] Clicked "Comment on this post"
- [ ] Typed safe comment: "Great post!"
- [ ] Clicked "Analyze Comment"
- [ ] Analysis completed
- [ ] ✅ Green "Safe" message shown
- [ ] Confidence score displayed
- [ ] "Post Comment" button enabled

### Comment Posting

- [ ] Clicked "Post Comment"
- [ ] Success message displayed
- [ ] Comment cleared
- [ ] No errors occurred

### Cyberbullying Detection

- [ ] Typed bullying comment: "You're stupid"
- [ ] Clicked "Analyze Comment"
- [ ] Analysis completed
- [ ] ❌ Red warning shown
- [ ] Severity level displayed
- [ ] Confidence score shown
- [ ] "Post Comment" button disabled
- [ ] Warning count increased (1/3)

### Warning System

Test 1st Warning:
- [ ] Attempted cyberbullying comment
- [ ] Warning 1/3 displayed
- [ ] Warning message shown
- [ ] Account not blocked

Test 2nd Warning:
- [ ] Attempted 2nd cyberbullying comment
- [ ] Warning 2/3 displayed
- [ ] "Final warning" message
- [ ] Account not blocked

Test 3rd Warning (Block):
- [ ] Attempted 3rd cyberbullying comment
- [ ] Warning 3/3 displayed
- [ ] Account blocked message
- [ ] Cannot comment anymore
- [ ] Comment section disabled

### Database Persistence

- [ ] Logged out
- [ ] Logged back in
- [ ] Warning count persisted
- [ ] Block status persisted (if blocked)
- [ ] Database file exists: `database/cyberbullying.db`

---

## Documentation Review Checklist

- [ ] Read README.md
- [ ] Read QUICK_START.md
- [ ] Read DATASET_SETUP.md
- [ ] Read USER_GUIDE.md
- [ ] Understand system architecture
- [ ] Know how to present project

---

## Troubleshooting Checklist

If issues occur, check:

### Model Not Found Error
- [ ] Verified model files exist in `models/`
- [ ] Ran `python train_model.py` again
- [ ] No errors during training

### Import Errors
- [ ] All packages installed
- [ ] Python version 3.8+
- [ ] Ran pip install command

### Dataset Errors
- [ ] CSV files in `data/` directory
- [ ] Column names exactly: `Text` and `oh_label`
- [ ] No special characters in filenames
- [ ] Files not corrupted

### Streamlit Errors
- [ ] Streamlit installed
- [ ] Correct port (8501)
- [ ] No other apps using port
- [ ] Firewall not blocking

### Database Errors
- [ ] `database/` directory exists
- [ ] Sufficient disk space
- [ ] Write permissions available

---

## Presentation Preparation Checklist

### Demo Preparation

- [ ] Fresh user account ready
- [ ] Test comments prepared:
  - 2-3 safe comments
  - 2-3 cyberbullying comments
- [ ] Database cleared (optional for clean demo)
- [ ] System tested end-to-end
- [ ] Screenshots taken (optional)

### Presentation Materials

- [ ] Architecture diagrams ready
- [ ] User flow diagram available
- [ ] Model metrics documented
- [ ] Database schema explained
- [ ] Code snippets highlighted

### Demo Script

- [ ] Introduction (1-2 min)
- [ ] Architecture overview (3-4 min)
- [ ] Live demo (5-7 min)
  - [ ] Show registration
  - [ ] Show feed
  - [ ] Analyze safe comment
  - [ ] Post safe comment
  - [ ] Attempt cyberbullying
  - [ ] Show warnings
  - [ ] Demonstrate blocking
- [ ] Show database (2-3 min)
- [ ] Discuss metrics (2-3 min)
- [ ] Q&A preparation

---

## Final Verification

### Everything Working?

- [ ] ✅ Datasets loaded and trained
- [ ] ✅ Model files created
- [ ] ✅ Application runs smoothly
- [ ] ✅ Registration works
- [ ] ✅ Login works
- [ ] ✅ Comment analysis works
- [ ] ✅ Warning system works
- [ ] ✅ Blocking works
- [ ] ✅ Database persists
- [ ] ✅ No critical errors

### Ready for Evaluation?

- [ ] ✅ Code is clean and commented
- [ ] ✅ Documentation is complete
- [ ] ✅ System demonstrates all features
- [ ] ✅ Prepared for questions
- [ ] ✅ Confident in presentation

---

## 🎉 Completion

Date completed: __________

Completed by: __________

Notes:
_________________________________________
_________________________________________
_________________________________________

---

## Quick Reference Commands

```bash
# Inspect datasets
python inspect_data.py

# Train model
python train_model.py

# Verify system
python verify_system.py

# Run application
streamlit run app.py
```

---

**Status**: [ ] Ready for Submission / [ ] Needs Work

**If ready**: Congratulations! Your system is complete! 🎓

**If needs work**: Review failed checklist items above ⬆️
