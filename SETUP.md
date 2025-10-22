# Quick Setup Guide

## 🚀 Setup in 3 Steps

### 1. Install Dependencies

```bash
cd service-repo
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 2. Get Your Hugging Face API Key

1. Go to [Hugging Face](https://huggingface.co/) and create a free account
2. Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Click "Create new token"
4. Give it a name like "semantle-api" and select "Read" permission
5. Copy the token

### 3. Configure API Key

Create a `.env` file:

```bash
echo "HUGGINGFACE_API_KEY=your_actual_key_here" > .env
```

Replace `your_actual_key_here` with your actual token from step 2.

## ✅ Start the Server

```bash
python3 main.py
```

The server will start at `http://localhost:8080`

## 🎮 Play the Game

In a new terminal:

```bash
python3 example_client.py
```

## 🧪 Test the API

```bash
# Test health check
curl http://localhost:8080/

# Test similarity
curl "http://localhost:8080/similarity?word1=happy&word2=joyful"
```

That's it! No need to download huge models - everything runs via API! ⚡
