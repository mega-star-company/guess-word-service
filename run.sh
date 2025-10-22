#!/bin/bash

# Quick run script for Semantle backend

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt"
    exit 1
fi

echo "🚀 Starting Semantle Backend Server..."
echo ""

# Check if .env file exists and has API key
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: No .env file found!"
    echo ""
    echo "The server will start but you need an API key to use it."
    echo ""
    echo "To get a FREE Hugging Face API key:"
    echo "  1. Run: ./configure_api.sh (recommended)"
    echo "  2. Or visit: https://huggingface.co/join"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Run the server
python3 main.py


