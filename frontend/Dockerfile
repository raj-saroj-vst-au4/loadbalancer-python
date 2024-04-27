FROM python:3.8-slim-buster

# RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask
# RUN apt-get install -y net-tools procps

COPY service.py /

ENV FLASK_APP=service

CMD ["flask", "run", "--host=0.0.0.0", "--port=7000"]


