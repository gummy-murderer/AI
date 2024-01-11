import json
import random
import requests
from pathlib import Path


current_file_path = Path(__file__).resolve()
feature_file = current_file_path.parent.parent / Path("resources/data") / 'npcFeature.json'
personality_file = current_file_path.parent.parent / Path("resources/data") / 'npcPersonality.json'

with open(str(feature_file), 'r', encoding='utf-8') as file:
    features = json.load(file)
with open(str(personality_file), 'r', encoding='utf-8') as file:
    personalities = json.load(file)


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
        personality_list = list(personalities["npcPersonality"].keys())
        feature_list = list(features["npcFeature"].keys())

        selected_personality = random.sample(personality_list, 1)
        selected_feature = random.sample(feature_list, 1)

        npc = {"npcName": "npc0", 
                "npcPersonality": selected_personality[0], 
                "npcFeature": selected_feature[0]}
        
        # name = npc["npcName"]
        name = npc_name
        personality = personalities["npcPersonality"][npc["npcPersonality"]]["Description"]
        feature = features["npcFeature"][npc["npcFeature"]]["Description"]
        
        return f"이름: {name}\n성격: {personality}.\n특징: {feature}."



if __name__ == "__main__":
    get_npc_information(3, random_=True)
    # make_ramdom_npc(3)