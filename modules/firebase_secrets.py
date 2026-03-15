"""
Firebase Configuration Handler
Reads from Streamlit secrets in production, falls back to local config in development
"""
import streamlit as st
import os

def get_firebase_config():
    """Get Firebase config from Streamlit secrets or local config"""
    
    # Try to load from Streamlit secrets (deployment)
    try:
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
    except Exception as e:
        # Fallback to local config file (development)
        try:
            from firebase_config import firebase_config
            print("✅ Using local firebase_config.py (development)")
            return firebase_config
        except ImportError:
            print("❌ ERROR: No Firebase configuration found!")
            print("   - For local development: Create firebase_config.py")
            print("   - For deployment: Add secrets to Streamlit Cloud")
            raise Exception("Firebase configuration not found")

# Export the config
firebase_config = get_firebase_config()