#!/bin/bash

# build the gateway image
bash conductor.sh build test-gateway latest gateway/.

# build the service image
bash conductor.sh build test-service latest service/.

# start the service containers
bash conductor.sh run test-service latest c1 -e 9000-8000
bash conductor.sh run test-service latest c2 -e 9001-8000

# get the IP and port of machine where the service containers are running
# C1_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c1)
# C2_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c2)
C1_IP="$1"
C1_PORT="$2"
C2_IP="$3"
C2_PORT="$4"

# start the gateway container
docker run -d -i -p 8000:8000 --name main -e CONTAINERA_ENDPOINT=http://${C1_IP}:${C1_PORT} -e CONTAINERB_ENDPOINT=http://${C2_IP}:${C2_PORT} test-gateway:latest

# create a peer connection between gateway and service containers
# bash conductor.sh peer main c1
# bash conductor.sh peer main c2

# command to generate load on the gateway server
# autocannon -c 2000 -a 2000 http://localhost:8000
