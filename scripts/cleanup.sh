#!/bin/bash
set -e

if [ -f websocket_handler.zip ]; then
    rm websocket_handler.zip
fi

if [ -d .venv ]; then
    rm -rf .venv
fi

if [ -d websocket_handler_build ]; then
    rm -rf websocket_handler_build
fi
