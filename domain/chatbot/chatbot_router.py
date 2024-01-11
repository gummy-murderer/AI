from fastapi import APIRouter
import json
import pprint

from domain.chatbot.chatbot_schema import GeneratorSchema, ConversationUserSchema, ConversationNPCSchema
from LLMs.langchain import chatbot, prompts
# from lang_agency import chatbot, memory
from lib.npc_management import get_npc_information


router = APIRouter(
    prefix="/api/chatbot",
)


@router.post("/intro_generator", 
             description="사용자 입력에 기반하여 소개 또는 시작 대화를 생성해 주는 API입니다.", 
             tags=["generator"])
async def intro_generator(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.intro(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/scenario_generator", 
             description="사용자 입력을 바탕으로 상세한 대화 시나리오를 생성해 주는 API입니다.", 
             tags=["generator"])
async def scenario_generator(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.scenario(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/conversation_with_user", 
             description="npc와 user간의 대화를 위한 API입니다.", 
             tags=["generator"])
async def conversation_with_user(conversation_user_schema: ConversationUserSchema):
    print(f"input")
    print(f"sender : {conversation_user_schema.sender}")
    print(f"receiver : {conversation_user_schema.receiver}")
    print(f"chatContent : {conversation_user_schema.chatContent}")
    print(f"chatDay : {conversation_user_schema.chatDay}")

    chat_contents = conversation_user_schema.previousChatContents
    start_index = max(len(chat_contents) - 5, 0)
    previous_contents = ""
    for content in chat_contents[start_index:]:
        # print(f"{content['sender']}: {content['chatContent']}")
        previous_contents += f"{content['sender']}: {content['chatContent']}\n"
    print(f"previous_contents")
    print(f"{previous_contents}")
    
    info = get_npc_information(conversation_user_schema.receiver, random_=True)
    print(info)

    while True:
        try:
            answer = chatbot.conversation_with_user(
                f" target_npc_info: ({info})\n" \
                + f"대화내용: \n" \
                + f"{previous_contents}\n" \
                + f"{conversation_user_schema.sender}: {conversation_user_schema.chatContent}\n" \
                + f"{conversation_user_schema.receiver}: " \
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "chatContent": answer, 
    }
    print(f"chatContent : {answer}")
    return final_response


@router.post("/conversation_between_npcs", 
             description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
             tags=["generator"])
async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
    print(f"input")
    print(f"npc_name_1 : {conversation_npc_schema.npc_name_1}")
    print(f"npc_name_2 : {conversation_npc_schema.npc_name_2}")
    
    while True:
        try:
            answer = chatbot.conversation_between_npc(
                prompts.conversation_between_npc_prompt,
                conversation_npc_schema.npc_name_1,
                conversation_npc_schema.npc_name_2
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "chatContent": answer, 
    }
    print(f"chatContent : {answer}")
    return final_response