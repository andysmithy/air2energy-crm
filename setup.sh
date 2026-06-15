#!/bin/bash
# Air2Energy Market Research Agent Setup

echo "🚀 Setting up Air2Energy Market Research Agent..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv air2energy_env

# Activate virtual environment
echo "🔧 Activating environment..."
source air2energy_env/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the agent:"
echo "1. Set your API key: export ANTHROPIC_API_KEY='your-key-here'"
echo "2. Activate environment: source air2energy_env/bin/activate"
echo "3. Run agent: python agent.py"
echo ""
echo "Or use the quick start script: ./run_agent.sh"