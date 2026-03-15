"""
SafeSpace - Landing Page
Modern dark theme with hero section
"""

import streamlit as st

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="SafeSpace - Cyberbullying-Proof Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================

st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main > div {padding: 0;}
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d3b4f 100%);
        min-height: 100vh;
        padding: 0;
        position: relative;
        overflow: hidden;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        padding: 4rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 2rem;
        margin-bottom: 4rem;
    }
    
    .logo {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-buttons {
        display: flex;
        gap: 1rem;
    }
    
    /* Main Hero Text */
    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        color: white;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        letter-spacing: -2px;
        text-transform: uppercase;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        max-width: 600px;
        margin-bottom: 2.5rem;
    }
    
    /* Feature Cards */
    .feature-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin-top: 5rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.5rem 2rem;
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
    }
    
    /* Buttons */
    .cta-button {
        background: white;
        color: #0a0e27;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Gradient Overlay */
    .gradient-overlay {
        position: absolute;
        top: 0;
        right: 0;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent 0%, rgba(0, 149, 246, 0.2) 100%);
        pointer-events: none;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        .feature-cards {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== LANDING PAGE ====================

def show_landing_page():
    """Display landing page"""
    
    st.markdown("""
    <div class="hero-section">
        <div class="gradient-overlay"></div>
        <div class="hero-content">
            
            <!-- Navigation Bar -->
            <div class="nav-bar">
                <div class="logo">
                    🛡️ SafeSpace
                </div>
            </div>
            
            <!-- Hero Content -->
            <div style="margin-top: 6rem;">
                <h1 class="hero-title">
                    Stop Cyberbullying<br>
                    Before Posting
                </h1>
                
                <p class="hero-subtitle">
                    A cyberbullying-proof social media platform powered by AI. 
                    Connect, share, and interact in a safe environment where 
                    harmful content is detected and prevented in real-time.
                </p>
            </div>
            
            <!-- Feature Cards -->
            <div class="feature-cards">
                <div class="feature-card">
                    <div class="feature-number">01</div>
                    <p class="feature-text">
                        AI-Powered Detection - Machine learning algorithms 
                        analyze every comment before it's posted, ensuring 
                        a harassment-free experience.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-number">02</div>
                    <p class="feature-text">
                        Smart Moderation System - Progressive warning system 
                        educates users and automatically blocks repeat 
                        offenders to maintain community safety.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-number">03</div>
                    <p class="feature-text">
                        Real-Time Protection - Instant feedback on content 
                        safety with confidence scores, keeping your feed 
                        clean and positive at all times.
                    </p>
                </div>
            </div>
            
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Buttons at top right using Streamlit
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    
    with col2:
        st.write("")  # Spacer
    
    with col3:
        if st.button("Login", key="login_btn", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    
    with col4:
        if st.button("Register", key="register_btn", use_container_width=True, type="primary"):
            st.session_state.page = 'register'
            st.rerun()
    
    # Get Started button in hero section
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 3])
    with col1:
        if st.button("Get Started", key="get_started", use_container_width=True, type="primary"):
            st.session_state.page = 'register'
            st.rerun()


# ==================== MAIN ====================

if __name__ == "__main__":
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    
    show_landing_page()