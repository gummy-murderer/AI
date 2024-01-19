from pathlib import Path
import json


# chat_management.py

CONVERSATION_MEMORY = 5


# NPC data
current_file_path = Path(__file__).resolve()
npc_file = current_file_path.parent.parent / Path("resources/data") / 'npc_2.json'

with open(str(npc_file), 'r', encoding='utf-8') as file:
    CHARACTERS = json.load(file)