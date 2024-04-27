FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.*
RUN pip install fastapi uvicorn
RUN pip install requests==2.26.*
RUN apt install -y inetutils-ping
RUN apt install -y curl net-tools procps

COPY gateway.py /
