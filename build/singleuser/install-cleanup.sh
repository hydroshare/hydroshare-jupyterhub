#/bin/bash


conda clean --all -y
apt-get clean 
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*
