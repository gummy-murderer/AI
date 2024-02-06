import random
from typing import Dict

from domain.scenario.schema import scenario_crud_schema
from lib import const

characters_data = scenario_crud_schema.CharactersSchema(**const.CHARACTERS)
place_data = scenario_crud_schema.PlacesSchema(**const.PLACES)


def get_character_info(name):
    for character in characters_data.npcs:
        if character.name == name:
            return character
    return None

def get_character_criminal_scenario(name):
    for character in characters_data.npcs:
        if character.name == name:
            return character.criminalScenario
    return None

def select_crime_scene(place_data):
    return random.choice(place_data.places)

def select_random_character(candidates: list, excluded_characters: list):
    filtered_candidates = [character.name for character in candidates if character.name not in excluded_characters]

    valid_characters = [get_character_info(character) for character in filtered_candidates if get_character_info(character)]

    if valid_characters:
        return random.choice(valid_characters)
    return None

def get_characters_info(candidates: list, excluded_characters: list):
    names = [character.name for character in candidates if character.name not in excluded_characters]

    characters_info = []
    for name in names:
        character_info = get_character_info(name)
        if character_info:
            characters_info.append(character_info)
    return characters_info

def generate_victim_input(victim_generation_data):
    muderer_info = get_character_criminal_scenario(victim_generation_data.murderer)
    if not muderer_info:
        return None, None
    
    for character_name in victim_generation_data.livingCharacters:
        if not get_character_info(character_name.name):
            return None, None

    crime_scene = select_crime_scene(place_data)
    victim = select_random_character(victim_generation_data.livingCharacters, victim_generation_data.murderer)

    excluded_characters = [victim_generation_data.murderer, victim.name]
    witness = select_random_character(victim_generation_data.livingCharacters, excluded_characters)
    
    living_characters_info = get_characters_info(victim_generation_data.livingCharacters, excluded_characters)
    living_characters_info = [{
            "name": living_character.name, 
            "personalityDescription": living_character.personalityDescription,
            "featureDescription": living_character.featureDescription,
            } for living_character in living_characters_info]
    
    input_data_json = {
        "information": {
            "day": victim_generation_data.day,
            "murderer": {
                "name": victim_generation_data.murderer,
                "motivation": muderer_info.motivation,
                "procedure": muderer_info.procedure,
                },
            "crimeScene": crime_scene.placeNameKo,
            "method": "칼",
            "victim": victim.name,
            "witness": witness.name,
            "livingCharacters": living_characters_info,
            "previousStory": victim_generation_data.previousStory
        }
    }
    input_data_pydantic = scenario_crud_schema.VictimGenerationContainer(**input_data_json)
    return input_data_json, input_data_pydantic

def generate_victim_output(answer, input_data, origin_data):

    game_npc_no_mapping = {character.name : character.gameNpcNo for character in origin_data.livingCharacters}

    alibi_list = [{
                "name": alibi.name,
                "alibi": alibi.alibi,
                "gameNpcNo": game_npc_no_mapping[alibi.name]
                } for alibi in answer.alibis if alibi.name in game_npc_no_mapping]
    
    output_data_json = {
        "victim": input_data.information.victim,
        "crimeScene": input_data.information.crimeScene,
        "method": input_data.information.method,
        "witness": input_data.information.witness,
        "eyewitnessInformation": answer.eyewitnessInformation,
        "dailySummary": answer.dailySummary,
        "alibis": alibi_list
    }

    return output_data_json

def generate_final_words_input(final_words_generation_data):
    muderer_info = get_character_criminal_scenario(final_words_generation_data.murderer)
    if not muderer_info:
        return None, None
    
    input_data_json = {
        "information": {
            "murderer": {
                "name": final_words_generation_data.murderer,
                "motivation": muderer_info.motivation,
                "procedure": muderer_info.procedure,
                },
            "gameResult": final_words_generation_data.gameResult,
            "previousStory": final_words_generation_data.previousStory
        }
    }
    input_data_pydantic = scenario_crud_schema.FinalWordsGenerationContainer(**input_data_json)
    return input_data_json, input_data_pydantic