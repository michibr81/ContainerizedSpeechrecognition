import json

def FindKeys(jsonpart,recognizedwords):
    foundkeys = []
    for el in jsonpart: #iterate through each possible entry
        key = list(el.keys())[0]    #getting the single jsonpartkey
        values = list(el.values())[0]
        for word in recognizedwords: #checking if any allowed 
            if(word is '<s>' or word is '</s>' or word is '<sil>'):
                continue
            if word in values:
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
        return foundKeys[0]
    
def FindShutterCommand(recognizedSpeech, commandMap):
    recognizedwords = [speechPart[0] for speechPart in recognizedSpeech]
    print(f"recognizedWords {recognizedwords}")
    
    location = FindCommandPart("Location",recognizedwords,commandMap)
    quantity = FindCommandPart("Quantity",recognizedwords,commandMap)
    direction = FindCommandPart("Direction",recognizedwords,commandMap)

    cmd = f"{location}Shutter{quantity}{direction}"
    print(cmd)
    return cmd
    
    # if(location != None and quantity != None and direction != None):
    #     shutterCmd = f"{location}Shutter{quantity}{direction}"
    #     print(f"Shuttercommand is {shutterCmd}")

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
#[('<s>', 0, 0, 2), ('büro', 0, 3, 45), ('fenster', 0, 46, 121), ('teilweise', 0, 122, 219), ('runter', 0, 220, 268), ('</s>', 0, 269, 301)]
#FindKeys(json.loads(commandMapStr)["Location"], ['<s>', 'büro', 'fenster', 'teilweise', 'hoch', '</s>'])


