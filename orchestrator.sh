#!/bin/bash

# build the gateway image
bash conductor.sh build test-gateway latest gateway/.

# build the service image
bash conductor.sh build test-service latest service/.

# start the service containers
bash conductor.sh run test-service latest c1 -e 9000-8000
bash conductor.sh run test-service latest c2 -e 9001-8000

# get the IP of containers
C1_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c1)
C2_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c2)

# start the gateway container
docker run -d -i -p 8000:8000 --name main -e CONTAINERA_ENDPOINT=http://${C1_IP}:8000 -e CONTAINERB_ENDPOINT=http://${C2_IP}:8000 test-gateway:latest

# create a peer connection between gateway and service containers
bash conductor.sh peer main c1
bash conductor.sh peer main c2

# command to generate load on the gateway server
# autocannon -c 2000 -a 2000 http://localhost:8000
