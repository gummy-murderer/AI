import lib.const as const
import json

characters = const.CHARACTERS


def get_npc_name(npc_name):
    return npc_name, characters['npcs'][npc_name]['npcName']


def conversation_between_npcs_format(npc1, npc2, answer):
    try:
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
    except:
        return None


def conversation_with_user_format(answer):
    if len(answer.split(':')) > 1:
        return False
    else:
        return True
    

def generate_victim_format(answer):
    try:
        print(answer)
        # return {i.split(':')[0]: i.split(':')[1] for i in answer.split('\n')}
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None
    

def generate_intro_format(answer):
    try:
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None
    

def generate_final_words_format(answer):
    try:
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None