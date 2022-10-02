FROM python:3.8

RUN apt update
RUN apt install apt-utils

RUN apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1
RUN apt install -y alsa-utils

WORKDIR /home
ADD recorded.wav /home
