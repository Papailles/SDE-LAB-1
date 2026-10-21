#!/usr/bin/env bash
# Exercise 1 - Registration Day, More Servers (solution)

# 1. three containers from the same image
docker run -d --name NAME_PLACEHOLDER -p PORT_PLACEHOLDER nginx:alpine #change name and port accordingly
docker run -d --name NAME_PLACEHOLDER -p PORT_PLACEHOLDER nginx:alpine #change name and port accordingly
docker run -d --name NAME_PLACEHOLDER -p PORT_PLACEHOLDER nginx:alpine #change name and port accordingly

# 2. all three respond
curl http://localhost:8081
curl http://localhost:8082
curl http://localhost:8083

# 3. three containers, same image
docker ps --filter "name=esse4-web"

# 4. requests to web-2 only: only its logs grow
curl http://localhost:8082
docker logs esse4-web-2
docker logs esse4-web-1

# 5. internal IPs
docker inspect esse4-web-1
docker inspect esse4-web-2

# 6. web-2 crashes
docker stop esse4-web-2
curl http://localhost:8082
curl http://localhost:8081
curl http://localhost:8083
docker ps -a

# 7. restart web-2, then clean up everything
docker start esse4-web-2
docker rm -f esse4-web-1 esse4-web-2 esse4-web-3