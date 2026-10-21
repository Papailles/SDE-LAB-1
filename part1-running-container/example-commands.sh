#!/usr/bin/env bash
# Part 1 - example: running an existing container (Docker CLI)

# 1.1 Exploring public images
docker pull nginx:alpine
docker run -d --name web-intro -p 8080:80 nginx:alpine
curl http://localhost:8080

# 1.2 Inspection and container management
docker ps
docker logs web-intro
docker inspect web-intro
docker stop web-intro
docker ps -a
docker start web-intro
docker rm -f web-intro
