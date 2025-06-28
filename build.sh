#!/bin/bash
# Update package lists
apt-get update

# Install system dependencies
apt-get install -y cmake libboost-all-dev libeigen3-dev

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Clear pip cache to avoid stale packages
pip cache purge

# Install Python dependencies
pip install -r requirements.txt


# Install camel_tools data packages

camel_data -i light

flask db init

flask db migrate -m "initial migration"

flask db upgrade

python seed.py