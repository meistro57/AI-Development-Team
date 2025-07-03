#!/bin/bash
# AI Development Team - Update Script

echo "🔄 Updating AI Development Team..."

cd ..

# Activate environment
source ai-dev-env/bin/activate

# Update Python packages
echo "📦 Updating Python packages..."
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# Update system packages
echo "🛠️  Updating system packages..."
sudo apt update
sudo apt upgrade -y

echo "✅ Update completed!"
