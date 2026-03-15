"""
Cloudinary Configuration Handler
Reads from Streamlit secrets in production, falls back to local config in development
"""
import streamlit as st
import os
import sys

def get_cloudinary_config():
    """Get Cloudinary config from Streamlit secrets or local config"""
    
    # Try to load from Streamlit secrets (deployment)
    try:
        # Check if secrets exist
        if hasattr(st, 'secrets') and 'cloudinary' in st.secrets:
            config = {
                'cloud_name': st.secrets["cloudinary"]["cloud_name"],
                'api_key': st.secrets["cloudinary"]["api_key"],
                'api_secret': st.secrets["cloudinary"]["api_secret"]
            }
            print("✅ Using Cloudinary config from Streamlit secrets (production)")
            return config
        else:
            print("⚠️ Streamlit secrets not found, trying local config...")
            raise KeyError("Secrets not configured")
            
    except (KeyError, AttributeError) as e:
        print(f"⚠️ Error reading secrets: {e}")
        # Fallback to local config file (development)
        try:
            # Add parent directory to path to import cloudinary_config
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, parent_dir)
            from cloudinary_config import cloudinary_config
            print("✅ Using local cloudinary_config.py (development)")
            return cloudinary_config
        except ImportError as ie:
            print("❌ ERROR: No Cloudinary configuration found!")
            print(f"   Import error: {ie}")
            print("   - For local development: Create cloudinary_config.py")
            print("   - For deployment: Add secrets to Streamlit Cloud")
            # Return dummy config
            return {
                'cloud_name': 'MISSING',
                'api_key': 'MISSING',
                'api_secret': 'MISSING'
            }

# Export the config
cloudinary_config = get_cloudinary_config()