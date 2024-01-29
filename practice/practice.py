from pathlib import Path
import json
import random

import practice_schema

CHARACTERS = json.load((Path(__file__).resolve().parents[1] / "resources/data/npc_4.json").open('r', encoding='utf-8'))
PLACES = json.load((Path(__file__).resolve().parents[1] / "resources/data/places.json").open('r', encoding='utf-8'))

characters_data = practice_schema.CharactersSchema(**CHARACTERS)
place_data = practice_schema.PlacesSchema(**PLACES)


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
    filtered_candidates = [character for character in candidates if character not in excluded_characters]

    valid_characters = [get_character_info(character) for character in filtered_candidates if get_character_info(character)]

    if valid_characters:
        return random.choice(valid_characters)
    return None

def get_characters_info(names: list):
    characters_info = []
    for name in names:
        character_info = get_character_info(name)
        if character_info:
            characters_info.append(character_info)
    return characters_info

def test(data):
    generate_victim_schema = practice_schema.VictimGenerationSchema(**data)
    muderer_info = get_character_criminal_scenario(generate_victim_schema.murderer)

    crime_scene = select_crime_scene(place_data)
    victim = select_random_character(generate_victim_schema.livingCharacters, generate_victim_schema.murderer)

    excluded_characters = [generate_victim_schema.murderer, victim.name]
    witness = select_random_character(generate_victim_schema.livingCharacters, excluded_characters)
    
    living_characters_info = get_characters_info(generate_victim_schema.livingCharacters)
    living_characters_info = [{
            "name": living_character.name, 
            "personalityDescription": living_character.personalityDescription,
            "featureDescription": living_character.featureDescription,
            } for living_character in living_characters_info]
    
    input_data = {
        "day": generate_victim_schema.day,
        "murderer": {
            "name": generate_victim_schema.murderer,
            "motivation": muderer_info.motivation,
            "procedure": muderer_info.procedure,
            },
        "crimeScene": crime_scene.placeNameKo,
        "victim": victim.name,
        "witness": witness.name,
        "livingCharacters": living_characters_info
    }
    print(input_data)
    pretty_printed = json.dumps(input_data, indent=4, ensure_ascii=False)
    print(pretty_printed)

    prompt = practice_schema.GameInfo(**input_data)
    print(prompt)

if __name__ == '__main__':
    data = {
        "gameNo": 0,
        "secretKey": "string",
        "day": 0,
        "murderer": "레오",
        "livingCharacters": [
            "소피아", "마르코", "이사벨", "알렉스", "니콜라스", "레오"
            ],
        "previousStory": "string"
    }

    test(data)
    # print(find_character_info('레오').criminalScenario)