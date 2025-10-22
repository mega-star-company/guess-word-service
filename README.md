# Semantle Backend Service

A backend service for the Semantle word guessing game using NVIDIA's `llama-embed-nemotron-8b` embedding model via **cloud API**. Players try to guess a target word based on semantic similarity feedback.

## ✨ Features

- 🎮 Word guessing game based on semantic similarity
- ☁️ **Cloud-based** - No need to download huge models!
- 🧠 Powered by state-of-the-art llama-embed-nemotron-8b embedding model
- 🎯 Three difficulty levels (Easy, Normal, Hard)
- 📊 Real-time similarity scoring and ranking
- ⚡ Fast API responses via Hugging Face Inference API
- 🔄 RESTful API built with FastAPI
- 🆓 **Free to use** with Hugging Face API (free tier available)

## How Semantle Works

Players try to guess a secret target word. After each guess, the game provides:

- **Similarity Score**: How semantically similar the guess is to the target (0-100%)
- **Rank**: Where this guess ranks among all guesses so far
- The game continues until the player guesses the correct word

## Requirements

- Python 3.9+
- Free Hugging Face account and API key
- ~50MB disk space (lightweight dependencies only!)
- No GPU or special hardware needed ✅

## 🚀 Installation (3 Simple Steps!)

### Step 1: Install Dependencies

```bash
cd service-repo
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Step 2: Configure API Key

Get a FREE Hugging Face API key:

**Option A: Use the wizard (recommended)**

```bash
./configure_api.sh
```

**Option B: Manual setup**

1. Sign up at [https://huggingface.co/join](https://huggingface.co/join) (free!)
2. Go to [Settings > Tokens](https://huggingface.co/settings/tokens)
3. Create a token with "Read" permission
4. Create `.env` file:

```bash
echo "HUGGINGFACE_API_KEY=hf_your_token_here" > .env
```

### Step 3: Test Connection (Optional but Recommended)

```bash
python3 test_connection.py
```

This will verify your API key works before starting the server.

## Running the Service

### Quick Start (macOS/Linux)

```bash
./run.sh
```

### Manual Start

```bash
source venv/bin/activate  # Activate virtual environment first
python3 main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at `http://localhost:8080`

**Note:** The first API request may take 10-20 seconds as the model loads on Hugging Face's servers (subsequent requests are instant!)

### API Documentation

Once running, visit:

- **Interactive API docs**: http://localhost:8080/docs
- **Alternative docs**: http://localhost:8080/redoc

## API Endpoints

### 1. Start a New Game

```bash
POST /game/start
```

**Request Body:**

```json
{
  "difficulty": "normal" // Options: "easy", "normal", "hard"
}
```

**Response:**

```json
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "guesses": [],
  "guess_count": 0,
  "game_over": false,
  "started_at": "2025-10-22T10:30:00"
}
```

### 2. Make a Guess

```bash
POST /game/guess
```

**Request Body:**

```json
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "word": "happy"
}
```

**Response:**

```json
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "word": "happy",
  "similarity": 73.45,
  "rank": 1,
  "guess_number": 1,
  "is_correct": false,
  "game_over": false
}
```

### 3. Get Game State

```bash
GET /game/{game_id}
```

**Response:**

```json
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "guesses": [
    {
      "word": "happy",
      "similarity": 73.45,
      "guess_number": 1,
      "rank": 1,
      "is_correct": false
    }
  ],
  "guess_count": 1,
  "game_over": false,
  "target_word": null,
  "started_at": "2025-10-22T10:30:00"
}
```

### 4. Give Up

```bash
POST /game/{game_id}/give-up
```

**Response:**

```json
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "target_word": "joyful",
  "message": "Game over! Better luck next time."
}
```

### 5. Check Similarity (Testing)

```bash
GET /similarity?word1=happy&word2=joyful
```

**Response:**

```json
{
  "word1": "happy",
  "word2": "joyful",
  "similarity": 85.32,
  "raw_similarity": 0.7064
}
```

## Example Usage

### Using cURL

```bash
# Start a game
curl -X POST http://localhost:8080/game/start \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "normal"}'

# Make a guess
curl -X POST http://localhost:8080/game/guess \
  -H "Content-Type: application/json" \
  -d '{"game_id": "YOUR_GAME_ID", "word": "happy"}'

# Get game state
curl http://localhost:8080/game/YOUR_GAME_ID
```

### Using Python

```bash
# Run the example client
python3 example_client.py

# Or use the test suite
python3 test_api.py
```

## Model Information

This service uses NVIDIA's `llama-embed-nemotron-8b` model:

- **Architecture**: Llama-3.1-8B with bidirectional attention
- **Parameters**: 7.5B
- **Embedding Dimension**: 4096
- **Max Sequence Length**: 32,768 tokens
- **Performance**: #1 on MTEB Multilingual leaderboard (as of Oct 2025)

### Model Citation

```bibtex
@misc{lee2024nv,
  title={NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models},
  author={Lee, Chankyu and Roy, Rajarshi and Xu, Mengyao and Raiman, Jonathan and Shoeybi, Mohammad and Catanzaro, Bryan and Ping, Wei},
  journal={arXiv preprint arXiv:2405.17428},
  year={2024}
}
```

## Performance Notes

- **First Request**: Model loading takes ~30-60 seconds on first startup
- **Subsequent Requests**: ~100-300ms per guess (GPU) or ~1-3s (CPU)
- **Memory Usage**: ~16GB VRAM (GPU) or ~32GB RAM (CPU)

## Difficulty Levels

- **Easy**: Common everyday words (happy, cat, home, etc.)
- **Normal**: Abstract concepts (wisdom, courage, harmony, etc.)
- **Hard**: Complex/rare words (ephemeral, serendipity, paradigm, etc.)

## Production Considerations

For production deployment, consider:

1. **Database**: Replace in-memory storage with Redis or PostgreSQL
2. **Authentication**: Add API key or OAuth authentication
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Caching**: Cache embeddings for common words
5. **Load Balancing**: Use multiple instances behind a load balancer
6. **Monitoring**: Add logging and monitoring (Prometheus, Grafana)
7. **CORS**: Configure specific allowed origins instead of "\*"

## Troubleshooting

### Model fails to load

- Ensure you have enough RAM/VRAM
- Try CPU mode if GPU memory is insufficient
- Check internet connection for model download

### Slow inference

- Use GPU instead of CPU
- Reduce batch size if out of memory
- Consider model quantization for faster inference

### CUDA errors

- Ensure CUDA drivers are up to date
- Verify PyTorch CUDA version matches your CUDA installation

## License

This project uses NVIDIA's llama-embed-nemotron-8b model which is for **non-commercial/research use only**.

See: [NVIDIA License](https://developer.nvidia.com/nvidia-software-license) and [Llama-3.1 Community License](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/LICENSE)

## Links

- [Model on Hugging Face](https://huggingface.co/nvidia/llama-embed-nemotron-8b)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Original Semantle Game](https://semantle.com/)
