"""
Firebase Authentication Module
Handles user authentication and session management with Firebase
"""

import streamlit as st
from modules.firebase_database import FirebaseManager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.firebase_secrets import firebase_config

class FirebaseAuthManager:
    def __init__(self, firebase_manager):
        """
        Initialize Firebase authentication manager
        
        Args:
            firebase_manager: FirebaseManager instance
        """
        self.firebase = firebase_manager
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        
        if 'username' not in st.session_state:
            st.session_state.username = None
        
        if 'email' not in st.session_state:
            st.session_state.email = None
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
        
        if 'token' not in st.session_state:
            st.session_state.token = None
    
    def register(self, email, password, confirm_password, username):
        """
        Register new user
        
        Args:
            email (str): User's email
            password (str): User's password
            confirm_password (str): Password confirmation
            username (str): User's username
            
        Returns:
            tuple: (success, message)
        """
        # Validation
        if not email or not password or not username:
            return False, "All fields are required!"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long!"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long!"
        
        if password != confirm_password:
            return False, "Passwords do not match!"
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return False, "Invalid email format!"
        
        # Register user in Firebase
        success, message, user_id = self.firebase.register_user(email, password, username)
        
        return success, message
    
    def login(self, email, password):
        """
        Login user
        
        Args:
            email (str): User's email
            password (str): User's password
            
        Returns:
            tuple: (success, message)
        """
        # Validation
        if not email or not password:
            return False, "Email and password are required!"
        
        # Login with Firebase
        success, message, user_data = self.firebase.login_user(email, password)
        
        if success and user_data:
            # Set session state
            st.session_state.logged_in = True
            st.session_state.user_id = user_data['user_id']
            st.session_state.username = user_data['username']
            st.session_state.email = user_data['email']
            st.session_state.user_data = user_data
            st.session_state.token = user_data.get('token', '')
            
            return True, message
        
        return False, message
    
    def logout(self):
        """Logout current user"""
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.email = None
        st.session_state.user_data = None
        st.session_state.token = None
    
    def is_authenticated(self):
        """
        Check if user is authenticated
        
        Returns:
            bool: True if authenticated
        """
        return st.session_state.get('logged_in', False)
    
    def get_current_user_id(self):
        """
        Get current logged-in user ID
        
        Returns:
            str: User ID or None
        """
        return st.session_state.get('user_id', None)
    
    def get_current_username(self):
        """
        Get current logged-in username
        
        Returns:
            str: Username or None
        """
        return st.session_state.get('username', None)
    
    def get_current_email(self):
        """
        Get current logged-in email
        
        Returns:
            str: Email or None
        """
        return st.session_state.get('email', None)
    
    def get_user_data(self):
        """
        Get current user's complete data
        
        Returns:
            dict: User data or None
        """
        return st.session_state.get('user_data', None)
    
    def refresh_user_data(self):
        """Refresh user data from Firebase"""
        if self.is_authenticated():
            user_id = self.get_current_user_id()
            user_data = self.firebase.get_user_data(user_id)
            if user_data:
                st.session_state.user_data = user_data
                st.session_state.username = user_data.get('username')
                st.session_state.email = user_data.get('email')
    
    def can_post_comment(self):
        """
        Check if current user can post comments
        
        Returns:
            tuple: (can_post, message)
        """
        if not self.is_authenticated():
            return False, "You must be logged in to comment."
        
        user_id = self.get_current_user_id()
        
        if self.firebase.is_user_blocked(user_id):
            return False, "Your account is blocked. You cannot post comments."
        
        return True, "You can post comments."
    
    def get_warning_count(self):
        """
        Get current user's warning count
        
        Returns:
            int: Warning count
        """
        user_data = self.get_user_data()
        if user_data:
            return user_data.get('warning_count', 0)
        return 0
    
    def is_blocked(self):
        """
        Check if current user is blocked
        
        Returns:
            bool: True if blocked
        """
        user_data = self.get_user_data()
        if user_data:
            return user_data.get('is_blocked', False)
        return False
    
    def update_profile(self, profile_data):
        """
        Update current user's profile
        
        Args:
            profile_data (dict): Profile fields to update
            
        Returns:
            bool: Success status
        """
        if not self.is_authenticated():
            return False
        
        user_id = self.get_current_user_id()
        success = self.firebase.update_user_profile(user_id, profile_data)
        
        if success:
            # Refresh user data
            self.refresh_user_data()
        
        return success


# Example usage
if __name__ == "__main__":
    print("Firebase Authentication module loaded successfully!")
