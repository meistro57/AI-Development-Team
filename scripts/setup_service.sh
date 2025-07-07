#!/bin/bash
# Install and enable the AI Development Team systemd service
set -e

SERVICE_FILE="ai-dev-team.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_FILE"

if [ $EUID -ne 0 ]; then
    echo "This script must be run with sudo or as root" >&2
    exit 1
fi

# Copy service file
cp "$(dirname "$0")/../config/$SERVICE_FILE" "$SERVICE_PATH"

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable --now "$SERVICE_FILE"

echo "✅ Service installed and started"
