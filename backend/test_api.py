import requests
import json

BASE_URL = 'http://localhost:5003'

def test_endpoints():
    # Test GET endpoint
    print("\nTesting GET /test:")
    response = requests.get(f"{BASE_URL}/test")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test POST endpoint
    print("\nTesting POST /register:")
    data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }
    response = requests.post(
        f"{BASE_URL}/register",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_endpoints() 