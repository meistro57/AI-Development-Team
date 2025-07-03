#!/bin/bash
# AI Development Team - Backup Script

BACKUP_DIR="$HOME/ai_dev_team_backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "📦 Creating backup..."

mkdir -p "$BACKUP_DIR"

# Backup configurations and code
tar -czf "$BACKUP_DIR/ai_dev_team_$DATE.tar.gz" \
    --exclude="ai-dev-env" \
    --exclude="projects/*/node_modules" \
    --exclude="projects/*/__pycache__" \
    --exclude="projects/*/venv" \
    --exclude="logs/*.log" \
    -C .. .

echo "✅ Backup created: $BACKUP_DIR/ai_dev_team_$DATE.tar.gz"

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/ai_dev_team_*.tar.gz | tail -n +11 | xargs -r rm

echo "🧹 Old backups cleaned up"
