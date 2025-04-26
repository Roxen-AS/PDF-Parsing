#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project requirements
pip install -r requirements.txt

# Done
echo "Setup complete. Environment ready!"
