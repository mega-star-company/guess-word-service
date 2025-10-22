#!/bin/bash
# Quick demo mode - runs with a placeholder key to show the setup

echo "🎮 Semantle Server - Demo Mode"
echo "================================"
echo ""
echo "⚠️  Running in demo mode without API key"
echo "    The server will start but won't work until you add a real API key."
echo ""
echo "To get a FREE API key:"
echo "  1. Visit: https://huggingface.co/join"
echo "  2. Sign up (takes 1 minute)"
echo "  3. Go to: https://huggingface.co/settings/tokens"
echo "  4. Create a token with 'Read' permission"
echo "  5. Run: ./configure_api.sh"
echo ""
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "HUGGINGFACE_API_KEY=demo_key_please_replace" > .env
    echo "📝 Created .env file with placeholder key"
    echo ""
fi

# Activate virtual environment and run
source venv/bin/activate
python3 main.py
