# 📊 Dataset Setup Guide

## Your Datasets

The system is configured to work with **4 cyberbullying detection datasets**:

1. **aggression_parsed_dataset.csv** - Aggressive content detection
2. **toxicity_parsed_dataset.csv** - Toxic comment detection  
3. **twitter_sexism_parsed_dataset.csv** - Sexism detection from Twitter
4. **youtube_parsed_dataset.csv** - Cyberbullying from YouTube comments

---

## Required CSV Format

Each CSV file **must** have these exact columns:

| Column Name | Description | Values |
|------------|-------------|--------|
| `Text` | The comment/message text | String (any text) |
| `oh_label` | Classification label | 0 or 1 |

**Label meanings:**
- `oh_label = 0` → Non-cyberbullying (safe content)
- `oh_label = 1` → Cyberbullying (harmful content)

---

## Example CSV Structure

```csv
Text,oh_label
"Great job! Keep up the good work!",0
"You're so stupid and worthless",1
"Thanks for sharing this helpful content",0
"Nobody likes you, just go away",1
"I really appreciate your help",0
"You should kill yourself",1
```

---

## Setup Instructions

### Step 1: Locate Your Datasets

You should have these 4 CSV files downloaded/prepared:
```
✓ aggression_parsed_dataset.csv
✓ toxicity_parsed_dataset.csv
✓ twitter_sexism_parsed_dataset.csv
✓ youtube_parsed_dataset.csv
```

### Step 2: Copy to Data Directory

```bash
# Navigate to project directory
cd cyberbullying_detection_system

# Create data directory if it doesn't exist
mkdir -p data

# Copy your CSV files to the data directory
cp /path/to/your/csvfiles/*.csv data/

# Or manually move them to:
# cyberbullying_detection_system/data/
```

Your directory structure should look like:
```
cyberbullying_detection_system/
├── data/
│   ├── aggression_parsed_dataset.csv
│   ├── toxicity_parsed_dataset.csv
│   ├── twitter_sexism_parsed_dataset.csv
│   └── youtube_parsed_dataset.csv
├── modules/
├── models/
├── app.py
└── train_model.py
```

### Step 3: Verify Dataset Format

Run the inspection script:

```bash
python inspect_data.py
```

**What this does:**
✅ Checks if files exist  
✅ Validates column names  
✅ Counts total samples  
✅ Shows class distribution  
✅ Displays sample texts  
✅ Checks data quality  

**Expected output:**
```
📄 FILE 1: aggression_parsed_dataset.csv
============================================
✅ Text column found
✅ oh_label column found

Label Distribution:
  Non-cyberbullying (0): XXX (XX%)
  Cyberbullying (1): XXX (XX%)

✅ File processed successfully!
```

### Step 4: Fix Common Issues

#### Issue 1: Wrong Column Names

**Problem:**
```
❌ Text column not found
❌ oh_label column not found
```

**Solution:**
Open your CSV and ensure columns are named exactly:
- `Text` (capital T)
- `oh_label` (lowercase oh, underscore, lowercase label)

#### Issue 2: Missing Values

**Problem:**
```
Missing Text values: 150
Missing oh_label values: 50
```

**Solution:**
The system will automatically remove rows with missing values, but you may want to clean your data first.

#### Issue 3: Incorrect Labels

**Problem:**
Labels are not 0 or 1 (e.g., "yes"/"no", "safe"/"bullying")

**Solution:**
Convert your labels to numeric:
- Non-cyberbullying → 0
- Cyberbullying → 1

You can use Excel, Python, or any tool to convert.

---

## Dataset Statistics

After running `inspect_data.py`, you'll see:

### Per-File Statistics
- Total rows
- Column names
- Missing values
- Label distribution
- Text length statistics
- Sample texts

### Overall Statistics
- Combined dataset size
- Total cyberbullying vs non-cyberbullying
- Class balance ratio

**Good class balance**: 40-60% split  
**Acceptable**: 30-70% split  
**Poor**: <30% or >70% (very imbalanced)

---

## Training the Model

Once datasets are verified:

```bash
python train_model.py
```

**What happens:**
1. ✅ Loads all 4 CSV files
2. ✅ Combines into single dataset
3. ✅ Removes duplicates and missing values
4. ✅ Preprocesses text (NLP)
5. ✅ Extracts features (TF-IDF)
6. ✅ Trains ML model
7. ✅ Evaluates performance
8. ✅ Saves model files

**Expected output:**
```
Found 4 CSV file(s):
  - aggression_parsed_dataset.csv
  - toxicity_parsed_dataset.csv
  - twitter_sexism_parsed_dataset.csv
  - youtube_parsed_dataset.csv

✅ TOTAL SAMPLES LOADED: X,XXX

[1/5] Preprocessing text data...
✅ Preprocessed X,XXX texts

[2/5] Extracting TF-IDF features...
✅ Feature matrix shape: (X,XXX, 5000)

[3/5] Splitting data...
✅ Training set: X,XXX samples
✅ Test set: XXX samples

[4/5] Training logistic_regression model...
Training completed!

[5/5] Evaluating model...
Accuracy:  0.XXXX
Precision: 0.XXXX
Recall:    0.XXXX
F1 Score:  0.XXXX

✅ TRAINING COMPLETED SUCCESSFULLY!
```

---

## Dataset Quality Tips

### 1. Balanced Classes
Try to have roughly equal numbers of:
- Cyberbullying examples (oh_label=1)
- Non-cyberbullying examples (oh_label=0)

### 2. Diverse Examples
Include variety:
- Different types of cyberbullying (insults, threats, harassment)
- Different types of normal content (comments, questions, praise)

### 3. Clean Text
Remove or handle:
- Excessive special characters
- URLs (system handles this)
- Emojis (if problematic)
- Very short texts (<3 words)

### 4. Sufficient Data
Recommended minimum:
- **1,000+ samples** for basic testing
- **5,000+ samples** for good performance
- **10,000+ samples** for excellent results

---

## Troubleshooting

### CSV File Not Loading

**Check:**
1. File is in `data/` directory
2. File extension is `.csv`
3. File is not corrupted
4. Columns are named correctly

### Empty Dataset After Loading

**Check:**
1. CSV actually has data rows
2. Encoding is UTF-8
3. No hidden characters in column names

### Low Model Accuracy

**Causes:**
1. Imbalanced dataset (90% one class)
2. Too few samples (<1000)
3. Poor quality labels
4. Text too similar between classes

**Solutions:**
1. Balance your dataset
2. Collect more data
3. Review and fix labels
4. Add more diverse examples

---

## Quick Commands Reference

```bash
# Inspect datasets
python inspect_data.py

# Train model
python train_model.py

# Run application
streamlit run app.py

# Verify system
python verify_system.py
```

---

## Need Sample Data?

If you don't have the datasets yet, create a sample:

```bash
python inspect_data.py --create-sample
```

This creates `data/sample_dataset.csv` with 10 examples for testing.

---

## Ready to Train?

Once you have:
✅ All 4 CSV files in `data/` directory  
✅ Verified with `inspect_data.py`  
✅ No errors or warnings  

**Run:**
```bash
python train_model.py
```

The model will be ready in a few minutes (depending on dataset size)!

---

## Support

If you encounter issues:
1. Run `python inspect_data.py` first
2. Check error messages carefully
3. Verify CSV format matches this guide
4. Review troubleshooting section above

Good luck! 🚀
