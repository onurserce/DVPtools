#!/bin/bash
cd "$HOME"
wget https://download.mono-project.com/sources/mono/mono-6.12.0.199.tar.xz
PREFIX="$HOME"/opt/mono
VERSION=6.12.0.199
tar xvf mono-$VERSION.tar.xz
./configure --prefix=$PREFIX
make
make install
echo "export PATH=$PATH:$PREFIX/bin" >> ~/.bashrc
echo >> ~/.bashrc
rm mono-$VERSION.tar.xz
rm -rf mono-$VERSION
cd "$HOME"
. "$HOME"/.bashrc
echo "mono-$VERSION is successfully installed in $PREFIX"
