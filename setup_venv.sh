#!/bin/bash

# This script will create a virtual environment and install the required packages for the project.

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# After running this script, you must still run source venv/bin/activate to activate the virtual environment.

# To deactivate the virtual environment, you can simply run
# deactivate

# To delete virtual environment, you can simply remove the venv directory.
# rm -rf venv
# source ~/.bashrc



