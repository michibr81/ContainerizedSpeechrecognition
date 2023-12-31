FROM ubuntu

#prepare
RUN apt update -y && apt upgrade -y
RUN apt install -y apt-utils python3-pip vim
RUN python3 -m pip install --upgrade pip

#install sound, speech-recog, mqtt
RUN apt install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1 alsa-base alsa-utils pulseaudio swig libpulse-dev flac
RUN pip install pyaudio SpeechRecognition paho-mqtt PocketSphinx

COPY ./scripts/ /home/scripts/
WORKDIR /home/scripts/

CMD ["python3","speech2mqtt.py"]