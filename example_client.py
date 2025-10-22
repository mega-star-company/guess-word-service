"""
Example client for playing Semantle
"""

import requests
import sys


class SemantleClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.game_id = None
    
    def start_game(self, difficulty: str = "normal"):
        """Start a new game."""
        response = requests.post(
            f"{self.base_url}/game/start",
            json={"difficulty": difficulty}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.game_id = data["game_id"]
            print(f"🎮 New game started! (Difficulty: {difficulty})")
            print(f"Game ID: {self.game_id}\n")
            return True
        else:
            print(f"❌ Failed to start game: {response.status_code}")
            return False
    
    def make_guess(self, word: str):
        """Make a guess."""
        if not self.game_id:
            print("❌ No active game. Start a game first!")
            return None
        
        response = requests.post(
            f"{self.base_url}/game/guess",
            json={"game_id": self.game_id, "word": word.lower().strip()}
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"❌ {error.get('detail', 'Invalid guess')}")
            return None
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    
    def get_game_state(self):
        """Get current game state."""
        if not self.game_id:
            print("❌ No active game.")
            return None
        
        response = requests.get(f"{self.base_url}/game/{self.game_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get game state: {response.status_code}")
            return None
    
    def give_up(self):
        """Give up and reveal the word."""
        if not self.game_id:
            print("❌ No active game.")
            return None
        
        response = requests.post(f"{self.base_url}/game/{self.game_id}/give-up")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to give up: {response.status_code}")
            return None


def print_similarity_bar(similarity: float):
    """Print a visual similarity bar."""
    bar_length = 40
    filled = int(bar_length * (similarity / 100))
    bar = "█" * filled + "░" * (bar_length - filled)
    
    # Color coding
    if similarity >= 90:
        color = "🔥"
    elif similarity >= 70:
        color = "🌟"
    elif similarity >= 50:
        color = "😊"
    elif similarity >= 30:
        color = "🤔"
    else:
        color = "❄️"
    
    return f"{color} [{bar}] {similarity:.2f}%"


def play_game():
    """Main game loop."""
    print("=" * 60)
    print("🎯 SEMANTLE - Semantic Word Guessing Game")
    print("=" * 60)
    print("\nTry to guess the secret word!")
    print("You'll get feedback based on semantic similarity.\n")
    
    client = SemantleClient()
    
    # Choose difficulty
    print("Choose difficulty:")
    print("1. Easy (common words)")
    print("2. Normal (abstract concepts)")
    print("3. Hard (complex words)")
    
    difficulty_map = {"1": "easy", "2": "normal", "3": "hard"}
    choice = input("\nEnter choice (1-3) [default: 2]: ").strip() or "2"
    difficulty = difficulty_map.get(choice, "normal")
    
    # Start game
    if not client.start_game(difficulty):
        return
    
    guess_count = 0
    
    while True:
        # Get user input
        word = input(f"\n[Guess #{guess_count + 1}] Enter your guess (or 'quit'/'hint'): ").strip().lower()
        
        if word == "quit":
            print("\n👋 Thanks for playing!")
            result = client.give_up()
            if result:
                print(f"The word was: {result['target_word']}")
            break
        
        if word == "hint":
            state = client.get_game_state()
            if state and state["guesses"]:
                top_guesses = sorted(state["guesses"], key=lambda x: x["similarity"], reverse=True)[:5]
                print("\n🎯 Your top 5 guesses:")
                for i, g in enumerate(top_guesses, 1):
                    print(f"  {i}. {g['word']}: {g['similarity']:.2f}%")
            else:
                print("\n💡 No guesses yet!")
            continue
        
        if not word:
            print("❌ Please enter a word!")
            continue
        
        # Make guess
        result = client.make_guess(word)
        
        if not result:
            continue
        
        guess_count += 1
        
        # Display result
        print("\n" + "─" * 60)
        print(f"Word: {result['word']}")
        print(print_similarity_bar(result['similarity']))
        print(f"Rank: #{result['rank']} out of {result['guess_number']} guesses")
        
        if result["is_correct"]:
            print("\n" + "🎉" * 20)
            print(f"🏆 CORRECT! You guessed the word in {guess_count} tries!")
            print("🎉" * 20)
            break
        else:
            # Give hints based on similarity
            if result["similarity"] >= 90:
                print("💬 You're EXTREMELY close!")
            elif result["similarity"] >= 70:
                print("💬 Very warm!")
            elif result["similarity"] >= 50:
                print("💬 Getting warmer...")
            elif result["similarity"] >= 30:
                print("💬 Somewhat related")
            else:
                print("💬 Pretty cold")
        
        print("─" * 60)


def main():
    """Entry point."""
    try:
        # Test connection
        response = requests.get("http://localhost:8080/")
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:8080")
        print("\nPlease start the server first:")
        print("  cd service-repo")
        print("  python3 main.py")
        sys.exit(1)
    
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

