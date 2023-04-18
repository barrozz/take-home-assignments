FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3.9 && \
    apt-get install -y python3-pip

WORKDIR /app
VOLUME /app
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD [ "/bin/bash" ]