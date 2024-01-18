import json
import random
import requests
from pathlib import Path


current_file_path = Path(__file__).resolve()
feature_file = current_file_path.parent.parent / Path("resources/data") / 'npcFeature.json'
personality_file = current_file_path.parent.parent / Path("resources/data") / 'npcPersonality.json'
npc_file = current_file_path.parent.parent / Path("resources/data") / 'npc.json'
npc_file_2 = current_file_path.parent.parent / Path("resources/data") / 'npc_2.json'

with open(str(feature_file), 'r', encoding='utf-8') as file:
    features = json.load(file)
with open(str(personality_file), 'r', encoding='utf-8') as file:
    personalities = json.load(file)
with open(str(npc_file), 'r', encoding='utf-8') as file:
    characters = json.load(file)
with open(str(npc_file_2), 'r', encoding='utf-8') as file:
    characters_2 = json.load(file)


def make_ramdom_npc(npc_num):
    url = "http://221.140.195.124:9199/api/v1/npc/enroll"

    feature_list = list(features["npcFeature"].keys())
    personality_list = list(personalities["npcPersonality"].keys())

    selected_features = random.sample(feature_list, npc_num)
    selected_personalities = random.sample(personality_list, npc_num)

    random.shuffle(selected_features)
    random.shuffle(selected_personalities)

    npcs = [{"npcName": f"npc{idx}", 
             "npcPersonality": j, 
             "npcFeature": i}
             for idx, (i, j) in enumerate(zip(selected_features, selected_personalities))]

    for npc in npcs:
        response = requests.post(url, json=npc)
    
        result = json.loads(response.text)
        print(f'Status Code: {response.status_code}')
        print(f'Response Content : {json.dumps(result, indent=4)}')

        if response.status_code == 200:
            pass
        else:
            return None
    else:
        return "success"
    

def get_npc_information(npc_name, random_=False):
    if random_:
        character_list = list(characters["npcs"].keys())
        selected_character = random.sample(character_list, 1)[0]

        name = characters["npcs"][selected_character]["npcName"]
        personality = characters["npcs"][selected_character]["PersonalityDescription"]
        feature = characters["npcs"][selected_character]["FeatureDescription"]

        return f"이름: {name}\n성격: {personality}.\n특징: {feature}.", name
    else:
        if npc_name in list(characters["npcs"].keys()):
            name = characters["npcs"][npc_name]["npcName"]
            personality = characters["npcs"][npc_name]["PersonalityDescription"]
            feature = characters["npcs"][npc_name]["FeatureDescription"]
            
            return f"이름: {name}\n성격: {personality}.\n특징: {feature}.", name
        else:
            return None




if __name__ == "__main__":
    result = get_npc_information("KoongddYa", random_=False)
    print(result)