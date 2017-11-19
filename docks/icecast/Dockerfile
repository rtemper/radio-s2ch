FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    icecast2

COPY icecast.xml /etc/

RUN chown icecast2:icecast \
   /var/log/icecast2 \
   /usr/share/icecast2

CMD icecast2 -c /etc/icecast.xml