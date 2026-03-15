"""
Firebase Configuration Handler
Reads from Streamlit secrets in production, falls back to local config in development
"""
import streamlit as st
import os
import sys

def get_firebase_config():
    """Get Firebase config from Streamlit secrets or local config"""
    
    # Try to load from Streamlit secrets (deployment)
    try:
        # Check if secrets exist
        if hasattr(st, 'secrets') and 'firebase' in st.secrets:
            config = {
                "apiKey": st.secrets["firebase"]["apiKey"],
                "authDomain": st.secrets["firebase"]["authDomain"],
                "databaseURL": st.secrets["firebase"]["databaseURL"],
                "projectId": st.secrets["firebase"]["projectId"],
                "storageBucket": st.secrets["firebase"]["storageBucket"],
                "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
                "appId": st.secrets["firebase"]["appId"]
            }
            print("✅ Using Firebase config from Streamlit secrets (production)")
            return config
        else:
            print("⚠️ Streamlit secrets not found, trying local config...")
            raise KeyError("Secrets not configured")
            
    except (KeyError, AttributeError) as e:
        print(f"⚠️ Error reading secrets: {e}")
        # Fallback to local config file (development)
        try:
            # Add parent directory to path to import firebase_config
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, parent_dir)
            from firebase_config import firebase_config
            print("✅ Using local firebase_config.py (development)")
            return firebase_config
        except ImportError as ie:
            print("❌ ERROR: No Firebase configuration found!")
            print(f"   Import error: {ie}")
            print("   - For local development: Create firebase_config.py")
            print("   - For deployment: Add secrets to Streamlit Cloud")
            # Return a dummy config to prevent total crash - will fail at Firebase init
            return {
                "apiKey": "MISSING",
                "authDomain": "MISSING",
                "databaseURL": "MISSING",
                "projectId": "MISSING",
                "storageBucket": "MISSING",
                "messagingSenderId": "MISSING",
                "appId": "MISSING"
            }

# Export the config
firebase_config = get_firebase_config()