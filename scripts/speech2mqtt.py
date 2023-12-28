#!/usr/bin/env python3

#import speechEngine as se# NOTE: requires PyAudio because it uses the Microphone class
#import time
from pocketsphinx import LiveSpeech
from pocketsphinx import get_model_path
#import inspect
import paho.mqtt.client as mqtt
import json
#import speechEngine as se
from enum import Enum
import commandComposition as comp
from pathlib import Path
import os

def make_relative_path_to_this(path):
    if(os.path.isabs(path)):
        return path
    else:
        base_path = Path(__file__).parent
        return str((base_path / path).resolve())
settings = None
#base_path = Path(__file__).parent
with open(make_relative_path_to_this("speech2mqtt.settings.json")) as f:
    settings = json.loads(f.read())

#Pocketsphinx
hmmpath = make_relative_path_to_this(settings["PocketSphinx"]["hmm"])
lmpath = make_relative_path_to_this(settings["PocketSphinx"]["lm"])
dic = make_relative_path_to_this(settings["PocketSphinx"]["dic"])

print("Livespeech before")
speech = LiveSpeech(
    audio_device=None,
    kws_threshold=1e-20,
    samprate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    verbose=False,
    hmm=hmmpath,
    lm=lmpath,
    dic=dic
    )

#MQTT
MQTT_SERVER = settings["Mqtt"]["Server"]
MQTT_PATH = settings["Mqtt"]["Path"]
MQTT_PORT = settings["Mqtt"]["Port"]


def on_connect(client, userdata, flags, rc):
    print("Connected to mqtt with result code "+str(rc))
client = mqtt.Client()
client.on_connect = on_connect 
client.connect(MQTT_SERVER, MQTT_PORT , 60)

#speech2mqtt
class SPEECH_DETECTION_STATE(Enum):
    WAITING_FOR_KEYPHRASE = 1, #initial state
    WAITING_FOR_COMMAND = 2,
    PEFORM_COMMAND_ACTION = 3

keyphrase = settings["Keyphrase"]

state = SPEECH_DETECTION_STATE.WAITING_FOR_KEYPHRASE
print(f"waiting for keyphrase '{keyphrase}'...")
for phrase in speech:    
    recognizedSpeech = phrase.segments(detailed=True)
    print(f"Recognized (raw): {recognizedSpeech}")
    recognizedwords = [speechPart[0] for speechPart in recognizedSpeech]
    print(f"Recognized (words): {','.join(recognizedwords)}")

    if(state == SPEECH_DETECTION_STATE.WAITING_FOR_KEYPHRASE and keyphrase in recognizedwords):
        print('keyphrase detected, waiting for command....')
        state = SPEECH_DETECTION_STATE.WAITING_FOR_COMMAND
    elif(state == SPEECH_DETECTION_STATE.WAITING_FOR_COMMAND):
        command = comp.IterateCategories(settings,recognizedwords)
        if(command is not None):
            print(f"Detected command: {command}")
            ret = client.publish(MQTT_PATH,command)
        state = SPEECH_DETECTION_STATE.WAITING_FOR_KEYPHRASE