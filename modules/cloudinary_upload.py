"""
Cloudinary Upload Module
Handles image uploads to Cloudinary
"""

import cloudinary
import cloudinary.uploader
from cloudinary_config import cloudinary_config
from PIL import Image
import io

class CloudinaryManager:
    def __init__(self):
        """Initialize Cloudinary configuration"""
        try:
            cloudinary.config(
                cloud_name=cloudinary_config['cloud_name'],
                api_key=cloudinary_config['api_key'],
                api_secret=cloudinary_config['api_secret']
            )
            print("✅ Cloudinary initialized successfully")
        except Exception as e:
            print(f"❌ Cloudinary initialization error: {e}")
    
    def upload_image(self, image_file, folder="cyberbullying_app", public_id=None):
        """
        Upload image to Cloudinary
        
        Args:
            image_file: Image file (from st.file_uploader or PIL Image)
            folder: Cloudinary folder name
            public_id: Optional custom ID for the image
            
        Returns:
            tuple: (success, image_url or error_message)
        """
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                image_file,
                folder=folder,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            
            # Get secure URL
            image_url = result.get('secure_url')
            
            return True, image_url
            
        except Exception as e:
            print(f"Error uploading image: {e}")
            return False, str(e)
    
    def upload_profile_picture(self, image_file, user_id):
        """
        Upload user profile picture
        
        Args:
            image_file: Image file from file uploader
            user_id: User's Firebase ID
            
        Returns:
            tuple: (success, image_url or error_message)
        """
        try:
            # Resize image for profile picture
            img = Image.open(image_file)
            
            # Resize to 400x400 (square)
            img.thumbnail((400, 400), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr.seek(0)
            
            # Upload to Cloudinary
            public_id = f"profile_{user_id}"
            success, result = self.upload_image(
                img_byte_arr,
                folder="cyberbullying_app/profiles",
                public_id=public_id
            )
            
            return success, result
            
        except Exception as e:
            print(f"Error uploading profile picture: {e}")
            return False, str(e)
    
    def upload_post_image(self, image_file, user_id, post_id):
        """
        Upload post image
        
        Args:
            image_file: Image file from file uploader
            user_id: User's Firebase ID
            post_id: Post ID (or timestamp)
            
        Returns:
            tuple: (success, image_url or error_message)
        """
        try:
            # Resize image for post
            img = Image.open(image_file)
            
            # Resize to max 1200px width while maintaining aspect ratio
            max_width = 1200
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr.seek(0)
            
            # Upload to Cloudinary
            public_id = f"post_{user_id}_{post_id}"
            success, result = self.upload_image(
                img_byte_arr,
                folder="cyberbullying_app/posts",
                public_id=public_id
            )
            
            return success, result
            
        except Exception as e:
            print(f"Error uploading post image: {e}")
            return False, str(e)
    
    def delete_image(self, public_id):
        """
        Delete image from Cloudinary
        
        Args:
            public_id: Public ID of the image to delete
            
        Returns:
            bool: Success status
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
            
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False
    
    def get_default_profile_picture(self):
        """
        Get default profile picture URL
        
        Returns:
            str: URL of default profile picture
        """
        # Using a placeholder service for default avatars
        return "https://ui-avatars.com/api/?name=User&background=random&size=400"


# Example usage
if __name__ == "__main__":
    print("Cloudinary Upload Module loaded successfully!")
