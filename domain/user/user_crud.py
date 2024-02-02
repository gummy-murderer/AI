from domain.user.schema import user_crud_schema
from lib import const

characters_data = user_crud_schema.CharactersSchema(**const.CHARACTERS)
place_data = user_crud_schema.PlacesSchema(**const.PLACES)


def get_character_info(name):
    for character in characters_data.npcs:
        if character.name == name:
            return character
    return None

def format_previous_chat_contents(conversation_user_schema):
    formatted_chat_contents = []
    for chat_content in conversation_user_schema.previousChatContents[-const.MAX_CHAT_CONTENTS:]:
        chat_content_dict = {
            "type": "user" if chat_content.sender == conversation_user_schema.sender else "character",
            "name": chat_content.sender,
            "content": chat_content.chatContent
        }
        formatted_chat_contents.append(chat_content_dict)
    return formatted_chat_contents

def conversation_with_user_input(conversation_user_schema):
    character_info = get_character_info(conversation_user_schema.receiver.name)

    previous_chat_contents_formatted = format_previous_chat_contents(conversation_user_schema)

    input_data_json = {
        "information": {
            "user": conversation_user_schema.sender,
            "character": {
                "name": character_info.name,
                "personalityDescription": character_info.personalityDescription,
                "featureDescription": character_info.featureDescription,
                "alibi": conversation_user_schema.receiver.alibi
            },
            "chatContent": conversation_user_schema.chatContent,
            "previousStory": conversation_user_schema.previousStory,
            "previousChatContents": previous_chat_contents_formatted
        }
    }
    input_data_pydantic = user_crud_schema.ConversationWithUserContainer(**input_data_json)

    return input_data_json, input_data_pydantic

def conversation_between_npc_input(conversation_npc_schema):
    character_info_1 = get_character_info(conversation_npc_schema.npcName1.name)
    character_info_2 = get_character_info(conversation_npc_schema.npcName2.name)

    input_data_json = {
        "information": {
            "character1": {
                "name": character_info_1.name,
                "personalityDescription": character_info_1.personalityDescription,
                "featureDescription": character_info_1.featureDescription,
                "alibi": conversation_npc_schema.npcName1.alibi
            },
            "character2": {
                "name": character_info_2.name,
                "personalityDescription": character_info_2.personalityDescription,
                "featureDescription": character_info_2.featureDescription,
                "alibi": conversation_npc_schema.npcName2.alibi
            },
            "previousStory": conversation_npc_schema.previousStory
        }
    }
    input_data_pydantic = user_crud_schema.ConversationBetweenNPCContainer(**input_data_json)
    print(input_data_pydantic.model_dump_json(indent=2))

    return input_data_json, input_data_pydantic

def conversation_between_npc_each_input(conversation_npc_schema):
    character_info_1 = get_character_info(conversation_npc_schema.npcName1.name)
    character_info_2 = get_character_info(conversation_npc_schema.npcName2.name)

    previous_chat_contents_formatted = format_previous_chat_contents(conversation_npc_schema)

    input_data_json = {
        "information": {
            "character1": {
                "name": character_info_1.name,
                "personalityDescription": character_info_1.personalityDescription,
                "featureDescription": character_info_1.featureDescription,
                "alibi": conversation_npc_schema.npcName1.alibi
            },
            "character2": {
                "name": character_info_2.name,
                "personalityDescription": character_info_2.personalityDescription,
                "featureDescription": character_info_2.featureDescription,
                "alibi": conversation_npc_schema.npcName2.alibi
            },
            "previousStory": conversation_npc_schema.previousStory,
            "previousChatContents": previous_chat_contents_formatted
        }
    }
    input_data_pydantic = user_crud_schema.ConversationBetweenNPCEachContainer(**input_data_json)
    print(input_data_pydantic.model_dump_json(indent=2))

    return input_data_json, input_data_pydantic