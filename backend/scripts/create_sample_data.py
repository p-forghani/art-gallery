import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.user import User
from app.models.art import Art
from datetime import datetime

def create_sample_data():
    app = create_app()
    with app.app_context():
        # Sample users
        users = [
            {
                'email': 'admin@example.com',
                'name': 'Admin User',
                'password': 'admin123',
                'is_admin': True
            },
            {
                'email': 'artist@example.com',
                'name': 'Artist User',
                'password': 'artist123',
                'is_admin': False
            }
        ]

        # Create users
        for user_data in users:
            if not User.objects(email=user_data['email']).first():
                user = User(**user_data)
                user.save()
                print(f"Created user: {user_data['email']}")

        # Sample artworks
        artworks = [
            {
                'name': 'Sunset Landscape',
                'description': 'A beautiful sunset over mountains',
                'category_id': 'landscape',
                'tag_ids': ['nature', 'sunset'],
                'price': 299.99,
                'image_path': 'sample/sunset.jpg',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Abstract Art',
                'description': 'Modern abstract painting',
                'category_id': 'abstract',
                'tag_ids': ['modern', 'colorful'],
                'price': 199.99,
                'image_path': 'sample/abstract.jpg',
                'created_at': datetime.utcnow()
            }
        ]

        # Create artworks
        for art_data in artworks:
            if not Art.objects(name=art_data['name']).first():
                art = Art(**art_data)
                art.save()
                print(f"Created artwork: {art_data['name']}")

if __name__ == '__main__':
    create_sample_data() 