#!/bin/bash

args=("$@")
for i in "${args[@]}"; do
    docker stop $i
    docker container rm --force $i
done
