#!/bin/bash

echo "Updating the server"
sudo apt-get update -y

echo "Installing pip and venv"
sudo apt-get install -y python3-pip python3-venv

echo "Installing virtual environment and packages"
cd code
python3 -m venv .venv
source .venv/bin/activate
pip install --break-system-packages -r ../requirements.txt
cd ..
