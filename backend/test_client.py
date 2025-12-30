"""
Test client for StormBuster API
Run this to test the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_models():
    """Test models endpoint"""
    print("\n📋 Testing Models Endpoint...")
    response = requests.get(f"{BASE_URL}/models?tier=professional")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_chat():
    """Test chat endpoint"""
    print("\n💬 Testing Chat Endpoint...")
    
    payload = {
        "message": "What's the best way to approach roofing leads after a hailstorm?",
        "model_id": "gpt-3.5-turbo",
        "subscription_tier": "professional",
        "context": "storm_damage"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"✅ Chat successful!")
        print(f"Model used: {result.get('model_used')}")
        print(f"Tokens: {result.get('tokens_used')}")
        print(f"Cost: ${result.get('cost', 0):.6f}")
        print(f"Response: {result.get('response', '')[:200]}...")
    else:
        print(f"❌ Chat failed: {result.get('error')}")

def test_analyze_storm():
    """Test storm analysis endpoint"""
    print("\n🌩️ Testing Storm Analysis Endpoint...")
    
    payload = {
        "date": "2024-01-15",
        "location": "Dallas, TX",
        "hail_size": "2.5 inches",
        "property_count": 150,
        "avg_property_value": "$350,000"
    }
    
    response = requests.post(f"{BASE_URL}/analyze-storm", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"✅ Analysis successful!")
        print(f"Response: {result.get('response', '')[:200]}...")
    else:
        print(f"❌ Analysis failed: {result.get('error')}")

def test_chat_history():
    """Test chat history endpoint"""
    print("\n📜 Testing Chat History Endpoint...")
    response = requests.get(f"{BASE_URL}/chat-history?limit=10")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Messages in history: {len(result.get('history', []))}")

def test_usage_stats():
    """Test usage stats endpoint"""
    print("\n📊 Testing Usage Stats Endpoint...")
    response = requests.get(f"{BASE_URL}/usage-stats?tier=professional")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Stats: {json.dumps(result.get('stats'), indent=2)}")

def main():
    """Run all tests"""
    print("=" * 70)
    print("STORMBUSTER API TEST CLIENT")
    print("=" * 70)
    
    try:
        # Test endpoints
        test_health()
        test_get_models()
        test_chat()
        test_analyze_storm()
        test_chat_history()
        test_usage_stats()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure the backend server is running:")
        print("  python backend/app.py")
        print("  or")
        print("  uvicorn backend.app:app --reload")

if __name__ == "__main__":
    main()

