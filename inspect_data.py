"""
Dataset Inspection and Validation Script
Analyzes CSV files in the data directory
"""

import pandas as pd
import os
from collections import Counter

def inspect_datasets(data_dir='data'):
    """
    Inspect all CSV files in the data directory
    
    Args:
        data_dir (str): Directory containing CSV files
    """
    print("="*70)
    print("  DATASET INSPECTION TOOL")
    print("="*70)
    
    # Check if directory exists
    if not os.path.exists(data_dir):
        print(f"\n❌ Directory '{data_dir}' not found!")
        print(f"\nPlease create the '{data_dir}' directory and add your CSV files.")
        return
    
    # Get CSV files
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"\n❌ No CSV files found in '{data_dir}' directory!")
        print(f"\nExpected CSV files with columns:")
        print("  - Text: Comment/message text")
        print("  - oh_label: 0 (non-cyberbullying) or 1 (cyberbullying)")
        return
    
    print(f"\n✅ Found {len(csv_files)} CSV file(s) in '{data_dir}' directory\n")
    
    total_samples = 0
    total_cyberbullying = 0
    total_non_cyberbullying = 0
    
    for i, csv_file in enumerate(csv_files, 1):
        filepath = os.path.join(data_dir, csv_file)
        
        print("="*70)
        print(f"📄 FILE {i}: {csv_file}")
        print("="*70)
        
        try:
            # Load CSV
            df = pd.read_csv(filepath)
            
            # Basic info
            print(f"\n📊 BASIC INFORMATION:")
            print(f"   Total rows: {len(df)}")
            print(f"   Total columns: {len(df.columns)}")
            print(f"   Columns: {df.columns.tolist()}")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Check for required columns
            has_text = 'Text' in df.columns or 'text' in df.columns
            has_label = 'oh_label' in df.columns or 'OH_label' in df.columns or 'Oh_label' in df.columns
            
            print(f"\n✓ COLUMN VALIDATION:")
            print(f"   {'✅' if has_text else '❌'} Text column found")
            print(f"   {'✅' if has_label else '❌'} oh_label column found")
            
            if not has_text or not has_label:
                print(f"\n   ⚠️  WARNING: Required columns missing!")
                print(f"   Expected: 'Text' and 'oh_label'")
                continue
            
            # Find actual column names (case-insensitive)
            text_col = next((col for col in df.columns if col.lower() == 'text'), None)
            label_col = next((col for col in df.columns if col.lower() == 'oh_label'), None)
            
            # Check for missing values
            text_missing = df[text_col].isna().sum()
            label_missing = df[label_col].isna().sum()
            
            print(f"\n📋 DATA QUALITY:")
            print(f"   Missing Text values: {text_missing}")
            print(f"   Missing oh_label values: {label_missing}")
            
            # Clean data
            df_clean = df.dropna(subset=[text_col, label_col])
            
            # Label distribution
            label_counts = df_clean[label_col].value_counts().to_dict()
            non_cyber = label_counts.get(0, 0)
            cyber = label_counts.get(1, 0)
            
            print(f"\n📈 LABEL DISTRIBUTION:")
            print(f"   Non-cyberbullying (0): {non_cyber:,} ({non_cyber/len(df_clean)*100:.1f}%)")
            print(f"   Cyberbullying (1): {cyber:,} ({cyber/len(df_clean)*100:.1f}%)")
            
            # Text statistics
            text_lengths = df_clean[text_col].astype(str).str.len()
            print(f"\n📝 TEXT STATISTICS:")
            print(f"   Avg text length: {text_lengths.mean():.1f} characters")
            print(f"   Min text length: {text_lengths.min()} characters")
            print(f"   Max text length: {text_lengths.max()} characters")
            
            # Sample texts
            print(f"\n💬 SAMPLE TEXTS:")
            print(f"\n   Non-cyberbullying examples:")
            non_cyber_samples = df_clean[df_clean[label_col] == 0][text_col].head(2)
            for idx, text in enumerate(non_cyber_samples, 1):
                text_preview = str(text)[:80] + "..." if len(str(text)) > 80 else str(text)
                print(f"   {idx}. {text_preview}")
            
            print(f"\n   Cyberbullying examples:")
            cyber_samples = df_clean[df_clean[label_col] == 1][text_col].head(2)
            for idx, text in enumerate(cyber_samples, 1):
                text_preview = str(text)[:80] + "..." if len(str(text)) > 80 else str(text)
                print(f"   {idx}. {text_preview}")
            
            # Update totals
            total_samples += len(df_clean)
            total_non_cyberbullying += non_cyber
            total_cyberbullying += cyber
            
            print(f"\n✅ File processed successfully!")
            
        except Exception as e:
            print(f"\n❌ ERROR processing file: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
    
    # Overall summary
    print("="*70)
    print("📊 OVERALL SUMMARY")
    print("="*70)
    print(f"\nTotal files processed: {len(csv_files)}")
    print(f"Total samples: {total_samples:,}")
    print(f"\nClass Distribution:")
    print(f"  Non-cyberbullying (0): {total_non_cyberbullying:,} ({total_non_cyberbullying/total_samples*100:.1f}%)")
    print(f"  Cyberbullying (1): {total_cyberbullying:,} ({total_cyberbullying/total_samples*100:.1f}%)")
    
    # Check class balance
    balance_ratio = min(total_cyberbullying, total_non_cyberbullying) / max(total_cyberbullying, total_non_cyberbullying)
    print(f"\nClass balance ratio: {balance_ratio:.2f}")
    
    if balance_ratio < 0.3:
        print("⚠️  WARNING: Severe class imbalance detected!")
        print("   Consider balancing your dataset for better model performance.")
    elif balance_ratio < 0.5:
        print("⚠️  Moderate class imbalance detected.")
    else:
        print("✅ Dataset is reasonably balanced.")
    
    print("\n" + "="*70)
    print("✅ DATASET INSPECTION COMPLETE")
    print("="*70)
    
    if total_samples > 0:
        print("\n🚀 NEXT STEPS:")
        print("   1. Review the statistics above")
        print("   2. Ensure data quality is acceptable")
        print("   3. Run: python train_model.py")
        print("   4. The model will be trained on all CSV files combined")
    else:
        print("\n⚠️  NO VALID DATA FOUND")
        print("   Please check your CSV files and try again.")
    
    print()


def create_sample_csv():
    """Create a sample CSV file for testing"""
    print("\n" + "="*70)
    print("  CREATING SAMPLE CSV FILE")
    print("="*70)
    
    # Sample data
    data = {
        'Text': [
            "You're so stupid and worthless",
            "Great job! Keep up the good work!",
            "Nobody likes you, loser",
            "I really appreciate your help",
            "You should kill yourself",
            "This is amazing content!",
            "You're ugly and dumb",
            "Thanks for sharing this",
            "Everyone hates you",
            "Well done, proud of you!"
        ],
        'oh_label': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    }
    
    df = pd.DataFrame(data)
    
    # Save to data directory
    os.makedirs('data', exist_ok=True)
    filepath = 'data/sample_dataset.csv'
    df.to_csv(filepath, index=False)
    
    print(f"\n✅ Created sample file: {filepath}")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {df.columns.tolist()}")
    print("\nYou can use this as a template for your own datasets!")
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create-sample':
        create_sample_csv()
    else:
        inspect_datasets('data')
