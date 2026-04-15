"""Minimal test script to verify the application works"""
import requests
import json

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_create_prompt():
    """Test creating a prompt"""
    try:
        response = requests.post(
            "http://localhost:8000/prompts/",
            json={"name": "test_prompt", "description": "Test description"}
        )
        print(f"Create prompt: {response.status_code}")
        if response.status_code == 201:
            print(f"Response: {response.json()}")
        return response
    except Exception as e:
        print(f"Create prompt failed: {e}")
        return None

if __name__ == "__main__":
    print("Testing Prompt Versioning System...")
    print("-" * 40)
    
    if test_health():
        print("\n✅ Server is running!")
        test_create_prompt()
    else:
        print("\n❌ Server is not responding. Make sure it's running on port 8000")