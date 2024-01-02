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
import logging

def make_relative_path_to_this(path):
    if(os.path.isabs(path)):
        return path
    else:
        base_path = Path(__file__).parent
        return str((base_path / path).resolve())
    
logging.basicConfig(filename=make_relative_path_to_this('speech2mqtt.log'), encoding='utf-8', level=logging.DEBUG)

settings = None
#base_path = Path(__file__).parent
with open(make_relative_path_to_this("speech2mqtt.settings.json")) as f:
    settings = json.loads(f.read())

#Pocketsphinx
hmmpath = make_relative_path_to_this(settings["PocketSphinx"]["hmm"])
lmpath = make_relative_path_to_this(settings["PocketSphinx"]["lm"])
dic = make_relative_path_to_this(settings["PocketSphinx"]["dic"])

logging.info("Livespeech before")
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
    logging.info("Connected to mqtt with result code "+str(rc))
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
logging.info(f"waiting for keyphrase '{keyphrase}'...")
for phrase in speech:    
    recognizedSpeech = phrase.segments(detailed=True)
    logging.info(f"Recognized (raw): {recognizedSpeech}")
    recognizedwords = [speechPart[0] for speechPart in recognizedSpeech]
    logging.info(f"Recognized (words): {','.join(recognizedwords)}")

    if(state == SPEECH_DETECTION_STATE.WAITING_FOR_KEYPHRASE and keyphrase in recognizedwords):
        logging.info('keyphrase detected, waiting for command....')
        state = SPEECH_DETECTION_STATE.WAITING_FOR_COMMAND
    elif(state == SPEECH_DETECTION_STATE.WAITING_FOR_COMMAND):
        command = comp.IterateCategories(settings,recognizedwords)
        if(command is not None):
            logging.info(f"Detected command: {command}")
            if client.is_connected != True:
                client.connect(MQTT_SERVER, MQTT_PORT , 60)
            ret = client.publish(MQTT_PATH,command)
        else:
            logging.info(f"Command was 'None'")
        state = SPEECH_DETECTION_STATE.WAITING_FOR_KEYPHRASE