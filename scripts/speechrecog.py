import speech_recognition as sr

keywords=[("Computer",0.85),("Hallo",0.85),("Raspi",0.85),("Rolladen",0.85)]

def DetectText(recognizer):
    audio = recognizer.listen(source)
    with open("recorded.wav", "wb") as f:
        f.write(audio.get_wav_data())
    print("got it")
    try:
        print("You said command" + r.recognize_sphinx(audio,keyword_entries=keywords))
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))


r = sr.Recognizer()
keyWord = 'sunshine'


for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

with sr.Microphone(device_index = 1) as source:
    r.adjust_for_ambient_noise(source)

    print('Please start speaking..\n')
    while True:
        audio = r.listen(source) #,10,5)
        try:
            text = r.recognize_vosk(audio)  #,keyword_entries=keywords)
            print('Recognized buzzword was:')
            print(text.lower())
            if keyWord.lower() in text.lower():
                print('Keyword detected in the speech.')
                DetectText(r)
            else:
                print('try again!')
        except Exception as e:
            print(e)
            print('Please speak again.')

