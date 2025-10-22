#!/bin/bash

# Semantle Backend Setup Script for macOS

echo "🎮 Setting up Semantle Backend Service..."
echo "=========================================="
echo ""

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "📥 Installing dependencies..."
echo "This may take a few minutes..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check for CUDA/GPU support
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 NVIDIA GPU detected, installing GPU-enabled PyTorch..."
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
else
    echo "💻 No GPU detected, installing CPU-only version..."
    echo "⚠️  Note: CPU inference will be slower than GPU"
fi

# Install requirements
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""
echo "Or use the run script:"
echo "  ./run.sh"
echo ""


