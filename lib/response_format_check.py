from pathlib import Path
import json

current_file_path = Path(__file__).resolve()
npc_file = current_file_path.parent.parent / Path("resources/data") / 'npc_2.json'

with open(str(npc_file), 'r', encoding='utf-8') as file:
    characters = json.load(file)


def get_npc_name(npc_name):
    return npc_name, characters['npcs'][npc_name]['npcName']


def conversation_between_npcs_format(npc1, npc2, answer):
    name_en1, name_ko1 = get_npc_name(npc1)
    name_en2, name_ko2 = get_npc_name(npc2)

    answer_list = [{"sender": i.split(':')[0], 
                    "chatContent": i.split(':')[1]} for i in answer.split("\n") if i]

    for idx, answer_ in enumerate(answer_list):
        if name_ko1 == answer_['sender']:
            answer_list[idx]['sender'] = name_en1
            answer_list[idx]['receiver'] = name_en2
        elif name_ko2 == answer_['sender']:
            answer_list[idx]['sender'] = name_en2
            answer_list[idx]['receiver'] = name_en1
    
    return answer_list


def conversation_with_user_format(answer):
    if len(answer.split(':')) > 1:
        return False
    else:
        return True