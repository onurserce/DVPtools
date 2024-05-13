#!/bin/bash
cd "$HOME"
mkdir ThermoRawFileParser
cd ThermoRawFileParser
wget https://github.com/compomics/ThermoRawFileParser/releases/download/v1.4.4/ThermoRawFileParser1.4.4.zip
unzip ThermoRawFileParser1.4.4.zip
rm ThermoRawFileParser1.4.4.zip
cd "$HOME"
echo "successfully installed ThermoRawFileParser version 1.4.4"
