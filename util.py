import json 

def load_json(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)
