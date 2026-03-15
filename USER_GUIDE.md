# 🎓 Cyberbullying Detection System - User Guide

## Quick Start Guide

### Step 1: Installation

1. Extract the project folder to your desired location
2. Open terminal/command prompt in the project directory
3. Run the setup script:

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
python train_model.py
```

### Step 2: Running the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

### Step 3: First Time Use

1. **Register an Account**
   - Click the "Register" tab
   - Enter a username (minimum 3 characters)
   - Enter a password (minimum 6 characters)
   - Confirm your password
   - Click "Register"

2. **Login**
   - Click the "Login" tab
   - Enter your username and password
   - Click "Login"

### Step 4: Using the System

#### Viewing the Feed
- After logging in, you'll see a social media-style feed
- Each post contains an image emoji, username, caption, and timestamp
- Your current warning count is displayed in the top right

#### Commenting on Posts
1. Click **"💬 Comment on this post"** under any post
2. Type your comment in the text box
3. Click **"🔍 Analyze Comment"**
4. Wait for the analysis result

#### Understanding Analysis Results

**Green (Safe) ✅**
- Your comment is appropriate
- You can click "📤 Post Comment" to publish
- Comment will be saved to the database

**Red (Cyberbullying) ❌**
- Your comment contains inappropriate content
- "Post Comment" button remains disabled
- You receive a warning
- Warning count increases

#### Warning System

- **Warning 1/3**: First violation notice
- **Warning 2/3**: Second violation - final warning
- **Warning 3/3**: Account blocked

**When Blocked:**
- You cannot post new comments
- You can still view the feed
- Message displayed: "Your account has been blocked"

## Features Explanation

### Real-Time Analysis
- NLP preprocessing removes noise from text
- TF-IDF converts text to numerical features
- ML model predicts cyberbullying probability
- Confidence score shows model certainty

### Severity Levels
- 🔴 **High (90%+)**: Severe cyberbullying
- 🟡 **Medium (70-90%)**: Moderate concern
- 🟠 **Low (50-70%)**: Minor concern

### Database Tracking
All activities are logged:
- User registrations
- Login attempts
- Comment analyses
- Posted comments
- Warning issuances
- Account blocks

## Example Usage Scenarios

### Scenario 1: Posting a Safe Comment

```
1. Type: "Great post! Really enjoyed this!"
2. Click "Analyze Comment"
3. Result: ✅ Safe - Confidence 95%
4. Click "Post Comment"
5. Success: Comment posted!
```

### Scenario 2: Attempting Cyberbullying

```
1. Type: "You're so stupid and worthless"
2. Click "Analyze Comment"
3. Result: ❌ Cyberbullying Detected
   - Severity: 🔴 High
   - Confidence: 92%
