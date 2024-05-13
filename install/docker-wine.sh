cd "$HOME"
wget https://raw.githubusercontent.com/scottyhardy/docker-wine/master/docker-wine
chmod +x docker-wine
module load apptainer
apptainer build docker-wine.sif docker://scottyhardy/docker-winels

# try the followin command:
apptainer run docker-wine.sif
module purge
