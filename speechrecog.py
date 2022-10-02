import speech_recognition as sr


r = sr.Recognizer()
keyWord = 'computer'

with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)

    print('Please start speaking..\n')
    while True: 
        audio = r.listen(source)
        try:
            text = r.recognize_sphinx(audio)
            print('Word was:')
            print(text.lower())
            if keyWord.lower() in text.lower():
                print('Keyword detected in the speech.')
        except Exception as e:
            print(e)
            print('Please speak again.')


#     print("Say Something");
#     audio = r.listen(source)
#     with open("recorded.wav", "wb") as f:
#         f.write(audio.get_wav_data())
#     print("got it");

# try:
#     print("You said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results; {0}".format(e))
