"""
Cyberbullying Detection System - Main Streamlit Application
Social Media Style Interface with Real-time Comment Analysis
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.database import DatabaseManager
from modules.authentication import AuthenticationManager
from modules.moderation import ModerationController, FeedbackNotification

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="SafeSpace - Cyberbullying Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .post-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid #dee2e6;
    }
    .safe-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .danger-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SYSTEM ====================

@st.cache_resource
def initialize_system():
    """Initialize all system components"""
    db = DatabaseManager()
    auth = AuthenticationManager(db)
    moderation = ModerationController(db, warning_threshold=3)
    
    # Load trained model and vectorizer
    model_path = 'models/cyberbullying_classifier.pkl'
    vectorizer_path = 'models/tfidf_vectorizer.pkl'
    
    model = None
    vectorizer = None
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            import joblib
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            print("✅ Model and vectorizer loaded successfully")
        except Exception as e:
            st.error(f"⚠️ Error loading model: {str(e)}")
            st.error("Please run: python train_model.py")
    else:
        st.error("⚠️ Model files not found. Please train the model first by running 'train_model.py'")
    
    return db, auth, model, vectorizer, moderation

# Initialize components
db, auth, model, vectorizer, moderation = initialize_system()

# ==================== SAMPLE POSTS DATA ====================

SAMPLE_POSTS = [
    {
        'id': 1,
        'username': 'travel_explorer',
        'image': '🏖️',
        'caption': 'Beautiful sunset at the beach! #travel #nature',
        'time': '2 hours ago'
    },
    {
        'id': 2,
        'username': 'foodie_heaven',
        'image': '🍕',
        'caption': 'Best pizza in town! Highly recommend 🍕',
        'time': '4 hours ago'
    },
    {
        'id': 3,
        'username': 'fitness_guru',
        'image': '💪',
        'caption': 'Morning workout complete! Stay active, stay healthy 💪',
        'time': '6 hours ago'
    },
    {
        'id': 4,
        'username': 'tech_enthusiast',
        'image': '💻',
        'caption': 'Just built my new gaming PC! Specs in comments',
        'time': '8 hours ago'
    },
    {
        'id': 5,
        'username': 'book_lover',
        'image': '📚',
        'caption': 'Finished reading an amazing book today. What are you reading?',
        'time': '10 hours ago'
    },
    {
        'id': 6,
        'username': 'music_addict',
        'image': '🎵',
        'caption': 'New album just dropped! On repeat all day 🎧',
        'time': '12 hours ago'
    },
    {
        'id': 7,
        'username': 'pet_paradise',
        'image': '🐶',
        'caption': 'My dog learned a new trick today! So proud 🐕',
        'time': '14 hours ago'
    },
    {
        'id': 8,
        'username': 'art_creator',
        'image': '🎨',
        'caption': 'Finished my latest painting. What do you think?',
        'time': '16 hours ago'
    }
]

# ==================== SESSION STATE ====================

def initialize_session_state():
    """Initialize session state variables"""
    auth.initialize_session_state()
    
    if 'comment_text' not in st.session_state:
        st.session_state.comment_text = {}
    
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = {}
    
    if 'selected_post' not in st.session_state:
        st.session_state.selected_post = None

initialize_session_state()

# ==================== AUTHENTICATION UI ====================

def show_login_page():
    """Display login/registration page"""
    st.markdown("<h1 class='main-header'>🛡️ SafeSpace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>A Cyberbullying Detection Platform</p>", unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login to your account")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                if username and password:
                    success, message = auth.login(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter username and password")
        
        with tab2:
            st.subheader("Create new account")
            
            new_username = st.text_input("Username", key="reg_username")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", use_container_width=True):
                success, message = auth.register(new_username, new_password, confirm_password)
                if success:
                    st.success(message)
                    st.info("Please login with your credentials")
                else:
                    st.error(message)

# ==================== MAIN FEED UI ====================

def analyze_comment(post_id, comment_text):
    """Analyze a comment for cyberbullying"""
    # Check if user can post
    can_post, message = auth.can_post_comment()
    if not can_post:
        st.error(message)
        return
    
    # Check if model and vectorizer are loaded
    if model is None or vectorizer is None:
        st.error("⚠️ Model not loaded. Please run: python train_model.py")
        return
    
    try:
        # Transform text using vectorizer (it handles preprocessing internally)
        # The TfidfVectorizer with stop_words='english' does the preprocessing
        features = vectorizer.transform([comment_text])
        
        # Get prediction and probability
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(max(probabilities))
        
        # Store result
        st.session_state.analysis_result[post_id] = {
            'label': int(prediction),
            'confidence': confidence,
            'is_cyberbullying': bool(prediction == 1),
            'original_text': comment_text
        }
        
        # If cyberbullying detected, track offense
        if prediction == 1:
            username = auth.get_current_user()
            moderation_result = moderation.track_offense(username)
            st.session_state.analysis_result[post_id]['moderation'] = moderation_result
            
            # Update user info
            auth.update_user_info()
    
    except Exception as e:
        st.error(f"❌ Error analyzing comment: {str(e)}")
        import traceback
        traceback.print_exc()

def post_comment(post_id):
    """Post a comment after successful analysis"""
    if post_id in st.session_state.analysis_result:
        result = st.session_state.analysis_result[post_id]
        
        # Only allow posting if comment is safe
        if result['label'] == 0:
            username = auth.get_current_user()
            db.save_comment(
                username=username,
                post_id=post_id,
                comment_text=result['original_text'],
                label=result['label'],
                confidence=result['confidence']
            )
            
            st.success("✅ Comment posted successfully!")
            
            # Clear comment data
            st.session_state.comment_text[post_id] = ""
            del st.session_state.analysis_result[post_id]
            
        else:
            st.error("❌ Cannot post cyberbullying content!")

def show_feed():
    """Display social media feed"""
    # Header with user info
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h1 class='main-header'>🛡️ SafeSpace Feed</h1>", unsafe_allow_html=True)
    
    with col2:
        user_info = auth.get_user_info()
        st.write(f"**User:** {user_info['username']}")
        st.write(f"**Warnings:** {user_info['warning_count']}/3")
        
        if st.button("Logout"):
            auth.logout()
            st.rerun()
    
    st.divider()
    
    # Check if user is blocked
    if user_info['is_blocked']:
        st.error("🚫 **Your account has been blocked due to repeated violations.**")
        st.info("You can view posts but cannot comment.")
        st.divider()
    
    # Display posts
    for post in SAMPLE_POSTS:
        post_id = post['id']
        
        # Post card
        with st.container():
            st.markdown(f"<div class='post-card'>", unsafe_allow_html=True)
            
            # Post header
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {post['image']} @{post['username']}")
            with col2:
                st.caption(post['time'])
            
            # Post caption
            st.write(post['caption'])
            st.write("")
            
            # Comment section
            with st.expander(f"💬 Comment on this post", expanded=False):
                # Initialize comment text
                if post_id not in st.session_state.comment_text:
                    st.session_state.comment_text[post_id] = ""
                
                # Comment input
                comment = st.text_area(
                    "Write your comment...",
                    value=st.session_state.comment_text[post_id],
                    key=f"comment_input_{post_id}",
                    height=100,
                    disabled=user_info['is_blocked']
                )
                
                # Store comment text
                st.session_state.comment_text[post_id] = comment
                
                # Buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    analyze_btn = st.button(
                        "🔍 Analyze Comment",
                        key=f"analyze_{post_id}",
                        disabled=user_info['is_blocked'] or not comment.strip(),
                        use_container_width=True
                    )
                
                with col2:
                    # Post button - only enabled if comment is safe
                    can_post_btn = (
                        post_id in st.session_state.analysis_result and
                        st.session_state.analysis_result[post_id]['label'] == 0
                    )
                    
                    post_btn = st.button(
                        "📤 Post Comment",
                        key=f"post_{post_id}",
                        disabled=not can_post_btn,
                        use_container_width=True
                    )
                
                # Handle analyze button
                if analyze_btn:
                    with st.spinner("Analyzing comment..."):
                        analyze_comment(post_id, comment)
                        st.rerun()
                
                # Handle post button
                if post_btn:
                    post_comment(post_id)
                    st.rerun()
                
                # Show analysis result
                if post_id in st.session_state.analysis_result:
                    result = st.session_state.analysis_result[post_id]
                    feedback = FeedbackNotification.show_result(
                        result['label'],
                        result['confidence']
                    )
                    
                    st.write("")
                    
                    if feedback['status'] == 'safe':
                        st.markdown(f"""
                        <div class='safe-message'>
                            <strong>{feedback['icon']} {feedback['message']}</strong><br>
                            Confidence: {feedback['confidence']:.2%}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:
                        st.markdown(f"""
                        <div class='danger-message'>
                            <strong>{feedback['icon']} {feedback['message']}</strong><br>
                            Severity Level: {feedback['level']}<br>
                            Confidence: {feedback['confidence']:.2%}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show moderation result
                        if 'moderation' in result:
                            mod_result = result['moderation']
                            
                            if mod_result['action'] == 'BLOCK':
                                st.markdown(f"""
                                <div class='danger-message'>
                                    <strong>🚫 ACCOUNT BLOCKED</strong><br>
                                    {mod_result['message']}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class='warning-message'>
                                    <strong>⚠️ WARNING ISSUED</strong><br>
                                    {mod_result['message']}
                                </div>
                                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("")

# ==================== MAIN APP ====================

def main():
    """Main application"""
    if not auth.is_authenticated():
        show_login_page()
    else:
        show_feed()

if __name__ == "__main__":
    main()