4. Warning: 1/3 violations
5. Post button disabled
```

### Scenario 3: Getting Blocked

```
After 3 cyberbullying attempts:
1. Warning count reaches 3/3
2. Account status: Blocked
3. Comment section disabled
4. Message: "Your account has been blocked"
```

## Understanding the System Architecture

### Data Flow
```
User Input → NLP Processing → Feature Extraction → ML Classification → Moderation → Database
```

### Processing Steps

1. **NLP Processing**
   - Converts text to lowercase
   - Removes URLs, mentions, hashtags
   - Removes special characters
   - Tokenizes into words
   - Removes common stopwords

2. **Feature Extraction**
   - Applies TF-IDF vectorization
   - Converts text to numerical features
   - Uses same vectorizer as training

3. **ML Classification**
   - Trained Logistic Regression model
   - Predicts: 0 (safe) or 1 (bullying)
   - Returns confidence score

4. **Moderation Logic**
   - Tracks warnings per user
   - Blocks after threshold (3 warnings)
   - Prevents blocked users from posting

5. **Database Storage**
   - Saves all comments
   - Tracks user status
   - Logs all actions

## Troubleshooting

### Issue: Model files not found
**Solution:**
```bash
python train_model.py
```

### Issue: Can't install packages
**Solution:**
The system will work with pre-installed packages. Core dependencies (numpy, pandas, scikit-learn) are usually available.

### Issue: Streamlit not found
**Solution:**
```bash
pip install streamlit --break-system-packages
```

### Issue: Database errors
**Solution:**
Delete `database/cyberbullying.db` and restart the app. The database will be recreated automatically.

### Issue: Login/Register not working
**Solution:**
1. Check if database exists: `database/cyberbullying.db`
2. Ensure username is 3+ characters
3. Ensure password is 6+ characters
4. Make sure passwords match (registration)

## Advanced Usage

### Adding Your Own Dataset

1. Create CSV files in the `data/` directory
2. Required columns:
   - Text column: `text`, `comment`, `tweet`, `message`, or `content`
   - Label column: `label`, `oh_label`, `class`, or `cyberbullying`
3. Labels: 0 = non-bullying, 1 = cyberbullying
4. Run training:
   ```bash
   python train_model.py
   ```

### Changing Warning Threshold

Edit `app.py`, line with `ModerationController`:
```python
moderation = ModerationController(db, warning_threshold=5)  # Change 3 to 5
```

### Using Different ML Model

Edit `train_model.py`, in the `train_model` function:
```python
train_model(texts, labels, model_type='svm')  # or 'random_forest', 'decision_tree'
```

## Academic Project Notes

### For Demonstration/Presentation

1. **Show the Architecture Diagrams**
   - User flow diagram
   - System architecture diagram

2. **Demonstrate Live**
   - Register a new user
   - Post safe comment
   - Attempt cyberbullying
   - Show warning system
   - Get account blocked

3. **Explain Technical Details**
   - NLP preprocessing steps
   - TF-IDF feature extraction
   - ML model training
   - Evaluation metrics

4. **Show Database**
   - User table with warnings
   - Comments table with labels
   - Logs table with actions

### Key Points to Highlight

✅ **Modular Architecture**: Clean separation of concerns
✅ **Real-time Detection**: Instant feedback to users
✅ **Progressive Discipline**: Warning system before blocking
✅ **Persistent Storage**: SQLite database
✅ **ML-Powered**: Supervised learning with evaluation
✅ **User-Friendly**: Social media-style interface

## System Requirements

- **OS**: Windows, Linux, macOS
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk**: 100MB for project files
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

## Performance Metrics

The sample model achieves:
- **Accuracy**: Variable based on training data
- **Precision**: High (minimizes false positives)
- **Recall**: Variable (detects cyberbullying)
- **F1 Score**: Balance of precision and recall

**Note**: Performance improves with larger, real datasets!

## FAQ

**Q: Can I use this for real social media?**
A: This is an academic project. For production use, additional security, scalability, and legal considerations are required.

**Q: How accurate is the detection?**
A: Accuracy depends on training data quality and quantity. The sample dataset is for demonstration only.

**Q: Can users appeal blocks?**
A: Currently no. This could be added as a future feature.

**Q: Is the password secure?**
A: Passwords are stored in plaintext (academic project). Production systems should use proper hashing (bcrypt, argon2).

**Q: Can I add more posts to the feed?**
A: Yes! Edit the `SAMPLE_POSTS` list in `app.py`

**Q: Does it work offline?**
A: Yes! Once set up, the entire system runs locally.

## Support

For academic purposes, refer to:
- README.md for technical documentation
- Module docstrings for code explanations
- Architecture diagrams for system flow

## Credits

- **NLP**: Text preprocessing and tokenization
- **ML**: scikit-learn for classification
- **UI**: Streamlit for web interface
- **DB**: SQLite for data persistence

---

**Remember**: This system demonstrates cyberbullying detection concepts for academic evaluation. Always practice responsible and ethical AI development!
