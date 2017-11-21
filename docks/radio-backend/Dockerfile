FROM ubuntu:xenial

# join this later
RUN apt-get update
RUN apt-get install -y \
  software-properties-common \
  curl

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y \
    python3.6 \
    python3.6-dev \
    libtag1-dev \
    build-essential

RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6

ADD backend/requirements.txt /tmp/requirements.txt
RUN pip3.6 install -r /tmp/requirements.txt

# mount volume instead of this later
ADD backend/ /code/
