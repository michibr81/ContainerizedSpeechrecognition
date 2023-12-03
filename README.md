# Containerized Speechrecognition

This project aims to get python SpeechRecogintion running in an docker container by using Pocktesphinx. 

By using the python library **SpeechRecognition** its almost any easy task with code copy-pasting to get some more or less good working speech-recognition running which uses an online api like google cloud.

- <https://pypi.org/project/SpeechRecognition/>
- <https://www.askpython.com/python-modules/speech-recognition>
- <https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst>
- <https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py>

As **Pocketsphinx** is the only algorithm which runs offline it may be a good solution, to avoid constantly sending spoken text from an private environment. 

Unfortunately there are two problems with pocketsphinx which have to be solved.

1. Installation of pocketsphinx is a problem on some system, as it has many dependencies which can conflict with other packages depeendencies on systems.
2. Accurracy is not as good as using some online api.

## Install and run in docker

The first problem with installing dependencies seems a good task for an docker image, which can be configured from scratch and the needed packages as the order of their installation can be freezed in an configuration file. 

### Configuration

- [Dockerfile](Dockerfile)

The image is based on `ubuntu` and the important parts are

```docker
RUN apt install -y portaudio19-dev 
RUN pip install pyaudio
RUN pip install SpeechRecognition
RUN apt install -y flac

#pocketshinx
RUN apt install -y pulseaudio swig libpulse-dev
RUN pip install PocketSphinx
```
The information-sources to solve the installation task are listed below

<https://raspberrypi.stackexchange.com/questions/84666/problem-on-installing-pyaudio-on-raspberry-pi>
<https://stackoverflow.com/questions/56332102/error-failed-building-wheel-for-pocketsphinx-while-trying-to-install-pocketsphi>

I also installed alsa-base and als-utils to have some help with exploring sound cards and test playing sound with `aplay` and recording with `arecord`.

Play sound

```sh
aplay file.wav -d 0 #-d for device
```

Record sound
```sh
arecord -d 10 -D plughw:1,0 sample.wav  #hw:1,0 my be different
```

Speaker test

```sh
cat /proc/asound/modules
speaker-test -c2 -twav -l7 -D plughw:1,0
```

<https://www.tinkerboy.xyz/raspberry-pi-test-sound-output/>


### Docker actions

As there may be people which ar new to docker (as was me), here the commands I used to build an image form upper configuration and run everything for testing.

In directory of [Dockerfile](Dockerfile)

```bash
docker build . -t speechrecog
```

Run interactive (with bash in container for testing), giving the sound-device from host:

```bash
docker run -it --device /dev/snd:/dev/snd speech bash
#with working folders
docker run -it --device /dev/snd:/dev/snd -v ./sphinx_models:/home/sphinx_models -v ./scripts:/home/scripts:rw  speechrecog bash
```

This changes the commandline to the one of the docker-container, where commands can be performed (e.g. for start the upper ones to play and record sound)

In some cases the sound-device isn't freed correctly when stopping the container and an error like 

*...Device or ressource busy...* may occur.

To solve this, it helps to clear all running containers:

```bash
docker ps --all #shows containers
docker container prune
```

If this helps not, its worth a try to remove the docker-image and all depending images (if remove with name does not work its wotrh to try id and vice versa)

```bash
docker image ls #lists the images
docker rmi <name_or_id> #removes an image
```



## Speechrecognition

To run the speechrecognition-logic, command

```bash
python3 speechrecognition.py
```

can be performed in docker container.

Using the python speechrecognition itself is explained on many sources on the web (for example: <https://www.simplilearn.com/tutorials/python-tutorial/speech-recognition-in-python>)

The parts I added, are using the regular speech-recogniton after detecting an buzzword and working with a keywords-list with detection accuracy, which is strongly recommended to achieve some speechrecognition which deservces this name.

Additionally the commands should be chosen well, as some words are detected better and some worse.

[speechrecog.py](speechrecog.py)