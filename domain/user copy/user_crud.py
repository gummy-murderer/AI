import random
import lib.const as const

characters = const.CHARACTERS


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
            return None, None