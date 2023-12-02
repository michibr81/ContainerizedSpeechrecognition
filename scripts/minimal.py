import speech_recognition as sr

r = sr.Recognizer()
keyWord = 'Computer'

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)

    print('Please start speaking..\n')
    while True:
        audio = r.listen(source) 
        print("Listening....")
        try:
            text = r.recognize_whisper(audio,language="english",show_dict=True,model="small")  #,keyword_entries=keywords)
            print('Recognized buzzword was:')
            print(text)
            # if keyWord.lower() in text.lower():
            #     print('Keyword detected in the speech.')
            #     #DetectText(r)
            # else:
            #     print('try again!')
        except Exception as e:
            print(e)
            print('Please speak again.')