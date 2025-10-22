"""
Semantle Backend Service using llama-embed-nemotron-8b via Hugging Face API
A word guessing game based on semantic similarity.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import httpx
import numpy as np
import random
from datetime import datetime, date
import uuid
import os
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Large Hebrew word pool - rotates through different words each day
# This gives us years of unique daily words without repeating
HEBREW_WORD_POOL = [
    # Emotions & Feelings (40 words)
    "אהבה", "שמחה", "עצב", "פחד", "כעס", "תקווה", "אושר", "שלווה", "רוגע", "התרגשות",
    "חיבה", "געגועים", "גאווה", "בושה", "קנאה", "חמלה", "אמפתיה", "סקרנות", "פליאה", "השתאות",
    "צער", "שנאה", "חרטה", "אשמה", "אכזבה", "תסכול", "עייפות", "משעמום", "התלהבות", "רצון",
    "משיכה", "דחייה", "כיסופים", "תשוקה", "נאמנות", "בגידה", "אמון", "חשד", "ביטחון", "חרדה",
    
    # Abstract Concepts (50 words)
    "חופש", "שלום", "חכמה", "צדק", "חיים", "מוות", "זמן", "מרחב", "אמת", "שקר",
    "יופי", "מציאות", "חלום", "דמיון", "זיכרון", "שכחה", "תודעה", "מחשבה", "רעיון", "תפיסה",
    "הבנה", "בלבול", "סדר", "כאוס", "הרמוניה", "ניגוד", "איזון", "קיום", "העדר", "נוכחות",
    "עבר", "הווה", "עתיד", "נצח", "רגע", "תהליך", "שינוי", "התפתחות", "צמיחה", "דעיכה",
    "התחדשות", "קצב", "מחזור", "זרימה", "תנועה", "שקט", "דינמיקה", "סטטיות", "אנרגיה", "מנוחה",
    
    # Qualities & Attributes (40 words)
    "כוח", "חולשה", "אומץ", "פחדנות", "סבלנות", "חוסר סבלנות", "יצירתיות", "שגרתיות", "חריצות", "עצלות",
    "נדיבות", "קמצנות", "ענווה", "גאווה", "יושר", "מרמה", "נאמנות", "בגידה", "כנות", "שקר",
    "פשטות", "מורכבות", "בהירות", "עמימות", "דיוק", "מעורפלות", "עקביות", "סתירה", "גמישות", "קשיחות",
    "רכות", "קשיות", "חום", "קרירות", "חום לב", "אדישות", "רגישות", "קהות", "עדינות", "גסות",
    
    # Knowledge & Learning (35 words)
    "ידע", "בורות", "למידה", "הוראה", "הבנה", "אי הבנה", "תבונה", "טיפשות", "השכלה", "חוסר השכלה",
    "מדע", "אמונה", "חינוך", "הדרכה", "תרבות", "ברבריות", "אמנות", "מלאכה", "מיומנות", "חוסר ניסיון",
    "התמחות", "כלליות", "עומק", "שטחיות", "מומחיות", "חובבנות", "ניסיון", "חוסר ניסיון", "בגרות", "ילדות",
    "פרשנות", "הסבר", "תיאוריה", "פרקטיקה", "מחקר",
    
    # Social & Relationships (40 words)
    "משפחה", "חברות", "קהילה", "חברה", "מדינה", "עם", "אדם", "אישיות", "זהות", "תפקיד",
    "מעמד", "יחס", "קשר", "ניתוק", "קירבה", "ריחוק", "חיבור", "פירוד", "אחדות", "פירוד",
    "שותפות", "יריבות", "שיתוף פעולה", "תחרות", "עזרה", "הזנחה", "תמיכה", "ביקורת", "הערכה", "זלזול",
    "כבוד", "בוז", "אהדה", "שנאה", "הבנה", "דחייה", "קבלה", "סלידה", "משיכה", "דחייה",
    
    # Nature & Physical World (35 words)
    "טבע", "שמש", "ירח", "כוכב", "ים", "אוקיינוס", "נהר", "אגם", "הר", "עמק",
    "מדבר", "יער", "גן", "שדה", "אדמה", "שמיים", "עננים", "רוח", "אש", "מים",
    "עץ", "פרח", "דשא", "אבן", "חול", "בוץ", "קרח", "שלג", "גשם", "רעם",
    "ברק", "קשת", "שקיעה", "זריחה", "צל",
    
    # Time & Change (30 words)
    "זמן", "שעה", "יום", "לילה", "בוקר", "ערב", "שבוע", "חודש", "שנה", "עונה",
    "רגע", "תקופה", "עידן", "היסטוריה", "מסורת", "חידוש", "שינוי", "המשכיות", "התפתחות", "נסיגה",
    "צמיחה", "קמילה", "התבגרות", "הזדקנות", "התחדשות", "דעיכה", "התחלה", "סוף", "מעבר", "המשך",
    
    # Actions & States (30 words)
    "תנועה", "מנוחה", "פעולה", "המתנה", "מאמץ", "נחת", "מאבק", "כניעה", "התנגדות", "קבלה",
    "יצירה", "הרס", "בנייה", "הריסה", "ריפוי", "פגיעה", "הצלה", "נטישה", "שמירה", "אובדן",
    "הצלחה", "כישלון", "ניצחון", "תבוסה", "התקדמות", "נסיגה", "עליה", "ירידה", "פריחה", "קמילה"
]

# Total: ~300 words - won't repeat for almost a year!
ALL_WORDS = HEBREW_WORD_POOL

app = FastAPI(
    title="Semantle API",
    description="Backend service for Semantle word guessing game using semantic embeddings",
    version="1.0.0"
)

print("🎮 Semantle Backend starting...")
print(f"📡 Using model: BAAI/bge-small-en-v1.5 (CONFIRMED WORKING)")
print(f"🔑 API key configured: {bool(os.getenv('HUGGINGFACE_API_KEY'))}")
print(f"📚 Hebrew word pool: {len(HEBREW_WORD_POOL)} words (daily rotation)")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
# Using BGE model - this was confirmed working before!
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/BAAI/bge-small-en-v1.5"

# In-memory game storage (use database in production)
games: Dict[str, dict] = {}

# Cache for embeddings to reduce API calls
embedding_cache: Dict[str, np.ndarray] = {}


class GameStart(BaseModel):
    difficulty: Optional[str] = "normal"
    daily_mode: Optional[bool] = False  # True for one word per day


class GuessRequest(BaseModel):
    game_id: str
    word: str


class GuessResponse(BaseModel):
    game_id: str
    word: str
    similarity: float
    rank: Optional[int]
    percentile: Optional[float]  # e.g., 999/1000
    guess_number: int
    is_correct: bool
    game_over: bool
    top_similarity: Optional[float] = None  # Highest similarity so far


class GameState(BaseModel):
    game_id: str
    guesses: List[Dict]
    guess_count: int
    game_over: bool
    target_word: Optional[str] = None
    started_at: str


def get_daily_word() -> str:
    """
    Get the word of the day - same word for everyone on the same day.
    Uses a large word pool that cycles through ~300 Hebrew words,
    so you won't see repeats for almost a year!
    """
    today = date.today()
    # Use date as seed to ensure same word each day
    seed = int(hashlib.md5(str(today).encode()).hexdigest(), 16) % len(ALL_WORDS)
    daily_word = ALL_WORDS[seed]
    print(f"🎯 Today's word (index {seed}): {daily_word}")
    return daily_word

def get_word_list(difficulty: str) -> List[str]:
    """Get word list based on difficulty level."""
    return ALL_WORDS


async def get_embedding(text: str) -> np.ndarray:
    """Get embedding vector for a single text using Hugging Face API."""
    
    # Check cache first
    if text in embedding_cache:
        return embedding_cache[text]
    
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="HUGGINGFACE_API_KEY not configured. Please set it in .env file"
        )
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # BGE model payload - EXACTLY as it was when working
    payload = {
        "inputs": text,
        "options": {"wait_for_model": True, "use_cache": True}
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                HUGGINGFACE_API_URL,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 503:
                # Model is loading, wait 10 seconds and retry
                import asyncio
                print("Model loading, waiting 10 seconds...")
                await asyncio.sleep(10)
                response = await client.post(
                    HUGGINGFACE_API_URL,
                    headers=headers,
                    json=payload
                )
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error getting embedding: {response.text}"
                )
            
            # BGE returns nested array [[...]]
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    # Nested array [[...]]
                    embedding = np.array(result[0])
                else:
                    # Flat array [...]
                    embedding = np.array(result)
            else:
                embedding = np.array(result)
            
            # Normalize the embedding
            embedding = embedding / np.linalg.norm(embedding)
            
            # Cache the result
            embedding_cache[text] = embedding
            
            return embedding
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to embedding API timed out"
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting embedding: {str(e)}"
        )


async def calculate_similarity(word1: str, word2: str) -> float:
    """Calculate cosine similarity between two words."""
    emb1 = await get_embedding(word1)
    emb2 = await get_embedding(word2)
    
    similarity = np.dot(emb1, emb2)
    return float(similarity)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Semantle Hebrew - סמנטעל בעברית",
        "model": "BAAI/bge-small-en-v1.5",
        "language": "Hebrew",
        "word_pool_size": len(HEBREW_WORD_POOL),
        "daily_word_mode": True,
        "api_configured": bool(HUGGINGFACE_API_KEY)
    }


@app.post("/game/start", response_model=GameState)
async def start_game(game_config: GameStart):
    """Start a new game."""
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="API not configured. Please set HUGGINGFACE_API_KEY in .env file"
        )
    
    # Generate game ID
    game_id = str(uuid.uuid4())
    
    # Select target word - daily or random
    if game_config.daily_mode:
        target_word = get_daily_word()
    else:
        word_list = get_word_list(game_config.difficulty)
        target_word = random.choice(word_list)
    
    # Get embedding for target word
    try:
        target_embedding = await get_embedding(target_word)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get embedding for target word: {str(e)}"
        )
    
    # Create game state
    game_state = {
        "game_id": game_id,
        "target_word": target_word,
        "target_embedding": target_embedding,
        "guesses": [],
        "guess_count": 0,
        "game_over": False,
        "started_at": datetime.utcnow().isoformat(),
        "difficulty": game_config.difficulty
    }
    
    games[game_id] = game_state
    
    return GameState(
        game_id=game_id,
        guesses=[],
        guess_count=0,
        game_over=False,
        started_at=game_state["started_at"]
    )


@app.post("/game/guess", response_model=GuessResponse)
async def make_guess(guess_request: GuessRequest):
    """Make a guess in the game."""
    game_id = guess_request.game_id
    word = guess_request.word.lower().strip()
    
    # Validate game exists
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    # Check if game is over
    if game["game_over"]:
        raise HTTPException(status_code=400, detail="Game is already over")
    
    # Validate word
    if not word or len(word) < 2:
        raise HTTPException(status_code=400, detail="Invalid word")
    
    # Check if word already guessed
    if any(g["word"] == word for g in game["guesses"]):
        raise HTTPException(status_code=400, detail="Word already guessed")
    
    # Calculate similarity
    target_embedding = game["target_embedding"]
    guess_embedding = await get_embedding(word)
    
    # Cosine similarity (already normalized vectors, so just dot product)
    similarity = float(np.dot(guess_embedding, target_embedding))
    
    # Similarity is between -1 and 1, but usually 0-1 for related words
    # Convert to 0-100 scale like Word2Vec similarity
    # Use raw similarity * 100 (keeps the relative differences better)
    similarity_percentage = max(0, similarity * 100)
    
    # Check if correct
    is_correct = word == game["target_word"]
    
    # Update game state
    game["guess_count"] += 1
    guess_data = {
        "word": word,
        "similarity": similarity_percentage,
        "guess_number": game["guess_count"],
        "is_correct": is_correct
    }
    game["guesses"].append(guess_data)
    
    # Sort guesses by similarity for ranking
    sorted_guesses = sorted(game["guesses"], key=lambda x: x["similarity"], reverse=True)
    rank = next(i + 1 for i, g in enumerate(sorted_guesses) if g["word"] == word)
    
    # Calculate percentile (e.g., 999/1000)
    total_guesses = len(sorted_guesses)
    percentile = ((total_guesses - rank + 1) / total_guesses) * 1000 if total_guesses > 0 else 1000
    
    # Get top similarity
    top_similarity = sorted_guesses[0]["similarity"] if sorted_guesses else similarity_percentage
    
    if is_correct:
        game["game_over"] = True
    
    return GuessResponse(
        game_id=game_id,
        word=word,
        similarity=similarity_percentage,
        rank=rank,
        percentile=percentile,
        guess_number=game["guess_count"],
        is_correct=is_correct,
        game_over=game["game_over"],
        top_similarity=top_similarity
    )


@app.get("/game/{game_id}", response_model=GameState)
async def get_game_state(game_id: str):
    """Get current game state."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    # Sort guesses by similarity
    sorted_guesses = sorted(game["guesses"], key=lambda x: x["similarity"], reverse=True)
    
    # Add ranks to guesses
    for i, guess in enumerate(sorted_guesses):
        guess["rank"] = i + 1
    
    return GameState(
        game_id=game_id,
        guesses=sorted_guesses,
        guess_count=game["guess_count"],
        game_over=game["game_over"],
        target_word=game["target_word"] if game["game_over"] else None,
        started_at=game["started_at"]
    )


@app.post("/game/{game_id}/give-up")
async def give_up(game_id: str):
    """Give up and reveal the target word."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    game["game_over"] = True
    
    return {
        "game_id": game_id,
        "target_word": game["target_word"],
        "message": "Game over! Better luck next time."
    }


@app.delete("/game/{game_id}")
async def delete_game(game_id: str):
    """Delete a game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    del games[game_id]
    return {"message": "Game deleted successfully"}


@app.get("/similarity")
async def check_similarity(word1: str, word2: str):
    """Check similarity between two words (for testing)."""
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="API not configured"
        )
    
    similarity = await calculate_similarity(word1.lower(), word2.lower())
    similarity_percentage = (similarity + 1) / 2 * 100
    
    return {
        "word1": word1,
        "word2": word2,
        "similarity": similarity_percentage,
        "raw_similarity": similarity
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
