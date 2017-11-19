FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    mpd

RUN mkdir -p \
  /home/mpd/playlist/stream1 \
  /home/mpd/playlist/stream2 \
  /home/mpd/music

RUN chown -R mpd /home/mpd

COPY mpd-stream?.conf /etc/

CMD mpd --no-daemon /etc/mpd-stream1.conf & mpd --no-daemon /etc/mpd-stream2.conf