docker stop pc_dev
docker build --tag pc_dev:latest --file Dockerfile .
docker run --rm --name pc_dev -d -v $(pwd):/app -p 5000:5000 pc_dev:latest
docker exec -it pc_dev /bin/bash
docker stop pc_dev