"""
Warning and Blocking Controller Module
Handles user warnings, blocking logic, and moderation actions
"""

class ModerationController:
    def __init__(self, database_manager, warning_threshold=3):
        """
        Initialize moderation controller
        
        Args:
            database_manager: Database manager instance
            warning_threshold (int): Number of warnings before blocking user
        """
        self.db = database_manager
        self.warning_threshold = warning_threshold
    
    def track_offense(self, username):
        """
        Track a cyberbullying offense for a user
        
        Args:
            username (str): Username of the offender
            
        Returns:
            dict: Moderation result containing action taken
        """
        # Increase warning count
        warning_count = self.db.increase_warning_count(username)
        
        # Check if user should be blocked
        if warning_count >= self.warning_threshold:
            self.db.block_user(username)
            return {
                'action': 'BLOCK',
                'warning_count': warning_count,
                'message': f"You have been blocked due to {warning_count} violations of our community guidelines.",
                'is_blocked': True
            }
        else:
            warnings_remaining = self.warning_threshold - warning_count
            return {
                'action': 'WARNING',
                'warning_count': warning_count,
                'warnings_remaining': warnings_remaining,
                'message': f"Warning {warning_count}/{self.warning_threshold}: Your comment contains inappropriate content. {warnings_remaining} warning(s) remaining before account suspension.",
                'is_blocked': False
            }
    
    def issue_warning(self, username):
        """
        Issue a warning to a user
        
        Args:
            username (str): Username
            
        Returns:
            dict: Warning information
        """
        warning_count = self.db.get_warning_count(username)
        warnings_remaining = self.warning_threshold - warning_count
        
        return {
            'warning_count': warning_count,
            'warnings_remaining': warnings_remaining,
            'message': f"You have {warning_count} warning(s). {warnings_remaining} remaining before suspension."
        }
    
    def check_user_status(self, username):
        """
        Check if user can post comments
        
        Args:
            username (str): Username
            
        Returns:
            dict: User status information
        """
        is_blocked = self.db.is_user_blocked(username)
        warning_count = self.db.get_warning_count(username)
        
        return {
            'is_blocked': is_blocked,
            'can_post': not is_blocked,
            'warning_count': warning_count,
            'message': 'Your account is blocked. You cannot post comments.' if is_blocked else 'You can post comments.'
        }
    
    def generate_warning_message(self, warning_count):
        """
        Generate appropriate warning message based on count
        
        Args:
            warning_count (int): Current warning count
            
        Returns:
            str: Warning message
        """
        warnings_remaining = self.warning_threshold - warning_count
        
        if warnings_remaining > 1:
            severity = "⚠️ Warning"
        elif warnings_remaining == 1:
            severity = "🚨 Final Warning"
        else:
            severity = "🚫 Account Suspended"
        
        return f"{severity}: {warning_count}/{self.warning_threshold} violations detected. {max(0, warnings_remaining)} warning(s) remaining."
    
    def show_block_message(self):
        """
        Generate block notification message
        
        Returns:
            str: Block notification
        """
        return """
        🚫 **ACCOUNT BLOCKED**
        
        Your account has been suspended due to repeated violations of our community guidelines.
        
        You have posted multiple comments containing cyberbullying, harassment, or offensive content.
        
        To appeal this decision, please contact the administrator.
        """


class FeedbackNotification:
    """
    Feedback and notification system for users
    """
    
    @staticmethod
    def show_result(label, confidence):
        """
        Show classification result to user
        
        Args:
            label (int): 0 for non-bullying, 1 for cyberbullying
            confidence (float): Confidence score
            
        Returns:
            dict: Feedback information
        """
        if label == 0:
            return {
                'status': 'safe',
                'icon': '✅',
                'message': 'Your comment is appropriate and can be posted.',
                'color': 'green',
                'confidence': confidence,
                'can_post': True
            }
        else:
            # Determine severity based on confidence
            if confidence >= 0.9:
                severity = 'HIGH'
                level = '🔴 Severe'
            elif confidence >= 0.7:
                severity = 'MEDIUM'
                level = '🟡 Moderate'
            else:
                severity = 'LOW'
                level = '🟠 Low'
            
            return {
                'status': 'bullying',
                'icon': '❌',
                'message': 'This comment contains inappropriate content and cannot be posted.',
                'color': 'red',
                'confidence': confidence,
                'severity': severity,
                'level': level,
                'can_post': False
            }
    
    @staticmethod
    def show_warning(warning_count, threshold=3):
        """
        Show warning notification
        
        Args:
            warning_count (int): Current warning count
            threshold (int): Warning threshold
            
        Returns:
            dict: Warning notification
        """
        warnings_remaining = threshold - warning_count
        
        return {
            'warning_count': warning_count,
            'threshold': threshold,
            'warnings_remaining': warnings_remaining,
            'message': f"⚠️ Warning: {warning_count}/{threshold} violations. {warnings_remaining} remaining before suspension."
        }
    
    @staticmethod
    def show_block_notification():
        """
        Show block notification
        
        Returns:
            dict: Block notification
        """
        return {
            'status': 'blocked',
            'icon': '🚫',
            'message': 'Your account has been blocked due to repeated violations.',
            'can_appeal': True
        }


# Example usage
if __name__ == "__main__":
    print("Moderation Controller module loaded successfully!")
    
    # Example feedback
    feedback = FeedbackNotification.show_result(label=1, confidence=0.95)
    print("\n=== Cyberbullying Detection Result ===")
    print(f"{feedback['icon']} {feedback['message']}")
    print(f"Confidence: {feedback['confidence']:.2%}")
    print(f"Severity: {feedback['level']}")
