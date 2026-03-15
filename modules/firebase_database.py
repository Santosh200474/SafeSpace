"""
Firebase Database Module
Handles all Firebase Firestore operations
"""

import pyrebase
from datetime import datetime
import streamlit as st
from firebase_config import firebase_config

class FirebaseManager:
    def __init__(self):
        """Initialize Firebase connection"""
        try:
            # Initialize Firebase
            self.firebase = pyrebase.initialize_app(firebase_config)
            self.auth = self.firebase.auth()
            self.db = self.firebase.database()
            print("✅ Firebase initialized successfully")
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            self.firebase = None
            self.auth = None
            self.db = None
    
    # ==================== AUTHENTICATION ====================
    
    def register_user(self, email, password, username):
        """
        Register a new user
        
        Args:
            email: User's email
            password: User's password
            username: User's username
            
        Returns:
            tuple: (success, message, user_id)
        """
        try:
            # Create user in Firebase Auth
            user = self.auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            
            # Store user data in Firestore
            user_data = {
                'username': username,
                'email': email,
                'user_id': user_id,
                'warning_count': 0,
                'is_blocked': False,
                'profile_picture': '',
                'bio': '',
                'created_at': datetime.now().isoformat()
            }
            
            self.db.child("users").child(user_id).set(user_data)
            
            return True, "Registration successful!", user_id
            
        except Exception as e:
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                return False, "Email already registered!", None
            elif "WEAK_PASSWORD" in error_message:
                return False, "Password should be at least 6 characters!", None
            else:
                return False, f"Registration failed: {error_message}", None
    
    def login_user(self, email, password):
        """
        Login user
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            tuple: (success, message, user_data)
        """
        try:
            # Sign in with Firebase Auth
            user = self.auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']
            
            # Get user data from database
            user_data = self.db.child("users").child(user_id).get().val()
            
            if user_data:
                # Check if user is blocked
                if user_data.get('is_blocked', False):
                    return False, "Your account is blocked!", None
                
                # Add token to user data
                user_data['token'] = user['idToken']
                user_data['user_id'] = user_id
                
                return True, "Login successful!", user_data
            else:
                return False, "User data not found!", None
                
        except Exception as e:
            error_message = str(e)
            if "INVALID_PASSWORD" in error_message or "EMAIL_NOT_FOUND" in error_message:
                return False, "Invalid email or password!", None
            else:
                return False, f"Login failed: {error_message}", None
    
    def get_user_data(self, user_id):
        """
        Get user data by user_id
        
        Args:
            user_id: Firebase user ID
            
        Returns:
            dict: User data or None
        """
        try:
            user_data = self.db.child("users").child(user_id).get().val()
            return user_data
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    def update_user_profile(self, user_id, profile_data):
        """
        Update user profile
        
        Args:
            user_id: Firebase user ID
            profile_data: Dictionary with profile fields to update
            
        Returns:
            bool: Success status
        """
        try:
            self.db.child("users").child(user_id).update(profile_data)
            return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    # ==================== POSTS ====================
    
    def create_post(self, user_id, username, caption, image_url):
        """
        Create a new post
        
        Args:
            user_id: User's Firebase ID
            username: User's username
            caption: Post caption/text
            image_url: URL of uploaded image
            
        Returns:
            tuple: (success, post_id)
        """
        try:
            post_data = {
                'user_id': user_id,
                'username': username,
                'caption': caption,
                'image_url': image_url,
                'likes': 0,
                'created_at': datetime.now().isoformat()
            }
            
            # Push creates a new unique ID
            result = self.db.child("posts").push(post_data)
            post_id = result['name']
            
            return True, post_id
            
        except Exception as e:
            print(f"Error creating post: {e}")
            return False, None
    
    def get_all_posts(self, limit=50):
        """
        Get all posts (latest first)
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            list: List of posts with post_id included
        """
        try:
            posts = self.db.child("posts").get().val()
            
            if not posts:
                return []
            
            # Convert to list and add post_id
            posts_list = []
            for post_id, post_data in posts.items():
                post_data['post_id'] = post_id
                posts_list.append(post_data)
            
            # Sort by created_at (newest first)
            posts_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            return posts_list[:limit]
            
        except Exception as e:
            print(f"Error getting posts: {e}")
            return []
    
    def get_user_posts(self, user_id):
    
    
    
        try:
        # Get ALL posts first
            all_posts = self.db.child("posts").get().val()
        
            if not all_posts:
                return []
        
        # Filter manually in Python (more reliable than Firebase query)
            user_posts = []
            for post_id, post_data in all_posts.items():
                if post_data.get('user_id') == user_id:
                    post_data['post_id'] = post_id
                    user_posts.append(post_data)
        
        # Sort by created_at (newest first)
            user_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
            return user_posts
        
        except Exception as e:
            print(f"Error getting user posts: {e}")
            return []
    
    # ==================== COMMENTS ====================
    
    def add_comment(self, post_id, user_id, username, comment_text, label, confidence):
        """
        Add a comment to a post
        
        Args:
            post_id: Post ID
            user_id: User's Firebase ID
            username: User's username
            comment_text: Comment text
            label: 0 (safe) or 1 (cyberbullying)
            confidence: ML model confidence score
            
        Returns:
            bool: Success status
        """
        try:
            comment_data = {
                'user_id': user_id,
                'username': username,
                'comment_text': comment_text,
                'label': label,
                'confidence': confidence,
                'created_at': datetime.now().isoformat()
            }
            
            self.db.child("posts").child(post_id).child("comments").push(comment_data)
            return True
            
        except Exception as e:
            print(f"Error adding comment: {e}")
            return False
    
    def get_post_comments(self, post_id):
        """
        Get all comments for a post
        
        Args:
            post_id: Post ID
            
        Returns:
            list: List of comments
        """
        try:
            comments = self.db.child("posts").child(post_id).child("comments").get().val()
            
            if not comments:
                return []
            
            comments_list = []
            for comment_id, comment_data in comments.items():
                comment_data['comment_id'] = comment_id
                comments_list.append(comment_data)
            
            # Sort by created_at (oldest first)
            comments_list.sort(key=lambda x: x.get('created_at', ''))
            return comments_list
            
        except Exception as e:
            print(f"Error getting comments: {e}")
            return []
    
    # ==================== MODERATION ====================
    
    def increase_warning_count(self, user_id):
        """
        Increase user's warning count
        
        Args:
            user_id: Firebase user ID
            
        Returns:
            int: New warning count
        """
        try:
            user_data = self.get_user_data(user_id)
            if user_data:
                current_warnings = user_data.get('warning_count', 0)
                new_warnings = current_warnings + 1
                
                self.db.child("users").child(user_id).update({
                    'warning_count': new_warnings
                })
                
                return new_warnings
            return 0
            
        except Exception as e:
            print(f"Error increasing warning count: {e}")
            return 0
    
    def block_user(self, user_id):
        """
        Block a user
        
        Args:
            user_id: Firebase user ID
            
        Returns:
            bool: Success status
        """
        try:
            self.db.child("users").child(user_id).update({
                'is_blocked': True
            })
            return True
            
        except Exception as e:
            print(f"Error blocking user: {e}")
            return False
    
    def is_user_blocked(self, user_id):
        """
        Check if user is blocked
        
        Args:
            user_id: Firebase user ID
            
        Returns:
            bool: True if blocked
        """
        try:
            user_data = self.get_user_data(user_id)
            if user_data:
                return user_data.get('is_blocked', False)
            return False
            
        except Exception as e:
            print(f"Error checking block status: {e}")
            return False
    
    # ==================== SEARCH ====================
    
    def search_users(self, search_term):
        """
        Search users by username
        
        Args:
            search_term: Search query
            
        Returns:
            list: List of matching users
        """
        try:
            all_users = self.db.child("users").get().val()
            
            if not all_users:
                return []
            
            search_term_lower = search_term.lower()
            results = []
            
            for user_id, user_data in all_users.items():
                username = user_data.get('username', '').lower()
                if search_term_lower in username:
                    user_data['user_id'] = user_id
                    results.append(user_data)
            
            return results
            
        except Exception as e:
            print(f"Error searching users: {e}")
            return []