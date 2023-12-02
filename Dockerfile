FROM ubuntu

#prepare
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y apt-utils
RUN apt install -y python3-pip
RUN apt install -y vim

RUN python3 -m pip install --upgrade pip

#sound
RUN apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1
RUN apt install -y alsa-base alsa-utils



#speech-recog
RUN apt install -y portaudio19-dev 
RUN pip install pyaudio
RUN pip install SpeechRecognition
RUN apt install -y flac
RUN apt install -y git

#pocketshinx
RUN apt install -y pulseaudio swig libpulse-dev
RUN pip install PocketSphinx
#RUN pip install vosk
#RUN pip install -U openai-whisper


WORKDIR /home

#used for testing sound card
#ADD recorded.wav /home  
#the speechrecogition-logic
#ADD vosk-model-en-us-0.22-lgraph /home/model/
#ADD speechrecog.py /home
#ADD sample.wav /home
#ADD minimal.py /home
#ADD callback.py /home
#ADD mytinydict.dict /home
#ADD tinypocketmqtt.py /home
#RUN python3 speechrecog.py

