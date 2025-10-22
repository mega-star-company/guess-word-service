# 🎮 START HERE - Semantle Game Setup

## What is this?

A word-guessing game where you try to find a secret word based on how semantically similar your guesses are. Think "hot and cold" but with AI understanding word meanings!

## ⚡ Quick Setup (2 Minutes)

### 1. Install Dependencies (30 seconds)

```bash
cd service-repo
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 2. Get FREE API Key (1 minute)

Run this command and follow the prompts:

```bash
./configure_api.sh
```

It will guide you to:

1. Create a free Hugging Face account
2. Get your API token
3. Save it automatically

### 3. Start Playing! (30 seconds)

**Terminal 1 - Start the server:**

```bash
python3 main.py
```

**Terminal 2 - Play the game:**

```bash
source venv/bin/activate
python3 example_client.py
```

## 🎯 How to Play

1. Server picks a secret word
2. You guess a word
3. Game tells you how similar your guess is (0-100%)
4. Keep guessing until you find it!

**Example:**

- Target word: "happy"
- You guess "joyful" → 85% similar! 🔥
- You guess "car" → 15% similar ❄️

## 🆘 Having Issues?

### "Command not found: python3"

You have Python installed as `python`. Replace `python3` with `python`.

### "No module named 'fastapi'"

You need to activate the virtual environment:

```bash
source venv/bin/activate
```

### "API not configured"

Run the configuration script:

```bash
./configure_api.sh
```

### "Model is loading..."

This is normal on first request. Wait 10-20 seconds and it will work!

## 📚 More Info

- **Full Documentation**: See `README.md`
- **What Changed**: See `CHANGES.md`
- **Quick Setup**: See `SETUP.md`

## 🎉 You're All Set!

Have fun playing Semantle! Try different strategies:

- Start with broad categories
- Narrow down based on feedback
- Think about word relationships and meanings

Good luck! 🚀
