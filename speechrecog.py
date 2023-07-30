import speech_recognition as sr

keywords=[("hello computer",0.8),("close shutters",0.7),("open shutters",0.7),("sunrise",0.8),("hey sunshine",0.8)]

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
keyWord = 'hey sunshine'

with sr.Microphone(device_index = 2) as source:
    r.adjust_for_ambient_noise(source)

    print('Please start speaking..\n')
    while True: 
        audio = r.listen(source,)
        try:
            text = r.recognize_sphinx(audio,keyword_entries=keywords)
            print('Recognized buzzword was:')
            print(text.lower())
            if keyWord.lower() in text.lower():
                print('Keyword detected in the speech.')
                DetectText(r)
        except Exception as e:
            print(e)
            print('Please speak again.')


