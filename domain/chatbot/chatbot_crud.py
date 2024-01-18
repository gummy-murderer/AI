import json
import random
from pathlib import Path
import copy


current_file_path = Path(__file__).resolve()
npc_file = current_file_path.parent.parent.parent / Path("resources/data") / 'npc.json'
npc_file_2 = current_file_path.parent.parent.parent / Path("resources/data") / 'npc_2.json'

# with open(str(npc_file), 'r', encoding='utf-8') as file:
#     characters = json.load(file)
with open(str(npc_file_2), 'r', encoding='utf-8') as file:
    characters = json.load(file)



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
        

def get_all_npc_information(info_type='dict'):
    if info_type=='dict':
        new_npc_data = {'npcs': {}}

        for npc_name, npc_info in characters['npcs'].items():
            npc_without_criminal_scenario = npc_info.copy()
            del npc_without_criminal_scenario['CriminalScenario']
            new_npc_data[npc_name] = npc_without_criminal_scenario
        return new_npc_data
    elif info_type=='str':
        new_npc_data = '등장인물'
        for npc_name, npc_info in characters['npcs'].items():
            for key, content in npc_info.items():
                if key != 'CriminalScenario':
                    new_npc_data += f'\n{key}: {content}'
            new_npc_data += '\n'
        return new_npc_data


def get_criminal_scenario(name: str):
    crim_data = {}
    for npc_name, npc_info in characters['npcs'].items():
        if npc_name == name:
            crim_data['npcName'] = npc_info['npcName']
            crim_data['Motivation'] = npc_info['CriminalScenario']['Motivation']
            crim_data['Procedure'] = npc_info['CriminalScenario']['Procedure']
            
    return crim_data


if __name__ == "__main__":
    result = get_criminal_scenario('Alex')
    print(result)