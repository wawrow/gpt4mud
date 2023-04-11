#!/bin/bash
set -e

if [ -f websocket_handler.zip ]; then
    rm websocket_handler.zip
fi
python3.11 -m venv .venv
source .venv/bin/activate
cp -Ra websocket_handler websocket_handler_build
cd websocket_handler_build

pip install -r requirements.txt --target .
# zip -r ../websocket_handler.zip .
cd ..

# rm -rf websocket_handler_build
