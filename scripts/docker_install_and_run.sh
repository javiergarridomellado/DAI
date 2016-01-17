#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo docker pull javiergarridomellado/iv_javiergarridomellado:apuestas
sudo docker run -t -i javiergarridomellado/iv_javiergarridomellado:apuestas /bin/bash
