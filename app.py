"""
SafeSpace - Social Media Platform with Cyberbullying Detection
Complete social media app with Firebase backend and URL routing
"""

import streamlit as st
import os
import sys
from datetime import datetime
import joblib
from PIL import Image

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.firebase_database import FirebaseManager
from modules.firebase_auth import FirebaseAuthManager
from modules.cloudinary_upload import CloudinaryManager
from modules.moderation import ModerationController, FeedbackNotification

# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="SafeSpace - Social Media",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== URL ROUTING UTILITIES ====================

def get_query_params():
    """Get current URL query parameters"""
    return st.query_params

def set_route(route):
    """Set the current route in URL"""
    st.query_params["page"] = route

def get_current_route():
    """Get the current route from URL"""
    params = get_query_params()
    return params.get("page", "/")

def navigate_to(route):
    """Navigate to a specific route"""
    set_route(route)
    st.rerun()

# ==================== GLOBAL HEADER COMPONENT ====================

def render_header(show_auth=True):
    """
    Reusable header/navigation component.
    Uses st.columns + st.button for navigation so st.session_state
    (and therefore auth state) is preserved across page changes.

    Args:
        show_auth: Whether to show login/register buttons (False for landing page)
    """
    import streamlit.components.v1 as _components

    is_logged_in = auth.is_authenticated()
    current_route = get_current_route()

    # ── CSS ──────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
        /* Hide Streamlit's fixed toolbar */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Remove the top gap left by the hidden toolbar */
        section.main > div.block-container {
            padding-top: 0 !important;
            padding-bottom: 1rem !important;
        }
        div.block-container {
            padding-top: 0 !important;
        }

        /* ── Header row styling (class added by JS) ── */
        .gh-header-row {
            background: rgba(255, 255, 255, 0.97) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-bottom: 1px solid #e8e8e8 !important;
            box-shadow: 0 1px 10px rgba(0, 0, 0, 0.07) !important;
            padding: 0 1.5rem !important;
            margin-bottom: 1.5rem !important;
            align-items: center !important;
            min-height: 54px !important;
            gap: 0 !important;
        }

        /* Vertically center every column inside the header */
        .gh-header-row [data-testid="column"] {
            display: flex !important;
            align-items: center !important;
            padding-top: 0.2rem !important;
            padding-bottom: 0.2rem !important;
        }

        /* Logo area */
        .gh-logo-area {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom : 17px;
        }
        .gh-logo {
            width: 34px; height: 34px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 9px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
            flex-shrink: 0;
        }
        .gh-brand {
            font-size: 1.2rem; font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.3px; white-space: nowrap;
        }

        /* Nav + action buttons — ghost/pill style */
        .gh-header-row .stButton > button {
            border: none !important;
            background: transparent !important;
            color: #555 !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            padding: 0.38rem 0.75rem !important;
            border-radius: 7px !important;
            height: auto !important;
            min-height: unset !important;
            line-height: 1.2 !important;
        }
        .gh-header-row .stButton > button:hover {
            background: #f0f0ff !important;
            color: #667eea !important;
        }

        /* Logout / Login outlined buttons */
        .gh-header-row .stButton > button[kind="secondary"] {
            border: 1px solid #e0e0e0 !important;
            color: #777 !important;
            font-size: 0.82rem !important;
        }
        .gh-header-row .stButton > button[kind="secondary"]:hover {
            background: #fff0f0 !important;
            color: #d93025 !important;
            border-color: #f5c0b8 !important;
        }

        /* Register primary button */
        .gh-header-row .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #fff !important;
            border: none !important;
        }
        .gh-header-row .stButton > button[kind="primary"]:hover {
            opacity: 0.88 !important;
        }

        /* Avatar image */
        .gh-avatar {
            width: 32px; height: 32px;
            border-radius: 50%; object-fit: cover;
            border: 2px solid #ddd; cursor: pointer;
            vertical-align: middle; display: block;
            transition: border-color 0.2s, transform 0.2s;
        }
        .gh-avatar:hover { border-color: #667eea; transform: scale(1.08); }

        /* Welcome badge */
        .gh-welcome {
            display: inline-flex; align-items: center; gap: 0.35rem;
            background: rgba(102, 126, 234, 0.08);
            border: 1px solid rgba(102, 126, 234, 0.2);
            color: #667eea; font-size: 0.85rem; font-weight: 500;
            padding: 0.3rem 0.8rem; border-radius: 20px; white-space: nowrap;
            margin-bottom: 17px;
        }

        @media (max-width: 768px) {
            .gh-header-row { padding: 0 0.75rem !important; }
            .gh-brand      { font-size: 1rem; }
            .gh-header-row .stButton > button {
                font-size: 0.8rem !important;
                padding: 0.3rem 0.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Header columns (Streamlit buttons preserve session state) ─────────
    col_left, col_center, col_right = st.columns([2, 4, 2])

    with col_left:
        st.markdown("""
        <div class="gh-logo-area">
            <div class="gh-logo">🛡️</div>
            <span class="gh-brand">SafeSpace</span>
        </div>
        """, unsafe_allow_html=True)

    with col_center:
        if is_logged_in:
            nc1, nc2, nc3, nc4 = st.columns(4)
            with nc1:
                if st.button("🏠 Feed", key="nav_feed", use_container_width=True):
                    navigate_to("/feed")
            with nc2:
                if st.button("➕ Create", key="nav_create", use_container_width=True):
                    navigate_to("/create-post")
            with nc3:
                if st.button("🔍 Search", key="nav_search", use_container_width=True):
                    navigate_to("/search")
            with nc4:
                if st.button("👤 Profile", key="nav_profile", use_container_width=True):
                    navigate_to("/profile")
        else:
            if show_auth:
                st.markdown(
                    '<div style="display:flex;justify-content:center;">'
                    '<span class="gh-welcome">✨ Welcome to SafeSpace</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )

    with col_right:
        if is_logged_in:
            user_data = auth.get_user_data()
            if user_data:
                profile_pic = user_data.get('profile_picture', '').strip()
                if not profile_pic:
                    profile_pic = cloudinary.get_default_profile_picture()
                rc1, rc2 = st.columns([1, 2])
                with rc1:
                    st.markdown(
                        f'<img src="{profile_pic}" class="gh-avatar" alt="Profile">',
                        unsafe_allow_html=True,
                    )
                with rc2:
                    if st.button("Logout", key="header_logout", use_container_width=True):
                        auth.logout()
                        navigate_to("/")
        else:
            if show_auth:
                rc1, rc2 = st.columns(2)
                with rc1:
                    if st.button("Login", key="header_login", use_container_width=True):
                        navigate_to("/login")
                with rc2:
                    if st.button("Register", key="header_register",
                                 use_container_width=True, type="primary"):
                        navigate_to("/register")

    # ── Apply header bar styling to the columns row via JS ────────────────
    # components.html runs in an iframe; window.parent accesses the Streamlit DOM.
    _components.html("""
    <script>
        (function tag() {
            try {
                var doc = window.parent.document;
                var blocks = doc.querySelectorAll('[data-testid="stHorizontalBlock"]');
                if (blocks.length > 0) {
                    blocks[0].classList.add('gh-header-row');
                } else {
                    setTimeout(tag, 80);
                }
            } catch (e) { setTimeout(tag, 80); }
        })();
    </script>
    """, height=0)

# ==================== CUSTOM CSS ====================

st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Font */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main Container - Light Gray Background */
    .main {
        background-color: #fafafa;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.5rem;
        color: #262626;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Post Card - Instagram Style */
    .post-card {
        background-color: #ffffff;
        padding: 0;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #dbdbdb;
    }
    
    /* Profile Header */
    .profile-header {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #dbdbdb;
        margin-bottom: 2rem;
    }
    
    /* Success Message - Green */
    .safe-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .safe-message strong {
        color: #155724;
    }
    
    /* Danger Message - Red */
    .danger-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .danger-message strong {
        color: #721c24;
    }
    
    /* Warning Message - Yellow */
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .warning-message strong {
        color: #856404;
    }
    
    /* Feed Images - SIGNIFICANTLY REDUCED */
    .post-image-wrapper {
        width: 100%;
        max-width: 500px;
        margin: 12px auto;
        display: block;
    }
    
    .post-image-wrapper img {
        width: 100%;
        height: auto;
        max-height: 350px;
        object-fit: cover;
        border-radius: 8px;
        display: block;
    }
    
    /* Stat Box - Clean Card */
    .stat-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dbdbdb;
    }
    
    /* Buttons - Instagram Style */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 8px 16px;
        border: 1px solid #dbdbdb;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #fafafa;
    }
    
    /* Primary Button - Blue */
    .stButton>button[kind="primary"] {
        background-color: #0095f6;
        color: white;
        border: none;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: #1877f2;
    }
    
    /* Text Inputs - Clean */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #dbdbdb;
        padding: 10px 12px;
        background-color: #fafafa;
        color: #262626;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #a8a8a8;
        background-color: #ffffff;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 1px dashed #dbdbdb;
        border-radius: 8px;
        padding: 2rem;
        background-color: #fafafa;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #dbdbdb;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        color: #8e8e8e;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        color: #262626;
        border-bottom: 2px solid #262626;
    }
    
    /* Metrics - Clean Numbers */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #262626;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8e8e8e;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #dbdbdb;
        margin: 1.5rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: transparent;
        color: #262626;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Links */
    a {
        color: #0095f6;
        text-decoration: none;
    }
    
    a:hover {
        color: #1877f2;
    }
    
    /* Landing Page Styles */
    .hero-section {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d3b4f 100%);
        min-height: 100vh;
        padding: 2rem;
        position: relative;
        margin: -5rem -5rem;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: white;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.7;
        max-width: 650px;
        margin-bottom: 2rem;
    }
    
    .feature-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin-top: 4rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(0, 149, 246, 0.3);
    }
    
    .feature-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0095f6;
        margin-bottom: 1rem;
    }
    
    .feature-text {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SYSTEM ====================

@st.cache_resource
def initialize_system():
    """Initialize all system components"""
    firebase = FirebaseManager()
    auth = FirebaseAuthManager(firebase)
    cloudinary = CloudinaryManager()
    moderation = ModerationController(firebase, warning_threshold=3)
    
    model_path = 'models/cyberbullying_classifier.pkl'
    vectorizer_path = 'models/tfidf_vectorizer.pkl'
    
    model = None
    vectorizer = None
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            print("✅ ML Model loaded successfully")
        except Exception as e:
            st.error(f"⚠️ Error loading ML model: {str(e)}")
    
    return firebase, auth, cloudinary, moderation, model, vectorizer

firebase, auth, cloudinary, moderation, model, vectorizer = initialize_system()

# ==================== SESSION STATE ====================

def initialize_session_state():
    """Initialize session state variables"""
    auth.initialize_session_state()
    
    if 'selected_user_id' not in st.session_state:
        st.session_state.selected_user_id = None
    
    if 'comment_text' not in st.session_state:
        st.session_state.comment_text = {}
    
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = {}

initialize_session_state()

# ==================== HELPER FUNCTIONS ====================

def analyze_comment(post_id, comment_text):
    """Analyze a comment for cyberbullying"""
    can_post, message = auth.can_post_comment()
    if not can_post:
        st.error(message)
        return
    
    if model is None or vectorizer is None:
        st.error("⚠️ ML Model not loaded. Please train the model first.")
        return
    
    try:
        features = vectorizer.transform([comment_text])
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(max(probabilities))
        
        st.session_state.analysis_result[post_id] = {
            'label': int(prediction),
            'confidence': confidence,
            'is_cyberbullying': bool(prediction == 1),
            'original_text': comment_text
        }
        
        if prediction == 1:
            user_id = auth.get_current_user_id()
            warning_count = firebase.increase_warning_count(user_id)
            
            if warning_count >= 3:
                firebase.block_user(user_id)
                st.session_state.analysis_result[post_id]['blocked'] = True
                st.session_state.analysis_result[post_id]['warning_count'] = warning_count
            else:
                st.session_state.analysis_result[post_id]['blocked'] = False
                st.session_state.analysis_result[post_id]['warning_count'] = warning_count
            
            auth.refresh_user_data()
    
    except Exception as e:
        st.error(f"❌ Error analyzing comment: {str(e)}")

def post_comment(post_id):
    """Post a comment after successful analysis"""
    if post_id in st.session_state.analysis_result:
        result = st.session_state.analysis_result[post_id]
        
        if result['label'] == 0:
            user_id = auth.get_current_user_id()
            username = auth.get_current_username()
            
            success = firebase.add_comment(
                post_id=post_id,
                user_id=user_id,
                username=username,
                comment_text=result['original_text'],
                label=result['label'],
                confidence=result['confidence']
            )
            
            if success:
                st.success("✅ Comment posted successfully!")
                
                if post_id in st.session_state.comment_text:
                    st.session_state.comment_text[post_id] = ""
                if post_id in st.session_state.analysis_result:
                    del st.session_state.analysis_result[post_id]
                
                st.rerun()
            else:
                st.error("❌ Failed to post comment. Please try again.")
        else:
            st.error("❌ Cannot post cyberbullying content!")

def display_post(post):
    """Display a single post with comments"""
    post_id = post['post_id']
    
    with st.container():
        st.markdown("<div class='post-card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"### 👤 @{post['username']}")
        with col2:
            created_at = post.get('created_at', '')
            if created_at:
                try:
                    date_str = created_at.split('T')[0]
                    st.caption(date_str)
                except:
                    pass
        
        if post.get('image_url'):
            st.markdown(f"""
            <div class='post-image-wrapper'>
                <img src='{post['image_url']}' alt='Post image'>
            </div>
            """, unsafe_allow_html=True)
        
        if post.get('caption'):
            st.write(post['caption'])
        
        st.write("")
        
        with st.expander(f"💬 Comments", expanded=False):
            
            comments = firebase.get_post_comments(post_id)
            
            if comments:
                st.markdown(f"**💬 {len(comments)} Comment(s):**")
                
                container = st.container(height=200)
                
                with container:
                    for idx, comment in enumerate(comments):
                        comment_user = comment.get('username', 'Unknown')
                        comment_text = comment.get('comment_text', 'No text')
                        comment_time = comment.get('created_at', '')
                        
                        time_str = ""
                        if comment_time:
                            try:
                                time_str = comment_time.split('T')[0]
                            except:
                                time_str = ""
                        
                        col1, col2 = st.columns([6, 1])
                        with col1:
                            st.markdown(f"**@{comment_user}**")
                            st.write(comment_text)
                        with col2:
                            if time_str:
                                st.caption(time_str)
                        
                        if idx < len(comments) - 1:
                            st.divider()
            else:
                st.caption("💭 No comments yet. Be the first to comment!")
            
            st.write("---")
            
            if auth.is_blocked():
                st.error("🚫 Your account is blocked. You cannot comment.")
            else:
                if post_id not in st.session_state.comment_text:
                    st.session_state.comment_text[post_id] = ""
                
                comment = st.text_area(
                    "Write your comment...",
                    value=st.session_state.comment_text[post_id],
                    key=f"comment_input_{post_id}",
                    height=100,
                    placeholder="Share your thoughts..."
                )
                
                st.session_state.comment_text[post_id] = comment
                
                col1, col2 = st.columns(2)
                
                with col1:
                    analyze_btn = st.button(
                        "🔍 Analyze Comment",
                        key=f"analyze_{post_id}",
                        disabled=not comment.strip(),
                        use_container_width=True
                    )
                
                with col2:
                    can_post_btn = (
                        post_id in st.session_state.analysis_result and
                        st.session_state.analysis_result[post_id]['label'] == 0
                    )
                    
                    post_btn = st.button(
                        "📤 Post Comment",
                        key=f"post_{post_id}",
                        disabled=not can_post_btn,
                        use_container_width=True,
                        type="primary" if can_post_btn else "secondary"
                    )
                
                if analyze_btn:
                    with st.spinner("Analyzing comment..."):
                        analyze_comment(post_id, comment)
                        st.rerun()
                
                if post_btn:
                    post_comment(post_id)
                
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
                        
                        if 'blocked' in result:
                            warning_count = result.get('warning_count', 0)
                            
                            if result['blocked']:
                                st.markdown(f"""
                                <div class='danger-message'>
                                    <strong>🚫 ACCOUNT BLOCKED</strong><br>
                                    You have been blocked due to {warning_count} violations of community guidelines.
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                warnings_remaining = 3 - warning_count
                                st.markdown(f"""
                                <div class='warning-message'>
                                    <strong>⚠️ WARNING {warning_count}/3</strong><br>
                                    {warnings_remaining} warning(s) remaining before account suspension.
                                </div>
                                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== PAGE FUNCTIONS ====================

def show_landing_page():
    """Display landing page"""
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d3b4f 100%);
            padding: 0;
        }
        .block-container {
            padding-top: 2rem;
            max-width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        st.markdown("<h1 style='color: white; font-size: 2rem; margin-top: 1rem;'>🛡️ SafeSpace</h1>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Login", key="nav_login", use_container_width=True):
            navigate_to("/login")
    
    with col3:
        if st.button("Register", key="nav_register", use_container_width=True, type="primary"):
            navigate_to("/register")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("""
        <div style='padding: 2rem 0;'>
            <h1 style='color: white; font-size: 4.5rem; font-weight: 900; line-height: 1.1; margin-bottom: 1.5rem; letter-spacing: -2px;'>
                STOP BULLYING<br>BEFORE POSTING
            </h1>
            
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Get Started", key="hero_cta", type="primary"):
            navigate_to("/register")
    
    with col_right:
    # Hero Image
        try:
            from PIL import Image
            hero_image = Image.open("assets/hero_image.png")  # Change filename if needed
            st.image(hero_image, use_container_width=True)
        except:
        # Fallback if image not found
            st.markdown("""
            <div style='height: 400px; background: linear-gradient(135deg, rgba(0, 149, 246, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                        border-radius: 20px; display: flex; align-items: center; justify-content: center;'>
                <div style='text-align: center; color: rgba(255,255,255,0.5); font-size: 1.2rem;'>
                    Add your image to assets/hero_image.png
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
                    
        <div style='background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2rem;'>
            <div style='font-size: 2.5rem; font-weight: 700; color: #0095f6; margin-bottom: 1rem;'>01</div>
            <p style='color: rgba(255, 255, 255, 0.8); line-height: 1.6;'>
                <strong>AI-Powered Detection</strong><br><br>
                Machine learning algorithms analyze every comment before it's posted, ensuring a harassment-free experience.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2rem;'>
            <div style='font-size: 2.5rem; font-weight: 700; color: #0095f6; margin-bottom: 1rem;'>02</div>
            <p style='color: rgba(255, 255, 255, 0.8); line-height: 1.6;'>
                <strong>Smart Moderation</strong><br><br>
                Progressive warning system educates users and automatically blocks repeat offenders to maintain community safety.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2rem;'>
            <div style='font-size: 2.5rem; font-weight: 700; color: #0095f6; margin-bottom: 1rem;'>03</div>
            <p style='color: rgba(255, 255, 255, 0.8); line-height: 1.6;'>
                <strong>Real-Time Protection</strong><br><br>
                Instant feedback on content safety with confidence scores, keeping your feed clean and positive at all times.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.5); padding: 2rem;'>
        <p>SafeSpace © 2024 - Making social media safer with AI</p>
    </div>
    """, unsafe_allow_html=True)

def show_login_page():
    """Display login/registration page"""
    
    # Render header without showing navigation (cleaner for auth pages)
    render_header(show_auth=True)
    
    st.markdown("<h1 class='main-header'>🛡️ SafeSpace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>Social Media with Cyberbullying Protection</p>", unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        current_route = get_current_route()
        default_tab = 1 if current_route == "/register" else 0
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Welcome Back!")
            
            st.write("")
            
            email = st.text_input("Email", key="login_email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            st.write("")
            
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                if email and password:
                    with st.spinner("Logging in..."):
                        success, message = auth.login(email, password)
                        if success:
                            st.success(message)
                            st.balloons()
                            navigate_to("/feed")
                        else:
                            st.error(message)
                else:
                    st.warning("Please enter both email and password")
        
        with tab2:
            st.subheader("Join SafeSpace!")
            
            st.write("")
            
            new_username = st.text_input("Username", key="reg_username", placeholder="Choose a unique username")
            new_email = st.text_input("Email", key="reg_email", placeholder="your.email@example.com")
            new_password = st.text_input("Password", type="password", key="reg_password", placeholder="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Re-enter your password")
            
            st.write("")
            
            if st.button("✨ Create Account", use_container_width=True, type="primary"):
                with st.spinner("Creating your account..."):
                    success, message = auth.register(new_email, new_password, confirm_password, new_username)
                    if success:
                        st.success(message)
                        st.info("✅ Account created! Please login with your credentials.")
                        st.balloons()
                        navigate_to("/login")
                    else:
                        st.error(message)

def show_feed_page():
    """Display main feed with all posts"""
    
    # Render global header
    render_header()
    
    # User status bar (below header)
    user_data = auth.get_user_data()
    if user_data:
        warning_count = user_data.get('warning_count', 0)
        is_blocked = user_data.get('is_blocked', False)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Logged in as:** @{auth.get_current_username()}")
        with col2:
            if is_blocked:
                st.error(f"⛔ Blocked")
            else:
                st.info(f"⚠️ Warnings: {warning_count}/3")
    
    st.divider()
    
    if user_data and user_data.get('is_blocked', False):
        st.error("🚫 **Your account has been blocked due to repeated violations.**")
        st.info("You can view posts but cannot comment or create new posts.")
        st.divider()
    
    posts = firebase.get_all_posts(limit=50)
    
    if posts:
        st.markdown(f"### 📱 Latest Posts ({len(posts)})")
        st.write("")
        
        for post in posts:
            display_post(post)
    else:
        st.info("📭 No posts yet. Be the first to create a post!")
        if st.button("Create First Post", type="primary"):
            navigate_to("/create-post")


def show_create_post_page():
    """Page to create a new post"""
    
    # Render global header
    render_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>📸 Create Post</h1>", unsafe_allow_html=True)
        
        st.write("")
        
        if auth.is_blocked():
            st.error("🚫 Your account is blocked. You cannot create posts.")
            return
        
        st.subheader("Upload Image")
        uploaded_image = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a picture for your post"
        )
        
        if uploaded_image:
            st.image(uploaded_image, caption="Preview", use_container_width=True)
        
        st.write("")
        
        st.subheader("Write Caption")
        caption = st.text_area(
            "What's on your mind?",
            height=150,
            placeholder="Share your thoughts..."
        )
        
        st.write("")
        
        if st.button("📤 Create Post", type="primary", use_container_width=True):
            if not uploaded_image:
                st.error("❌ Please upload an image!")
            elif not caption.strip():
                st.error("❌ Please write a caption!")
            else:
                with st.spinner("Creating your post..."):
                    try:
                        user_id = auth.get_current_user_id()
                        username = auth.get_current_username()
                        
                        post_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        success, image_url = cloudinary.upload_post_image(
                            uploaded_image,
                            user_id,
                            post_timestamp
                        )
                        
                        if success:
                            success, post_id = firebase.create_post(
                                user_id=user_id,
                                username=username,
                                caption=caption,
                                image_url=image_url
                            )
                            
                            if success:
                                st.success("✅ Post created successfully!")
                                st.balloons()
                                
                                import time
                                time.sleep(1)
                                navigate_to("/feed")
                            else:
                                st.error("❌ Failed to create post in database.")
                        else:
                            st.error(f"❌ Failed to upload image: {image_url}")
                    
                    except Exception as e:
                        st.error(f"❌ Error creating post: {str(e)}")


def show_profile_page():
    """Display user profile page"""
    
    # Render global header
    render_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>👤 My Profile</h1>", unsafe_allow_html=True)
        
        st.write("")
        
        user_data = auth.get_user_data()
        
        if user_data:
            st.markdown("""
            <div style='background-color: #ffffff; padding: 2rem; border-radius: 8px; border: 1px solid #dbdbdb; margin-bottom: 2rem;'>
                <h2 style='font-size: 1.75rem; font-weight: 300; color: #262626; margin-bottom: 0.5rem;'>@{}</h2>
                <p style='color: #8e8e8e; font-size: 0.95rem;'>{}</p>
            </div>
            """.format(user_data.get('username'), user_data.get('email')), unsafe_allow_html=True)
            
            st.subheader("📸 Profile Picture")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                current_pic = user_data.get('profile_picture', '')
                if current_pic and current_pic.strip():
                    st.image(current_pic, width=200, caption="Current Profile Picture")
                else:
                    st.image(cloudinary.get_default_profile_picture(), width=200, caption="Default Avatar")
            
            with col_b:
                new_pic = st.file_uploader(
                    "Upload new profile picture",
                    type=['png', 'jpg', 'jpeg'],
                    help="Update your profile picture"
                )
                
                if new_pic:
                    st.image(new_pic, width=200, caption="Preview")
                    
                    if st.button("💾 Save Profile Picture", type="primary"):
                        with st.spinner("Uploading..."):
                            user_id_upload = auth.get_current_user_id()
                            success, image_url = cloudinary.upload_profile_picture(new_pic, user_id_upload)
                            
                            if success:
                                update_success = auth.update_profile({'profile_picture': image_url})
                                
                                if update_success:
                                    st.success("✅ Profile picture updated!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update profile.")
                            else:
                                st.error(f"❌ Upload failed: {image_url}")
            
            st.divider()
            
            st.subheader("📊 Account Statistics")
            
            user_id = auth.get_current_user_id()
            user_posts = firebase.get_user_posts(user_id)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="📝 Posts", value=len(user_posts))
            
            with col2:
                st.metric(label="⚠️ Warnings", value=f"{user_data.get('warning_count', 0)}/3")
            
            with col3:
                status = "🚫 Blocked" if user_data.get('is_blocked') else "✅ Active"
                color = "red" if user_data.get('is_blocked') else "green"
                st.markdown(f"**Account Status**")
                st.markdown(f"<h3 style='color: {color}; margin: 0;'>{status}</h3>", unsafe_allow_html=True)
            
            st.divider()
            
            st.subheader(f"📱 My Posts ({len(user_posts)})")
            
            if user_posts:
                for post in user_posts:
                    display_post(post)
            else:
                st.info("📭 You haven't created any posts yet.")
                if st.button("Create Your First Post", type="primary"):
                    navigate_to("/create-post")


def show_search_page():
    """Search for users"""
    
    # Render global header
    render_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>🔍 Search Users</h1>", unsafe_allow_html=True)
        
        st.write("")
        
        search_term = st.text_input(
            "Search by username",
            placeholder="Enter username...",
            key="search_input"
        )
        
        if search_term and len(search_term) >= 2:
            with st.spinner("Searching..."):
                results = firebase.search_users(search_term)
            
            if results:
                st.success(f"Found {len(results)} user(s)")
                st.write("")
                
                for user in results:
                    col_a, col_b, col_c = st.columns([1, 3, 1])
                    
                    with col_a:
                        profile_pic = user.get('profile_picture', '')
                        if profile_pic and profile_pic.strip():
                            st.image(profile_pic, width=80)
                        else:
                            st.image(cloudinary.get_default_profile_picture(), width=80)
                    
                    with col_b:
                        st.markdown(f"### @{user.get('username')}")
                        st.caption(user.get('email', ''))
                    
                    with col_c:
                        if st.button("View", key=f"view_{user.get('user_id')}"):
                            st.session_state.selected_user_id = user.get('user_id')
                            navigate_to("/view-user")
                    
                    st.divider()
            else:
                st.info("No users found matching your search.")
        elif search_term:
            st.warning("Please enter at least 2 characters to search.")


def show_user_profile_page():
    """Display another user's profile"""
    
    # Render global header
    render_header()
    
    user_id = st.session_state.get('selected_user_id')
    
    if not user_id:
        navigate_to("/search")
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        
        user_data = firebase.get_user_data(user_id)
        
        if user_data:
            st.markdown(f"""
            <div style='background-color: #ffffff; padding: 2rem; border-radius: 8px; border: 1px solid #dbdbdb; margin-bottom: 2rem;'>
                <h2 style='font-size: 1.75rem; font-weight: 300; color: #262626;'>@{user_data.get('username')}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            profile_pic = user_data.get('profile_picture', '')
            if profile_pic and profile_pic.strip():
                st.image(profile_pic, width=200)
            else:
                st.image(cloudinary.get_default_profile_picture(), width=200)
            
            st.divider()
            
            user_posts = firebase.get_user_posts(user_id)
            
            if user_posts:
                st.subheader(f"📱 Posts ({len(user_posts)})")
                st.write("")
                
                for post in user_posts:
                    display_post(post)
            else:
                st.info("This user hasn't posted anything yet.")
        else:
            st.error("User not found.")

# ==================== MODERATION CONTROLLER ====================

class ModerationController:
    def __init__(self, firebase_manager, warning_threshold=3):
        self.firebase = firebase_manager
        self.warning_threshold = warning_threshold
    
    def track_offense(self, user_id):
        warning_count = self.firebase.increase_warning_count(user_id)
        
        if warning_count >= self.warning_threshold:
            self.firebase.block_user(user_id)
            return {
                'action': 'BLOCK',
                'warning_count': warning_count,
                'message': f"Your account has been blocked due to {warning_count} violations.",
                'is_blocked': True
            }
        else:
            warnings_remaining = self.warning_threshold - warning_count
            return {
                'action': 'WARNING',
                'warning_count': warning_count,
                'warnings_remaining': warnings_remaining,
                'message': f"Warning {warning_count}/{self.warning_threshold}: {warnings_remaining} warning(s) remaining before suspension.",
                'is_blocked': False
            }

# ==================== MAIN APPLICATION WITH ROUTING ====================

def main():
    """Main application with URL routing"""
    
    # Get current route from URL
    route = get_current_route()
    
    # Check authentication status
    is_logged_in = auth.is_authenticated()
    
    # Define protected routes (require login)
    protected_routes = ["/feed", "/create-post", "/profile", "/search", "/view-user"]
    
    # Route handling
    if route in protected_routes and not is_logged_in:
        # Protected route but not logged in - redirect to login
        navigate_to("/login")
    
    elif route == "/" or route == "":
        # Landing page
        show_landing_page()
    
    elif route == "/login":
        # Login page
        if is_logged_in:
            navigate_to("/feed")
        else:
            show_login_page()
    
    elif route == "/register":
        # Register page
        if is_logged_in:
            navigate_to("/feed")
        else:
            show_login_page()
    
    elif route == "/feed":
        # Feed page (protected)
        show_feed_page()
    
    elif route == "/create-post":
        # Create post page (protected)
        show_create_post_page()
    
    elif route == "/profile":
        # Profile page (protected)
        show_profile_page()
    
    elif route == "/search":
        # Search page (protected)
        show_search_page()
    
    elif route == "/view-user":
        # View user profile page (protected)
        show_user_profile_page()
    
    else:
        # Unknown route - redirect to landing
        navigate_to("/")

# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    main()