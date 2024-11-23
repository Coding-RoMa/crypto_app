#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Downloading and building TA-Lib C library..."
mkdir -p /tmp/ta-lib
cd /tmp/ta-lib

# Download TA-Lib source code
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvzf ta-lib-0.4.0-src.tar.gz
cd ta-lib-0.4.0

# Build and install TA-Lib
./configure --prefix=/usr
make
sudo make install

echo "TA-Lib C library built successfully."
