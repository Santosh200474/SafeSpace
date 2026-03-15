"""
Authentication Module
Handles user login, registration, and session management
"""

import streamlit as st
from modules.database import DatabaseManager

class AuthenticationManager:
    def __init__(self, database_manager):
        """
        Initialize authentication manager
        
        Args:
            database_manager: Database manager instance
        """
        self.db = database_manager
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        
        if 'username' not in st.session_state:
            st.session_state.username = None
        
        if 'user_info' not in st.session_state:
            st.session_state.user_info = None
    
    def login(self, username, password):
        """
        Login user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            tuple: (success, message)
        """
        success, message = self.db.authenticate_user(username, password)
        
        if success:
            # Check if user is blocked
            if self.db.is_user_blocked(username):
                return False, "Your account is blocked. You cannot login."
            
            # Set session state
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_info = self.db.get_user_info(username)
        
        return success, message
    
    def register(self, username, password, confirm_password):
        """
        Register new user
        
        Args:
            username (str): Username
            password (str): Password
            confirm_password (str): Password confirmation
            
        Returns:
            tuple: (success, message)
        """
        # Validation
        if not username or not password:
            return False, "Username and password are required!"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long!"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long!"
        
        if password != confirm_password:
            return False, "Passwords do not match!"
        
        # Register user
        success, message = self.db.register_user(username, password)
        
        return success, message
    
    def logout(self):
        """Logout current user"""
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_info = None
    
    def is_authenticated(self):
        """
        Check if user is authenticated
        
        Returns:
            bool: True if authenticated
        """
        return st.session_state.get('logged_in', False)
    
    def get_current_user(self):
        """
        Get current logged-in username
        
        Returns:
            str: Username or None
        """
        return st.session_state.get('username', None)
    
    def get_user_info(self):
        """
        Get current user information
        
        Returns:
            dict: User information
        """
        return st.session_state.get('user_info', None)
    
    def update_user_info(self):
        """Refresh user information from database"""
        if self.is_authenticated():
            username = self.get_current_user()
            st.session_state.user_info = self.db.get_user_info(username)
    
    def can_post_comment(self):
        """
        Check if current user can post comments
        
        Returns:
            tuple: (can_post, message)
        """
        if not self.is_authenticated():
            return False, "You must be logged in to comment."
        
        username = self.get_current_user()
        
        if self.db.is_user_blocked(username):
            return False, "Your account is blocked. You cannot post comments."
        
        return True, "You can post comments."


# Example usage for testing
if __name__ == "__main__":
    print("Authentication module loaded successfully!")
