from pathlib import Path
import json


# lib/chat_management.py

CONVERSATION_MEMORY = 5


# NPC data
current_file_path = Path(__file__).resolve()
npc_file = current_file_path.parent.parent / Path("resources/data") / 'npc_4.json'

with open(str(npc_file), 'r', encoding='utf-8') as file:
    CHARACTERS = json.load(file)


# LLMS/chains.py
MODELS = ["gpt-3.5-turbo-1106", "gpt-4", "gpt-4-1106-preview"]