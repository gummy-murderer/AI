import lib.const as const

characters = const.CHARACTERS


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


def get_specific_npc_information(living_characters):
    new_npc_data = '등장인물'
    for living_character in living_characters:
        # print(characters['npcs'][living_character])
        for key, content in characters['npcs'][living_character].items():
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