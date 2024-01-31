from pathlib import Path
import json
import random

import practice.user_schema as user_schema

CHARACTERS = json.load((Path(__file__).resolve().parents[1] / "resources/data/npc_4.json").open('r', encoding='utf-8'))
PLACES = json.load((Path(__file__).resolve().parents[1] / "resources/data/places.json").open('r', encoding='utf-8'))

characters_data = user_schema.CharactersSchema(**CHARACTERS)
place_data = user_schema.PlacesSchema(**PLACES)

