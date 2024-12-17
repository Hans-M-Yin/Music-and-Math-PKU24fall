#!/bin/bash

# 更新包列表
sudo apt update

# 安装必要的工具（如果尚未安装）
sudo apt install -y python3-venv python3-pip

# 创建虚拟环境
python3 -m venv musicMath

# 激活虚拟环境
source musciMath/bin/activate

# 安装 Flask 和 music21
pip install Flask music21

echo "虚拟环境已创建并安装所需包。"