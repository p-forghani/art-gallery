import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

def test_endpoints():
    app = create_app()
    client = app.test_client()
    
    # Test the test endpoint
    print("\nTesting GET /test:")
    response = client.get('/test')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test registration
    print("\nTesting POST /register:")
    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test login
    print("\nTesting POST /login:")
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.get_json()}")

if __name__ == '__main__':
    test_endpoints() 