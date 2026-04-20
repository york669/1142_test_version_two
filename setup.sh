#!/bin/bash

# 安裝系統依賴
sudo apt-get update
sudo apt-get install -y build-essential wget

# 下載並安裝 TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
cd ..

# 安裝 Python 依賴
pip install -r requirements.txt