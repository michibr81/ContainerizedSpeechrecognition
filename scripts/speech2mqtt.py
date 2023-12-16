#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
#import speech_recognition as sr
from pocketsphinx import LiveSpeech
from pocketsphinx import get_model_path #, get_data_path
import inspect
import paho.mqtt.client as mqtt
#import winsound
import json
import speechEngine as se
#<s>,büro,<sil>,teilweise,hoch,</s>

print("Livespeech before")
speech = LiveSpeech(
    audio_device=None,
    kws_threshold=1e-20,
    samprate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    verbose=False,
    # hmm='/home/sphinx_models/cmusphinx-cont-voxforge-de/model_parameters/voxforge.cd_cont_6000',
    # lm='/home/sphinx_models/cmusphinx-voxforge-de.lm.bin',
    # dic='/home/sphinx_models/tinyde.dict'
    hmm='/media/DATENLT/Programmierung/_GIT_REPOS/ContainerizedSpeechrecog/sphinx_models/cmusphinx-cont-voxforge-de/model_parameters/voxforge.cd_cont_6000',
    lm='/media/DATENLT/Programmierung/_GIT_REPOS/ContainerizedSpeechrecog/sphinx_models/cmusphinx-voxforge-de.lm.bin',
    dic='/media/DATENLT/Programmierung/_GIT_REPOS/ContainerizedSpeechrecog/sphinx_models/tinyde.dict'   
    )

print("Livespeech started")
print(type(speech.ad))

MQTT_SERVER = 'MBraspi4'
MQTT_PATH = "MBR/automation/shutters"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
client = mqtt.Client()
client.on_connect = on_connect
 
client.connect(MQTT_SERVER, 1883, 60)

commandMapStr = """
{
    "Location":[
        {"Bath":["bad","badezimmer"]},
        {"Office":["büro"]},
        {"All":["alle"]},
        {"South":["süd","südseite","sonnenseite"]},
        {"Living":["essstube","esstisch","esszimmer"]}
    ],
    "Direction":[        
        {"Down":["runter","herrunter","zu","herab"]},
        {"Up":["hoch","rauf","herauf"]}
    ],
    "Quantity":[
        {"Half":["halb","teilweise"]},
        {"Full":["komplett","ganz"]}
    ]
}
"""
commandMap = json.loads(commandMapStr)
#print(commandMap)

# an for in loop to iterate in speech
for phrase in speech:
    print("waiting for keyphrase")
    recognizedSpeech = phrase.segments(detailed=True)
    print(f"TYPE ---------: {type(recognizedSpeech)}")
    print(recognizedSpeech)
    recognizedwords = [speechPart[0] for speechPart in recognizedSpeech]
    print("recognizedwords: " + ",".join(recognizedwords))
    if 'computer' in recognizedwords:
        print('keyphrase detected')
        print("waiting for command")
        for phrase in speech:
            recognizedSpeech = phrase.segments(detailed=True)
            print(f"recognizedWors TYPE: {type(recognizedwords)}")
            print(recognizedSpeech)
            recognizedwords = [speechPart for speechPart in recognizedSpeech]

            command = se.FindShutterCommand(recognizedwords, commandMap)
            print(command)
            ret= client.publish(MQTT_PATH,command)   
