# 🔑 Fix API Key Permissions

## The Problem

You're seeing this error:

```
This authentication method does not have sufficient permissions to call Inference Providers
```

This means your Hugging Face API token was created without the right permissions.

## ✅ Solution: Create Token with Correct Permissions

### Step 1: Go to Hugging Face Tokens Page

Open: **https://huggingface.co/settings/tokens**

### Step 2: Create New Token

1. Click **"Create new token"**

2. Fill in:

   - **Name**: `semantle-inference`
   - **Type**: Select **"Read"** (this is fine)

3. **IMPORTANT**: Under **"Scopes"**, make sure these are checked:

   - ✅ **"Read access to contents of all repos"**
   - ✅ **"Make calls to the serverless Inference API"** ← THIS ONE IS CRITICAL!

4. Click **"Create token"**

5. **Copy the token** (starts with `hf_...`)

### Step 3: Update Your .env File

```bash
cd /Users/talben-avi/guess-word/service-repo

# Replace YOUR_NEW_TOKEN with the token you just copied
echo "HUGGINGFACE_API_KEY=hf_YOUR_NEW_TOKEN" > .env
```

### Step 4: Restart Backend

```bash
# Stop the running server (Ctrl+C in Terminal 1)
# Then restart:
./run.sh
```

### Step 5: Test It

```bash
# In a new terminal
curl -X POST http://localhost:8080/game/start \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "normal"}'
```

If it works, you'll get JSON with a `game_id`. ✅

---

## 🖼️ Visual Guide

When creating the token on Hugging Face, it should look like this:

```
Token name: semantle-inference
Type: Read

Scopes:
  ✅ Read access to contents of all repos
  ✅ Make calls to the serverless Inference API    ← MUST BE CHECKED!
  ☐ Write access to contents of all repos
  ☐ Manage repo settings
  ... (other options)
```

---

## 🆘 Still Not Working?

### Option 1: Try a "Write" Token

If "Read" token doesn't work, create a **"Write"** token instead:

- Type: **Write**
- Name: `semantle-full-access`
- All default permissions should be fine

### Option 2: Use Classic Token (If Available)

Some Hugging Face accounts can create "Classic" tokens:

- These have full permissions by default
- Look for "Classic" option when creating token

---

## 🧪 Quick Test Command

After updating the token, test if it works:

```bash
cd service-repo
source venv/bin/activate
python3 -c "
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
api_key = os.getenv('HUGGINGFACE_API_KEY')
print(f'API Key: {api_key[:10]}...')

headers = {'Authorization': f'Bearer {api_key}'}
response = httpx.post(
    'https://api-inference.huggingface.co/models/nvidia/llama-embed-nemotron-8b',
    headers=headers,
    json={'inputs': 'test', 'options': {'wait_for_model': True}},
    timeout=60
)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    print('✅ API Key works!')
else:
    print(f'❌ Error: {response.text}')
"
```

If this prints "✅ API Key works!" you're good to go!

---

## 📝 Summary

**The issue:** Token missing "Inference API" permission  
**The fix:** Create new token with inference permission checked  
**Time needed:** 2 minutes

Let me know if you get stuck!
