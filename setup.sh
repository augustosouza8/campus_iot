#!/bin/bash

echo "🔧 Setting up virtual environment..."

# Step 1: Create venv if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "✅ Virtual environment created."
else
  echo "ℹ️  Virtual environment already exists."
fi

# Step 2: Activate venv
source venv/bin/activate
echo "✅ Virtual environment activated."

# Step 3: Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Setup complete. You can now run the app."
