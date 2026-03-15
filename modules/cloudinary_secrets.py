"""
Cloudinary Configuration Handler
Reads from Streamlit secrets in production, falls back to local config in development
"""
import streamlit as st

def get_cloudinary_config():
    """Get Cloudinary config from Streamlit secrets or local config"""
    
    # Try to load from Streamlit secrets (deployment)
    try:
        config = {
            'cloud_name': st.secrets["cloudinary"]["cloud_name"],
            'api_key': st.secrets["cloudinary"]["api_key"],
            'api_secret': st.secrets["cloudinary"]["api_secret"]
        }
        print("✅ Using Cloudinary config from Streamlit secrets (production)")
        return config
    except Exception as e:
        # Fallback to local config file (development)
        try:
            from cloudinary_config import cloudinary_config
            print("✅ Using local cloudinary_config.py (development)")
            return cloudinary_config
        except ImportError:
            print("❌ ERROR: No Cloudinary configuration found!")
            print("   - For local development: Create cloudinary_config.py")
            print("   - For deployment: Add secrets to Streamlit Cloud")
            raise Exception("Cloudinary configuration not found")

# Export the config
cloudinary_config = get_cloudinary_config()