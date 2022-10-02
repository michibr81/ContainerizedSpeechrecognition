FROM ubuntu

#prepare
RUN apt update
RUN apt install -y apt-utils
RUN apt install -y python3-pip

#sound
#RUN apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1
RUN apt install -y alsa-base alsa-utils

#speech-recog
RUN apt install -y portaudio19-dev 
RUN pip install pyaudio
RUN pip install SpeechRecognition
RUN apt install -y flac

#pocketshinx
RUN apt install -y pulseaudio swig libpulse-dev
RUN pip install PocketSphinx

WORKDIR /home
ADD recorded.wav /home

ADD speechrecog.py /home


#RUN python3 speechrecog.py
