import unittest
from app import create_app
from config import Config
import certifi

class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb+srv://alireza:ali1378reza1742@cluster0.ug6m1cu.mongodb.net/test_db?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true'
    MONGODB_SETTINGS = {
        'host': MONGO_URI,
        'ssl': True,
        'ssl_cert_reqs': None,
        'tlsCAFile': certifi.where()
    }

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Clear the test database
        self.app.mongo.db.users.delete_many({})

    def tearDown(self):
        # Clean up the test database
        self.app.mongo.db.users.delete_many({})
        self.app_context.pop()

    def test_register(self):
        # Test registration with valid data
        response = self.client.post('/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        })
        self.assertEqual(response.status_code, 201)
        
    def test_login(self):
        # First register a user
        self.client.post('/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        })
        
        # Test login with valid credentials
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

if __name__ == '__main__':
    unittest.main() 