#!/bin/bash

echo "🔑 Semantle API Configuration"
echo "=============================="
echo ""
echo "To use this service, you need a FREE Hugging Face API key."
echo ""
echo "Steps to get your API key:"
echo "1. Go to: https://huggingface.co/join"
echo "2. Create a free account (if you don't have one)"
echo "3. Go to: https://huggingface.co/settings/tokens"
echo "4. Click 'Create new token'"
echo "5. Name it 'semantle-api' and select 'Read' permission"
echo "6. Copy the token"
echo ""
echo "=============================="
echo ""
read -p "Paste your Hugging Face API key here: " api_key

if [ -z "$api_key" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

# Create .env file
echo "HUGGINGFACE_API_KEY=$api_key" > .env

echo ""
echo "✅ API key configured successfully!"
echo ""
echo "You can now start the server with:"
echo "  python3 main.py"
echo ""
echo "Or use the quick start script:"
echo "  ./run.sh"
echo ""

