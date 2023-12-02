#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import speech_recognition as sr
from pocketsphinx import LiveSpeech
from pocketsphinx import get_model_path #, get_data_path

print("#######################################")
print(get_model_path('en-us'))

r = sr.Recognizer()
m = sr.Microphone()

print("Livespeech before")
speech = LiveSpeech(
    #keyphrase='sunshine', 
    #lm=False,
    kws_threshold=1e-20,
    samprate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    verbose=False,
    hmm='/usr/local/lib/python3.10/dist-packages/pocketsphinx/model/en-us/en-us',
    lm='/usr/local/lib/python3.10/dist-packages/pocketsphinx/model/en-us/en-us.lm.bin',
    dic='mytinydict.dict' #/usr/local/lib/python3.10/dist-packages/pocketsphinx/model/en-us/cmudict-en-us.dict'
    )

print("Livespeech started")
 
# an for in loop to iterate in speech
for phrase in speech:
    print("waiting")
        # printing if the keyword is spoken with segments along side.
    print(phrase.segments(detailed=True))

# do some more unrelated things
while True: time.sleep(0.1)  