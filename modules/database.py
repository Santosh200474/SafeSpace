"""
Database Module - SQLite Operations
Handles all database interactions including user management, comments, and moderation
"""

import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="database/cyberbullying.db"):
        """Initialize database connection and create tables"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                warning_count INTEGER DEFAULT 0,
                is_blocked INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                post_id INTEGER NOT NULL,
                comment_text TEXT NOT NULL,
                label INTEGER NOT NULL,
                confidence REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        
        # Logs table for audit trail
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ========== USER MANAGEMENT ==========
    
    def register_user(self, username, password):
        """Register a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            self.log_action(username, "REGISTRATION", "User registered successfully")
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists!"
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.log_action(username, "LOGIN", "User logged in")
            return True, "Login successful!"
        return False, "Invalid username or password!"
    
    def get_user_info(self, username):
        """Get user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT username, warning_count, is_blocked FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'username': user[0],
                'warning_count': user[1],
                'is_blocked': user[2]
            }
        return None
    
    def is_user_blocked(self, username):
        """Check if user is blocked"""
        user_info = self.get_user_info(username)
        if user_info:
            return user_info['is_blocked'] == 1
        return False
    
    # ========== MODERATION LOGIC ==========
    
    def increase_warning_count(self, username):
        """Increase user warning count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET warning_count = warning_count + 1 WHERE username = ?",
            (username,)
        )
        conn.commit()
        
        # Get updated warning count
        cursor.execute(
            "SELECT warning_count FROM users WHERE username = ?",
            (username,)
        )
        warning_count = cursor.fetchone()[0]
        conn.close()
        
        self.log_action(username, "WARNING_ISSUED", f"Warning count: {warning_count}")
        return warning_count
    
    def block_user(self, username):
        """Block a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET is_blocked = 1 WHERE username = ?",
            (username,)
        )
        conn.commit()
        conn.close()
        
        self.log_action(username, "USER_BLOCKED", "User blocked due to repeated violations")
    
    def get_warning_count(self, username):
        """Get user's current warning count"""
        user_info = self.get_user_info(username)
        if user_info:
            return user_info['warning_count']
        return 0
    
    # ========== COMMENT MANAGEMENT ==========
    
    def save_comment(self, username, post_id, comment_text, label, confidence):
        """Save a comment with its classification result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO comments 
               (username, post_id, comment_text, label, confidence) 
               VALUES (?, ?, ?, ?, ?)""",
            (username, post_id, comment_text, label, confidence)
        )
        conn.commit()
        conn.close()
        
        action = "COMMENT_POSTED" if label == 0 else "CYBERBULLYING_DETECTED"
        self.log_action(username, action, f"Post {post_id}: {comment_text[:50]}...")
    
    def get_user_comments(self, username):
        """Get all comments by a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT comment_text, label, confidence, created_at 
               FROM comments 
               WHERE username = ? 
               ORDER BY created_at DESC""",
            (username,)
        )
        comments = cursor.fetchall()
        conn.close()
        
        return comments
    
    # ========== LOGGING ==========
    
    def log_action(self, username, action, details=""):
        """Log user actions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO logs (username, action, details) VALUES (?, ?, ?)",
            (username, action, details)
        )
        conn.commit()
        conn.close()
    
    def get_user_logs(self, username, limit=50):
        """Get user activity logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT action, details, timestamp 
               FROM logs 
               WHERE username = ? 
               ORDER BY timestamp DESC 
               LIMIT ?""",
            (username, limit)
        )
        logs = cursor.fetchall()
        conn.close()
        
        return logs
