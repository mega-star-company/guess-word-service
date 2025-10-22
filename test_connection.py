#!/usr/bin/env python3
"""
Quick test to verify your Hugging Face API key works
"""

import os
from dotenv import load_dotenv
import httpx
import sys

# Load .env file
load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

def test_api_key():
    """Test if the API key works."""
    print("🧪 Testing Hugging Face API Connection...")
    print("=" * 50)
    
    if not API_KEY:
        print("❌ Error: HUGGINGFACE_API_KEY not found in .env file")
        print("\nPlease run: ./configure_api.sh")
        print("Or create a .env file with your API key")
        return False
    
    print(f"✅ API key found: {API_KEY[:8]}...")
    print("\n📡 Testing connection to Hugging Face API...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": "hello",
        "options": {"wait_for_model": True}
    }
    
    url = "https://api-inference.huggingface.co/models/nvidia/llama-embed-nemotron-8b"
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                print("✅ API connection successful!")
                print(f"✅ Received embedding vector (dimension: {len(response.json())})")
                print("\n" + "=" * 50)
                print("🎉 Everything is working! You can now start the server:")
                print("   python3 main.py")
                print("=" * 50)
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed - Invalid API key")
                print("\nPlease check your API key and try again:")
                print("   ./configure_api.sh")
                return False
            elif response.status_code == 503:
                print("⏳ Model is loading on Hugging Face servers...")
                print("This is normal for the first request. Waiting...")
                
                # Retry once
                import time
                time.sleep(10)
                response = client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    print("✅ API connection successful!")
                    print("✅ Model loaded and ready!")
                    return True
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(response.text)
                    return False
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_api_key()
    sys.exit(0 if success else 1)

