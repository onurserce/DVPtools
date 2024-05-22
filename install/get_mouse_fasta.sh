#!/bin/bash
mkdir -p "$HOME"/data
cd "$HOME"/data
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000000589/UP000000589_10090.fasta.gz
gzip -d UP000000589_10090.fasta.gz
echo "successfully downloaded and unpacked the mouse reference proteome"