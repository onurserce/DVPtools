#!/bin/bash
diann_dir="$HOME"/bin
mkdir -p "$diann_dir"
cd "$diann_dir"
wget "https://github.com/vdemichev/DiaNN/releases/download/1.8.1/diann_1.8.1.tar.gz"
tar -xvf "diann_1.8.1.tar.gz"
rm "diann_1.8.1.tar.gz"
cd "$HOME"
echo "diann_1.8.1 installation successful"