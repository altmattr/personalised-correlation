docker stop pc_dev
docker build --tag pc_dev:latest --file Dockerfile .
docker run --rm --name pc_dev -d -v $(pwd):/app -p 5050:5000 pc_dev:latest
docker attach pc_dev
docker stop pc_dev