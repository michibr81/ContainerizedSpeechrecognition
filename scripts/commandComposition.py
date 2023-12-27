import json

def IterateCategories(json,recognizedwords):
    assembledCommand = FindCommand(json, recognizedwords)
    if(assembledCommand is None):
        print("No command assembled, returnig....")
        return
    print(f"Assembled command was: {assembledCommand}")
    return assembledCommand

def FindCommand(json, recognizedwords):
    for category in json["CommandCategories"]:        
        cmd = CompositeCommand(category,recognizedwords)
        if(cmd is not None):
            return cmd
        
def CompositeCommand(categoryjson, recognizedwords):
    foundcommands = []
    for partOrderEntry in categoryjson["PartsOrder"]:
        categorypartjson = next((item for item in categoryjson.get("Parts", []) if item.get("Name") == partOrderEntry), None)
        for word in recognizedwords:                
            foundcommand = find_type_name_by_options(word, categorypartjson["Types"])
            if(foundcommand is not None):
                foundcommands.append(foundcommand)
                break
    if(len(foundcommands) != len(categoryjson["PartsOrder"])):
        return None                      
    return "".join(foundcommands)

def find_type_name_by_options(word, types):
    for type_info in types:
        if any(option.lower() == word.lower() for option in type_info.get("Options", [])):
            return type_info.get("Name")
    return None

#tests
# from pathlib import Path
# base_path = Path(__file__).parent
# with open((base_path / "cmds.json").resolve()) as f:
#     jsn = json.loads(f.read())
#     IterateCategories(jsn,["büro", "fenster","teilweise","runter"] )

