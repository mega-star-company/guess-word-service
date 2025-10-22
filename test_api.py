"""
Test script for the Semantle API
Run this after starting the server to test functionality
"""

import requests
import time
from typing import Optional

BASE_URL = "http://localhost:8080"


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_similarity():
    """Test the similarity endpoint."""
    print("Testing similarity calculation...")
    response = requests.get(
        f"{BASE_URL}/similarity",
        params={"word1": "happy", "word2": "joyful"}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Similarity between 'happy' and 'joyful': {data['similarity']:.2f}%\n")
    return response.status_code == 200


def test_game_flow():
    """Test a complete game flow."""
    print("Testing complete game flow...")
    
    # Start a new game
    print("1. Starting new game...")
    response = requests.post(
        f"{BASE_URL}/game/start",
        json={"difficulty": "easy"}
    )
    
    if response.status_code != 200:
        print(f"Failed to start game: {response.status_code}")
        return False
    
    game_data = response.json()
    game_id = game_data["game_id"]
    print(f"Game started with ID: {game_id}\n")
    
    # Make some guesses
    test_words = ["happy", "sad", "angry", "love", "joy"]
    print("2. Making guesses...")
    
    for word in test_words:
        print(f"Guessing: {word}")
        response = requests.post(
            f"{BASE_URL}/game/guess",
            json={"game_id": game_id, "word": word}
        )
        
        if response.status_code != 200:
            print(f"Failed to make guess: {response.status_code}")
            continue
        
        result = response.json()
        print(f"  Similarity: {result['similarity']:.2f}%")
        print(f"  Rank: {result['rank']}")
        print(f"  Correct: {result['is_correct']}\n")
        
        if result["is_correct"]:
            print(f"🎉 Guessed the word in {result['guess_number']} tries!")
            return True
        
        time.sleep(0.5)  # Small delay between guesses
    
    # Get game state
    print("3. Getting game state...")
    response = requests.get(f"{BASE_URL}/game/{game_id}")
    
    if response.status_code != 200:
        print(f"Failed to get game state: {response.status_code}")
        return False
    
    state = response.json()
    print(f"Total guesses: {state['guess_count']}")
    print(f"Game over: {state['game_over']}\n")
    
    # Give up to reveal the word
    print("4. Giving up to reveal word...")
    response = requests.post(f"{BASE_URL}/game/{game_id}/give-up")
    
    if response.status_code != 200:
        print(f"Failed to give up: {response.status_code}")
        return False
    
    result = response.json()
    print(f"Target word was: {result['target_word']}\n")
    
    return True


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    # Test invalid game ID
    print("1. Testing invalid game ID...")
    response = requests.post(
        f"{BASE_URL}/game/guess",
        json={"game_id": "invalid-id", "word": "test"}
    )
    print(f"Status (should be 404): {response.status_code}\n")
    
    # Test duplicate guess
    print("2. Testing duplicate guess...")
    # Start game
    response = requests.post(
        f"{BASE_URL}/game/start",
        json={"difficulty": "easy"}
    )
    game_id = response.json()["game_id"]
    
    # Make first guess
    requests.post(
        f"{BASE_URL}/game/guess",
        json={"game_id": game_id, "word": "test"}
    )
    
    # Try same guess again
    response = requests.post(
        f"{BASE_URL}/game/guess",
        json={"game_id": game_id, "word": "test"}
    )
    print(f"Status (should be 400): {response.status_code}\n")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Semantle API Test Suite")
    print("=" * 60 + "\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Similarity Calculation", test_similarity),
        ("Complete Game Flow", test_game_flow),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 60}")
        print(f"Running: {test_name}")
        print("=" * 60 + "\n")
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Error: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Delay between tests
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the server is running at http://localhost:8080")
        print("Start it with: python3 main.py")

