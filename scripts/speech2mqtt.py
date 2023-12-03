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

print("Livespeech before")
speech = LiveSpeech(
    audio_device=None,
    kws_threshold=1e-20,
    samprate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    verbose=False,
    hmm='/home/sphinx_models/cmusphinx-cont-voxforge-de/model_parameters/voxforge.cd_cont_6000',
    lm='/home/sphinx_models/cmusphinx-voxforge-de.lm.bin',
    dic='/home/sphinx_models/tinyde.dict'    
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

def FindKeys(jsonpart,recognizedwords):
    foundkeys = []
    print("search for " + ",".join(recognizedwords) + " in json: " + json.dumps(jsonpart))
    for el in jsonpart: #iterate through each direction
        for key in el: # just for getting the single jsonpartkey
            print(el[key])
            for word in recognizedwords: #checking if any allowed 
                if word in el[key]:
                    print(f"{word} is found: add " + key + " to found keys")
                    foundkeys.append(key)
    return list(set(foundkeys)) #remove double ones


def FindCommandPart(partDescription, recognizedwords, commandMap):    
    cmdPartMap = commandMap[partDescription]
    foundKeys = FindKeys(cmdPartMap,recognizedwords)

    if(len(foundKeys) == 0):
            print(f"No {partDescription} found")
    elif(len(foundKeys) >1):
        print(f"Too many {partDescription}s found ")
    else:
        print(f"{partDescription} found: " + foundKeys[0])

# an for in loop to iterate in speech
for phrase in speech:
    print("waiting for keyphrase")
    recognizedSpeech = phrase.segments(detailed=True)
    print(recognizedSpeech)
    recognizedwords = [speechPart[0] for speechPart in recognizedSpeech]
    print("recognizedwords: " + ",".join(recognizedwords))
    if 'computer' in recognizedwords:
        print('keyphrase detected')
        print("waiting for command")
        for phrase in speech:
            recognizedSpeech = phrase.segments(detailed=True)
            print(recognizedSpeech)
            recognizedwords = [speechPart[0] for speechPart in recognizedSpeech]

            FindCommandPart("Direction",recognizedwords,commandMap)
            
            # #start with direction
            # directions = commandMap["Direction"]
            # direction = FindKeys(directions,recognizedwords)
            
            # if(len(direction) == 0):
            #      print("No direction found")
            # elif(len(direction) >1):
            #     print("too many directions found ")
            # else:
            #     print("Direction found: " + direction[0])





            # for dir in directions:
            #     for word in dir:
            #         if word in recognizedwords:
            #             return dir
            # if('büro' in words):
            #     print("command for badezimmer detected")
            #     if('halb' in words or 'teilweise' in words):
            #         print("command for teilweise detected")
            #         if('herrunter' in words or 'runter' in words):
            #             print("command for runter detected")
            #             print("Fahre Büro halb runter")
            #             ret= client.publish(MQTT_PATH,"OfficeShutterHalfDown")



        


