#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import speech_recognition as sr
from pocketsphinx import LiveSpeech
from pocketsphinx import get_model_path #, get_data_path

#stop_listening = None
keywords=[("Hey",0.85),("Sunshine",0.85),("Raspi",0.85),("Shutter",0.85)]

print("#######################################")
print(get_model_path('en-us'))

# this is called from the background thread
def callback(recognizer, audio):
    # global stop_listening
    # if stop_listening:
    #     stop_listening(wait_for_stop=True)
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Speech Recognition thinks you said ")
        #print(recognizer.recognize_whisper(audio,language="german",show_dict=True,model="small"))
        print(recognizer.recognize_sphinx(audio,keyword_entries=keywords))

        #stop_listening = r.listen_in_background(m, callback)    #start again
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))


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
    hmm='/home/sphinx_models/cmusphinx-cont-voxforge-de/model_parameters/voxforge.cd_cont_6000',
    #hmm='/usr/local/lib/python3.10/dist-packages/pocketsphinx/model/en-us/en-us',
    #lm='/usr/local/lib/python3.10/dist-packages/pocketsphinx/model/en-us/en-us.lm.bin',
    lm='/home/sphinx_models/cmusphinx-voxforge-de.lm.bin',
    #dic='/home/sphinx_models/mytinydict.dict' #/usr/local/lib/python3.10/dist-packages/pocketsphinx/model/en-us/cmudict-en-us.dict'
    #dic='/home/sphinx_models/cmusphinx-voxforge-de.dic'
    dic='/home/sphinx_models/tinyde.dict'
    )

print("Livespeech started")
 
# an for in loop to iterate in speech
for phrase in speech:
    print("waiting")
        # printing if the keyword is spoken with segments along side.
    print(phrase.segments(detailed=True))


# with m as source:
#     r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# # start listening in the background (note that we don't have to do this inside a `with` statement)
# stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
#for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
