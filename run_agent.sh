#!/bin/bash
# Quick run script for Air2Energy Market Research Agent

# Check if virtual environment exists
if [ ! -d "air2energy_env" ]; then
    echo "🚨 Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
source air2energy_env/bin/activate

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    echo "Or add it to your ~/.bashrc or ~/.zshrc"
    echo ""
    read -p "Enter your Anthropic API key now (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        export ANTHROPIC_API_KEY=$api_key
        echo "✅ API key set for this session"
    fi
fi

# Run the agent
echo "🤖 Starting Air2Energy Market Research Agent..."
python agent.py

# Deactivate when done
deactivate